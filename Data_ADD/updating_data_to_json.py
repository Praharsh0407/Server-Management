import json

# Function to update a specific server's information
def update_server_info(server_list, server_name, ip_address, mac_address):
    updated = False
    for server in server_list:
        if server['name'] == server_name:
            server['ip_address'] = ip_address
            server['mac_address'] = mac_address
            updated = True
            break
    return updated

# Load existing data from the JSON file
with open('Data_ADD/servers.json', 'r') as file:
    server_data = json.load(file)

# Collect information for the server to be updated
server_name = input("Enter server name to update: ")
ip_address = input("Enter new IP address: ")
mac_address = input("Enter new MAC address: ")

# Update the server information
updated = update_server_info(server_data, server_name, ip_address, mac_address)

if updated:
    # Write the updated data back to the JSON file
    with open('Data_ADD/servers.json', 'w') as file:
        json.dump(server_data, file, indent=4)
    print("Server information updated successfully.")
else:
    print("Server not found in the list.")