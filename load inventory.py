import ansible_runner
import json

def load_inventory():
    try:
        # Load inventory
        #inventory_data = ansible_runner.get_inventory(action='list', inventories=['hosts.yml'])
        inventory_data = ansible_runner.get_inventory(action='list', inventories=['/workspaces/ensf400-lab5-ansible/hosts.yml'])
        inventory = json.loads(inventory_data[0])  # Parse JSON string to dictionary

        all_hosts = []

        # Extract hosts information
        for group_name, group_info in inventory.items():
            if group_name == '_meta':
                continue  # Skip meta information
            if group_name in ['all', 'ungrouped']:
                continue  # Skip special group names
            for host_name in group_info['hosts']:
                host_vars = inventory['_meta']['hostvars'][host_name]
                host_info = {
                    'name': host_name,
                    'ansible_host': host_vars.get('ansible_host', 'N/A'),
                    'group': group_name
                }
                all_hosts.append(host_info)

        return all_hosts
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return []

def ping_hosts(hosts):
    if not hosts:
        print("No hosts to ping.")
        return

    # Extract hostnames for pinging
    hostnames = [host['name'] for host in hosts]

    try:
        # Run ping module on all hosts
        result = ansible_runner.run(inventory='/workspaces/ensf400-lab5-ansible/hosts.yml', module='ping', host_pattern=','.join(hostnames))

        # Print ping results
        print("\nPing Results:")
        for host_result in result.events:
            if 'host' in host_result:
                print(f"Host: {host_result['host']}, Status: {host_result['event']}, Result: {host_result['stdout']}")
            else:
                print("Unable to retrieve ping results for a host.")
    except Exception as e:
        print(f"Error running ping module: {e}")

if __name__ == "__main__":
    hosts = load_inventory()
    ping_hosts(hosts)
