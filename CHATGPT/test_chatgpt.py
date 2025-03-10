import random

# ------------------------------
# Definition der Wett-Systeme
# Alle Funktionen haben den gleichen Aufruf: (bet_outcome, last_bet, state, base_bet)
# und liefern ein Tupel (next_bet, state)
# ------------------------------

def martingale_system(bet_outcome, last_bet, state, base_bet):
    # Bei Gewinn oder beim ersten Einsatz: setze den Grundeinsatz
    if bet_outcome is None or bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 2
    return next_bet, state

def reverse_martingale_system(bet_outcome, last_bet, state, base_bet):
    # Bei Gewinn: setze das Doppelte, bei Verlust oder Start: Grundeinsatz
    if bet_outcome is None or not bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 2
    return next_bet, state

def fibonacci_system(bet_outcome, last_bet, state, base_bet):
    # Fibonacci-Folge: state["fib_index"] hält den Index in der Folge (beginnend bei 0)
    if "fib_index" not in state:
        state["fib_index"] = 0

    def fib(n):
        a, b = 1, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    if bet_outcome is None:
        next_bet = base_bet
    else:
        if not bet_outcome:
            state["fib_index"] += 1
        else:
            state["fib_index"] = max(0, state["fib_index"] - 2)
        next_bet = fib(state["fib_index"]) * base_bet
    return next_bet, state

def labouchere_system(bet_outcome, last_bet, state, base_bet):
    # Labouchere: state["sequence"] enthält eine Liste von Zahlen
    if "sequence" not in state or not state["sequence"]:
        state["sequence"] = [1, 2, 3, 4]
    seq = state["sequence"]
    next_bet = (seq[0] + seq[-1]) * base_bet
    if bet_outcome is None:
        return next_bet, state
    if bet_outcome:
        if len(seq) > 1:
            state["sequence"] = seq[1:-1]
        else:
            state["sequence"] = []
    else:
        state["sequence"].append(seq[0] + seq[-1])
    if not state["sequence"]:
        state["sequence"] = [1, 2, 3, 4]
    return next_bet, state

def d_alembert_system(bet_outcome, last_bet, state, base_bet):
    # D'Alembert: Erhöhe bei Verlust den Einsatz um base_bet, senke bei Gewinn (aber nicht unter base_bet)
    if bet_outcome is None:
        next_bet = base_bet
    elif bet_outcome:
        next_bet = max(base_bet, last_bet - base_bet)
    else:
        next_bet = last_bet + base_bet
    return next_bet, state

def reverse_d_alembert_system(bet_outcome, last_bet, state, base_bet):
    # Reverse D'Alembert: Umgekehrte Logik
    if bet_outcome is None:
        next_bet = base_bet
    elif bet_outcome:
        next_bet = last_bet + base_bet
    else:
        next_bet = max(base_bet, last_bet - base_bet)
    return next_bet, state

def james_bond_system(bet_outcome, last_bet, state, base_bet):
    # James-Bond-System: Feste Wettstrategie (hier: 10-facher Grundeinsatz)
    next_bet = base_bet * 10
    return next_bet, state

def one_three_two_six_system(bet_outcome, last_bet, state, base_bet):
    # 1-3-2-6-System: Progression bei aufeinanderfolgenden Gewinnen
    sequence = [1, 3, 2, 6]
    if "stage" not in state:
        state["stage"] = 0
    if bet_outcome is None:
        state["stage"] = 0
    elif bet_outcome:
        state["stage"] += 1
        if state["stage"] >= len(sequence):
            state["stage"] = 0
    else:
        state["stage"] = 0
    next_bet = sequence[state["stage"]] * base_bet
    return next_bet, state

def oscars_grind_system(bet_outcome, last_bet, state, base_bet):
    # Oscar's Grind: Ziel ist ein Gewinn von einer Einheit pro Serie
    if "series_profit" not in state or "current_bet" not in state:
        state["series_profit"] = 0
        state["current_bet"] = base_bet
    if bet_outcome is None:
        next_bet = base_bet
    elif bet_outcome:
        state["series_profit"] += state["current_bet"]
        if state["series_profit"] >= base_bet:
            state["series_profit"] = 0
            state["current_bet"] = base_bet
        next_bet = state["current_bet"]
    else:
        state["series_profit"] -= state["current_bet"]
        state["current_bet"] += base_bet
        next_bet = state["current_bet"]
    return next_bet, state

def semi_martingale_system(bet_outcome, last_bet, state, base_bet):
    # Semi-Martingale: Bei Verlust Erhöhung um Faktor 1.5, bei Gewinn Zurücksetzen auf base_bet
    if bet_outcome is None or bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 1.5
    return next_bet, state


def andrucci_system(bet_outcome, last_bet, state, base_bet):
    """
    Andrucci-System:
    - Das System geht davon aus, dass nach einer Serie von Verlusten ein Gewinn folgen muss.
    - Es wird ein Verlustzähler ("loss_streak") im state geführt.
    - Bei Verlust wird der Verlustzähler um 1 erhöht und der nächste Einsatz beträgt:
          base_bet * (loss_streak + 1)^2
      (dadurch steigt der Einsatz quadratisch mit der Anzahl der Verluste).
    - Bei Gewinn wird der Verlustzähler zurückgesetzt und der Grundeinsatz gesetzt.

    Parameter:
      bet_outcome: Bool (True=Gewinn, False=Verlust, None=erster Einsatz)
      last_bet: Letzter Einsatzbetrag
      state: systemspezifischer Zustand (Dictionary)
      base_bet: Grundeinsatz

    Rückgabe:
      (next_bet, state)
    """
    # Initialisiere den Verlustzähler, falls noch nicht vorhanden:
    if "loss_streak" not in state:
        state["loss_streak"] = 0

    if bet_outcome is None:
        # Beim ersten Einsatz: Verlustzähler auf 0, setze Grundeinsatz.
        state["loss_streak"] = 0
        next_bet = base_bet
    elif not bet_outcome:
        # Verlust: Verlustzähler erhöhen und Einsatz entsprechend anpassen.
        state["loss_streak"] += 1
        next_bet = base_bet * (state["loss_streak"] + 1) ** 2
    else:
        # Gewinn: Verlustzähler zurücksetzen, setze Grundeinsatz.
        state["loss_streak"] = 0
        next_bet = base_bet

    return next_bet, state

