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
import kw_documentation
from dotenv import load_dotenv
from connection import Connection
from catalog import Catalog

class CBAMLibrary:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def connect_to_cbam(self, host=None, client_id=None, client_secret=None, catalog_version="SOL005", **kwargs):
        load_dotenv()
        host = host or os.getenv("HOST")
        client_id = client_id or os.getenv("CLIENT_ID")
        client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.connection = Connection(host, client_id, client_secret, **kwargs)
        self.catalog = Catalog._get_version(catalog_version)

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

    def get_vnfs(self):
        response = self.connection.get("/vnflcm/v1/vnf_instances")
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
        response = self.connection.post(self.catalog.endpoint, files= {"content": open(vnfd, "rb")})
        return response.json()


def add_documentation(cls, documentation):
    """Utility method for separating Robot documentation from keyword implementation."""
    methods = list(filter(lambda x: not x.startswith("_"), dir(cls)))
    for method_name in methods:
        method = getattr(cls, method_name)
        if callable(method):
            name = method.__name__
            if hasattr(documentation, name):
                getattr(cls, name).__doc__ = getattr(documentation, name)

add_documentation(CBAMLibrary, kw_documentation)
