import random
import matplotlib.pyplot as plt
import numpy as np


def simulate_roulette(betting_system, initial_bankroll=1000, max_rounds=1000, min_bet=1, max_bet=1000):
    """
    Simuliert eine Roulette-Spielsession mit einem bestimmten Wettsystem

    Args:
        betting_system: Funktion, die die Wettstrategie implementiert
        initial_bankroll: Startkapital
        max_rounds: Maximale Anzahl an Spielrunden
        min_bet: Minimaler Einsatz pro Runde
        max_bet: Maximaler Einsatz pro Runde

    Returns:
        tuple: (Liste mit Kapitalverlauf, Endkapital, Anzahl gespielter Runden)
    """
    bankroll = initial_bankroll
    bankroll_history = [bankroll]
    rounds_played = 0

    # Wir verfolgen, wie oft wir gewonnen haben
    wins = 0
    losses = 0

    # Systemspezifischer Status, der zwischen den Runden übergeben wird
    system_state = {}

    for _ in range(max_rounds):
        if bankroll <= 0:
            break

        # Hole Wette vom Wettsystem
        bet_type, bet_amount, numbers = betting_system(bankroll, rounds_played, wins, losses, system_state, min_bet,
                                                       max_bet)

        # Stelle sicher, dass der Einsatz gültig ist
        bet_amount = min(max(bet_amount, min_bet), max_bet)
        bet_amount = min(bet_amount, bankroll)

        if bet_amount < min_bet:
            break

        # Simulation der Roulettedrehung (0-36)
        result = random.randint(0, 36)

        # Prüfe, ob gewonnen wurde
        won = False
        payout = 0

        if bet_type == "straight" and result in numbers:
            # Straight Bet (einzelne Zahl): 35 zu 1
            payout = bet_amount * 36
            won = True
        elif bet_type == "split" and result in numbers:
            # Split Bet (zwei Zahlen): 17 zu 1
            payout = bet_amount * 18
            won = True
        elif bet_type == "street" and result in numbers:
            # Street Bet (drei Zahlen): 11 zu 1
            payout = bet_amount * 12
            won = True
        elif bet_type == "corner" and result in numbers:
            # Corner Bet (vier Zahlen): 8 zu 1
            payout = bet_amount * 9
            won = True
        elif bet_type == "six_line" and result in numbers:
            # Six Line Bet (sechs Zahlen): 5 zu 1
            payout = bet_amount * 6
            won = True
        elif bet_type == "dozen" and result in numbers:
            # Dozen Bet (12 Zahlen): 2 zu 1
            payout = bet_amount * 3
            won = True
        elif bet_type == "column" and result in numbers:
            # Column Bet (12 Zahlen): 2 zu 1
            payout = bet_amount * 3
            won = True
        elif bet_type == "even_odd" and result in numbers and result != 0:
            # Gerade/Ungerade: 1 zu 1
            payout = bet_amount * 2
            won = True
        elif bet_type == "red_black" and result in numbers and result != 0:
            # Rot/Schwarz: 1 zu 1
            payout = bet_amount * 2
            won = True
        elif bet_type == "low_high" and result in numbers and result != 0:
            # Niedrig/Hoch: 1 zu 1
            payout = bet_amount * 2
            won = True

        # Aktualisiere Bankroll
        if won:
            wins += 1
            bankroll = bankroll - bet_amount + payout
        else:
            losses += 1
            bankroll = bankroll - bet_amount

        bankroll_history.append(bankroll)
        rounds_played += 1

        # Stoppe, wenn wir das Ziel erreicht haben
        if bankroll <= 0:
            break

    return bankroll_history, bankroll, rounds_played


