import ansible_runner

# Load inventory
inventory_path = 'hosts.yml'
inventory = ansible_runner.get_inventory(action='list', inventories=[inventory_path])

# Task 2: Run hello.yml playbook
playbook_path = 'hello.yml'

# Run playbook on app_group
result = ansible_runner.run(private_data_dir='.', playbook=playbook_path, host_pattern='app_group')

# Print playbook run results
print("\nPlaybook Run Results:")
for host_result in result.events:
    if 'host' in host_result:
        print(f"Host: {host_result['host']}, Status: {host_result.get('event', 'N/A')}, Result: {host_result.get('stdout', 'N/A')}")
    else:
        print(f"Status: {host_result.get('event', 'N/A')}, Result: {host_result.get('stdout', 'N/A')}")