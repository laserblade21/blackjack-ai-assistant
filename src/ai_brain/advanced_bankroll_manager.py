import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import math
from collections import deque

class AdvancedBankrollManager:
    """Enhanced bankroll management with Kelly Criterion and risk analytics"""
    
    def __init__(self, initial_bankroll=1000, base_unit_percentage=1.0, 
                 risk_level="moderate", min_bet=5, max_bet=500):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.base_unit_percentage = base_unit_percentage
        self.risk_level = risk_level
        self.min_bet = min_bet
        self.max_bet = max_bet
           # Enhanced risk profiles with Kelly multipliers
        self.risk_profiles = {
            "ultra_conservative": {"kelly_fraction": 0.25, "max_units": 1.5, "tc_sensitivity": 0.3},
            "conservative": {"kelly_fraction": 0.5, "max_units": 2, "tc_sensitivity": 0.4},
            "moderate": {"kelly_fraction": 0.75, "max_units": 4, "tc_sensitivity": 0.5}, 
            "aggressive": {"kelly_fraction": 1.0, "max_units": 6, "tc_sensitivity": 0.7},
            "very_aggressive": {"kelly_fraction": 1.25, "max_units": 8, "tc_sensitivity": 0.8}
        }
        
        # Analytics tracking
        self.total_wagered = 0
        self.max_bankroll = initial_bankroll
        self.min_bankroll = initial_bankroll
        self.bankroll_history = deque(maxlen=100)  # Last 100 bankroll values
        self.bet_history = deque(maxlen=1000)      # Last 1000 bets
        self.variance_tracking = []
        self.drawdown_periods = []
        self.current_drawdown = 0
        self.max_drawdown = 0
        
    def calculate_kelly_bet_size(self, true_count, win_probability=0.47, blackjack_probability=0.048):
        """
        Calculate optimal bet size using modified Kelly Criterion
        
        Args:
            true_count: Current true count
            win_probability: Base probability of winning
            blackjack_probability: Probability of getting blackjack
        """
        profile = self.risk_profiles[self.risk_level]
        
        # Adjust win probability based on true count
        # Each +1 TC increases win probability by ~0.5%
        adjusted_win_prob = min(0.52, win_probability + (true_count * 0.005))
        
        # Calculate expected value considering blackjack payouts
        # Regular win: +1 unit, Loss: -1 unit, Blackjack: +1.5 units
        expected_value = (adjusted_win_prob * 1.0) + (blackjack_probability * 0.5) - ((1 - adjusted_win_prob - blackjack_probability) * 1.0)
        
        if expected_value <= 0:
            # Negative expectation, bet minimum
            kelly_fraction = 0.1
        else:
            # Kelly fraction = (bp - q) / b where b=odds, p=win prob, q=lose prob
            kelly_fraction = expected_value / 1.0  # Simplified for even money bets
            
        # Apply risk profile multiplier
        kelly_fraction *= profile["kelly_fraction"]
        
        # Apply true count sensitivity
        if true_count > 0:
            tc_multiplier = 1 + (true_count * profile["tc_sensitivity"])
            kelly_fraction *= min(tc_multiplier, profile["max_units"])
            
        # Convert to bet size
        base_unit = (self.current_bankroll * self.base_unit_percentage) / 100
        bet_size = base_unit * kelly_fraction
        
        # Apply limits
        bet_size = max(self.min_bet, min(bet_size, self.max_bet))
        bet_size = min(bet_size, self.current_bankroll * 0.2)  # Never bet more than 20%
        
        return round(bet_size, 2)
    def get_bet_size_with_volatility_control(self, true_count=0, confidence=0.5, recent_variance=None):
        base_bet = self.calculate_kelly_bet_size(true_count, confidence)
        if len(self.bankroll_history) >= 10:
            recent_volatility = self.calculate_recent_volatility()
            if recent_volatility > 0.15:
                base_bet *= 0.8
            elif recent_volatility < 0.05:
                base_bet *= 1.1
        if self.current_drawdown > 0.2:
            base_bet *= 0.6
        elif self.current_drawdown > 0.1:
            base_bet *= 0.8
        return max(self.min_bet, round(base_bet, 2))

    def calculate_recent_volatility(self):
        if len(self.bankroll_history) < 5:
            return 0.1
        returns = []
        for i in range(1, len(self.bankroll_history)):
            if self.bankroll_history[i-1] > 0:
                return_rate = (self.bankroll_history[i] - self.bankroll_history[i-1]) / self.bankroll_history[i-1]
                returns.append(return_rate)
        if not returns:
            return 0.1
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        return math.sqrt(variance)

    def update_bankroll(self, result, bet_amount, hand_type="normal"):
        old_bankroll = self.current_bankroll
        multiplier = 1.0
        if hand_type == "blackjack":
            multiplier = 1.5
        elif hand_type == "double":
            multiplier = 2.0
        if result == "win":
            winnings = bet_amount * multiplier
            self.current_bankroll += winnings
        elif result == "loss":
            self.current_bankroll -= bet_amount
        self.total_wagered += bet_amount
        self.max_bankroll = max(self.max_bankroll, self.current_bankroll)
        self.min_bankroll = min(self.min_bankroll, self.current_bankroll)
        self.bankroll_history.append(self.current_bankroll)
        self.bet_history.append(bet_amount)
        peak_drawdown = (self.max_bankroll - self.current_bankroll) / self.max_bankroll
        self.current_drawdown = peak_drawdown
        self.max_drawdown = max(self.max_drawdown, peak_drawdown)

    def get_advanced_stats(self):
        roi = ((self.current_bankroll - self.initial_bankroll) / self.initial_bankroll) * 100
        if len(self.bankroll_history) >= 10:
            volatility = self.calculate_recent_volatility()
            sharpe_ratio = (roi / 100) / max(volatility, 0.001)
        else:
            sharpe_ratio = 0
        avg_recent_bet = sum(list(self.bet_history)[-50:]) / min(50, len(self.bet_history)) if self.bet_history else 0
        return {
            "current_bankroll": self.current_bankroll,
            "initial_bankroll": self.initial_bankroll,
            "profit_loss": self.current_bankroll - self.initial_bankroll,
            "roi_percentage": roi,
            "max_bankroll": self.max_bankroll,
            "min_bankroll": self.min_bankroll,
            "total_wagered": self.total_wagered,
            "current_unit_size": self.calculate_base_unit(),
            "max_drawdown": self.max_drawdown * 100,
            "current_drawdown": self.current_drawdown * 100,
            "sharpe_ratio": sharpe_ratio,
            "volatility": self.calculate_recent_volatility() * 100,
            "avg_recent_bet": avg_recent_bet,
            "risk_level": self.risk_level
        }

    def calculate_base_unit(self):
        return (self.current_bankroll * self.base_unit_percentage) / 100

    def is_broke(self, min_threshold=10):
        return self.current_bankroll < min_threshold

    def should_reduce_risk(self):
        return (self.current_drawdown > 0.25 or
                (len(self.bankroll_history) >= 20 and 
                 self.calculate_recent_volatility() > 0.2))