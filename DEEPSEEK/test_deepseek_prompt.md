### Übersicht des Codes

Der Code umfasst eine Simulationsanwendung für Roulette-Strategien, die verschiedenen Systeme wie Martingale, Paroli und Andrucci implementiert. Die Hauptkomponenten sind:

1. **evaluate_bet-Funktion**: Überprüft, ob ein Spin mit einer bestimmten Wette (Farbe, Unparität, etc.) gewonnen wird.
2. **andrucci_system**: Implementiert das Andrucci-System, das die Wette auf eine Nummer basierend auf dem aktuellen Tagessaldo taktiert.
3. **run_simulation-Funktion**: Simuliert mehrere Strategien über 240 Tage mit 120 Spins pro Tag. Jede Strategie wird getestet und Ergebnisse werden aggregiert.

### Struktur des Codes

- **evaluate_bet**: 
  - Prüft Farben (rot, schwarz), Unparität, Dutzend und Null.
  - Gibt True/False zurück, basierend auf der Wette und dem Spin.

- **andrucci_system**:
  - Basiert auf der aktuellen Tagessaldo. Wettbetrag erhöht sich bei Verlusten, senkt sich bei Gewinnen. Nutzt die "number" Wette mit einem vorher berechneten Betrag.
  - Gibt den gültigen Betrag und die gewählte Zahl zurück.

- **run_simulation**:
  - **Strategien**: Es gibt insgesamt 8 Strategien, darunter Martingale, Paroli, Andrucci und James Bond (eine spezielle Variation).
  - **Simulation**:
    - Jede Strategie wird täglich simuliert. Startkapital variiert je nach Strategie.
    - Für jede Runde werden Spin- und Wetthistorien gespeichert.
    - Die Simulation berücksichtigt die Maximal- und Minimal-Spiele pro Tag.

- **Plotting**:
  - Graphen für jedes System mit der Tagessaldo über den Zeitschritt (Spiele).

### Ergebnisabfrage

- **run_simulation()** erzeugt eine DataFrame-Tabelle, die Durchschnittsresultate aller Strategien zeigt. Die Tabelle enthält Kolumnen wie Startkapital, Endkapital, Gesamtgewinne und Verluste.

### Abhängigkeiten

- **Pandas** (für Tabelle) und **Matplotlib** (für Grafiken) sind erforderlich.
- Alle Werte sind in der Einheit "Euro", mit.TABLE_MIN (1 Euro) als minimaler Wettabgabe.

### Sonstige Details

- **James Bond**: Spezielle Implementierung, die drei unterschiedliche Wetten (High, Dutzend 2, Null) mit variablen Beträgen tätigt.
- **Handhabung von Fehlern**: Bei ungültigen Wettbeträgen wird der Mindestbetrag verwendet.

### Beispiel Ausgabe

Die Tabelle zeigt, dass einige Strategien (z.B. Martingale) erhebliche Gewinne erzielen, während andere (z.B. Andrucci) verlustreicher sind. Grafiken helfen, den Tagessaldoverlauf zu verstehen. 

**Hinweis**: Die Simulation unter Berücksichtigung zufälliger Spin-Ergebnisse ist probabilistisch und kann Ergebnisvarianten weisen.