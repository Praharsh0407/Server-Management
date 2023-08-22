import json

# Function to update a specific server's information based on IP address
def update_server_info_by_ip(server_list, ip_address, new_ip_address, new_mac_address):
    updated = False
    for server in server_list:
        if server['ip_address'] == ip_address:
            server['ip_address'] = new_ip_address
            server['mac_address'] = new_mac_address
            updated = True
            break
    return updated

# Load existing data from the JSON file
with open('Data_ADD/servers.json', 'r') as file:
    server_data = json.load(file)

# Collect IP address for the server to be updated
ip_address = input("Enter IP address of the server to update: ")

# Check if the server with the specified IP address exists
server_exists = any(server['ip_address'] == ip_address for server in server_data)

if server_exists:
    new_ip_address = input("Enter new IP address: ")
    new_mac_address = input("Enter new MAC address: ")

    # Update the server information
    updated = update_server_info_by_ip(server_data, ip_address, new_ip_address, new_mac_address)

    if updated:
        # Write the updated data back to the JSON file
        with open('Data_ADD/servers.json', 'w') as file:
            json.dump(server_data, file, indent=4)
        print("Server information updated successfully.")
    else:
        print("An error occurred while updating server information.")
else:
    print("Server not found with the specified IP address.")
