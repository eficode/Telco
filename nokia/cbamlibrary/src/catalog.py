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

class CatalogSOL005:
    endpoint = "/vnfpkgm/v1/vnf_packages"


class Catalog18:
    endpoint = "/api/catalog/adapter/vnfpackages"


class Catalog:
    SOL005 = CatalogSOL005()
    v18 = Catalog18()

    @staticmethod
    def _get_version(version):
        try:
            return getattr(Catalog, version)
        except AttributeError:
            existing_versions = list(filter(lambda x: not x.startswith("_"), Catalog.__dict__.keys()))
            raise ValueError(f"No such catalog version: '{version}'. Supported versions are: {existing_versions}") from None
