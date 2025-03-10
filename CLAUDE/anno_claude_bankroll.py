# Import the systems from the provided file
from test_claude import (
    martingale_system,
    reverse_martingale_system,
    dalembert_system,
    fibonacci_system,
    labouchere_system,
    oscar_grind_system,
    paroli_system,
    andrucci_system,
    james_bond_system,
    column_bet_system,
    roulette_systems,
    mart_warten
)

import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
import os
from datetime import datetime

# Configuration for European roulette standards
MIN_BET = 5  # Minimum bet in Euros
MAX_BET = 500  # Maximum bet in Euros
STARTING_BANKROLL = 1000  # Initial starting bankroll on day 1
DAYS = 2400  # Number of days to simulate
ROUNDS_PER_DAY = 120  # Number of rounds per day

# European roulette wheel (numbers 0-36)
WHEEL = list(range(37))

# Define winning payouts for different bet types
PAYOUTS = {
    "straight": 35,  # Single number (e.g., betting on 17)
    "red_black": 1,  # Red or Black
    "even_odd": 1,  # Even or Odd
    "low_high": 1,  # Low (1-18) or High (19-36)
    "dozen": 2,  # Dozen (1-12, 13-24, 25-36)
    "column": 2,  # Column bet
}

# Define the numbers for different bet types
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
EVEN_NUMBERS = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
ODD_NUMBERS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
LOW_NUMBERS = list(range(1, 19))
HIGH_NUMBERS = list(range(19, 37))

# European roulette wheel (0 is neither red nor black, even nor odd, low nor high)
DOZEN1 = list(range(1, 13))
DOZEN2 = list(range(13, 25))
DOZEN3 = list(range(25, 37))
COLUMN1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
COLUMN2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
COLUMN3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]


def spin_wheel():
    """Spin the roulette wheel and return a random number."""
    return random.choice(WHEEL)


def check_win(bet_type, bet_numbers, spin_result):
    """Check if the bet wins based on the spin result."""
    if bet_type == "straight":
        return spin_result in bet_numbers
    elif bet_type == "red_black":
        if spin_result == 0:
            return False
        if bet_numbers == RED_NUMBERS:
            return spin_result in RED_NUMBERS
        else:
            return spin_result in BLACK_NUMBERS
    elif bet_type == "even_odd":
        if spin_result == 0:
            return False
        if bet_numbers == EVEN_NUMBERS:
            return spin_result % 2 == 0
        else:
            return spin_result % 2 == 1
    elif bet_type == "low_high":
        if spin_result == 0:
            return False
        if bet_numbers == LOW_NUMBERS:
            return 1 <= spin_result <= 18
        else:
            return 19 <= spin_result <= 36
    elif bet_type == "dozen":
        if spin_result == 0:
            return False
        if bet_numbers == DOZEN1:
            return spin_result in DOZEN1
        elif bet_numbers == DOZEN2:
            return spin_result in DOZEN2
        else:
            return spin_result in DOZEN3
    elif bet_type == "column":
        if spin_result == 0:
            return False
        if bet_numbers == COLUMN1:
            return spin_result in COLUMN1
        elif bet_numbers == COLUMN2:
            return spin_result in COLUMN2
        else:
            return spin_result in COLUMN3
    return False


def play_round(system, bankroll, rounds_played, wins, losses, state):
    """Play a single round of roulette with the given system."""
    if bankroll < MIN_BET:
        return bankroll, wins, losses, False  # Cannot play with less than minimum bet

    # Get the bet from the system
    bet_type, bet_amount, bet_numbers = system(bankroll, rounds_played, wins, losses, state, MIN_BET, MAX_BET)

    # Ensure bet_amount is at least MIN_BET and no more than bankroll
    bet_amount = max(MIN_BET, min(bet_amount, bankroll, MAX_BET))

    # Spin the wheel
    spin_result = spin_wheel()

    # Check if the bet wins
    win = check_win(bet_type, bet_numbers, spin_result)

    if win:
        # Update state to indicate a win
        state["last_win"] = True
        wins += 1
        # Calculate payout based on bet type
        payout = bet_amount * PAYOUTS[bet_type]
        bankroll = bankroll + payout
    else:
        # Update state to indicate a loss
        state["last_win"] = False
        losses += 1
        bankroll = bankroll - bet_amount

    return bankroll, wins, losses, True


