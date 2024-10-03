import json

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Admin")

    def modify_user(self, users_data, username, new_data):
        if username in users_data:
            users_data[username].update(new_data)
            self.save_data(users_data)
        else:
            print(f"User {username} not found.")

    def save_data(self, users_data):
        with open('users.json', 'w') as file:
            json.dump(users_data, file, indent=4)
    
    def show_users(self, users):
        print("Lista pracowników i ich ról:")
        for username, user_data in users.items():
            print(f"Użytkownik: {username}, Rola: {user_data['role']}")

class Employee(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Employee")

    def sell_product(self, product, quantity, product_list, finance):
        if product in product_list and product_list[product]['stock'] >= quantity:
            product_list[product]['stock'] -= quantity
            finance['balance'] += product_list[product]['price'] * quantity
            self.save_finance(finance)
            self.save_products(product_list)
            print(f"Sold {quantity} of {product}")
        else:
            print(f"Nie ma kurwa nie dla psa")

    def save_finance(self, finance):
        with open('finance.json', 'w') as file:
            json.dump(finance, file, indent=4)

    def save_products(self, product_list):
        with open('products.json', 'w') as file:
            json.dump(product_list, file, indent=4)

class Company:
    def __init__(self):
        self.users = self.load_users()
        self.products = self.load_products()
        self.finance = self.load_finance()

    def load_users(self):
        with open('users.json', 'r') as file:
            return json.load(file)

    def load_products(self):
        with open('products.json', 'r') as file:
            return json.load(file)

    def load_finance(self):
        with open('finance.json', 'r') as file:
            return json.load(file)

    def generate_report(self):
        report = "Company Report:\n"
        report += "Users:\n"
        for user in self.users:
            report += f" - {user}: {self.users[user]['role']}\n"
        
        report += "\nProducts:\n"
        for product in self.products:
            report += f" - {product}: {self.products[product]['stock']} in stock, price: {self.products[product]['price']}\n"
        
        report += f"\nCompany Balance: {self.finance['balance']}"

        with open('report.txt', 'w') as file:
            file.write(report)
        print("Report wygenerowany.")

def login(company):
    username = input("Enter username: ")
    password = input("Enter password: ")

    
    for user_data in company.users.values():  
        if user_data['username'] == username and user_data['password'] == password:
            role = user_data['role']
            if role == "Admin":
                return Admin(username, password)
            elif role == "Employee":
                return Employee(username, password)
            else:
                print("Unknown role")
                return None

    print("Invalid credentials")
    return None


def main():
    company = Company()
    user = login(company)

    if user:
        if isinstance(user, Admin):
            print("Logged in as Admin")
            while True:
                choice = input("1. Modify User 2. Generate Report 3. Show all the workers list 4.Exit\n")
                if choice == '1':
                    username = input("Enter username to modify: ")
                    new_role = input("Enter new role: ")
                    new_data = {'role': new_role}
                    user.modify_user(company.users, username, new_data)
                elif choice == '2':
                    company.generate_report()
                elif choice == '3':
                    user.show_users(company.users)
                elif choice == '4':
                    break

        elif isinstance(user, Employee):
            print("Logged in as Employee")
            while True:
                choice = input("1. Sell Product 2. Exit\n")
                if choice == '1':
                    product = input("Enter product name: ")
                    quantity = int(input("Enter quantity: "))
                    user.sell_product(product, quantity, company.products, company.finance)
                elif choice == '2':
                    break  
main()
