import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
TABLE_MIN = 5
TABLE_MAX = 500


def evaluate_bet(spin, bet_type, number_bet=None):
    if bet_type == 'red':
        return spin in red_numbers
    elif bet_type == 'black':
        return spin not in red_numbers and spin != 0
    elif bet_type == 'even':
        return spin % 2 == 0 and spin != 0
    elif bet_type == 'odd':
        return spin % 2 == 1
    elif bet_type == 'low':
        return 1 <= spin <= 18
    elif bet_type == 'high':
        return 19 <= spin <= 36
    elif bet_type.startswith('dozen_'):
        dozen = int(bet_type.split('_')[1])
        return (dozen - 1) * 12 < spin <= dozen * 12
    elif bet_type.startswith('column_'):
        column = int(bet_type.split('_')[1])
        return (spin - column) % 3 == 0
    elif bet_type == 'zero':
        return spin == 0
    elif bet_type == 'number':
        return spin == number_bet
    return False


def andrucci_system(balance, bet_history, **kwargs):
    base_bet = kwargs.get('base_bet', TABLE_MIN)
    lookback = kwargs.get('lookback', 30)

    if len(bet_history) < lookback:
        number = random.randint(0, 36)
        return (base_bet, number, True) if balance >= base_bet else (0, None, False)

    freq = defaultdict(int)
    for entry in bet_history[-lookback:]:
        freq[entry['spin_result']] += 1

    hot_number = max(freq, key=freq.get) if freq else random.randint(0, 36)

    return (base_bet, hot_number, True) if balance >= base_bet else (0, None, False)


strategies = [
    {
        'name': 'Martingale',
        'bet_type': 'red',
        'function': lambda b, h: min(h[-1]['bet'] * 2 if h and h[-1]['result'] == 'loss' else TABLE_MIN, TABLE_MAX),
        'payout': 1,
        'bankroll_factor': 100
    },
    {
        'name': 'Paroli',
        'bet_type': 'black',
        'function': lambda b, h: min(h[-1]['bet'] * 2 if h and h[-1]['result'] == 'win' else TABLE_MIN, TABLE_MAX),
        'payout': 1,
        'bankroll_factor': 20
    },
    {
        'name': 'D\'Alembert',
        'bet_type': 'even',
        'function': lambda b, h: min(
            max(h[-1]['bet'] + TABLE_MIN if h and h[-1]['result'] == 'loss' else h[-1]['bet'] - TABLE_MIN, TABLE_MIN),
            TABLE_MAX) if h else TABLE_MIN,
        'payout': 1,
        'bankroll_factor': 50
    },
    {
        'name': 'James Bond',
        'bet_type': 'combo',
        'function': lambda b, h: (
        min(b * 0.7, TABLE_MAX), min(b * 0.25, TABLE_MAX), min(b * 0.05, TABLE_MAX)) if b >= 100 else (0, 0, 0),
        'payout': (2, 2, 36),
        'bankroll_factor': 200
    },
    {
        'name': 'Andrucci',
        'bet_type': 'number',
        'function': andrucci_system,
        'payout': 35,
        'bankroll_factor': 35
    }
]


def run_simulation(days=240, spins_per_day=120):
    results = []
    plt.figure(figsize=(12, 6 * len(strategies)))

    for i, strategy in enumerate(strategies):
        daily_balances = []
        strategy_daily_histories = []
        total_wins = 0
        total_losses = 0

        for day in range(days):
            balance = strategy['bankroll_factor'] * TABLE_MIN
            daily_history = []
            active = True

            while active and len(daily_history) < spins_per_day:
                try:
                    if strategy['name'] == 'James Bond':
                        bets = strategy['function'](balance, daily_history)
                        bet_amount = sum(bets)
                        if bet_amount < TABLE_MIN or bet_amount > TABLE_MAX:
                            active = False
                            break
                    elif strategy['name'] == 'Andrucci':
                        bet = strategy['function'](balance, daily_history)
                        bet_amount, number_bet, valid = bet
                        valid = valid and TABLE_MIN <= bet_amount <= TABLE_MAX
                    else:
                        bet = strategy['function'](balance, daily_history)
                        bet_amount = max(TABLE_MIN, min(bet, TABLE_MAX))
                        valid = bet_amount <= balance

                    if not valid or bet_amount == 0:
                        active = False
                        break

                except Exception:
                    bet_amount = TABLE_MIN

                spin = random.randint(0, 36)

                if strategy['name'] == 'James Bond':
                    high_win = evaluate_bet(spin, 'high') * bets[0] * 2
                    dozen_win = evaluate_bet(spin, 'dozen_2') * bets[1] * 2
                    zero_win = evaluate_bet(spin, 'zero') * bets[2] * 36
                    total_win = high_win + dozen_win + zero_win
                    result = 'win' if total_win > 0 else 'loss'
                    balance += total_win - sum(bets)
                elif strategy['name'] == 'Andrucci':
                    win = evaluate_bet(spin, 'number', number_bet)
                    payout = bet_amount * 35 if win else -bet_amount
                    balance += payout
                    result = 'win' if win else 'loss'
                else:
                    win = evaluate_bet(spin, strategy['bet_type'])
                    payout = bet_amount * strategy['payout'] if win else -bet_amount
                    balance += payout
                    result = 'win' if win else 'loss'

                daily_history.append({
                    'spin': len(daily_history) + 1,
                    'bet': bet_amount,
                    'result': result,
                    'balance': balance
                })

            strategy_daily_histories.append(daily_history)
            daily_balances.append(balance)
            total_wins += sum(1 for h in daily_history if h['result'] == 'win')
            total_losses += sum(1 for h in daily_history if h['result'] == 'loss')

        results.append({
            'Strategie': strategy['name'],
            'Startkapital': strategy['bankroll_factor'] * TABLE_MIN,
            'Endkapital': sum(daily_balances) / days,
            'Bestes Tagessaldo': max(daily_balances),
            'Schlechtestes Tagessaldo': min(daily_balances),
            'Gesamtgewinne': total_wins,
            'Gesamtverluste': total_losses
        })

        plt.subplot(len(strategies), 1, i + 1)
        for day in range(days):
            day_history = strategy_daily_histories[day]
            if not day_history:
                continue
            x = list(range(day * spins_per_day + 1, day * spins_per_day + len(day_history) + 1))
            y = [h['balance'] for h in day_history]
            if len(x) == len(y):
                plt.plot(x, y, label=f'Tag {day + 1}')
        plt.title(strategy['name'])
        plt.xlabel('Spiele (kumulativ)')
        plt.ylabel('Kapital')
        plt.legend()

    plt.tight_layout()
    plt.show()
    return pd.DataFrame(results)


df = run_simulation(days=240, spins_per_day=120)
print("\nZweitägige Simulationsergebnisse (Durchschnitt):")
print(df.to_markdown(index=False))