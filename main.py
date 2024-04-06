class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.balance_sheet = {}

    def update_balance(self, other_user_id, amount):
        if other_user_id in self.balance_sheet:
            self.balance_sheet[other_user_id] += amount
        else:
            self.balance_sheet[other_user_id] = amount

    def print_balance_sheet(self):
        for user_id, amount in self.balance_sheet.items():
            action = "owes" if amount < 0 else "is owed"
            print(f"{self.name} {action} {abs(amount)} by {user_id}")

class Split:
    def __init__(self, user, amount=0):
        self.user = user
        self.amount = amount

class Expense:
    def __init__(self, amount, paid_by, splits):
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits

    def settle_expense(self):
        raise NotImplementedError

class EqualExpense(Expense):
    def settle_expense(self):
        each_share = self.amount / len(self.splits)
        for split in self.splits:
            split.amount = each_share
            owed_amount = each_share - split.amount
            self.paid_by.update_balance(split.user.user_id, -owed_amount)
            split.user.update_balance(self.paid_by.user_id, owed_amount)

class ExactExpense(Expense):
    def settle_expense(self):
        for split in self.splits:
            owed_amount = split.amount
            self.paid_by.update_balance(split.user.user_id, -owed_amount)
            split.user.update_balance(self.paid_by.user_id, owed_amount)

class PercentageExpense(Expense):
    def settle_expense(self):
        for split in self.splits:
            owed_amount = (self.amount * split.amount) / 100 
            self.paid_by.update_balance(split.user.user_id, -owed_amount)
            split.user.update_balance(self.paid_by.user_id, owed_amount)

class ExpenseFactory:
    @staticmethod
    def create_expense(expense_type, amount, paid_by, splits):
        if expense_type == "EQUAL":
            return EqualExpense(amount, paid_by, splits)
        elif expense_type == "EXACT":
            return ExactExpense(amount, paid_by, splits)
        elif expense_type == "PERCENTAGE":
            return PercentageExpense(amount, paid_by, splits)
        else:
            raise ValueError("Unknown expense type")


users = {
    "1": User("1", "Ram"),  
    "2": User("2", "Shyam"),
    "3": User("3", "Gyan"),
}

def add_expense(expense_type, amount, paid_by_id, split_info):
    paid_by = users[paid_by_id]  
    splits = []
    for user_id, share in split_info.items():
        if user_id in users:  
            splits.append(Split(users[user_id], share))
        else:
            print(f"User ID {user_id} not found in users.")
    expense = ExpenseFactory.create_expense(expense_type, amount, paid_by, splits)
    expense.settle_expense()


if __name__ == "__main__":
    add_expense("EXACT", 300, "1", {"2": 100, "3": 200})
    add_expense("EQUAL", 300, "1", {"2": 0, "3": 0})  

    for user in users.values():
        user.print_balance_sheet()

