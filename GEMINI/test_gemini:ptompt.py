import random

# Roulette Simulation Funktionen
def roulette_drehen():
    """Simuliert eine Drehung des Roulette-Rads und gibt eine Zahl zwischen 0 und 36 zurück."""
    return random.randint(0, 36)

def get_roulette_ergebnis(zahl):
    """
    Gibt ein Dictionary mit Roulette-Ergebnissen für eine gegebene Zahl zurück.
    Enthält Informationen über Farbe, Gerade/Ungerade, Hälften und Reihen.
    """
    ergebnisse = {}
    if zahl == 0:
        ergebnisse['farbe'] = 'Grün'
        ergebnisse['rot_schwarz'] = 'Schwarz' # Für einfache Chancen Simulation, 0 wird meist als Schwarz behandelt bei Verlust-Entscheidung für R/S Wetten
        ergebnisse['gerade_ungerade'] = 'Ungerade' # Analog für Gerade/Ungerade
        ergebnisse['halb'] = 'Zweite Hälfte' # Analog für Hälften
        ergebnisse['drittel'] = 'Drittes Drittel' # Analog für Reihen
    elif zahl in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
        ergebnisse['farbe'] = 'Rot'
        ergebnisse['rot_schwarz'] = 'Rot'
        ergebnisse['gerade_ungerade'] = 'Ungerade' if zahl % 2 != 0 else 'Gerade'
        if 1 <= zahl <= 18:
            ergebnisse['halb'] = 'Erste Hälfte'
        else:
            ergebnisse['halb'] = 'Zweite Hälfte'
        if 1 <= zahl <= 12:
            ergebnisse['drittel'] = 'Erstes Drittel'
        elif 13 <= zahl <= 24:
            ergebnisse['drittel'] = 'Zweites Drittel'
        else:
            ergebnisse['drittel'] = 'Drittes Drittel'

    else: # Schwarze Zahlen
        ergebnisse['farbe'] = 'Schwarz'
        ergebnisse['rot_schwarz'] = 'Schwarz'
        ergebnisse['gerade_ungerade'] = 'Ungerade' if zahl % 2 != 0 else 'Gerade'
        if 1 <= zahl <= 18:
            ergebnisse['halb'] = 'Erste Hälfte'
        else:
            ergebnisse['halb'] = 'Zweite Hälfte'
        if 1 <= zahl <= 12:
            ergebnisse['drittel'] = 'Erstes Drittel'
        elif 13 <= zahl <= 24:
            ergebnisse['drittel'] = 'Zweites Drittel'
        else:
            ergebnisse['drittel'] = 'Drittes Drittel'
    return ergebnisse

# Roulette System Funktionen
def system_martingale(bankroll, einsatz_basis, protokoll, system_name="Martingale"):
    if not protokoll: # Starteinsatz
        return einsatz_basis
    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'L': # Verlust
        vorheriger_einsatz = einsatz_basis # Annahme: Grundeinsatz war der Start
        if protokoll.count('L') > 1:
            vorheriger_einsatz = einsatz_basis * (2**(protokoll.count('L')-1)) # Verdoppeln nach jedem Verlust
        naechster_einsatz = vorheriger_einsatz * 2
        if naechster_einsatz > bankroll:
            return 0 # Kein ausreichender Bankroll für Verdopplung
        return naechster_einsatz
    else: # Gewinn
        return einsatz_basis # Zurück zum Grundeinsatz

def system_paroli(bankroll, einsatz_basis, protokoll, system_name="Paroli"):
    if not protokoll: # Starteinsatz
        return einsatz_basis
    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'W': # Gewinn
        vorheriger_einsatz = einsatz_basis # Annahme: Grundeinsatz war der Start
        if protokoll.count('W') > 1:
            vorheriger_einsatz = einsatz_basis * (2**(protokoll.count('W')-1)) # Verdoppeln nach jedem Gewinn
        naechster_einsatz = vorheriger_einsatz * 2
        if naechster_einsatz > bankroll:
            return 0 # Kein ausreichender Bankroll für Verdopplung
        return naechster_einsatz
    else: # Verlust
        return einsatz_basis # Zurück zum Grundeinsatz

