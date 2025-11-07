from getpass import getpass

class GuestView:
    def show_guest_menu(self):
        print("Guest Menu")
        print("1. Login")
        print("2. Register")
        print("3. Browse Books")
        print("4. Exit")
        return input("Choose an option: ")

    def get_registration_details(self):
        print("Register New User")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = getpass("Enter your password: ")
        
        while True:
            role = input("Choose a role (reader/author): ").lower()
            if role in ["reader", "author"]:
                break
            self.show_message("Invalid role. Please choose 'reader' or 'author'.")
        
        return name, email, password, role

    def get_login_details(self):
        print("Login")
        email = input("Enter your email: ")
        password = getpass("Enter your password: ")
        return email, password

    def show_message(self, message):
        print(message)
