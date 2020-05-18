# Copyright 2020 Eficode Oy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import urllib3
import requests
from dotenv import load_dotenv

class CBAMLibrary:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def connect_to_cbam(self, host=None, client_id=None, client_secret=None, catalog_version="SOL005", **kwargs):
        load_dotenv()
        host = host or os.getenv("HOST")
        client_id = client_id or os.getenv("CLIENT_ID")
        client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.connection = Connection(host, client_id, client_secret, **kwargs)
        self.catalog = Catalog(self.connection)._get_version(catalog_version)

    def create_vnf(self, vnfd_id, name, description=None):
        payload = {
            "vnfdId": vnfd_id,
            "vnfInstanceName": name
        }
        if description is not None:
            payload["vnfInstanceDescription"] = description
        response = self.connection.post("/vnflcm/v1/vnf_instances", json=payload)
        return response.json()

    def delete_vnf(self, vnf_id):
        self.connection.delete(f"/vnflcm/v1/vnf_instances/{vnf_id}")

    def delete_vnfd(self, vnfd_id):
        self.connection.delete(f"{self.catalog.endpoint}/{vnfd_id}")

    def disable_insecure_request_warning(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_vnf_by_name(self, vnf_name):
        vnfs = self.get_vnfs()
        for vnf in vnfs:
            if vnf["vnfInstanceName"] == vnf_name:
                return vnf
        raise ValueError(f"No VNF with name '{vnf_name}' was found.")

    def get_vnf(self, id):
        response = self.connection.get(f"/vnflcm/v1/vnf_instances/{id}")
        return response.json()

    def get_vnfs(self):
        response = self.connection.get("/vnflcm/v1/vnf_instances")
        return response.json()

    def get_vnfd(self, id):
        response = self.connection.get(self.catalog.endpoint + f"/{id}")
        return response.json()

    def get_vnfds(self):
        response = self.connection.get(self.catalog.endpoint)
        return response.json()

    def modify_vnf(self, vnf_id, modifications):
        # Body can arrive in dict, string or list type. Dict doesn't require any changes, others need to be parsed into valid json.
        # Multiline variables created with BuiltIns Set Variable are created as lists, turn them into a string
        if isinstance(modifications, list):
            modifications = "\n".join(modifications)
        # Deserialize json strings
        if isinstance(modifications, str):
            modifications = json.loads(modifications)
        response = self.connection.patch(f"/vnflcm/v1/vnf_instances/{vnf_id}", json=modifications)

    def onboard_vnfd(self, vnfd):
        return self.catalog.onboard_vnfd(vnfd)

class Connection:
    def __init__(self, host, client_id, client_secret, **kwargs):
        self.host = host
        self.client_id = client_id
        self.client_secret = client_secret
        self.global_kwargs = kwargs
        self.request_token()
        self.refresh_token_used = False

    def request_token(self, grant_type="client_credentials", options={}):
        default = {
            "grant_type": grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(f"https://{self.host}/auth/realms/cbam/protocol/openid-connect/token", data={**default, **options}, **self.global_kwargs)
        if response.status_code != 200:
            raise Exception("Token request failed: " + response.text)
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    def refresh_access_token(self):
        self.request_token(grant_type="refresh_token", options={"refresh_token": self.refresh_token})
        self.refresh_token_used = True

    def request(self, method, path, **kwargs):
        url = f"https://{self.host}{path}"
        auth_header = {"Authorization": f"Bearer {self.access_token}"}
        kwargs["headers"] = {**auth_header, **kwargs["headers"]} if "headers" in kwargs else auth_header
        response = getattr(requests, method)(url, **kwargs, **self.global_kwargs)
        if response.status_code == 401 and not self.refresh_token_used:
            self.refresh_access_token()
            # Remove previous, expired auth header
            kwargs["headers"].pop("Authorization")
            return self.request(method, path, **kwargs)
        response.raise_for_status()
        self.refresh_token_used = False
        return response

    def get(self, path, **kwargs):
        return self.request("get", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("post", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("put", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("delete", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("patch", path, **kwargs)


class CatalogSOL005:
    endpoint = "/vnfpkgm/v1/vnf_packages"

    def __init__(self, connection):
        self.connection = connection

    def onboard_vnfd(self, vnfd):
        response = self.create_vnf_package_resource()
        self.upload_vnf_package_content(response['id'], vnfd)
        return response

    def create_vnf_package_resource(self):
        response = self.connection.post(self.endpoint)
        return response.json()

    def upload_vnf_package_content(self, vnfPkgId, vnfd):
        self.connection.put(self.endpoint + f"/{vnfPkgId}/package_content", headers = {'Content-Type': 'application/zip'}, data = open(vnfd, "rb"))

class Catalog18:
    endpoint = "/api/catalog/adapter/vnfpackages"

    def __init__(self, connection):
        self.connection = connection

    def onboard_vnfd(self, vnfd):
        response = self.connection.post(self.endpoint, files= {"content": open(vnfd, "rb")})
        return response.json()

class Catalog:

    def __init__(self, connection):
        self.SOL005 = CatalogSOL005(connection)
        self.v18 = Catalog18(connection)

    def _get_version(self, version):
        try:
            return getattr(self, version)
        except AttributeError:
            existing_versions = list(filter(lambda x: not x.startswith("_"), self.__dict__.keys()))
            raise ValueError(f"No such catalog version: '{version}'. Supported versions are: {existing_versions}") from None
