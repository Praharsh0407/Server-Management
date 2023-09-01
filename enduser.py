import os
import json

# Function to save server data to the JSON file
def save_server_data(server_data):
    with open('Data_ADD\\servers.json', 'w') as file:
        json.dump(server_data, file, indent=4)

# Start server monitoring in the background on Windows
os.system("start /B python server_monitoring.py")

# Load existing data from the JSON file
with open('Data_ADD\\servers.json', 'r') as file:
    server_data = json.load(file)

while True:
    print("\nOptions:")
    print("1. Add server data and save")
    print("2. Run updating_data_to_json.py (Update server data)")
    print("3. Save and Exit")
    print("4. Exit without saving")

    choice = input("Select an option (1/2/3/4): ")

    if choice == '1':
        # Execute Data_ADD.py to collect credentials and add data
        os.system("python Data_ADD\\adding_data_to_json.py")

        # Reload the updated data from the JSON file
        with open('Data_ADD\\servers.json', 'r') as file:
            server_data = json.load(file)

        # Save the JSON file
        save_server_data(server_data)

        print("Server information added and saved to the JSON file.")
    elif choice == '2':
        # Run updating_data_to_json.py
        os.system("python Data_ADD\\updating_data_to_json.py")
        # Reload the updated data from the JSON file
        with open('Data_ADD\\servers.json', 'r') as file:
            server_data = json.load(file)
    elif choice == '3':
        # Save and exit
        save_server_data(server_data)
        break
    elif choice == '4':
        # Exit without saving
        break
    else:
        print("Invalid choice. Please select a valid option.")