def simulate_day(system, starting_bankroll):
    """Simulate a day (ROUNDS_PER_DAY rounds) with the given system."""
    bankroll = starting_bankroll
    wins = 0
    losses = 0
    rounds_played = 0
    state = {}

    bankroll_history = [bankroll]

    for _ in range(ROUNDS_PER_DAY):
        prev_bankroll = bankroll
        bankroll, wins, losses, played = play_round(system, bankroll, rounds_played, wins, losses, state)

        if played:
            rounds_played += 1
        else:
            # If player couldn't play (bankroll < MIN_BET), end the day
            break

        bankroll_history.append(bankroll)

    return {
        'final_bankroll': bankroll,
        'wins': wins,
        'losses': losses,
        'rounds_played': rounds_played,
        'profit': bankroll - starting_bankroll,
        'bankroll_history': bankroll_history
    }


def simulate_system(system_func, system_name):
    """Simulate the performance of a betting system over DAYS of play, carrying forward the bankroll."""
    daily_results = []
    daily_profits = []
    daily_win_rates = []
    daily_rounds_played = []
    all_bankroll_series = []  # Track all bankrolls across days
    daily_bankrolls = []  # Track end-of-day bankrolls

    # Start with the initial bankroll
    current_bankroll = STARTING_BANKROLL
    daily_bankrolls.append(current_bankroll)

    max_bankroll = current_bankroll
    bankrupt_days = 0
    system_state = {}  # Persistent state for the system between days

    for day in range(DAYS):
        result = simulate_day(system_func, current_bankroll)

        # Update current bankroll for the next day
        current_bankroll = result['final_bankroll']
        daily_bankrolls.append(current_bankroll)

        # Track maximum bankroll achieved
        max_bankroll = max(max_bankroll, current_bankroll)

        # Check if bankrupt (below minimum bet)
        if current_bankroll < MIN_BET:
            bankrupt_days += 1
            # Reset bankroll to starting value after bankruptcy
            current_bankroll = STARTING_BANKROLL

        daily_results.append(result)
        daily_profits.append(result['profit'])

        if result['rounds_played'] > 0:
            win_rate = result['wins'] / result['rounds_played'] * 100
        else:
            win_rate = 0

        daily_win_rates.append(win_rate)
        daily_rounds_played.append(result['rounds_played'])

        # Add the bankroll history for this day
        all_bankroll_series.extend(result['bankroll_history'])

    return {
        'name': system_name,
        'daily_results': daily_results,
        'daily_profits': daily_profits,
        'daily_win_rates': daily_win_rates,
        'daily_rounds_played': daily_rounds_played,
        'total_profit': daily_bankrolls[-1] - STARTING_BANKROLL,
        'avg_profit_per_day': sum(daily_profits) / DAYS,
        'avg_win_rate': sum(daily_win_rates) / DAYS,
        'avg_rounds_per_day': sum(daily_rounds_played) / DAYS,
        'bankrupt_days': bankrupt_days,
        'profit_days': sum(1 for profit in daily_profits if profit > 0),
        'loss_days': sum(1 for profit in daily_profits if profit <= 0),
        'daily_bankrolls': daily_bankrolls,
        'all_bankroll_series': all_bankroll_series,
        'max_bankroll': max_bankroll
    }


def run_simulation():
    """Run the simulation for all betting systems."""
    system_names = [
        "Martingale",
        "Reverse Martingale",
        "D'Alembert",
        "Fibonacci",
        "Labouchere",
        "Oscar's Grind",
        "Paroli",
        "Andrucci",
        "James Bond",
        "Column Bet",
        "mart_warten"
    ]

    all_results = {}

    for i, system_func in enumerate(roulette_systems):
        print (i,system_names)
        system_name = system_names[i]
        print(f"Simulating {system_name} system...")
        results = simulate_system(system_func, system_name)
        all_results[system_name] = results

    return all_results


