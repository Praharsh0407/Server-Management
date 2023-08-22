import json

# Load existing data from the JSON file
with open('Data_ADD/servers.json', 'r') as file:
    server_data = json.load(file)

# Collect information for a new server
server_number = input("Enter server number: ")
ip_address = input("Enter IP address: ")
mac_address = input("Enter MAC address: ")

# Format the server name
server_name = f"Server {server_number}"

# Create a new server entry
new_server = {
    "name": server_name,
    "ip_address": ip_address,
    "mac_address": mac_address
}

# Append the new server entry to the existing data
server_data.append(new_server)

# Write the updated data back to the JSON file
with open('Data_ADD/servers.json', 'w') as file:
    json.dump(server_data, file, indent=4)

print("Server information added to the JSON file.")
