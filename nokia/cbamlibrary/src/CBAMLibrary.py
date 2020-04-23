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


class CBAMLibrary:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def connect_to_cbam(self, host=None, client_id=None, client_secret=None, **kwargs):
        load_dotenv()
        host = host or os.getenv("HOST")
        client_id = client_id or os.getenv("CLIENT_ID")
        client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.connection = Connection(host, client_id, client_secret, **kwargs)

    def create_vnf(self, vnfd_id, name):
        response = self.connection.post("/vnflcm/v1/vnf_instances", json={"vnfdId": vnfd_id, "vnfInstanceName": name})
        return response.json()

    def delete_vnf(self, vnf_id):
        self.connection.delete(f"/vnflcm/v1/vnf_instances/{vnf_id}")

    def delete_vnfd(self, vnfd_id):
        self.connection.delete(f"/api/catalog/adapter/vnfpackages/{vnfd_id}")

    def disable_insecure_request_warning(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_vnfs(self):
        response = self.connection.get("/vnflcm/v1/vnf_instances")
        vnfs = response.json()
        for vnf in vnfs:
            vnf.pop("_links")
        print(json.dumps(vnfs, indent=2))
        return vnfs

    def get_vnfds(self):
        response = self.connection.get("/api/catalog/adapter/vnfpackages")
        vnfds = response.json()
        for vnfd in vnfds:
            vnfd.pop("links")
        print(json.dumps(vnfds, indent=2))
        return vnfds

    def onboard_vnfd(self, vnfd):
        response = self.connection.post("/api/catalog/adapter/vnfpackages", files= {"content": open(vnfd, "rb")})
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
