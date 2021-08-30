class Category:

    def __init__(self, name):
        self.ledger = list()
        self.name = name.title()

    def __str__(self):
        result = f"{self.name.center(30, '*')}\n"
        for entry in self.ledger:
            amt = "{:.2f}".format(entry['amount'])
            result = result + f"{entry['description'].ljust(23)[:23]}{amt.rjust(7)[:7]}\n"
        total = "{:.2f}".format(self.get_balance())
        result = result + f"Total: {total}"
        return result

    def deposit(self, amount, description = ''):
        self.ledger.append( { "amount": amount, "description": description } )

    def get_balance(self):
        balance = 0
        for entry in self.ledger:
            balance += entry["amount"]
        return balance

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.deposit(amount * -1, description)
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def transfer(self, amount, category):
        if self.withdraw(amount, f"Transfer to {category.name}"):
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False


def create_spend_chart(categories):
    chart = {
        100: '100| ',
        90: ' 90| ',
        80: ' 80| ',
        70: ' 70| ',
        60: ' 60| ',
        50: ' 50| ',
        40: ' 40| ',
        30: ' 30| ',
        20: ' 20| ',
        10: ' 10| ',
        0: '  0| '
    }
    category_names = list()
    spent = list()
    total = 0
    result = "Percentage spent by category\n"
    for category in categories:
        category_names.append(category.name)
        cat_total = get_spent(category)
        spent.append(cat_total)
        total += cat_total
    fill_chart(chart, [int((cat / total) * 10) * 10 for cat in spent])
    for x in range(100, -1, -10):
        result += f"{chart[x]}\n"
    result += "-".rjust(5) + "-" * (len(categories) * 3)
    result += add_category_names(category_names)
    return result


def add_category_names(names):
    rows = len(max(names, key=len))
    names_string = ""
    for row in range(0, rows):
        text = "\n" + " " * 5
        for name in names:
            if row < len(name):
                text += name[row].ljust(3)
            else:
                text += " " * 3
        names_string += text
    return names_string


def fill_chart(chart, percentages):
    for percentage in percentages:
        for key in range(100, -1, -10):
            if key > percentage:
                chart[key] += ' ' * 3
            else:
                chart[key] += 'o'.ljust(3)


def get_spent(category):
    spent = 0
    for entry in category.ledger:
        if entry['amount'] < 0:
            spent += abs(entry['amount'])
    return spent