def compare_systems(systems, runs=100, initial_bankroll=1000, max_rounds=1000):
    """
    Vergleicht die Performance verschiedener Wettsysteme

    Args:
        systems: Liste von Wettsystem-Funktionen
        runs: Anzahl der Simulationen pro System
        initial_bankroll: Startkapital für jede Simulation
        max_rounds: Maximale Anzahl an Runden pro Simulation

    Returns:
        dict: Performance-Statistiken für jedes System
    """
    results = {}

    for system_func in systems:
        system_name = system_func.__name__
        print(f"Simuliere {system_name}...")

        system_results = []
        bankrolls = []
        rounds = []

        for _ in range(runs):
            bankroll_history, final_bankroll, rounds_played = simulate_roulette(
                system_func, initial_bankroll, max_rounds
            )
            system_results.append(bankroll_history)
            bankrolls.append(final_bankroll)
            rounds.append(rounds_played)

        results[system_name] = {
            "avg_bankroll": np.mean(bankrolls),
            "med_bankroll": np.median(bankrolls),
            "min_bankroll": np.min(bankrolls),
            "max_bankroll": np.max(bankrolls),
            "std_bankroll": np.std(bankrolls),
            "avg_rounds": np.mean(rounds),
            "profit_rate": sum(1 for b in bankrolls if b > initial_bankroll) / runs,
            "bankroll_histories": system_results
        }

    return results


def plot_results(results, initial_bankroll=1000):
    """
    Erstellt Plots zum Vergleich der Wettsysteme

    Args:
        results: Performance-Statistiken für jedes System
        initial_bankroll: Startkapital für jede Simulation
    """
    # Plot für durchschnittliches Endkapital
    plt.figure(figsize=(12, 6))
    systems = list(results.keys())
    avg_bankrolls = [results[system]["avg_bankroll"] for system in systems]

    plt.bar(systems, avg_bankrolls)
    plt.axhline(y=initial_bankroll, color='r', linestyle='-', label='Initial Bankroll')
    plt.title('Durchschnittliches Endkapital nach Wettsystem')
    plt.ylabel('Endkapital')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot für Gewinnrate
    plt.figure(figsize=(12, 6))
    profit_rates = [results[system]["profit_rate"] * 100 for system in systems]

    plt.bar(systems, profit_rates)
    plt.title('Gewinnrate nach Wettsystem (% der Simulationen mit Profit)')
    plt.ylabel('Gewinnrate (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Beispielhafte Verläufe für jedes System
    plt.figure(figsize=(14, 8))
    for system in systems:
        # Wähle eine zufällige Simulation aus
        histories = results[system]["bankroll_histories"]
        random_idx = random.randint(0, len(histories) - 1)
        history = histories[random_idx]
        plt.plot(history, label=system)

    plt.axhline(y=initial_bankroll, color='r', linestyle='--', label='Initial Bankroll')
    plt.title('Beispielhafter Verlauf des Kapitals nach Wettsystem')
    plt.xlabel('Anzahl Spiele')
    plt.ylabel('Bankroll')
    plt.legend()
    plt.tight_layout()
    plt.show()


# Definition der Roulette-Systeme
# Alle geben zurück: (bet_type, bet_amount, list_of_numbers)

def martingale_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Martingale-System: Nach jedem Verlust verdoppeln wir den Einsatz.
    Setzt auf Rot/Schwarz.
    """
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    if not state:
        state["current_bet"] = min_bet

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            # Nach einem Gewinn gehen wir zurück zum Mindesteinsatz
            state["current_bet"] = min_bet
            state["last_win"] = False
        else:
            # Nach einem Verlust verdoppeln wir den Einsatz
            state["current_bet"] = min(state["current_bet"] * 2, max_bet, bankroll)

    bet_amount = state["current_bet"]

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "red_black", bet_amount, red_numbers


def reverse_martingale_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Umgekehrtes Martingale-System: Nach jedem Gewinn verdoppeln wir den Einsatz.
    Setzt auf Rot/Schwarz.
    """
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    if not state:
        state["current_bet"] = min_bet

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            # Nach einem Gewinn verdoppeln wir den Einsatz
            state["current_bet"] = min(state["current_bet"] * 2, max_bet, bankroll)
            state["last_win"] = False
        else:
            # Nach einem Verlust zurück zum Mindesteinsatz
            state["current_bet"] = min_bet

    bet_amount = state["current_bet"]

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "red_black", bet_amount, black_numbers


def dalembert_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    D'Alembert-System: Nach Verlust erhöhen wir den Einsatz um die Einheit, nach Gewinn verringern.
    Setzt auf Gerade/Ungerade.
    """
    even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]

    if not state:
        state["current_bet"] = min_bet
        state["unit"] = min_bet

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            # Nach einem Gewinn verringern wir den Einsatz um eine Einheit
            state["current_bet"] = max(state["current_bet"] - state["unit"], min_bet)
            state["last_win"] = False
        else:
            # Nach einem Verlust erhöhen wir den Einsatz um eine Einheit
            state["current_bet"] = min(state["current_bet"] + state["unit"], max_bet, bankroll)

    bet_amount = state["current_bet"]

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "even_odd", bet_amount, even_numbers


def fibonacci_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Fibonacci-System: Der Einsatz folgt der Fibonacci-Folge nach Verlusten.
    Setzt auf Niedrig/Hoch.
    """
    high_numbers = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]

    if not state:
        state["sequence"] = [1, 1]
        state["position"] = 0

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            # Nach einem Gewinn gehen wir zwei Positionen zurück
            state["position"] = max(0, state["position"] - 2)
            state["last_win"] = False
        else:
            # Nach einem Verlust bewegen wir uns in der Sequenz nach vorne
            if state["position"] + 1 >= len(state["sequence"]):
                # Erweitere die Fibonacci-Sequenz um einen Wert
                state["sequence"].append(state["sequence"][-1] + state["sequence"][-2])
            state["position"] += 1

    # Stelle sicher, dass wir nicht über die Grenzen gehen
    state["position"] = min(state["position"], len(state["sequence"]) - 1)

    bet_amount = min(state["sequence"][state["position"]] * min_bet, max_bet, bankroll)

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "low_high", bet_amount, high_numbers


