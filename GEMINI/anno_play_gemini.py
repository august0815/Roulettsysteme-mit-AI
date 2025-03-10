import random
import matplotlib.pyplot as plt

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
def system_martingale(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Martingale"):
    if not protokoll: # Starteinsatz
        return min_einsatz

    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'L': # Verlust
        vorheriger_einsatz = min_einsatz # Starteinsatz
        if protokoll.count('L') > 1: # Verdoppeln nur, wenn es vorherige Verluste gab
            vorheriger_einsatz = min_einsatz #Beginne mit dem Grundeinsatz
            for _ in range(protokoll.count('L') - 1): # Iteratives Verdoppeln für jeden vorherigen Verlust
                vorheriger_einsatz *= 2 # Einsatz verdoppeln in jedem Schritt

        naechster_einsatz = vorheriger_einsatz * 2 #  Nächsten Einsatz berechnen (nochmal verdoppeln)
        naechster_einsatz = max(naechster_einsatz, min_einsatz) # Mindesteinsatz beachten
        naechster_einsatz = min(naechster_einsatz, max_einsatz) # Maximaleinsatz beachten
        if naechster_einsatz > bankroll:
            return 0 # Kein ausreichender Bankroll
        return naechster_einsatz
    else: # Gewinn
        return min_einsatz # Zurück zum Grundeinsatz


def system_paroli(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Paroli"):
    if not protokoll: # Starteinsatz
        return min_einsatz
    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'W': # Gewinn
        vorheriger_einsatz = min_einsatz # Annahme: Grundeinsatz war der Start
        if protokoll.count('W') > 1:
            vorheriger_einsatz = min_einsatz #Beginne mit dem Grundeinsatz
            for _ in range(protokoll.count('W') - 1): # Iteratives Verdoppeln für jeden vorherigen Gewinn
                vorheriger_einsatz *= 2 # Einsatz verdoppeln in jedem Schritt
        naechster_einsatz = vorheriger_einsatz * 2
        naechster_einsatz = max(naechster_einsatz, min_einsatz) # Mindesteinsatz beachten
        naechster_einsatz = min(naechster_einsatz, max_einsatz) # Maximaleinsatz beachten
        if naechster_einsatz > bankroll:
            return 0 # Kein ausreichender Bankroll für Verdopplung
        return naechster_einsatz
    else: # Verlust
        return min_einsatz # Zurück zum Grundeinsatz

def system_dalembert(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="D'Alembert"):
    einsatz = einsatz_basis # wird unten auf min_einsatz gesetzt, falls protokoll leer
    if not protokoll: # Starteinsatz
        einsatz = min_einsatz
        return einsatz

    letztes_ergebnis = protokoll[-1]
    if letztes_ergebnis == 'L': # Verlust: Einsatz erhöhen
        einsatz += einsatz_basis
    elif letztes_ergebnis == 'W' and einsatz > min_einsatz: # Gewinn: Einsatz reduzieren, aber nicht unter Grundeinsatz
        einsatz -= einsatz_basis

    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten

    if einsatz > bankroll:
        return 0
    return einsatz

def system_fibonacci(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Fibonacci"):
    fibonacci_reihe = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55] # Beispielhafte Fibonacci-Reihe, kann erweitert werden
    einsatz_index = 0 # Startindex
    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'L': # Verlust: Index erhöhen
            einsatz_index = min(einsatz_index + 1, len(fibonacci_reihe) - 1) # Nicht über Ende der Reihe hinaus
        elif letztes_ergebnis == 'W': # Gewinn: Index um zwei Schritte zurück (wenn möglich)
            einsatz_index = max(einsatz_index - 2, 0)
    einsatz = fibonacci_reihe[einsatz_index] * einsatz_basis
    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten

    if einsatz > bankroll:
        return 0
    return einsatz

def system_labouchere(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Labouchere"):
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
    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten

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

def system_oscars_grind(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Oscar's Grind"):
    if 'oscars_grind_einsatz' not in system_oscars_grind.__dict__:
        system_oscars_grind.oscars_grind_einsatz = min_einsatz # Starteinsatz ist Mindesteinsatz
        system_oscars_grind.oscars_grind_gewinnziel = 1 # Einheit Gewinn pro Session
        system_oscars_grind.oscars_grind_aktueller_gewinn = 0

    einsatz = system_oscars_grind.oscars_grind_einsatz
    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten


    if einsatz > bankroll:
        return 0

    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'W':
            system_oscars_grind.oscars_grind_aktueller_gewinn += einsatz # Gewinn verbuchen
            if system_oscars_grind.oscars_grind_aktueller_gewinn < system_oscars_grind.oscars_grind_gewinnziel:
                system_oscars_grind.oscars_grind_einsatz += einsatz_basis # Einsatz erhöhen, wenn Gewinnziel noch nicht erreicht
                system_oscars_grind.oscars_grind_einsatz = min(system_oscars_grind.oscars_grind_einsatz, max_einsatz) # Max Einsatz beachten beim Erhöhen
            else: # Gewinnziel erreicht, Session beenden, Einsatz zurücksetzen
                system_oscars_grind.oscars_grind_einsatz = min_einsatz # Einsatz zurücksetzen auf Mindesteinsatz
                system_oscars_grind.oscars_grind_aktueller_gewinn = 0 # Gewinn zurücksetzen für neue Session
        elif letztes_ergebnis == 'L':
            system_oscars_grind.oscars_grind_aktueller_gewinn -= einsatz # Verlust verbuchen
            if system_oscars_grind.oscars_grind_aktueller_gewinn < 0: # Nur erhöhen, wenn man im Minus ist
                 system_oscars_grind.oscars_grind_einsatz += einsatz_basis # Einsatz erhöhen nach Verlust, um Verluste aufzuholen
                 system_oscars_grind.oscars_grind_einsatz = min(system_oscars_grind.oscars_grind_einsatz, max_einsatz) # Max Einsatz beachten beim Erhöhen
    return system_oscars_grind.oscars_grind_einsatz

def system_sektorensetzen(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Sektoren-Setzen"):
    sektoren = {
        "Sektor 1": [1, 13, 36, 24, 3, 15, 34, 22, 5, 17, 32, 20, 7, 11, 30, 26, 9, 28], #Beispielhafte Sektoren, leicht erweitert für mehr Zahlen
        "Sektor 2": [2, 14, 35, 23, 4, 16, 33, 21, 6, 18, 31, 19, 8, 10, 29, 25, 12, 30], # Überlappung bei 30 absichtlich, da Sektoren oft nicht 100% trennscharf
        "Sektor 3": [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 17, 34, 25, 2, 21, 4, 19, 15, 32] # Umfasst alle Zahlen, um Fehler zu vermeiden, echte Sektorenlogik wäre komplexer
    }
    gewaehlter_sektor = random.choice(list(sektoren.keys())) # Zufällige Sektorwahl als Platzhalter
    zahlen_im_sektor = sektoren[gewaehlter_sektor]
    einsatz_pro_zahl = einsatz_basis / len(zahlen_im_sektor)
    einsatz_gesamt = einsatz_pro_zahl * len(zahlen_im_sektor)

    einsatz_gesamt = max(einsatz_gesamt, min_einsatz) # Mindesteinsatz beachten (als Gesamtbetrag für alle Sektorzahlen)
    einsatz_gesamt = min(einsatz_gesamt, max_einsatz * 6) #  Maximaleinsatz * 6 als Beispiel, da Sektor ca. 6 Zahlen, anpassbar

    if einsatz_gesamt > bankroll:
        return 0
    return einsatz_gesamt

def system_flat_betting(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Flat Betting (Rot/Schwarz)"):
    einsatz = min_einsatz # Flat Bet immer Mindesteinsatz
    einsatz = min(einsatz, max_einsatz) # Max Einsatz Limit beachten, falls Mindesteinsatz > Max Einsatz (unwahrscheinlich, aber sicher ist sicher)
    return einsatz

def system_1326(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="1-3-2-6 System"):
    einsatz_folge = [1, 3, 2, 6]
    if 'system_1326_stufe' not in system_1326.__dict__:
        system_1326.system_1326_stufe = 0 # Startstufe

    aktuelle_stufe = system_1326.system_1326_stufe

    einsatz_einheit = einsatz_basis # Grundeinsatz ist 1 Einheit
    einsatz = einsatz_folge[aktuelle_stufe] * einsatz_einheit

    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten


    if einsatz > bankroll:
        return 0

    if protokoll:
        letztes_ergebnis = protokoll[-1]
        if letztes_ergebnis == 'W':
            system_1326.system_1326_stufe = min(aktuelle_stufe + 1, 3) # Stufe erhöhen, max bis 3
        elif letztes_ergebnis == 'L':
            system_1326.system_1326_stufe = 0 # Zurück zum Start bei Verlust

    return einsatz

def system_immer_gleiche_zahl(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Immer gleiche Zahl"):
    einsatz = min_einsatz # Immer Mindesteinsatz auf gleiche Zahl
    einsatz = min(einsatz, max_einsatz * 35) # Max Einsatz auf Zahl (Plein) -  Anpassung notwendig,  je nach Casino-Regel
    return einsatz

def system_proportional_einsatz(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Proportionaler Einsatz"):
    prozentsatz = 0.01 # Beispiel: 1% des Bankrolls setzen
    einsatz = bankroll * prozentsatz
    einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
    einsatz = min(einsatz, max_einsatz) # Maximaleinsatz beachten
    return einsatz # Einsatz ist ein fester Prozentsatz des aktuellen Bankrolls

def system_andrucci(bankroll, einsatz_basis, protokoll, min_einsatz, max_einsatz, system_name="Andrucci"):
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
        max_count = 0
        candidates = []

        for number, count in counts.items():
            if count > max_count:
                max_count = count
                candidates = [number]
            elif count == max_count and count > 1:
                candidates.append(number)

        if candidates:
            chosen_number = random.choice(candidates)

        if chosen_number:
            system_andrucci.andrucci_chosen_number = str(chosen_number)
            system_andrucci.andrucci_bet_counter = 0
        else:
            return 0

    # Betting phase
    system_andrucci.andrucci_bet_counter += 1
    if system_andrucci.andrucci_bet_counter <= 30:
        einsatz = einsatz_basis
        einsatz = max(einsatz, min_einsatz) # Mindesteinsatz beachten
        einsatz = min(einsatz, max_einsatz * 35) # Maximaler Einsatz auf Plein beachten -  Anpassung notwendig, je nach Casino-Regel

        if einsatz > bankroll:
            return 0
        return einsatz
    else: # Reset after 30 bets and start number selection again in next round
        system_andrucci.andrucci_chosen_number = None
        system_andrucci.andrucci_bet_counter = 0
        return 0

# Simulationsfunktion (KORRIGIERT und DEBUGGING ERWEITERT)
def roulette_simulation(system_funktionen, start_bankrolls, einsatz_basis, anzahl_spiele_pro_tag, setz_modus='rot_schwarz', setz_wahl='Rot', min_einsatz=5, max_einsatz=100):
    """
    Simuliert Roulette-Spiele über mehrere Spieltage mit verschiedenen Systemen und Bankroll Management.

    Args:
        system_funktionen (dict): Dictionary mit Systemnamen als Schlüssel und Systemfunktionen als Werte.
        start_bankrolls (dict): Dictionary mit Systemnamen als Schlüssel und Startkapital (Bankroll) als Werte.
        einsatz_basis (float): Basis-Einsatz für Systeme, die diesen verwenden.
        anzahl_spiele_pro_tag (int): Anzahl der zu simulierenden Spiele pro Spieltag.
        setz_modus (str): Der Setzmodus (z.B. 'rot_schwarz', 'erste_haelfte', 'drittel' etc.).
        setz_wahl (str): Die Wahl innerhalb des Setzmodus (z.B. 'Rot' für 'rot_schwarz', 'Erste Hälfte' für 'erste_haelfte').
        min_einsatz (int): Minimaler Einsatz am Tisch.
        max_einsatz (int): Maximaler Einsatz am Tisch (für einfache Chancen).

    Returns:
        dict: Ein Dictionary mit Endergebnissen für jedes System.
        dict: Ein Dictionary mit Bankroll-Verläufen für jedes System.
    """
    system_ergebnisse = {}
    system_ergebnisse_verlauf = {} # Verlauf der Bankrolls für grafische Ausgabe

    anzahl_spieltage = 240 # <--------------------  H I E R  GEÄNDERT  von 2 auf 240 Spieltage ---------------

    for system_name, system_funktion in system_funktionen.items():
        bankroll = start_bankrolls[system_name] # Startbankroll aus Dictionary
        system_ergebnisse_verlauf[system_name] = {} # Verlauf initialisieren - wird nun dynamisch für jeden Spieltag erstellt
        protokoll_system = [] # Protokoll spezifisch für jedes System

        for spieltag in range(anzahl_spieltage):
            tag_bankroll_start = bankroll # Startbankroll pro Spieltag speichern
            system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'] = [] # Initialisiere Liste für aktuellen Spieltag
            for spiel_nr in range(anzahl_spiele_pro_tag):
                ergebnis_zahl = roulette_drehen()
                roulette_ergebnis = get_roulette_ergebnis(ergebnis_zahl)

                einsatz = system_funktion(bankroll, einsatz_basis, protokoll_system, min_einsatz, max_einsatz, system_name)

                gesetzte_zahl_andrucci = None # Reset für jede Runde, wird nur für Andrucci gesetzt falls aktiv
                if system_name == "Andrucci" and system_andrucci.andrucci_chosen_number:
                    gesetzte_zahl_andrucci = system_andrucci.andrucci_chosen_number

                if einsatz == 0: # Kein Einsatz möglich (z.B. wegen Bankroll-Mangel oder Limit)
                    system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'].append(bankroll) # Verlauf aufzeichnen
                    # Pad the rest of the day's bankroll values with the last value
                    for _ in range(spiel_nr + 1, anzahl_spiele_pro_tag):
                        system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'].append(bankroll)
                    break # Simulation für dieses System beenden (Bankroll < Mindesteinsatz)


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

                if gewonnen:
                    bankroll += einsatz + gewinn_summe # Korrekte Gewinnberechnung: Einsatz zurück + Gewinn
                    protokoll_system.append(str(ergebnis_zahl) if system_name == "Andrucci" else 'W') #Protokoll Zahl für Andrucci, 'W'/'L' für andere
                else:
                    bankroll -= einsatz
                    protokoll_system.append(str(ergebnis_zahl) if system_name == "Andrucci" else 'L') #Protokoll Zahl für Andrucci, 'W'/'L' für andere

                system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'].append(bankroll) # Bankroll-Verlauf aufzeichnen
                if bankroll <= 0: # Bankroll aufgebraucht
                    # Pad the rest of the day's bankroll values with the last value (which is 0 or less)
                    for _ in range(spiel_nr + 1, anzahl_spiele_pro_tag):
                        system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'].append(bankroll)
                    break # Simulation für dieses System beenden (Bankrott)
            else: # else-Zweig zum for-loop, wird ausgeführt wenn loop normal (ohne break) endet - Spieltagende erreicht
                pass # Spieltagende normal erreicht, Bankroll wird nicht zurückgesetzt, sondern für nächsten Spieltag weitergeführt
                # Pad remaining values if the day completed fully to ensure consistent length for plotting. Not strictly necessary but good practice.
                while len(system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}']) < anzahl_spiele_pro_tag:
                    system_ergebnisse_verlauf[system_name][f'Spieltag {spieltag+1}'].append(bankroll)


        system_ergebnisse[system_name] = bankroll # Endergebnis nach allen Spieltagen festhalten

    return system_ergebnisse, system_ergebnisse_verlauf


# Hauptprogramm
if __name__ == "__main__":
    system_funktionen = {
        "Martingale": system_martingale,
        "Paroli": system_paroli,
        "D'Alembert": system_dalembert,
        "Fibonacci": system_fibonacci,
        "Labouchere": system_labouchere,
        "Oscars Grind": system_oscars_grind,
        "Flat Betting": system_flat_betting,
        "1-3-2-6 System": system_1326,
        "Proportionaler Einsatz": system_proportional_einsatz,
        "Andrucci": system_andrucci,
        "Immer gleiche Zahl": system_immer_gleiche_zahl # Immer gleiche Zahl wieder aktiviert
        #"Sektorensetzen": system_sektorensetzen, # Sektorensetzen System -  für komplexe Limits angepasst, aber ggf.  vereinfachen oder entfernen für bessere Vergleichbarkeit, falls Limits zu komplex
    }

    start_kapital_basis = 1000.0 # Basis für Bankroll-Berechnung,  kann systemabhängig angepasst werden
    basis_einsatz = 5.0 # Basis-Einsatz Einheit für Progressionen etc. (nicht direkt für Flat Bet etc.)
    anzahl_spiele_pro_tag_simulation = 120 # Anzahl Spiele pro Spieltag
    setz_modus_wahl = 'rot_schwarz'
    setz_wahl_innerhalb_modus = 'Rot'
    min_tisch_einsatz = 5.0
    max_tisch_einsatz_einfache_chancen = 100.0 # Maximaler Einsatz für einfache Chancen (Rot/Schwarz etc.)
    # Maximaler Einsatz für Plein (volle Zahl) wird system_andrucci und system_immer_gleiche_zahl  intern berechnet (max_tisch_einsatz_einfache_chancen * 35 als Beispiel,  Casino Regeln beachten!)


    # Bankroll Management - Startkapital je System (angepasst an Systeme und Tischlimits)
    start_bankrolls = {
        "Martingale": 5000.0,      # Hoch Risiko,  hoher Startbankroll benötigt,  aber Tischlimit kann schnell erreicht werden
        "Paroli": 1000.0,         # Moderates Risiko,  Bankroll für Gewinnsträhnen, aber Verluste begrenzt
        "D'Alembert": 800.0,       # Konservativ,  kleinerer Bankroll
        "Fibonacci": 1200.0,       # Moderate Progression,  mittlerer Bankroll
        "Labouchere": 1500.0,      # Etwas höhere Varianz,  mittlerer bis höherer Bankroll
        "Oscars Grind": 700.0,     # Konservativ,  kleinerer Bankroll,  langsamerer Progressionsstil
        "Flat Betting": 500.0,      # Sehr konservativ,  kleinster Bankroll ausreichend
        "1-3-2-6 System": 900.0,    # Moderate Progression,  mittlerer Bankroll
        "Proportionaler Einsatz": 600.0, #  Dynamisch,  Bankroll passt sich an,  Startwert eher konservativ
        "Andrucci": 1500.0,        # Hohe Varianz,  ausreichend für 30 Runden Zyklen +  Verluststrecken
        "Immer gleiche Zahl": 500.0 #  Direkte Zahl,  hohe Varianz,  aber Flat Bet,  Bankroll für Durststrecken
        #"Sektorensetzen": 1000.0,  #  Sektorwetten,  mittlere Varianz,  Bankroll für  Schwankungen,  ggf.  anpassen nach Limit-Vereinfachung
    }


    print(f"Roulette Simulation über 240 Spieltage ({anzahl_spiele_pro_tag_simulation} Spiele pro Tag)") # <------ HIER GEÄNDERT Ausgabe für 240 Spieltage
    print(f"Basis-Einsatz-Einheit: {basis_einsatz}, Mindest-Tisch-Einsatz: {min_tisch_einsatz}, Max-Tisch-Einsatz (einfache Chancen): {max_tisch_einsatz_einfache_chancen}")
    print(f"Setzmodus: {setz_modus_wahl}, Setzwahl: {setz_wahl_innerhalb_modus}")
    print("-" * 50)

    endergebnisse, verlauf_bankrolls = roulette_simulation(
        system_funktionen=system_funktionen,
        start_bankrolls=start_bankrolls,
        einsatz_basis=basis_einsatz,
        anzahl_spiele_pro_tag=anzahl_spiele_pro_tag_simulation,
        setz_modus=setz_modus_wahl,
        setz_wahl=setz_wahl_innerhalb_modus,
        min_einsatz=min_tisch_einsatz,
        max_einsatz=max_tisch_einsatz_einfache_chancen
    )

    print(f"\nEndergebnisse nach 240 Spieltagen (je 120 Spiele):") # <------ HIER GEÄNDERT Ausgabe für 240 Spieltage
    for system, end_bankroll in endergebnisse.items():
        gewinn_verlust = end_bankroll - start_bankrolls[system]
        print(f"{system}: Startkapital: {start_bankrolls[system]:.2f}, Endkapital: {end_bankroll:.2f},  {'Gewinn' if gewinn_verlust >= 0 else 'Verlust'} von {abs(gewinn_verlust):.2f})")

    # Grafische Ausgabe
    plt.figure(figsize=(12, 6)) # Größe des Diagramms anpassen
    for system_name, verlauf in verlauf_bankrolls.items():
        spieltage_bankroll_werte = [] # Sammelliste für alle Bankroll-Werte über alle Spieltage
        spieltage_runden_gesamt = [] # Sammelliste für alle Spielrunden-Nummern über alle Spieltage

        for spieltag_nr in range(1, 241): # <------ HIER GEÄNDERT für 240 Spieltage
            bankroll_werte_tag = verlauf[f'Spieltag {spieltag_nr}']
            spieltage_bankroll_werte.extend(bankroll_werte_tag) # Bankroll-Werte des aktuellen Spieltags hinzufügen
            start_runde_tag = (spieltag_nr - 1) * anzahl_spiele_pro_tag_simulation + 1 #Startrundennummer für aktuellen Spieltag
            end_runde_tag = spieltag_nr * anzahl_spiele_pro_tag_simulation # Endrundennummer für aktuellen Spieltag
            spieltage_runden_gesamt.extend(range(start_runde_tag , end_runde_tag + 1 )) #Rundennummern für aktuellen Spieltag

        plt.plot(spieltage_runden_gesamt, spieltage_bankroll_werte, label=f'{system_name}') # Nur noch eine Linie pro System für gesamten Verlauf


    plt.xlabel('Spielrunden (Gesamt über 240 Spieltage)') # <------ HIER GEÄNDERT Achsenbeschriftung angepasst
    plt.ylabel('Bankroll')
    plt.title('Bankroll-Verlauf über 240 Spieltage für verschiedene Roulette-Systeme') # <------ HIER GEÄNDERT Titel angepasst
    plt.legend()
    plt.grid(True) # Gitternetzlinien hinzufügen
    plt.tight_layout() # Layout verbessern für bessere Lesbarkeit
    plt.show()