# ------------------------------
# Definition der Wett-Modi (Setzoptionen)
# Jeder Modus liefert per Funktion (übergeben wird die Roulettezahl) ein Boolean, ob die Wette gewonnen wurde,
# und besitzt einen Auszahlungsmultiplikator (1:1 oder 2:1).
# ------------------------------

red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
black_numbers = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
column1_numbers = {1,4,7,10,13,16,19,22,25,28,31,34}
column2_numbers = {2,5,8,11,14,17,20,23,26,29,32,35}
column3_numbers = {3,6,9,12,15,18,21,24,27,30,33,36}

def bet_rot(outcome):
    return outcome in red_numbers

def bet_schwarz(outcome):
    return outcome in black_numbers

def bet_erste18(outcome):
    return 1 <= outcome <= 18

def bet_zweite18(outcome):
    return 19 <= outcome <= 36

def bet_dozen1(outcome):
    return 1 <= outcome <= 12

def bet_dozen2(outcome):
    return 13 <= outcome <= 24

def bet_dozen3(outcome):
    return 25 <= outcome <= 36

def bet_column1(outcome):
    return outcome in column1_numbers

def bet_column2(outcome):
    return outcome in column2_numbers

def bet_column3(outcome):
    return outcome in column3_numbers

# Dictionary der Wett-Modi: key -> (Wettfunktion, Auszahlungsmultiplikator)
bet_types = {
    "rot":      (bet_rot, 1),
    "schwarz":  (bet_schwarz, 1),
    "erste18":  (bet_erste18, 1),
    "zweite18": (bet_zweite18, 1),
    "dozen1":   (bet_dozen1, 2),
    "dozen2":   (bet_dozen2, 2),
    "dozen3":   (bet_dozen3, 2),
    "column1":  (bet_column1, 2),
    "column2":  (bet_column2, 2),
    "column3":  (bet_column3, 2)
}

# Dictionary der Wett-Systeme: Name -> Funktionsreferenz
betting_systems = {
    "Martingale": martingale_system,
    "Reverse Martingale": reverse_martingale_system,
    "Fibonacci": fibonacci_system,
    "Labouchere": labouchere_system,
    "D'Alembert": d_alembert_system,
    "Reverse D'Alembert": reverse_d_alembert_system,
    "James Bond": james_bond_system,
    "1-3-2-6": one_three_two_six_system,
    "Oscar's Grind": oscars_grind_system,
    "Semi-Martingale": semi_martingale_system,
    "Abdrucci-system":andrucci_system
}

# ------------------------------
# Initialisierung der Simulation
# Für jede Kombination aus Wett-System und Wett-Modus wird folgender Zustand gespeichert:
#   - "balance": aktueller Saldo (Start bei 0)
#   - "last_bet": letzter Einsatz (Start = base_bet)
#   - "state": systemspezifischer Zustand (als leeres Dict)
# ------------------------------

base_bet = 10
num_spins = 100

# simulation_results[system][bet_type] = { "balance": float, "last_bet": float, "state": dict }
simulation_results = {}

for system_name in betting_systems:
    simulation_results[system_name] = {}
    for bet_type in bet_types:
        simulation_results[system_name][bet_type] = {
            "balance": 0.0,
            "last_bet": base_bet,
            "state": {}
        }

# ------------------------------
# Simulation: 100 Spins Roulette
# ------------------------------

for spin in range(1, num_spins + 1):
    # Ziehe eine zufällige Roulette-Zahl (0 bis 36)
    outcome = random.randint(0, 36)
    # Für Debugzwecke kann man hier z. B. den Spin ausgeben:
    # print(f"Spin {spin}: Ergebnis = {outcome}")

    # Für jede Wett-System / Wett-Modus-Kombination:
    for system_name, system_func in betting_systems.items():
        for bet_type, (bet_func, multiplier) in bet_types.items():
            entry = simulation_results[system_name][bet_type]
            last_bet = entry["last_bet"]
            state = entry["state"]
            balance = entry["balance"]

            # Bestimme, ob der Wettmodus gewonnen hat:
            win = bet_func(outcome)

            # Rufe die Wett-System Funktion auf:
            next_bet, new_state = system_func(win, last_bet, state.copy(), base_bet)

            # Berechne den Gewinn/Verlust:
            # Bei Gewinn: Nettoverdienst = Einsatz * multiplier
            # Bei Verlust: Nettoverlust = -Einsatz
            profit = last_bet * multiplier if win else -last_bet
            balance += profit

            # Aktualisiere den Eintrag:
            simulation_results[system_name][bet_type] = {
                "balance": balance,
                "last_bet": next_bet,
                "state": new_state
            }

# ------------------------------
# Ausgabe der Endergebnisse
# ------------------------------
print("Endergebnisse nach", num_spins, "Spins:\n")
for system_name in betting_systems:
    print(f"Wett-System: {system_name}")
    for bet_type in bet_types:
        entry = simulation_results[system_name][bet_type]
        balance = entry["balance"]
        print(f"  {bet_type:10s}: Saldo = {balance:8.2f}")
    print()
