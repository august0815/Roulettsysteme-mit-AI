import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict


def get_recommended_bankroll(system_func, min_bet, max_bet):
    """
    Bestimmt ein empfohlenes Startkapital für ein bestimmtes Wettsystem basierend auf dem Systemtyp.
    """
    system_name = system_func.__name__
    if system_name in ["martingale_system", "reverse_martingale_system", "fibonacci_system"]:
        return min_bet * 400  # z.B. 5€ Mindesteinsatz => 2000€ Startkapital
    elif system_name in ["dalembert_system", "labouchere_system"]:
        return min_bet * 300  # z.B. 5€ Mindesteinsatz => 1500€ Startkapital
    elif system_name in ["andrucci_system", "james_bond_system"]:
        return min_bet * 250  # z.B. 5€ Mindesteinsatz => 1250€ Startkapital
    else:
        return min_bet * 200  # z.B. 5€ Mindesteinsatz => 1000€ Startkapital


# ---------------- Simulation einer Spieltagssession ----------------

def simulate_roulette(betting_system, initial_bankroll=1000, daily_rounds=120, total_days=240,
                      min_bet=5, max_bet=3000, table_max=3000, daily_loss_limit_pct=0.5):
    """
    Simuliert eine Roulette-Spielsession über mehrere Tage.
    Jeder Spieltag startet mit dem übergebenen initialen Tageskapital.
    Sollte während des Tages ein Verlustlimit erreicht werden oder nicht mehr genügend Kapital vorhanden sein, wird der Tag abgebrochen.
    """
    daily_data = []
    overall_bankroll_history = []

    for day in range(1, total_days + 1):
        current_bankroll = initial_bankroll  # Jeder Tag startet mit dem Tageskapital
        daily_history = [current_bankroll]
        rounds_played_today = 0
        wins_today = 0
        losses_today = 0
        highest_bankroll_today = current_bankroll
        system_state = {}

        for round_num in range(daily_rounds):
            if current_bankroll < min_bet:
                break
            if (initial_bankroll - current_bankroll) >= (initial_bankroll * daily_loss_limit_pct):
                break

            bet_type, bet_amount, numbers = betting_system(
                current_bankroll, rounds_played_today, wins_today, losses_today, system_state, min_bet, max_bet
            )

            bet_amount = min(max(bet_amount, min_bet), max_bet, table_max, current_bankroll)
            result = random.randint(0, 36)
            won = False
            payout = 0

            if bet_type == "straight" and result in numbers:
                payout = bet_amount * 36
                won = True
            elif bet_type == "split" and result in numbers:
                payout = bet_amount * 18
                won = True
            elif bet_type == "street" and result in numbers:
                payout = bet_amount * 12
                won = True
            elif bet_type == "corner" and result in numbers:
                payout = bet_amount * 9
                won = True
            elif bet_type == "six_line" and result in numbers:
                payout = bet_amount * 6
                won = True
            elif bet_type == "dozen" and result in numbers:
                payout = bet_amount * 3
                won = True
            elif bet_type == "column" and result in numbers:
                payout = bet_amount * 3
                won = True
            elif bet_type == "even_odd" and result in numbers and result != 0:
                payout = bet_amount * 2
                won = True
            elif bet_type == "red_black" and result in numbers and result != 0:
                payout = bet_amount * 2
                won = True
            elif bet_type == "low_high" and result in numbers and result != 0:
                payout = bet_amount * 2
                won = True

            if won:
                wins_today += 1
                current_bankroll = current_bankroll - bet_amount + payout
                system_state["last_win"] = True
            else:
                losses_today += 1
                current_bankroll = current_bankroll - bet_amount
                system_state["last_win"] = False

            highest_bankroll_today = max(highest_bankroll_today, current_bankroll)
            daily_history.append(current_bankroll)
            rounds_played_today += 1

            if current_bankroll <= 0:
                break

        daily_profit = current_bankroll - initial_bankroll
        daily_data.append({
            "Tag": day,
            "Startkapital": initial_bankroll,
            "Endkapital": current_bankroll,
            "Gewinn/Verlust": daily_profit,
            "Gespielt": rounds_played_today,
            "Gewonnen": wins_today,
            "Verloren": losses_today,
            "Höchststand": highest_bankroll_today,
            "Gewinnrate": wins_today / rounds_played_today if rounds_played_today > 0 else 0
        })
        overall_bankroll_history.extend(daily_history)

    return pd.DataFrame(daily_data), overall_bankroll_history


# ---------------- Konto-Management: Simulation mit Abhebung/Wiedereinzahlung ----------------

def simulate_system_account(betting_system, daily_rounds=120, total_days=240, min_bet=5, max_bet=3000, table_max=3000,
                            daily_loss_limit_pct=0.5, initial_account=100000):
    """
    Simuliert für ein Wettsystem den Spieltag mit täglicher Abhebung des Tageskapitals und anschließender Wiedereinzahlung.
    """
    daily_bankroll = get_recommended_bankroll(betting_system, min_bet, max_bet)
    account_balance = initial_account
    account_history = [account_balance]

    for day in range(total_days):
        current_daily_bankroll = min(daily_bankroll, account_balance)
        daily_df, daily_history = simulate_roulette(
            betting_system,
            initial_bankroll=current_daily_bankroll,
            daily_rounds=daily_rounds,
            total_days=1,
            min_bet=min_bet,
            max_bet=max_bet,
            table_max=table_max,
            daily_loss_limit_pct=daily_loss_limit_pct
        )
        day_end_bankroll = daily_history[-1]
        profit = day_end_bankroll - current_daily_bankroll
        account_balance += profit
        account_history.append(account_balance)
    return account_balance, account_history


