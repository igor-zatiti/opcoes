import numpy as np
import matplotlib.pyplot as plt

class Option:
    def __init__(self, opt_type, direction, strike, premium, quantity=1):
        self.opt_type = opt_type.lower()
        self.direction = 1 if direction in [1, 'long', 'buy', 'comprado', 'compra'] else -1
        self.strike = float(strike)
        self.premium = float(premium)
        self.quantity = int(quantity)

    def payoff(self, price):
        price = float(price)
        if self.opt_type == 'call':
            intrinsic = max(price - self.strike, 0)
        else:
            intrinsic = max(self.strike - price, 0)
        if self.direction == 1:
            return self.quantity * (intrinsic - self.premium)
        else:
            return self.quantity * (self.premium - intrinsic)

class Portfolio:
    def __init__(self):
        self.options = []

    def add_option(self, option):
        self.options.append(option)

    def payoff(self, price):
        return sum(opt.payoff(price) for opt in self.options)

    def price_range(self):
        if not self.options:
            return np.linspace(0, 100, 100)
        strikes = [opt.strike for opt in self.options]
        min_price = min(strikes) * 0.5
        max_price = max(strikes) * 1.5
        return np.linspace(min_price, max_price, 200)

    def __str__(self):
        lines = []
        for i, opt in enumerate(self.options, 1):
            dir_text = 'Long' if opt.direction == 1 else 'Short'
            lines.append(f"{i}. {dir_text} {opt.opt_type.title()} - Strike {opt.strike} - Premium {opt.premium} - Qty {opt.quantity}")
        return "\n".join(lines)


def main():
    portfolio = Portfolio()

    while True:
        print("\nCurrent portfolio:")
        if portfolio.options:
            print(portfolio)
        else:
            print("(empty)")
        print("\nMenu:")
        print("1. Add option")
        print("2. Show payoff graph")
        print("3. Exit")
        choice = input("Select: ").strip()

        if choice == '1':
            opt_type = input("Option type (call/put): ").strip().lower()
            if opt_type not in {'call', 'put'}:
                print("Invalid option type. Use 'call' or 'put'.")
                continue
            direction = input("Direction (long/short): ").strip().lower()
            if direction not in {'long', 'short'}:
                print("Invalid direction. Use 'long' or 'short'.")
                continue
            strike = input("Strike price: ")
            premium = input("Premium: ")
            quantity = input("Quantity (default 1): ").strip() or '1'
            option = Option(opt_type, direction, strike, premium, quantity)
            portfolio.add_option(option)
            print("Option added.")
        elif choice == '2':
            if not portfolio.options:
                print("No options in portfolio.")
                continue
            prices = portfolio.price_range()
            payoff = [portfolio.payoff(p) for p in prices]
            plt.figure()
            plt.plot(prices, payoff, label='Payoff')
            plt.axhline(0, color='gray', linestyle='--')
            plt.xlabel('Underlying Price')
            plt.ylabel('Profit / Loss')
            plt.title('Option Strategy Payoff')
            plt.legend()
            plt.show()
        elif choice == '3':
            break
        else:
            print("Invalid selection.")

if __name__ == '__main__':
    main()
