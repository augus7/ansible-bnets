#! /usr/bin/python

DOCUMENTATION = '''
module: bnets_guest_ssid.py
author:
  - "Augusto Remillano II"
description: Configures bnets router's guest WLAN
requirements:
  - mt_api
options:
  hostname:
    description:
      - hotstname of mikrotik router
  username:
    description:
      - username used to connect to mikrotik router
  password:
    description:
      - password used for authentication to mikrotik router
  state:
    description:
      - client present or absent
    required: False
    choices:
      - present
      - absent
'''

EXAMPLES = '''
# Add a new radius entry
- name: change ssid
  change_ssid.py:
    hostname: "{{ inventory_hostname }}"
    username: "{{ username }}"
    password: "{{ password }}"
    parameter: wireless
    settings:
        name: wlan-guest
        master-interface: wlan-home
        security-profile: default
        ssid: BAYANIHANETS-test12345
        disabled: "no"
        wps-mode: disabled
        mode: ap-bridge 
  delegate_to: 127.0.0.1
'''

import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '/home/august/mt_pythonlibs'))

from ansible.module_utils.basic import *
from mt_common import MikrotikIdempotent

def main():

    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(required=True),
            username=dict(required=True),
            password=dict(required=True),
            settings=dict(required=False, type='dict'),
            parameter = dict(
                required  = True,
                choices   = ['wireless'],
                type      = 'str'
            ),
            state=dict(
                required = False,
                choices = ['present', 'absent'],
                type = 'str'
            ),
        ),
    )

    idempotent_parameter = 'name'
    params = module.params


    mt_obj = MikrotikIdempotent(
        hostname = params['hostname'],
        username = params['username'],
        password = params['password'],
        state    = params['state'],
        desired_params = params['settings'],
        idempotent_param = idempotent_parameter,
        api_path = '/interface/wireless',
    )

    mt_obj.sync_state()

    if mt_obj.failed:
        module.fail_json(
            msg = mt_obj.failed_msg
        )
    elif mt_obj.changed:
        module.exit_json(
            failed=False,
            changed=True,
            msg=mt_obj.changed_msg,
            diff={ "prepared": {
                "old": mt_obj.old_params,
                "new": mt_obj.new_params,
            }},
        )
    else:
        module.exit_json(
            failed=False,
            changed=False,
            #msg='',
            msg=params['settings'],
        )

if __name__ == '__main__':
  main()