def system_dalembert(bankroll, einsatz_basis, protokoll, system_name="D'Alembert"):
    einsatz = einsatz_basis
    if not protokoll: # Starteinsatz
        return einsatz
    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'L': # Verlust: Einsatz erhöhen
        einsatz += einsatz_basis
    elif letztes_ergebnis == 'W' and einsatz > einsatz_basis: # Gewinn: Einsatz reduzieren, aber nicht unter Grundeinsatz
        einsatz -= einsatz_basis
    if einsatz > bankroll:
        return 0
    return max(einsatz, einsatz_basis) # Stelle sicher, dass der Einsatz nicht unter den Basis-Einsatz fällt

def system_fibonacci(bankroll, einsatz_basis, protokoll, system_name="Fibonacci"):
    fibonacci_reihe = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] # Beispielhafte Fibonacci-Reihe, kann erweitert werden
    einsatz_index = 0 # Startindex
    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'L': # Verlust: Index erhöhen
            einsatz_index = min(einsatz_index + 1, len(fibonacci_reihe) - 1) # Nicht über Ende der Reihe hinaus
        elif letztes_ergebnis == 'W': # Gewinn: Index um zwei Schritte zurück (wenn möglich)
            einsatz_index = max(einsatz_index - 2, 0)
    einsatz = fibonacci_reihe[einsatz_index] * einsatz_basis
    if einsatz > bankroll:
        return 0
    return einsatz

def system_labouchere(bankroll, einsatz_basis, protokoll, system_name="Labouchere"):
    if 'labouchere_reihe' not in system_labouchere.__dict__: # Initialisierung der Zahlenreihe beim ersten Aufruf
        system_labouchere.labouchere_reihe = [1, 2, 3] # Startreihe
    reihe = system_labouchere.labouchere_reihe

    if not protokoll or not reihe: # Starteinsatz oder Reihe leer -> System beendet (oder neu starten)
        system_labouchere.labouchere_reihe = [1, 2, 3] # Reihe zurücksetzen für neuen Durchgang
        return 0 # Kein Einsatz, System muss neu initialisiert werden, oder man startet mit neuem Durchgang

    if len(reihe) == 0: # Reihe ist leer, System beendet diesen Durchgang
        system_labouchere.labouchere_reihe = [1, 2, 3] # Reihe zurücksetzen für neuen Durchgang
        return 0 # Kein Einsatz, System muss neu initialisiert werden, oder man startet mit neuem Durchgang

    if len(reihe) == 1:
        einsatz_wert = reihe[0]
    else:
        einsatz_wert = reihe[0] + reihe[-1]

    einsatz = einsatz_wert * einsatz_basis
    if einsatz > bankroll:
        return 0

    if protokoll[-1] == 'W': # Gewinn: Zahlen streichen
        if len(reihe) >= 2:
            system_labouchere.labouchere_reihe = reihe[1:-1] # Erste und letzte Zahl entfernen
        elif len(reihe) == 1:
            system_labouchere.labouchere_reihe = [] # Reihe leeren
    elif protokoll[-1] == 'L': # Verlust: Summe am Ende anhängen
        system_labouchere.labouchere_reihe.append(einsatz_wert)

    return einsatz

def system_oscars_grind(bankroll, einsatz_basis, protokoll, system_name="Oscar's Grind"):
    if 'oscars_grind_einsatz' not in system_oscars_grind.__dict__:
        system_oscars_grind.oscars_grind_einsatz = einsatz_basis
        system_oscars_grind.oscars_grind_gewinnziel = 1 # Einheit Gewinn pro Session
        system_oscars_grind.oscars_grind_aktueller_gewinn = 0

    einsatz = system_oscars_grind.oscars_grind_einsatz

    if einsatz > bankroll:
        return 0

    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'W':
            system_oscars_grind.oscars_grind_aktueller_gewinn += einsatz # Gewinn verbuchen
            if system_oscars_grind.oscars_grind_aktueller_gewinn < system_oscars_grind.oscars_grind_gewinnziel:
                system_oscars_grind.oscars_grind_einsatz += einsatz_basis # Einsatz erhöhen, wenn Gewinnziel noch nicht erreicht
            else: # Gewinnziel erreicht, Session beenden, Einsatz zurücksetzen
                system_oscars_grind.oscars_grind_einsatz = einsatz_basis
                system_oscars_grind.oscars_grind_aktueller_gewinn = 0 # Gewinn zurücksetzen für neue Session
        elif letztes_ergebnis == 'L':
            system_oscars_grind.oscars_grind_aktueller_gewinn -= einsatz # Verlust verbuchen
            if system_oscars_grind.oscars_grind_aktueller_gewinn < 0: # Nur erhöhen, wenn man im Minus ist
                 system_oscars_grind.oscars_grind_einsatz += einsatz_basis # Einsatz erhöhen nach Verlust, um Verluste aufzuholen

    return system_oscars_grind.oscars_grind_einsatz

