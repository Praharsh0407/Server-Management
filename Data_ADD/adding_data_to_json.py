import json

# Load existing data from the JSON file
with open('Data_ADD\servers.json', 'r') as file:
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
with open('Data_ADD\servers.json', 'w') as file:
    json.dump(server_data, file, indent=4)

print("Server information added to the JSON file.")

import json

# Load existing data from the JSON file
with open('Data_ADD\servers.json', 'r') as file:
    server_data = json.load(file)

# Function to format server name
def format_server_name(name):
    if name.startswith("Server"):
        return name
    else:
        return f"Server {name}"

# Update existing entries
for server in server_data:
    server["name"] = format_server_name(server["name"])

# Write the updated data back to the JSON file
with open('Data_ADD\servers.json', 'w') as file:
    json.dump(server_data, file, indent=4)

print("Server names updated in the JSON file.")