def compare_systems_account(systems, runs=10, initial_account=100000, daily_rounds=120, total_days=240,
                            min_bet=5, max_bet=3000, table_max=3000, daily_loss_limit_pct=0.5):
    """
    Führt für jedes System mehrere Simulationen mit Konto-Management durch.
    """
    results = {}
    for system_func in systems:
        system_name = system_func.__name__
        final_accounts = []
        for run in range(runs):
            final_account, _ = simulate_system_account(
                system_func,
                daily_rounds=daily_rounds,
                total_days=total_days,
                min_bet=min_bet,
                max_bet=max_bet,
                table_max=table_max,
                daily_loss_limit_pct=daily_loss_limit_pct,
                initial_account=initial_account
            )
            final_accounts.append(final_account)
        results[system_name] = {
            "final_accounts": final_accounts,
            "avg_final_account": np.mean(final_accounts)
        }
    return results


# ---------------- Definition der Wettsysteme ----------------

def martingale_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    if not state:
        state["current_bet"] = min_bet
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["current_bet"] = min_bet
        else:
            state["current_bet"] = min(state["current_bet"] * 2, max_bet, bankroll)
    return "red_black", state["current_bet"], red_numbers


def reverse_martingale_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    if not state:
        state["current_bet"] = min_bet
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["current_bet"] = min(state["current_bet"] * 2, max_bet, bankroll)
        else:
            state["current_bet"] = min_bet
    return "red_black", state["current_bet"], black_numbers


def dalembert_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    if not state:
        state["current_bet"] = min_bet
        state["unit"] = min_bet
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["current_bet"] = max(state["current_bet"] - state["unit"], min_bet)
        else:
            state["current_bet"] = min(state["current_bet"] + state["unit"], max_bet, bankroll)
    return "even_odd", state["current_bet"], even_numbers


def fibonacci_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    high_numbers = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
    if not state:
        state["sequence"] = [1, 1]
        state["position"] = 0
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["position"] = max(0, state["position"] - 2)
        else:
            if state["position"] + 1 >= len(state["sequence"]):
                state["sequence"].append(state["sequence"][-1] + state["sequence"][-2])
            state["position"] += 1
    state["position"] = min(state["position"], len(state["sequence"]) - 1)
    bet_amount = min(state["sequence"][state["position"]] * min_bet, max_bet, bankroll)
    return "low_high", bet_amount, high_numbers


def labouchere_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    if not state:
        state["sequence"] = [1, 2, 3, 4, 5]
        state["last_win"] = False
    if not state["sequence"]:
        state["sequence"] = [1, 2, 3, 4, 5]
    if len(state["sequence"]) == 1:
        bet_amount = state["sequence"][0] * min_bet
    else:
        bet_amount = (state["sequence"][0] + state["sequence"][-1]) * min_bet
    bet_amount = min(bet_amount, max_bet, bankroll)
    return "red_black", bet_amount, red_numbers


def oscar_grind_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    if not state:
        state["current_bet"] = min_bet
        state["profit"] = 0
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["profit"] += state["current_bet"]
            if state["profit"] >= min_bet:
                state["current_bet"] = min_bet
                state["profit"] = 0
            else:
                next_bet = state["current_bet"] + min_bet
                if state["profit"] + next_bet > min_bet:
                    next_bet = min_bet - state["profit"]
                state["current_bet"] = min(next_bet, max_bet)
        else:
            state["profit"] -= state["current_bet"]
    bet_amount = min(state["current_bet"], bankroll)
    return "red_black", bet_amount, black_numbers


def paroli_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    odd_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
    if not state:
        state["current_bet"] = min_bet
        state["win_streak"] = 0
        state["last_win"] = False
    if rounds_played > 0:
        if state.get("last_win", False):
            state["win_streak"] += 1
            if state["win_streak"] >= 3:
                state["current_bet"] = min_bet
                state["win_streak"] = 0
            else:
                state["current_bet"] = min(state["current_bet"] * 3, max_bet, bankroll)
        else:
            state["current_bet"] = min_bet
            state["win_streak"] = 0
    return "even_odd", state["current_bet"], odd_numbers


def andrucci_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    if not state:
        state["observation"] = []
        state["betting_on"] = None
        state["observation_rounds"] = 30
        state["last_win"] = False
    if len(state["observation"]) < state["observation_rounds"]:
        simulated_number = random.randint(1, 36)
        state["observation"].append(simulated_number)
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        return "red_black", min_bet, red_numbers
    else:
        if not state["betting_on"]:
            counts = {}
            for num in state["observation"]:
                counts[num] = counts.get(num, 0) + 1
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            state["betting_on"] = [sorted_counts[0][0]]
        bet_amount = min(min_bet, bankroll)
        return "straight", bet_amount, state["betting_on"]


def james_bond_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    if not state:
        state["unit"] = min_bet
    unit = min(max(min_bet, bankroll / 20), max_bet / 14)
    state["unit"] = unit
    high_numbers = list(range(19, 37))
    return "low_high", 14 * unit, high_numbers


def column_bet_system(bankroll, rounds_played, wins, losses, state, min_bet, max_bet):
    column1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    bet_amount = min(min_bet, bankroll)
    return "column", bet_amount, column1


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

# ---------------- Hauptprogramm ----------------

if __name__ == "__main__":
    results_account = compare_systems_account(
        roulette_systems,
        runs=20,
        initial_account=100000,
        daily_rounds=120,
        total_days=240,
        min_bet=5,
        max_bet=3000,
        table_max=3000,
        daily_loss_limit_pct=0.5
    )

    print("\nEndstand des Kontos für jedes Wettsystem:")
    for system, stats in results_account.items():
        print(f"{system}: Endstand des Kontos (Ø über 10 Durchläufe): {stats['avg_final_account']:.2f} €")
