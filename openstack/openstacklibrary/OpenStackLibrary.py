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
import ast
import json
import openstack
import kw_documentation

class OpenStackLibrary:

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def call_connection_method(self, method_name, *args, **kwargs):
        method = getattr(self.connection, method_name)
        return method(*args, **kwargs)

    def close_connection(self):
        self.connection.close()
        self.connection = None

    def connect(self, cloud, **kwargs):
        password = kwargs.pop("password", None) or os.environ.get("OS_PASSWORD")
        self.connection = openstack.connect(cloud=cloud, password=password, **kwargs)

    def create_aggregate(self, name, availability_zone=None):
        aggregate = self.connection.create_aggregate(name, availability_zone)
        return aggregate

    def create_network(self, name, shared=False, admin_state_up=True, external=False, provider=None, project_id=None, availability_zone_hints=None, port_security_enabled=None, mtu_size=None, dns_domain=None):
        if isinstance(provider, str):
            provider = ast.literal_eval(provider)
        return self.connection.create_network(name, shared, admin_state_up, external, provider, project_id, availability_zone_hints, port_security_enabled, mtu_size, dns_domain)

    def create_flavor(self, name, ram, vcpus, disk, flavorid='auto', ephemeral=0, swap=0, rxtx_factor=1.0, is_public=True):
        return self.connection.create_flavor(name, ram, vcpus, disk, flavorid, ephemeral, swap, rxtx_factor, is_public)

    def create_image(self, name, **image_attrs):
        return self.connection.create_image(name, **image_attrs)

    def import_image(self, name, method="glance-direct", uri=None, store=None, **image_attrs):
        image = self.connection.image.create_image(name, **image_attrs)
        # The name value in image_attrs is ignored, so set it after image is created using update_image
        self.update_image(image, name=name)
        return self.connection.image.import_image(image, method=method, uri=uri)

    def update_image(self, image, **attrs):
        return self.connection.image.update_image(image, **attrs)

    def create_project(self, name, domain_id, description=None, enabled=True):
        return self.connection.create_project(name, description, domain_id, enabled)

    def create_security_group(self, name, description, project_id=None):
        return self.connection.create_security_group(name, description, project_id)

    def create_security_group_rule(self, security_group, port_range_min=None, port_range_max=None, protocol=None, remote_ip_prefix=None, remote_group_id=None, direction='ingress', ethertype='IPv4', project_id=None):
        return self.connection.create_security_group_rule(security_group, port_range_min, port_range_max, protocol, remote_ip_prefix, remote_group_id, direction, ethertype, project_id)

    def create_user(self, name, password=None, email=None, default_project=None, enabled=True, domain_id=None, description=None):
        return self.connection.create_user(name, password, email, default_project, enabled, domain_id, description)

    def get_domain_id(self, domain_name):
        for domain in self.connection.identity.domains():
            if domain.name == domain_name:
                return domain.id
        raise ValueError(f"No domain with name '{domain_name}' was found.")

    def list_flavors(self, *fields):
        flavors = self.connection.compute.flavors()
        flavor_list = []
        for flavor in flavors:
            flavor_dict = {}
            if fields:
                for field in fields:
                    flavor_dict[field] = getattr(flavor, field)
                flavor_list.append(flavor_dict)
            else:
                flavor_list.append(flavor)
        print(json.dumps(flavor_list, indent=2))

    def update_aggregate(self, aggregate, **arguments):
        return self.connection.update_aggregate(aggregate, **arguments)

    def update_security_group(self, security_group, **arguments):
        return self.connection.update_security_group(security_group, **arguments)


def add_documentation(cls, documentation):
    """Utility method for separating Robot documentation from keyword implementation."""
    methods = list(filter(lambda x: not x.startswith("_"), dir(cls)))
    for method_name in methods:
        method = getattr(cls, method_name)
        if callable(method):
            name = method.__name__
            if hasattr(documentation, name):
                getattr(cls, name).__doc__ = getattr(documentation, name)

add_documentation(OpenStackLibrary, kw_documentation)
