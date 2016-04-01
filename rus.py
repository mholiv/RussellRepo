#!/usr/bin/env python2
# Copyright (C) 2013 - Remy van Elst

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pysphere 
import re
import sys


try:
    import json
except ImportError:
    import simplejson as json

useSSL = False
server_fqdn = 'serverString'
server_username = 'userName'
server_password = 'password'

#If you want guests
guest_name = 'someguest'


def vcenter_connect(server_fqdn, server_username, server_password):
    vserver = pysphere.VIServer()
    try:
        vserver.connect(server_fqdn, server_username, server_password)
    except Exception as error:
        print(('Could not connect to vCenter: %s') % (error))

    return vserver


def hostinfo(name):
    vserver = vcenter_connect(server_fqdn,server_username,server_password)
    try:
        vm = vserver.get_vm_by_name(name)
    except Exception as e:
        print("[Error]: %s" % e)
        sys.exit(1)

    # Inject some variables for all hosts
    vars = {
        'admin'              : 'sysadmin@example.org',
        'source_database'    : 'VMWare'
    }

    if 'ldap' in name.lower():
        vars['baseDN'] = 'dc=example,dc=org'


    print json.dumps(vars, indent=4)

def grouplist():
    inventory ={}
    inventory['local'] = [ '127.0.0.1' ]
    vserver = vcenter_connect(server_fqdn,server_username,server_password)
    vms_in_vserver = vserver.get_registered_vms(status='poweredOn')
    inventory["no_group"] = {
        'hosts' : []
    }

    for vsphere_vm in vms_in_vserver:
        virtual_machine = vserver.get_vm_by_path(vsphere_vm)
        virtual_machine_name = virtual_machine.get_property('name')
        inventory['no_group']['hosts'].append(virtual_machine_name)

    print json.dumps(inventory, indent=4)

if __name__ == '__main__':

    if useSSL is True:
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

    if (server_fqdn, server_username, server_password):

        #### IF YOU WANT GROUPLIST
        grouplist()

        #### IF YOU WANT HOST INFO
        #hostinfo(guest_name)

    else:
        sys.exit(1)