def system_sektorensetzen(bankroll, einsatz_basis, protokoll, system_name="Sektoren-Setzen"):
    sektoren = {
        "Sektor 1": [1, 13, 36, 24, 3, 15, 34, 22, 5, 17, 32, 20, 7, 11, 30, 26, 9, 28], #Beispielhafte Sektoren, leicht erweitert für mehr Zahlen
        "Sektor 2": [2, 14, 35, 23, 4, 16, 33, 21, 6, 18, 31, 19, 8, 10, 29, 25, 12, 30], # Überlappung bei 30 absichtlich, da Sektoren oft nicht 100% trennscharf
        "Sektor 3": [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 17, 34, 25, 2, 21, 4, 19, 15, 32] # Umfasst alle Zahlen, um Fehler zu vermeiden, echte Sektorenlogik wäre komplexer
    }
    gewaehlter_sektor = random.choice(list(sektoren.keys())) # Zufällige Sektorwahl als Platzhalter
    zahlen_im_sektor = sektoren[gewaehlter_sektor]
    einsatz_pro_zahl = einsatz_basis / len(zahlen_im_sektor)
    if einsatz_pro_zahl * len(zahlen_im_sektor) > bankroll:
        return 0
    return einsatz_pro_zahl * len(zahlen_im_sektor)

def system_flat_betting(bankroll, einsatz_basis, protokoll, system_name="Flat Betting (Rot/Schwarz)"):
    return einsatz_basis # Immer den gleichen Einsatz setzen

def system_1326(bankroll, einsatz_basis, protokoll, system_name="1-3-2-6 System"):
    einsatz_folge = [1, 3, 2, 6]
    if 'system_1326_stufe' not in system_1326.__dict__:
        system_1326.system_1326_stufe = 0 # Startstufe

    aktuelle_stufe = system_1326.system_1326_stufe

    einsatz_einheit = einsatz_basis # Grundeinsatz ist 1 Einheit
    einsatz = einsatz_folge[aktuelle_stufe] * einsatz_einheit

    if einsatz > bankroll:
        return 0

    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'W':
            system_1326.system_1326_stufe = min(aktuelle_stufe + 1, 3) # Stufe erhöhen, max bis 3
        elif letztes_ergebnis == 'L':
            system_1326.system_1326_stufe = 0 # Zurück zum Start bei Verlust

    return einsatz

def system_immer_gleiche_zahl(bankroll, einsatz_basis, protokoll, system_name="Immer gleiche Zahl"):
    return einsatz_basis # Immer gleichen Einsatz

def system_proportional_einsatz(bankroll, einsatz_basis, protokoll, system_name="Proportionaler Einsatz"):
    prozentsatz = 0.01 # Beispiel: 1% des Bankrolls setzen
    einsatz = bankroll * prozentsatz
    return einsatz # Einsatz ist ein fester Prozentsatz des aktuellen Bankrolls

