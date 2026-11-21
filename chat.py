
import math
 
class Bank:
#ده الكونستراكتور بياخد 1 attribute  

    def __init__(self, customer_list=None):
        self.customer_list = []
        self.transactions = []

        if customer_list:
            for item in customer_list:
                if isinstance(item, dict):
                    customer_id = str(item.get("id", "")).strip()
                    balance = self.validate_amount(
                        item.get("balance", 0)
                    )

                    if customer_id and balance is not None:
                        if balance >= 0 and not self.find_customer(customer_id):
                            self.customer_list.append({
                                "id": customer_id,
                                "balance": balance
                            })

    # Validate amounts
    def validate_amount(self, amount):
        try:
            amount = float(amount)
            if math.isfinite(amount):
                return amount
            return None
        except (ValueError, TypeError):
            return None

    # Find customer
    def find_customer(self, customer_id):
        for customer in self.customer_list:
            if customer["id"] == str(customer_id):
                return customer
        return None

    # Add customer
    def add_customer(self, customer_id, balance=0):
        customer_id = str(customer_id).strip()
        balance = self.validate_amount(balance)

        if not customer_id:
            return "Invalid customer ID."

        if balance is None or balance < 0:
            return "Invalid balance."

        if self.find_customer(customer_id):
            return "Customer already exists."

        self.customer_list.append({
            "id": customer_id,
            "balance": balance
        })

        return "Customer added successfully."

    # Show customer balance
    def show_balance(self, customer_id):
        customer = self.find_customer(customer_id)

        if customer is None:
            return "Customer not found."

        return customer["balance"]

    # Deposit
    def deposit_money(self, customer_id, amount):
        customer = self.find_customer(customer_id)
        amount = self.validate_amount(amount)

        if customer is None:
            return "Customer not found."

        if amount is None or amount <= 0:
            return "Invalid amount."

        customer["balance"] += amount

        self.transactions.append({
            "type": "deposit",
            "customer_id": str(customer_id),
            "amount": amount
        })

        return "Deposit successful."

    # Withdraw
    def withdraw_money(self, customer_id, amount):
        customer = self.find_customer(customer_id)
        amount = self.validate_amount(amount)

        if customer is None:
            return "Customer not found."

        if amount is None or amount <= 0:
            return "Invalid amount."

        if customer["balance"] < amount:
            return "Insufficient balance."

        customer["balance"] -= amount

        self.transactions.append({
            "type": "withdraw",
            "customer_id": str(customer_id),
            "amount": amount
        })

        return "Withdraw successful."

    # Transfer money
    def transfer_money(self, sender_id, receiver_id, amount):
        sender = self.find_customer(sender_id)
        receiver = self.find_customer(receiver_id)
        amount = self.validate_amount(amount)

        if sender is None or receiver is None:
            return "Customer not found."

        if sender_id == receiver_id:
            return "Cannot transfer to the same account."

        if amount is None or amount <= 0:
            return "Invalid amount."

        if sender["balance"] < amount:
            return "Insufficient balance."

        sender["balance"] -= amount
        receiver["balance"] += amount

        self.transactions.append({
            "type": "transfer_out",
            "customer_id": str(sender_id),
            "amount": amount,
            "to": str(receiver_id)
        })

        self.transactions.append({
            "type": "transfer_in",
            "customer_id": str(receiver_id),
            "amount": amount,
            "from": str(sender_id)
        })

        return "Transfer successful."

    # Customer statistics
    def calculate_number_customer(self):
        if not self.customer_list:
            return "No customers found."

        sorted_customers = sorted(
            self.customer_list,
            key=lambda x: (
                0, int(x["id"])
            ) if x["id"].isdigit() else (
                1, x["id"]
            )
        )

        total_balance = sum(
            customer["balance"]
            for customer in self.customer_list
        )

        return {
            "total_balance": total_balance,
            "smallest_id": sorted_customers[0]["id"],
            "largest_id": sorted_customers[-1]["id"],
            "total_customers": len(self.customer_list)
        }

    # Transaction history
    def transaction_history(self, customer_id):
        if not self.find_customer(customer_id):
            return "Customer not found."

        history = [
            transaction
            for transaction in self.transactions
            if transaction["customer_id"] == str(customer_id)
        ]

        return history if history else "No transactions found."

    # Transaction statistics
    def average_access(self):
        if not self.transactions:
            return "No transactions found."

        deposits = [
            t["amount"] for t in self.transactions
            if t["type"] == "deposit"
        ]

        withdrawals = [
            t["amount"] for t in self.transactions
            if t["type"] == "withdraw"
        ]

        return {
            "total_operations": len(self.transactions),
            "deposit_count": len(deposits),
            "withdraw_count": len(withdrawals),
            "average_transaction": sum(
                t["amount"] for t in self.transactions
            ) / len(self.transactions)
        }



# ---------------- EXECUTION ----------------

initial_customers = [
    {"id": "12", "balance": 1000},
    {"id": "44", "balance": 2500},
    {"id": "55", "balance": 500},
    {"id": "60", "balance": 3000},
    {"id": "70", "balance": 1500},
    {"id": "80", "balance": 4000}
]

my_bank = Bank(initial_customers)

while True:
    print("\n===== BANK SYSTEM =====")
    print("1. Add Customer")
    print("2. Show Balance")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Transfer")
    print("6. Transaction History")
    print("7. Statistics")
    print("8. Exit")

    choice = input("Choose an operation: ").strip()

    if choice == "1":
        customer_id = input("Enter customer ID: ")
        balance = input("Enter initial balance: ")
        print(my_bank.add_customer(customer_id, balance))

    elif choice == "2":
        customer_id = input("Enter customer ID: ")
        print(my_bank.show_balance(customer_id))

    elif choice == "3":
        customer_id = input("Enter customer ID: ")
        amount = input("Enter deposit amount: ")
        print(my_bank.deposit_money(customer_id, amount))

    elif choice == "4":
        customer_id = input("Enter customer ID: ")
        amount = input("Enter withdrawal amount: ")
        print(my_bank.withdraw_money(customer_id, amount))

    elif choice == "5":
        sender = input("Enter sender ID: ")
        receiver = input("Enter receiver ID: ")
        amount = input("Enter transfer amount: ")
        print(my_bank.transfer_money(sender, receiver, amount))

    elif choice == "6":
        customer_id = input("Enter customer ID: ")
        print(my_bank.transaction_history(customer_id))

    elif choice == "7":
        print(my_bank.calculate_number_customer())
        print(my_bank.average_access())

    elif choice == "8":
        print("Thank you for using our bank!")
        break

    else:
        print("Invalid choice. Try again.")