def plot_results(all_results):
    """Plot the simulation results with enhanced visualizations."""
    # Get timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a directory for the plots if it doesn't exist
    if not os.path.exists('plots'):
        os.makedirs('plots')

    # 1. Plot bankroll evolution over time for all systems
    plt.figure(figsize=(15, 10))

    for system_name, results in all_results.items():
        # Plot daily bankrolls (end of each day)
        days = range(len(results['daily_bankrolls']))
        plt.plot(days, results['daily_bankrolls'], label=system_name)

    plt.title('Bankroll Evolution Over 2400 Days')
    plt.xlabel('Day')
    plt.ylabel('Bankroll (€)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left')

    # Add horizontal line for starting bankroll
    plt.axhline(y=STARTING_BANKROLL, color='black', linestyle='--', alpha=0.5, label='Starting Bankroll')

    # Add horizontal line for minimum bet (bankruptcy threshold)
    plt.axhline(y=MIN_BET, color='red', linestyle='--', alpha=0.5, label='Bankruptcy Threshold')

    plt.legend()
    plt.tight_layout()

    # Save the figure
    bankroll_evolution_filename = f'plots/bankroll_evolution_{timestamp}.png'
    plt.savefig(bankroll_evolution_filename)
    plt.show()

    # 2. Create comparative bar charts
    plt.figure(figsize=(15, 12))

    # Sort systems by final bankroll
    system_names = list(all_results.keys())
    final_bankrolls = [results['daily_bankrolls'][-1] for results in all_results.values()]
    sorted_indices = np.argsort(final_bankrolls)[::-1]  # Descending order

    sorted_system_names = [system_names[i] for i in sorted_indices]
    sorted_final_bankrolls = [final_bankrolls[i] for i in sorted_indices]

    # 2a. Final Bankrolls
    plt.subplot(2, 2, 1)
    colors = ['g' if b > STARTING_BANKROLL else 'r' for b in sorted_final_bankrolls]
    plt.bar(range(len(sorted_system_names)), sorted_final_bankrolls, color=colors)
    plt.axhline(y=STARTING_BANKROLL, color='black', linestyle='--', alpha=0.5)
    plt.xticks(range(len(sorted_system_names)), sorted_system_names, rotation=45, ha='right')
    plt.title('Final Bankroll After 2400 Days')
    plt.ylabel('Bankroll (€)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 2b. Maximum Bankrolls
    plt.subplot(2, 2, 2)
    max_bankrolls = [results['max_bankroll'] for i in sorted_indices for system_name, results in
                     zip(system_names, all_results.values()) if system_name == sorted_system_names[i]]
    plt.bar(range(len(sorted_system_names)), max_bankrolls, color='blue')
    plt.xticks(range(len(sorted_system_names)), sorted_system_names, rotation=45, ha='right')
    plt.title('Maximum Bankroll Achieved')
    plt.ylabel('Bankroll (€)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 2c. Average Daily Profit
    plt.subplot(2, 2, 3)
    avg_profits = [results['avg_profit_per_day'] for i in sorted_indices for system_name, results in
                   zip(system_names, all_results.values()) if system_name == sorted_system_names[i]]
    colors = ['g' if p > 0 else 'r' for p in avg_profits]
    plt.bar(range(len(sorted_system_names)), avg_profits, color=colors)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    plt.xticks(range(len(sorted_system_names)), sorted_system_names, rotation=45, ha='right')
    plt.title('Average Daily Profit')
    plt.ylabel('Profit (€)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 2d. Bankrupt Days
    plt.subplot(2, 2, 4)
    bankrupt_days = [results['bankrupt_days'] for i in sorted_indices for system_name, results in
                     zip(system_names, all_results.values()) if system_name == sorted_system_names[i]]
    plt.bar(range(len(sorted_system_names)), bankrupt_days, color='red')
    plt.xticks(range(len(sorted_system_names)), sorted_system_names, rotation=45, ha='right')
    plt.title('Number of Bankrupt Days')
    plt.ylabel('Days')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    # Save the figure
    comparison_charts_filename = f'plots/system_comparison_{timestamp}.png'
    plt.savefig(comparison_charts_filename)
    plt.show()

    return bankroll_evolution_filename, comparison_charts_filename


def print_results(all_results):
    """Print a detailed summary of the simulation results."""
    # Create a summary table
    summary_data = []

    for system_name, results in all_results.items():
        summary_data.append({
            'System': system_name,
            'Final Bankroll': f"€{results['daily_bankrolls'][-1]:.2f}",
            'Max Bankroll': f"€{results['max_bankroll']:.2f}",
            'Avg. Daily Profit': f"€{results['avg_profit_per_day']:.2f}",
            'Win Rate': f"{results['avg_win_rate']:.2f}%",
            'Avg. Rounds/Day': f"{results['avg_rounds_per_day']:.1f}",
            'Profitable Days': results['profit_days'],
            'Bankrupt Days': results['bankrupt_days'],
            'Total Profit': f"€{results['daily_bankrolls'][-1] - STARTING_BANKROLL:.2f}"
        })

    # Sort by final bankroll
    summary_data.sort(key=lambda x: float(x['Final Bankroll'].replace('€', '')), reverse=True)

    # Convert to DataFrame for nicer display
    summary_df = pd.DataFrame(summary_data)

    print("\n===== ROULETTE BETTING SYSTEMS SIMULATION SUMMARY =====")
    print(f"Simulation Parameters:")
    print(f"- Days Simulated: {DAYS}")
    print(f"- Rounds per Day: {ROUNDS_PER_DAY}")
    print(f"- Starting Bankroll: €{STARTING_BANKROLL}")
    print(f"- Minimum Bet: €{MIN_BET}")
    print(f"- Maximum Bet: €{MAX_BET}")
    print(f"- Bankruptcy Threshold: €{MIN_BET} (minimum bet)")
    print("\n===== PERFORMANCE RANKING (by Final Bankroll) =====")
    print(summary_df.to_string(index=False))

    # Print detailed analysis for top system
    top_system = summary_data[0]['System']
    top_results = all_results[top_system]

    print(f"\n===== DETAILED ANALYSIS OF TOP SYSTEM: {top_system} =====")
    print(f"Starting Bankroll: €{STARTING_BANKROLL}")
    print(f"Final Bankroll: {summary_data[0]['Final Bankroll']}")
    print(f"Maximum Bankroll: {summary_data[0]['Max Bankroll']}")
    print(f"Total Profit: {summary_data[0]['Total Profit']}")
    print(f"Average Daily Profit: {summary_data[0]['Avg. Daily Profit']}")
    print(f"Win Rate: {summary_data[0]['Win Rate']}")
    print(f"Average Rounds per Day: {summary_data[0]['Avg. Rounds/Day']}")
    print(f"Profitable Days: {top_results['profit_days']} ({top_results['profit_days'] / DAYS * 100:.2f}%)")
    print(f"Loss Days: {top_results['loss_days']} ({top_results['loss_days'] / DAYS * 100:.2f}%)")
    print(f"Bankrupt Days: {top_results['bankrupt_days']} ({top_results['bankrupt_days'] / DAYS * 100:.2f}%)")

    # Print risk assessment
    print("\n===== RISK ASSESSMENT =====")
    for system_name, results in all_results.items():
        bankrupt_rate = results['bankrupt_days'] / DAYS * 100
        risk_level = "Low" if bankrupt_rate < 10 else "Medium" if bankrupt_rate < 30 else "High"
        print(f"{system_name}: {risk_level} Risk (Bankruptcy Rate: {bankrupt_rate:.2f}%)")

    return summary_df


if __name__ == "__main__":
    print("Starting Roulette Systems Simulation...")
    print(f"Simulating {DAYS} days with {ROUNDS_PER_DAY} rounds per day")
    print(f"Each system starts with €{STARTING_BANKROLL} and carries forward bankroll between days")
    print(f"Bankruptcy occurs when bankroll falls below minimum bet (€{MIN_BET})")

    # Run the simulation
    results = run_simulation()

    # Print the results
    summary = print_results(results)

    # Plot and save the results
    bankroll_evolution_file, comparison_charts_file = plot_results(results)

    print(f"\nSimulation completed. Results have been plotted and saved:")
    print(f"- Bankroll evolution chart: {bankroll_evolution_file}")
    print(f"- System comparison charts: {comparison_charts_file}")