def labouchere_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Labouchere-System: Basiert auf einer Liste von Zahlen, Einsatz ist die Summe des ersten und letzten Elements.
    Setzt auf Rot/Schwarz.
    """
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

    if not state:
        # Beginne mit einer Liste von Einheiten
        state["sequence"] = [1, 2, 3, 4, 5]

    if not state["sequence"]:
        # Wenn die Sequenz leer ist, starten wir neu
        state["sequence"] = [1, 2, 3, 4, 5]

    if len(state["sequence"]) == 1:
        bet_amount = state["sequence"][0] * min_bet
    else:
        bet_amount = (state["sequence"][0] + state["sequence"][-1]) * min_bet

    # Begrenze den Einsatz
    bet_amount = min(bet_amount, max_bet, bankroll)

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "red_black", bet_amount, red_numbers


def oscar_grind_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Oscar's Grind-System: Ziel ist es, 1 Einheit Profit zu machen und dann neu zu starten.
    Erhöht den Einsatz nach Gewinnen, bleibt gleich nach Verlusten.
    """
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    if not state:
        state["current_bet"] = min_bet
        state["profit"] = 0

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            state["profit"] += state["current_bet"]
            # Wenn wir unser Profit-Ziel erreicht haben, starten wir neu
            if state["profit"] >= min_bet:
                state["current_bet"] = min_bet
                state["profit"] = 0
            else:
                # Nach einem Gewinn erhöhen wir den Einsatz um eine Einheit (maximal bis zur Zielerreichung)
                next_bet = state["current_bet"] + min_bet
                # Stelle sicher, dass der nächste Einsatz nicht mehr als nötig ist, um das Ziel zu erreichen
                if state["profit"] + next_bet > min_bet:
                    next_bet = min_bet - state["profit"]
                state["current_bet"] = min(next_bet, max_bet)
            state["last_win"] = False
        else:
            state["profit"] -= state["current_bet"]
            # Nach einem Verlust bleibt der Einsatz gleich

    bet_amount = min(state["current_bet"], bankroll)

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "red_black", bet_amount, black_numbers