def system_andrucci(bankroll, einsatz_basis, protokoll, system_name="Andrucci"):
    if 'andrucci_chosen_number' not in system_andrucci.__dict__:
        system_andrucci.andrucci_chosen_number = None
        system_andrucci.andrucci_bet_counter = 0

    if system_andrucci.andrucci_chosen_number is None: # Nummernauswahl Phase
        if len(protokoll) >= 36: #Track last 36 spins for number selection
            last_results = [int(res) for res in protokoll[-36:] if res.isdigit()] #Extract last 36 numbers from protokoll
        else:
            last_results = [int(res) for res in protokoll if res.isdigit()]

        if not last_results: # No history yet or no numbers in history
            return 0 # No bet in first rounds

        counts = {}
        for number in last_results:
            counts[number] = counts.get(number, 0) + 1

        chosen_number = None
        max_count = 0 # Track max count to handle ties, if multiple numbers repeat equally
        candidates = [] # List to store candidate numbers

        for number, count in counts.items():
            if count > max_count:
                max_count = count
                candidates = [number] # Start new candidate list if higher count is found
            elif count == max_count and count > 1: #Handle ties, only add if count > 1
                candidates.append(number) # Add to candidates if count is equal to max_count


        if candidates: # If candidates exist, choose randomly among those with highest frequency
             chosen_number = random.choice(candidates) # Randomly choose from candidates with max count
        else: # No repeating number found sufficiently
            return 0 # No bet if no repeating number with sufficient frequency


        if chosen_number:
            system_andrucci.andrucci_chosen_number = str(chosen_number) # as string for protokoll consistency
            system_andrucci.andrucci_bet_counter = 0 # Reset counter when new number is chosen, important for logic
        else:
            return 0 # No bet if no repeating number found in tracking

    # Betting phase
    system_andrucci.andrucci_bet_counter += 1
    if system_andrucci.andrucci_bet_counter <= 30: # Bet for 30 rounds
        einsatz = einsatz_basis
        if einsatz > bankroll:
            return 0
        return einsatz
    else: # Reset after 30 bets and start number selection again in next round
        system_andrucci.andrucci_chosen_number = None
        system_andrucci.andrucci_bet_counter = 0
        return 0 # No bet in round when resetting


# Simulationsfunktion (KORRIGIERT)
def roulette_simulation(system_funktionen, start_bankroll, einsatz_basis, anzahl_spiele=100, setz_modus='rot_schwarz', setz_wahl='Rot', setz_zahl_andrucci = None):
    """
    Simuliert Roulette-Spiele mit verschiedenen Systemen und Setzmodi.

    Args:
        system_funktionen (dict): Dictionary mit Systemnamen als Schlüssel und Systemfunktionen als Werte.
        start_bankroll (float): Startkapital für alle Systeme.
        einsatz_basis (float): Basis-Einsatz für Systeme, die diesen verwenden.
        anzahl_spiele (int): Anzahl der zu simulierenden Spiele.
        setz_modus (str): Der Setzmodus (z.B. 'rot_schwarz', 'erste_haelfte', 'drittel' etc.).
        setz_wahl (str): Die Wahl innerhalb des Setzmodus (z.B. 'Rot' für 'rot_schwarz', 'Erste Hälfte' für 'erste_haelfte').
        setz_zahl_andrucci (str, optional): Zahl auf die bei Andrucci gesetzt wird. Wird intern vom System gesetzt und ist hier nur für die Simulation relevant.

    Returns:
        dict: Ein Dictionary mit Endergebnissen für jedes System.
    """
    system_ergebnisse = {}
    for system_name, system_funktion in system_funktionen.items():
        bankroll = start_bankroll
        protokoll_system = [] # Protokoll spezifisch für jedes System
        for spiel_nr in range(anzahl_spiele): #Spielnummer hinzugefügt für Protokollierung falls nötig
            ergebnis_zahl = roulette_drehen()
            roulette_ergebnis = get_roulette_ergebnis(ergebnis_zahl)

            einsatz = system_funktion(bankroll, einsatz_basis, protokoll_system) #Protokoll für jedes System

            gesetzte_zahl_andrucci = None # Reset für jede Runde, wird nur für Andrucci gesetzt falls aktiv
            if system_name == "Andrucci" and system_andrucci.andrucci_chosen_number: #Special handling for Andrucci
                gesetzte_zahl_andrucci = system_andrucci.andrucci_chosen_number # Get chosen number for Andrucci


            if einsatz == 0: # Kein Einsatz möglich (z.B. wegen Bankroll-Mangel)
                system_ergebnisse[system_name] = bankroll # Ergebnis festhalten auch wenn vorzeitig Stop
                break # Simulation für dieses System beenden


            gewonnen = False
            gewinn_summe = 0 # Gewinnsumme für diese Runde

            if system_name == "Andrucci" and gesetzte_zahl_andrucci: # Gewinnbedingung für Andrucci
                if str(ergebnis_zahl) == gesetzte_zahl_andrucci: # Compare as strings for consistency
                    gewonnen = True
                    gewinn_summe = einsatz * 35 # 35:1 Auszahlung für Plein (volle Zahl)
            elif setz_modus == 'rot_schwarz': # Gewinnbedingungen für andere Setzmodi (einfache Chancen)
                if roulette_ergebnis['rot_schwarz'] == setz_wahl:
                    gewonnen = True
                    gewinn_summe = einsatz # 1:1 Auszahlung für einfache Chancen
            elif setz_modus == 'erste_haelfte':
                if roulette_ergebnis['halb'] == setz_wahl:
                    gewonnen = True
                    gewinn_summe = einsatz # 1:1 Auszahlung für einfache Chancen
            elif setz_modus == 'drittel':
                if roulette_ergebnis['drittel'] == setz_wahl:
                    gewonnen = True
                    gewinn_summe = einsatz # 1:1 Auszahlung für einfache Chancen
            # Hier könnten weitere Setzmodi und Gewinnbedingungen hinzugefügt werden (Reihen, Gerade/Ungerade etc.)

            if gewonnen:
                bankroll += einsatz + gewinn_summe # Korrekte Gewinnberechnung: Einsatz zurück + Gewinn
                protokoll_system.append(str(ergebnis_zahl) if system_name == "Andrucci" else 'W') #Protokoll Zahl für Andrucci, 'W'/'L' für andere
            else:
                bankroll -= einsatz
                protokoll_system.append(str(ergebnis_zahl) if system_name == "Andrucci" else 'L') #Protokoll Zahl für Andrucci, 'W'/'L' für andere
            if bankroll <= 0: # Bankroll aufgebraucht
                system_ergebnisse[system_name] = bankroll # Ergebnis festhalten auch wenn vorzeitig Stop
                break # Simulation für dieses System beenden
        else: # else-Zweig zum for-loop, wird ausgeführt wenn loop normal (ohne break) endet
            system_ergebnisse[system_name] = bankroll # Ergebnis festhalten wenn alle Spiele gespielt wurden


    return system_ergebnisse


