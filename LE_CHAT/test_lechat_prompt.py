import random

class RouletteSimulation:
    def __init__(self, strategies, initial_balance=100):
        self.strategies = strategies
        self.initial_balance = initial_balance
        self.results = {name: [] for name in strategies.keys()}

    def spin(self):
        # Simuliert einen Roulette-Spin (0-36)
        return random.randint(0, 36)

    def play_round(self):
        result = self.spin()
        for name, strategy in self.strategies.items():
            if not self.results[name]:
                self.results[name].append(self.initial_balance)

            balance = self.results[name][-1]
            bet = strategy(self.results[name][1:], balance)

            if bet > balance:
                bet = balance

            # Überprüfen, ob der Einsatz gewonnen hat
            if self.is_winning_bet(result, bet):
                balance += bet * 35  # Gewinn bei einer Zahl
            else:
                balance -= bet

            self.results[name].append(balance)

    def is_winning_bet(self, result, bet):
        # Hier können verschiedene Setzarten überprüft werden
        # Für dieses Beispiel nehmen wir an, dass nur auf eine Zahl gesetzt wird
        return result == bet

    def simulate(self, rounds=100):
        for _ in range(rounds):
            self.play_round()
        self.print_results()

    def print_results(self):
        for name, balance_history in self.results.items():
            final_balance = balance_history[-1]
            print(f"{name}: Endguthaben = {final_balance}")

# Definition der Setzstrategien
def martingale(previous_bets, balance):
    if not previous_bets:
        return 1
    return previous_bets[-1] * 2

def anti_martingale(previous_bets, balance):
    if not previous_bets:
        return 1
    return previous_bets[-1] // 2 or 1

def fibonacci(previous_bets, balance):
    if len(previous_bets) < 2:
        return 1
    return previous_bets[-1] + previous_bets[-2]

def paroli(previous_bets, balance):
    if not previous_bets or len(previous_bets) == 1:
        return 1
    if previous_bets[-1] < previous_bets[-2]:
        return 1
    return previous_bets[-1] * 2

def d_alembert(previous_bets, balance):
    if not previous_bets:
        return 1
    return previous_bets[-1] + 1 if previous_bets[-1] < 0 else previous_bets[-1] - 1

def labouchere(sequence, balance):
    if not sequence:
        return 1
    bet = sequence[0] + sequence[-1]
    return bet

def oscar_grind(previous_bets, balance):
    if not previous_bets or sum(previous_bets) >= 1:
        return 1
    return previous_bets[-1] + 1

def one_three_two_six(previous_bets, balance):
    sequence = [1, 3, 2, 6]
    if not previous_bets:
        return sequence[0]
    return sequence[len(previous_bets) % len(sequence)]

def james_bond(previous_bets, balance):
    return min(balance, 200)  # Beispiel: Setze 200 Einheiten

def all_in(previous_bets, balance):
    return balance

def andrucci(previous_bets, balance, chosen_number=7):
    if not previous_bets or previous_bets[-1] != chosen_number:
        return 1
    return previous_bets[-1]

# Strategien in einem Dictionary speichern
strategies = {
    "Martingale": martingale,
    "Anti-Martingale": anti_martingale,
    "Fibonacci": fibonacci,
    "Paroli": paroli,
    "D'Alembert": d_alembert,
    "Labouchere": labouchere,
    "Oscar's Grind": oscar_grind,
    "1-3-2-6": one_three_two_six,
    "James Bond": james_bond,
    "All-In": all_in,
    "Andrucci": andrucci
}

# Simulation starten
simulation = RouletteSimulation(strategies)
simulation.simulate(rounds=100)
