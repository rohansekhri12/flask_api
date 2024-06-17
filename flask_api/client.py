import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'
USERS_URL = f'{BASE_URL}/users'
AUTH_URL = f'{BASE_URL}/login'
REGISTER_URL = f'{BASE_URL}/register'

headers = {}

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {'username': username, 'password': password}
    response = requests.post(REGISTER_URL, json=data)
    print(response.json())

def login():
    global headers
    while True:
        print("\nEnter 'exit' to quit.")
        username = input("Enter username: ")
        if username.lower() == 'exit':
            sys.exit("Exiting script.")
        password = input("Enter password: ")
        if password.lower() == 'exit':
            sys.exit("Exiting script.")
        
        data = {'username': username, 'password': password}
        response = requests.post(AUTH_URL, json=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            headers = {'Authorization': f'Bearer {access_token}'}
            print("Login successful")
            break
        else:
            print("Login failed. Please try again or type 'exit' to quit.")

def create_user():
    
    name = input("Enter name: ")
    age = input("Enter age: ")
    email = input("Enter email: ")
    data = {
        
        'name': name,
        'age': age,
        'email': email
    }
    response = requests.post(USERS_URL, json=data, headers=headers)
    print(json.dumps(response.json(), indent=4))

def get_user():
    user_id = input("Enter user ID: ")
    response = requests.get(f"{USERS_URL}/{user_id}", headers=headers)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(response.json())

def update_user():
    user_id = input("Enter user ID: ")
    print("Which field would you like to update?")
   
    print("1. Name")
    print("2. Age")
    print("3. Email")
    print("4. Update all fields")
    choice = input("Enter choice: ")
    
    data = {}
  
    if choice == '1':
        name = input("Enter new name: ")
        data['name'] = name
    elif choice == '2':
        age = input("Enter new age: ")
        data['age'] = age
    elif choice == '3':
        email = input("Enter new email: ")
        data['email'] = email
    elif choice == '4':
        name = input("Enter new name: ")
        age = input("Enter new age: ")
        email = input("Enter new email: ")
        data = {
            'name': name,
            'age': age,
            'email': email
        }
    else:
        print("Invalid choice.")
        return

    response = requests.put(f"{USERS_URL}/{user_id}", json=data, headers=headers)
    print(json.dumps(response.json(), indent=4))

def delete_user():
    user_id = input("Enter user ID: ")
    response = requests.delete(f"{USERS_URL}/{user_id}", headers=headers)
    print(json.dumps(response.json(), indent=4))

def get_all_users():
    response = requests.get(USERS_URL, headers=headers)
    if response.status_code == 200:
        users = response.json()
        if isinstance(users, list):
            for user in users:
                print(json.dumps(user, indent=4))
        else:
            print(json.dumps(users, indent=4))
    else:
        print("Failed to retrieve users.")
        print(response.json())

def add_new_authenticated_user():
    register()

def menu():
    login()  # Prompt user to login before showing the menu
    while True:
        print("\nMenu:")
        print("1. Create User")
        print("2. Get User")
        print("3. Update User")
        print("4. Delete User")
        print("5. Get All Users")
        print("6. Add New Authenticated User")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            create_user()
        elif choice == '2':
            get_user()
        elif choice == '3':
            update_user()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            get_all_users()
        elif choice == '6':
            add_new_authenticated_user()
        elif choice == '7':
            sys.exit("Exiting script.")
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    menu()

