# Copyright 2013 VMware, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

#from neutron_lib.api import converters
from networking_ovn.neutron_lib.api import converters
#from neutron_lib import constants
from networking_ovn.neutron_lib import constants 
#from neutron_lib import exceptions as nexception
from networking_ovn.neutron_lib import exceptions as nexception

#from neutron._i18n import _
from networking_ovn._i18n import _
#from neutron.api import extensions
from networking_ovn.neutorn_lib.api import extensions


DEFAULT_PORT_SECURITY = True


class PortSecurityPortHasSecurityGroup(nexception.InUse):
    message = _("Port has security group associated. Cannot disable port "
                "security or ip address until security group is removed")


class PortSecurityAndIPRequiredForSecurityGroups(nexception.InvalidInput):
    message = _("Port security must be enabled and port must have an IP"
                " address in order to use security groups.")


PORTSECURITY = 'port_security_enabled'
EXTENDED_ATTRIBUTES_2_0 = {
    'networks': {
        PORTSECURITY: {'allow_post': True, 'allow_put': True,
                       'convert_to': converters.convert_to_boolean,
                       'enforce_policy': True,
                       'default': DEFAULT_PORT_SECURITY,
                       'is_visible': True},
    },
    'ports': {
        PORTSECURITY: {'allow_post': True, 'allow_put': True,
                       'convert_to': converters.convert_to_boolean,
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'enforce_policy': True,
                       'is_visible': True},
    }
}


class Portsecurity(extensions.ExtensionDescriptor):
    """Extension class supporting port security."""

    @classmethod
    def get_name(cls):
        return "Port Security"

    @classmethod
    def get_alias(cls):
        return "port-security"

    @classmethod
    def get_description(cls):
        return "Provides port security"

    @classmethod
    def get_updated(cls):
        return "2012-07-23T10:00:00-00:00"

    def get_extended_resources(self, version):
        if version == "2.0":
            return EXTENDED_ATTRIBUTES_2_0
        else:
            return {}
