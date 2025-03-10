import random

# Define the Roulette wheel with 37 slots (0-36)
roulette_wheel = list(range(37))

def spin_wheel():
    return random.choice(roulette_wheel)

def bet_on_red_or_black(number):
    return number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

def bet_on_first_half(number):
    return number in range(1, 19)

def bet_on_rows(number):
    # Example: Bet on the first row (1-3)
    return number in [1, 2, 3]

# Define betting systems
def martingale(balance, unit=1):
    bet = unit
    while balance > 0:
        yield bet
        result = spin_wheel()
        if bet_on_red_or_black(result):  # Example: Bet on red/black
            balance += bet
        else:
            balance -= bet
        bet *= 2

def fibonacci(balance):
    a, b = 1, 1
    while balance > 0:
        yield min(a, balance)
        result = spin_wheel()
        if bet_on_red_or_black(result):  # Example: Bet on red/black
            balance += a
        else:
            balance -= a
        a, b = b, a + b

def d_alambert(balance, unit=1):
    bet = unit
    while balance > 0:
        yield bet
        result = spin_wheel()
        if bet_on_red_or_black(result):  # Example: Bet on red/black
            balance += bet
        else:
            balance -= bet
        bet += (-1 if bet_on_red_or_black(result) else 1) * unit

# Add more betting systems here...

def simulate_roulette(systems, rounds=100):
    results = {name: [] for name in systems}
    initial_balance = 1000  # Starting balance
    for _ in range(rounds):
        balances = {name: initial_balance for name in systems}
        for system_name, system_func in systems.items():
            generator = system_func(balances[system_name])
            try:
                while True:
                    bet_amount = next(generator)
                    result = spin_wheel()
                    if bet_on_red_or_black(result):  # Example: Bet on red/black
                        balances[system_name] += bet_amount
                    else:
                        balances[system_name] -= bet_amount
            except StopIteration:
                results[system_name].append(balances[system_name])
    return results

# Define the betting systems to test
betting_systems = {
    "Martingale": martingale,
    "Fibonacci": fibonacci,
    "D'Alembert": d_alambert,
    # Add more systems here...
}

# Run the simulation
results = simulate_roulette(betting_systems)

# Output the results
for system_name, balances in results.items():
    print(f"{system_name} System Results:")
    for i, balance in enumerate(balances):
        print(f"Game {i+1}: Balance = {balance}")