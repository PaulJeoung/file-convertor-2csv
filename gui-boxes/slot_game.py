import random
import tkinter as tk
from tkinter import messagebox

class SlotMachine:
    def __init__(self):
        self.symbols = ['Cherry', 'Bell', 'Lemon', 'Orange', 'Star', 'Apple']
        self.prices = {'Cherry': 2, 'Bell': 5, 'Lemon': 3, 'Orange': 4, 'Star': 10, 'Apple': 7}

    def spin(self):
        result = [random.choice(self.symbols) for _ in range(3)]
        return result

    def calculate_reward(self, symbols, bet):
        symbol_counts = {symbol: symbols.count(symbol) for symbol in set(symbols)}
        total_reward = 0
        for symbol, count in symbol_counts.items():
            if count >= 2:  # Two or more symbols in a row
                total_reward += self.prices[symbol] * count
        return total_reward * bet

def spin_slot_machine():
    global balance
    bet = int(bet_entry.get())
    if bet >= balance:
        messagebox.showinfo("Invalid Bet", "Bet amount cannot exceed balance.")
        return
    
    spin_button.config(state=tk.DISABLED)
    symbols = slot_machine.spin()
    reward = slot_machine.calculate_reward(symbols, bet)

    spin_animation(symbols)
    root.after(100, lambda: update_balance_and_result(symbols, reward, bet))

def spin_animation(symbols):
    for i in range(25):
        new_symbols = [random.choice(slot_machine.symbols) for _ in range(3)]
        result_label.config(text="Spinning: " + ' - '.join(new_symbols))
        root.update()
        root.after(50)

def update_balance_and_result(symbols, reward, bet):
    global balance
    if reward > 0:
        balance += reward
    else:
        balance -= bet
    update_balance_label(balance)
    update_result_label(symbols, reward)
    # Enable spin button after animation completes
    spin_button.config(state=tk.NORMAL)

def update_result_label(symbols, reward, bet):
    result_label.config(text=f"Result: {symbols}. {'Congratulations! You won $' + str(reward) if reward > 0 else '{bet}을 잃었네요...'}")

def update_balance_label(balance):
    balance_label.config(text=f"Balance: ${balance}")

slot_machine = SlotMachine()

root = tk.Tk()
root.title("Slot Machine")

balance = 100
balance_label = tk.Label(root, text=f"Balance: ${balance}")
balance_label.pack()

bet_label = tk.Label(root, text="Enter bet amount:")
bet_label.pack()

bet_entry = tk.Entry(root)
bet_entry.pack()

spin_button = tk.Button(root, text="Spin", command=spin_slot_machine)
spin_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack()

root.mainloop()
