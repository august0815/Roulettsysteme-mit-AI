import random
import matplotlib.pyplot as plt

# ------------------------------
# Definition der Wett-Systeme
# Alle Systeme haben als Schnittstelle: (bet_outcome, last_bet, state, base_bet) -> (next_bet, state)
# ------------------------------

def martingale_system(bet_outcome, last_bet, state, base_bet):
    # Bei Gewinn oder beim ersten Einsatz: Grundeinsatz, sonst Verdopplung
    if bet_outcome is None or bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 2
    return next_bet, state

def reverse_martingale_system(bet_outcome, last_bet, state, base_bet):
    # Bei Gewinn: Verdopplung, bei Verlust oder Start: Grundeinsatz
    if bet_outcome is None or not bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 2
    return next_bet, state

def fibonacci_system(bet_outcome, last_bet, state, base_bet):
    # Fibonacci-Folge: state["fib_index"] als Index (Start bei 0)
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
    # Labouchere-System: state["sequence"] enthält eine Zahlenfolge
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
    # D'Alembert: Bei Verlust Erhöhung um base_bet, bei Gewinn Reduktion (mindestens base_bet)
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
    # James-Bond: Fester Einsatz (10-facher Grundeinsatz)
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
    # Semi-Martingale: Bei Verlust Erhöhung um Faktor 1.5, sonst Zurücksetzen auf base_bet
    if bet_outcome is None or bet_outcome:
        next_bet = base_bet
    else:
        next_bet = last_bet * 1.5
    return next_bet, state

# Dictionary der Wett-Systeme
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
    "Semi-Martingale": semi_martingale_system
}

# ------------------------------
# Definition der Wett-Modi (Setzoptionen)
# Jeder Modus liefert über eine Funktion (über Outcome) einen Boolean, ob die Wette gewonnen wurde,
# sowie einen Auszahlungsmultiplikator (1:1 oder 2:1)
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

# Dictionary der Wett-Modi: Name -> (Wettfunktion, Auszahlungsmultiplikator)
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

# ------------------------------
# Simulationsparameter und Bankroll Management
# ------------------------------
days = 240            # Anzahl der Spieltage
spins_per_day = 120   # Spins pro Tag
base_bet = 5          # Grundeinsatz (auch Tisch-Mindestwette)
table_min = 5         # Mindesteinsatz
table_max = 500       # Tischmaximum (pro Einsatz)
starting_bankroll = 500  # Täglicher Start-Bankroll für jede Kombination

# Wir speichern den täglichen Verlauf für jede Kombination:
# daily_results[system_name][bet_type] = Liste mit Bankroll am Ende jedes Tages
daily_results = {sys: {bt: [] for bt in bet_types} for sys in betting_systems}

# ------------------------------
# Simulation: Jeder Spieltag wird separat simuliert
# ------------------------------
for day in range(1, days + 1):
    # Für jede System-/Wett-Kombination: Initialisiere Bankroll, letzten Einsatz und state
    session = {}
    for sys_name in betting_systems:
        session[sys_name] = {}
        for bt in bet_types:
            session[sys_name][bt] = {
                "bankroll": starting_bankroll,
                "last_bet": base_bet,
                "state": {}
            }
    # Simuliere spins für den Tag
    for spin in range(1, spins_per_day + 1):
        # Ziehe eine zufällige Roulettezahl (0-36)
        outcome = random.randint(0, 36)
        # Für jede System-/Wett-Kombination
        for sys_name, sys_func in betting_systems.items():
            for bt, (bet_func, multiplier) in bet_types.items():
                entry = session[sys_name][bt]
                bankroll = entry["bankroll"]
                last_bet = entry["last_bet"]
                state = entry["state"]

                # Kann der Spieler noch den Mindesteinsatz setzen?
                if bankroll < table_min:
                    # Spieler ist praktisch "pleite" – keine weiteren Einsätze an diesem Tag
                    continue

                # Der vom System berechnete Einsatz wird an Tischlimits und verfügbare Bankroll angepasst
                current_bet = last_bet
                # Mindestens Tischminimum:
                if current_bet < table_min:
                    current_bet = table_min
                # Nicht über Tischmaximum:
                if current_bet > table_max:
                    current_bet = table_max
                # Nicht mehr als vorhandenes Kapital:
                if current_bet > bankroll:
                    current_bet = bankroll
                # Falls das angepasste current_bet unter table_min liegt, kann nicht gesetzt werden:
                if current_bet < table_min:
                    continue

                # Prüfe Gewinn: Bei 0 verliert fast jede Wette, da 0 in keiner Wettoption enthalten ist
                win = bet_func(outcome)
                # Berechne Gewinn/Verlust:
                profit = current_bet * multiplier if win else -current_bet
                bankroll += profit

                # Aktualisiere Systemzustand für den nächsten Einsatz:
                next_bet, new_state = sys_func(win, current_bet, state, base_bet)
                # Aktualisiere den Eintrag
                session[sys_name][bt]["bankroll"] = bankroll
                session[sys_name][bt]["last_bet"] = next_bet
                session[sys_name][bt]["state"] = new_state

    # Ende des Tages: Speichere den finalen Bankroll jedes Systems/Wett-Typs
    for sys_name in betting_systems:
        for bt in bet_types:
            final_bankroll = session[sys_name][bt]["bankroll"]
            daily_results[sys_name][bt].append(final_bankroll)

# ------------------------------
# Textuelle Zusammenfassung der Endergebnisse
# ------------------------------
print("Tägliche End-Bankroll (letzter Tag) für jede System-/Wett-Kombination:")
for sys_name in betting_systems:
    print(f"\nWett-System: {sys_name}")
    for bt in bet_types:
        final = daily_results[sys_name][bt][-1]
        print(f"  {bt:10s}: End-Bankroll = {final:6.2f}")

# ------------------------------
# Grafische Darstellung
# Erstelle für jedes Wett-System einen eigenen Subplot (insgesamt 10) und zeichne die Tagesverläufe aller 10 Wett-Modi
# ------------------------------
num_systems = len(betting_systems)
cols = 2
rows = (num_systems + 1) // cols

fig, axs = plt.subplots(rows, cols, figsize=(14, 3 * rows), sharex=True)
fig.suptitle("Tagesverlauf der Bankroll pro Wett-System und Wett-Modus", fontsize=16)

system_names = list(betting_systems.keys())
x = range(1, days + 1)
for idx, sys_name in enumerate(system_names):
    ax = axs[idx // cols][idx % cols] if rows > 1 else axs[idx]
    for bt in bet_types:
        bankroll_progress = daily_results[sys_name][bt]
        ax.plot(x, bankroll_progress, label=bt)
    ax.set_title(sys_name)
    ax.set_xlabel("Spieltag")
    ax.set_ylabel("Bankroll")
    ax.grid(True)
    ax.legend(fontsize='small')
# Leere Subplots entfernen, falls vorhanden
if num_systems % cols != 0:
    for j in range(num_systems, rows * cols):
        fig.delaxes(axs[j // cols][j % cols])
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
