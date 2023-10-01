#!/usr/bin/env python3

import os

from ansible.module_utils.basic import AnsibleModule


def get_index(data, name):
    for i, d in enumerate(data):
        if d['name'] == name:
            return i
    return None


def add_context(data, new_data, index):
    if index is None:
        data.append(new_data)
    else:
        data[index] = new_data


def update_config(data, new_data):
    index = get_index(data, new_data['name'])
    add_context(data, new_data, index)


def run_module():
    # Define available arguments/parameters a user can pass to the module
    module_args = dict(
        kubeconfig_path=dict(type='str', required=True),
        context_name=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result
    
    try:
        import yaml
    except ImportError:
        module.fail_json(msg='yaml module is required for this module')

    # Get kubeconfig data
    with open(module.params['kubeconfig_path'], 'r') as f:
        new_kubeconfig = yaml.safe_load(f)

    cluster_data = new_kubeconfig['clusters'][0]['cluster']
    user_data = new_kubeconfig['users'][0]['user']

    # Set Cluster
    cluster = {
        'name': module.params['context_name'],
        'cluster': cluster_data,
    }

    # Set User name
    user_name = module.params['context_name'] + '-user'

    # Set Context
    context = {
        'name': module.params['context_name'],
        'context': {
            'cluster': module.params['context_name'],
            'user': user_name,
        }
    }

    # Set User
    user = {
        'name': user_name,
        'user': user_data,
    }

    # Get existing kubeconfig data
    try:
        with open(os.path.expanduser('~/.kube/config'), 'r') as f:
            kubeconfig = yaml.safe_load(f)
    except FileNotFoundError:
        result['changed'] = True
        kubeconfig = {
            'apiVersion': 'v1',
            'clusters': [],
            'contexts': [],
            'kind': 'Config',
            'preferences': {},
            'users': [user],
        }
    
    # Update kubeconfig
    update_config(kubeconfig['clusters'], cluster)
    update_config(kubeconfig['contexts'], context)
    update_config(kubeconfig['users'], user)

    # Set current context
    kubeconfig['current-context'] = module.params['context_name']

    # Write kubeconfig
    with open(os.path.expanduser('~/.kube/config'), 'w') as f:
        yaml.dump(kubeconfig, f)

    result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
