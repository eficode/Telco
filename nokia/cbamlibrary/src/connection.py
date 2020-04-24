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

import requests

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

    def delete(self, path, **kwargs):
        return self.request("delete", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("patch", path, **kwargs)