def paroli_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Paroli-System: Verdreifache den Einsatz nach einem Gewinn für bis zu drei Gewinne in Folge.
    Setzt auf Gerade/Ungerade.
    """
    odd_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]

    if not state:
        state["current_bet"] = min_bet
        state["win_streak"] = 0

    if rounds_played > 0:
        if "last_win" in state and state["last_win"]:
            state["win_streak"] += 1

            # Nach dem dritten Gewinn in Folge starten wir neu
            if state["win_streak"] >= 3:
                state["current_bet"] = min_bet
                state["win_streak"] = 0
            else:
                # Nach einem Gewinn verdreifachen wir den Einsatz
                state["current_bet"] = min(state["current_bet"] * 3, max_bet, bankroll)

            state["last_win"] = False
        else:
            # Nach einem Verlust gehen wir zurück zum Mindesteinsatz
            state["current_bet"] = min_bet
            state["win_streak"] = 0

    bet_amount = state["current_bet"]

    # Bestimme, ob wir gewonnen haben, für die nächste Runde
    state["last_win"] = False

    return "even_odd", bet_amount, odd_numbers


def andrucci_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Andrucci-System: Basiert auf der Annahme, dass bestimmte Zahlen in einem Zeitraum häufiger erscheinen.
    Beobachtet 30 Runden und setzt dann auf die häufigsten Zahlen.
    """
    if not state:
        state["observation"] = []
        state["betting_on"] = None
        state["observation_rounds"] = 30

    # In der Beobachtungsphase setzen wir minimal
    if len(state["observation"]) < state["observation_rounds"]:
        # Simuliere eine Zahl und füge sie zur Beobachtung hinzu
        simulated_number = random.randint(1, 36)
        state["observation"].append(simulated_number)

        # Wir setzen während der Beobachtungsphase auf Rot/Schwarz mit Minimaleinsatz
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        return "red_black", min_bet, red_numbers
    else:
        # Nach der Beobachtungsphase setzen wir auf die häufigste Zahl
        if not state["betting_on"]:
            # Finde die häufigste Zahl
            counts = {}
            for num in state["observation"]:
                if num not in counts:
                    counts[num] = 0
                counts[num] += 1

            # Sortiere nach Häufigkeit
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            # Wähle nur die häufigste Zahl aus
            state["betting_on"] = [sorted_counts[0][0]]

    # Setze auf die häufigste Zahl
    bet_amount = min(min_bet, bankroll)
    return "straight", bet_amount, state["betting_on"]


def james_bond_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    James Bond-System: Setze 14 Einheiten auf Hoch (19-36), 5 Einheiten auf Six-Line (13-18),
    1 Einheit auf 0.
    """
    if not state:
        state["unit"] = min_bet

    total_units = 20  # 14 + 5 + 1
    unit = min(max(min_bet, bankroll / total_units), max_bet / 14)
    state["unit"] = unit

    # Wir machen hier mehrere Wetten gleichzeitig, für die Simulation vereinfachen wir
    # und setzen auf die Zahlen 19-36 (Hoch) mit 70% des Einsatzes
    high_numbers = list(range(19, 37))
    return "low_high", 14 * unit, high_numbers


def column_bet_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    """
    Spalten-Wett-System: Setzt immer auf eine bestimmte Spalte.
    """
    # Erste Spalte: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
    column1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

    bet_amount = min(min_bet, bankroll)

    return "column", bet_amount, column1


# Sammlung aller Systeme
roulette_systems = [
    martingale_system,
    reverse_martingale_system,
    dalembert_system,
    fibonacci_system,
    labouchere_system,
    oscar_grind_system,
    paroli_system,
    andrucci_system,
    james_bond_system,
    column_bet_system
]

# Beispiel für den Aufruf der Vergleichsfunktion
if __name__ == "__main__":
    # Simuliere alle Systeme und vergleiche sie
    results = compare_systems(roulette_systems, runs=1000, initial_bankroll=1000, max_rounds=5000)

    # Plotte die Ergebnisse
    plot_results(results, initial_bankroll=1000)

    # Zeige detaillierte Statistiken
    print("\nDetaillierte Ergebnisse:")
    for system, stats in results.items():
        print(f"\n{system}:")
        print(f"  Durchschn. Endkapital: {stats['avg_bankroll']:.2f}")
        print(f"  Median Endkapital: {stats['med_bankroll']:.2f}")
        print(f"  Min/Max Endkapital: {stats['min_bankroll']:.2f} / {stats['max_bankroll']:.2f}")
        print(f"  Standardabweichung: {stats['std_bankroll']:.2f}")
        print(f"  Durchschn. Spielrunden: {stats['avg_rounds']:.2f}")
        print(f"  Gewinnrate: {stats['profit_rate'] * 100:.2f}%")