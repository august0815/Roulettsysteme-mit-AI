**Roulette Strategy Simulation: Overview**

This Python module includes a collection of strategies for simulating bets in roulette. Each strategy follows specific rules to determine the bet amount and target based on the current state (bankroll, number of rounds played, previous outcomes). Below is an overview of each included strategy:

### 1. **Martingale System**
   - **Mechanism**: Double the bet after a loss until a win recovers all losses.
   - **State**: Tracks the last winning bet size.

### 2. **Reverse Martingale System**
   - **Mechanism**: Halve the bet after a win to minimize gains, reverting when losing streaks occur.
   - **State**: Tracks the current bet amount and recent wins/losses.

### 3. **D'Almbert System**
   - **Mechanism**: Adjusts bets based on consecutive losses (bet increases) or wins (decreases).
   - **State**: Tracks net results over three rounds for betting adjustments.

### 4. **Fibonacci System**
   - **Mechanism**: Uses Fibonacci progression for bet sizes after losses.
   - **State**: Manages the current position in the sequence and cumulative bets.

### 5. **Labouchere System**
   - **Mechanism**: Creates a sequence of numbers; bets the sum, then removes adjacent numbers if won or adds new ones if lost.
   - **State**: Tracks the current sequence and accumulated bets.

### 6. **Oscar's Grind System**
   - **Mechanism**: Uses fixed increments for losing streaks.
   - **State**: Manages the number of consecutive losses to determine bet size.

### 7. **Paroli System**
   - **Mechanism**: Double previous win after a win, revert if lost consecutively.
   - **State**: Tracks recent wins and adjusts bets accordingly.

### 8. **Andrucci's 1-3-2-4 System**
   - **Mechanism**: Bet amounts follow the sequence [1,3,2,4] for four consecutive numbers; repeat after a win or if losing streak.
   - **State**: Manages the current bet position and sequence status.

### 9. **James Bond's Strategy**
   - **Mechanism**: High (14 units), Six-Line (5 units), and Zero (1 unit) bets in specific rounds.
   - **State**: Distributes the total stake across predefined bets per round.

### 10. **Column Betting System**
    - **Mechanism**: Consistently bets on one column (numbers divisible by 3, starting at 1).
    - **State**: No dynamic state; always bets same amount and column.

### 11. **Modified Martingale with 5-Black Trigger**
   - **Mechanism**: Only activates Martingale logic when the last 5 spins are black.
   - **State**: Tracks the color of the last 5 spins.

### Strategy Usage:
Each strategy is passed parameters such as bankroll, rounds played, previous wins/losses, and state variables. The strategies dynamically adjust bets based on these inputs to simulate various betting behaviors in roulette.

**Example Usage**:
```python
from roulette_strategies import RouletteStrategies

# Initialize with a certain amount of money
bankroll = 100
rounds_played = 0
wins = 0
losses = 0
state = {}

strategies = RouletteStrategies(roulette_systems)
current_strategy = strategies.get_current_strategy()

while bankroll > 0 and rounds_played < max_rounds:
    bet_amount, target_numbers = current_strategy(bankroll, rounds_played, wins, losses, state)
    # Simulate a spin and update outcomes
    outcome = random.choice(['red', 'black'])
    if outcome in target_numbers:
        wins += 1
        state['last_win'] = True
    else:
        losses += 1
        state['last_win'] = False
    rounds_played += 1
    # Apply strategy's logic here (not shown for brevity)
```

This setup allows for flexible simulation of different strategies, tracking their performance over time and under various betting scenarios. Each strategy adapts its bets based on historical outcomes and internal state management to mimic real-world gambling behavior. 

**Note**: The actual implementation details for each strategy are encapsulated within their respective functions, ensuring they manage their own state (stored in the `state` dictionary) as needed. This allows strategies to remember previous bets and outcomes, enabling dynamic adjustments like doubling after a loss or reverting to base bets after consecutive wins. 

The inclusion of diverse strategies enables analysis of risk management techniques, bankroll control, and long-term volatility under different betting disciplines. Each strategy's effectiveness can be evaluated by simulating numerous rounds and observing metrics like total profit, bankruptcy risk, and adherence to set goals (e.g., doubling the initial bankroll). 

This module serves as a foundational tool for both educational purposes and practical applications in understanding roulette betting strategies through systematic simulation.