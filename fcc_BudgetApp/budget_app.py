class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        total = 0
        lines = []
        lines.append(f"{self.name.center(30, '*')}")

        for entry in self.ledger:
            total += entry["amount"]
            desc = entry['description'][:23]
            amt_str = f"{entry['amount']:.2f}"[:7]
            lines.append(f"{desc.ljust(23)}{amt_str.rjust(7)}")
        lines.append(f"Total: {total:.2f}")

        return '\n'.join(lines)


    def deposit(self, amount, description = ''):
        if amount < 0:
            print("Amount should be positive.")
            return
        entry = {'amount': amount, 'description': description}
        self.ledger.append(entry)

    def withdraw(self, amount, description = ''):
        if amount <= 0:
            print("Amount should be greater than zero.")
            return False
        if not self.check_funds(amount):
            return False
        
        entry = {'amount': -amount, 'description': description}
        self.ledger.append(entry)
        return True
        
    def get_balance(self):
        if not self.ledger:
            return 0
        bal = 0
        for i in self.ledger:
            bal += i['amount']
        return bal

    def transfer(self, amount, category):
        if amount < 0:
            print('Amount cannot be negative')
            return False
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        if amount < 0:
            print('Amount cannot be negative')
            return False
        return amount <= self.get_balance()


def create_spend_chart(categories):
    category_spends = {}
    # creating a dict[category_name: spent]
    for category in categories:
        spend = 0

        for entry in category.ledger:
            amount = entry['amount']
            if amount < 0:
                spend += -amount
    
        category_spends[category.name] = spend

    total_spend = sum(category_spends.values())
        
    # calculating percent spent for category
    category_percentages = {}
    for key, value in category_spends.items():
        percent = (value / total_spend * 100) if total_spend > 0 else 0
        category_percentages[key] = percent


    # Chart Body
    chart = []
    chart.append("Percentage spent by category")
    # x-axis
    for i in range(100, -1, -10):
        line = f"{i:3}| "
        for percent in category_percentages.values():
            if i <= percent:
                line += "o  "
            else:
                line += "   "
        chart.append(line)

    # matching key lengths to the max_key_len
    cat_names = list(category_percentages.keys())
    max_len_name = len(max(cat_names, key=lambda x: len(x)))
    padded_names = [name.ljust(max_len_name) for name in cat_names]

    # y - axis
    n = len(category_percentages)
    chart.append(f"    -{'---'*n}")

    for chars in zip(*padded_names):
        line = "     " + "".join(f"{char}  " for char in chars)
        chart.append(line)

    return "\n".join(chart)

# ------------ Testing

def main():
    wallet = Category('wallet')
    wallet.deposit(15000.00)

    cash = Category('cash')
    cash.deposit(10000)

    misc = Category('misc')

    wallet.transfer(3500, misc)
    cash.transfer(4250, misc)


    categories = [wallet, cash]
    print(create_spend_chart(categories))


if __name__ == "__main__":
    main()