# Hauptprogramm
if __name__ == "__main__":
    system_funktionen = {
        "Martingale": system_martingale,
        "Paroli": system_paroli,
        "D'Alembert": system_dalembert,
        "Fibonacci": system_fibonacci,
        "Labouchere": system_labouchere,
        "Oscars Grind": system_oscars_grind,
        "Sektorensetzen": system_sektorensetzen,
        "Flat Betting": system_flat_betting,
        "1-3-2-6 System": system_1326,
        "Immer gleiche Zahl": system_immer_gleiche_zahl,
        "Proportionaler Einsatz": system_proportional_einsatz,
        "Andrucci": system_andrucci, # Andrucci System hinzugefügt
    }

    start_kapital = 1000.0
    basis_einsatz = 10.0
    anzahl_spiele_simulation = 150
    setz_modus_wahl = 'rot_schwarz' # Setzmodus für die Simulation (hier Rot/Schwarz - irrelevant für Andrucci, relevant für andere Systeme)
    setz_wahl_innerhalb_modus = 'Rot' # Setzwahl innerhalb des Modus (hier 'Rot' - irrelevant für Andrucci, relevant für andere Systeme)
    setz_zahl_andrucci = None # Wird vom Andrucci System intern bestimmt, hier initial irrelevant

    print(f"Roulette Simulation über {anzahl_spiele_simulation} Spiele")
    print(f"Startkapital: {start_kapital}, Basis-Einsatz: {basis_einsatz}")
    print(f"Setzmodus: {setz_modus_wahl}, Setzwahl: {setz_wahl_innerhalb_modus}") # Nur relevant für Systeme außer Andrucci
    print("-" * 50)

    endergebnisse = roulette_simulation(
        system_funktionen=system_funktionen,
        start_bankroll=start_kapital,
        einsatz_basis=basis_einsatz,
        anzahl_spiele=anzahl_spiele_simulation,
        setz_modus=setz_modus_wahl,
        setz_wahl=setz_wahl_innerhalb_modus,
        setz_zahl_andrucci = setz_zahl_andrucci # Wird im Andrucci System selbst bestimmt
    )

    print("\nEndergebnisse nach 100 Spielen:")
    for system, end_bankroll in endergebnisse.items():
        gewinn_verlust = end_bankroll - start_kapital
        print(f"{system}: Kapital: {end_bankroll:.2f}  ({'Gewinn' if gewinn_verlust >= 0 else 'Verlust'} von {abs(gewinn_verlust):.2f})")