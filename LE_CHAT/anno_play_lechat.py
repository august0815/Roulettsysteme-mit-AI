import random
import matplotlib.pyplot as plt

class RouletteSimulation:
    def __init__(self, strategies, initial_balance=500, min_bet=5, max_bet=500, table_max=1000):
        self.strategies = strategies
        self.initial_balance = initial_balance
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.table_max = table_max
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

            # Bankroll-Management: Einsatz darf nicht höher als das Tischmaximum oder den Kontostand sein
            if bet > min(balance, self.table_max):
                bet = min(balance, self.table_max)

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

    def simulate(self, rounds=240, days=2):
        for day in range(days):
            for _ in range(rounds // days):
                self.play_round()
            # Reset balance for each day
            for name in self.results:
                self.results[name].append(self.initial_balance)
        self.print_results()
        self.plot_results()

    def print_results(self):
        for name, balance_history in self.results.items():
            final_balance = balance_history[-1]
            print(f"{name}: Endguthaben = {final_balance}")

    def plot_results(self):
        plt.figure(figsize=(14, 8))
        for name, balance_history in self.results.items():
            plt.plot(balance_history, label=name)
        plt.xlabel('Runde')
        plt.ylabel('Guthaben')
        plt.title('Roulette-Simulation: Guthabenverlauf')
        plt.legend()
        plt.grid(True)
        plt.show()

# Definition der Setzstrategien
def martingale(previous_bets, balance):
    if not previous_bets:
        return 5
    return min(previous_bets[-1] * 2, balance)

def anti_martingale(previous_bets, balance):
    if not previous_bets:
        return 5
    return max(previous_bets[-1] // 2, 5)

def fibonacci(previous_bets, balance):
    if len(previous_bets) < 2:
        return 5
    return min(previous_bets[-1] + previous_bets[-2], balance)

def paroli(previous_bets, balance):
    if not previous_bets or len(previous_bets) == 1:
        return 5
    if previous_bets[-1] < previous_bets[-2]:
        return 5
    return min(previous_bets[-1] * 2, balance)

def d_alembert(previous_bets, balance):
    if not previous_bets:
        return 5
    return min(previous_bets[-1] + 5 if previous_bets[-1] < 0 else max(previous_bets[-1] - 5, 5), balance)

def labouchere(sequence, balance):
    if not sequence:
        return 5
    bet = sequence[0] + sequence[-1]
    return min(bet, balance)

def oscar_grind(previous_bets, balance):
    if not previous_bets or sum(previous_bets) >= 1:
        return 5
    return min(previous_bets[-1] + 5, balance)

def one_three_two_six(previous_bets, balance):
    sequence = [5, 15, 10, 30]
    if not previous_bets:
        return sequence[0]
    return min(sequence[len(previous_bets) % len(sequence)], balance)

def james_bond(previous_bets, balance):
    return min(200, balance)  # Beispiel: Setze 200 Einheiten

def all_in(previous_bets, balance):
    return balance

def andrucci(previous_bets, balance, chosen_number=7):
    if not previous_bets or previous_bets[-1] != chosen_number:
        return 5
    return min(previous_bets[-1], balance)

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
simulation.simulate(rounds=240, days=2)
