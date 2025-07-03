from collections import deque
from src.ai_brain.advanced_bankroll_manager import AdvancedBankrollManager

class OptimizedBankrollManager(AdvancedBankrollManager):
    """Enhanced version of your existing bankroll manager"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.true_count_history = deque(maxlen=50)
        self.count_accuracy_bonus = 1.0

    def calculate_true_count_kelly_bet(self, true_count, cards_remaining_ratio=0.5):
        """Enhanced Kelly calculation using true count"""
        profile = self.risk_profiles[self.risk_level]

        # Base advantage calculation (more precise than your current version)
        if true_count <= 0:
            advantage = -0.005  # Slight house edge
        else:
            advantage = (true_count * 0.005) - 0.005  # Adjust for house edge

        # Enhanced probability calculations
        base_win_prob = 0.47
        if true_count > 0:
            adjusted_win_prob = min(0.52, base_win_prob + (true_count * 0.005))
        else:
            adjusted_win_prob = max(0.42, base_win_prob + (true_count * 0.003))

        # Blackjack probability adjustment
        bj_prob_adjustment = max(0, true_count * 0.002)
        blackjack_prob = min(0.055, 0.048 + bj_prob_adjustment)

        # Kelly calculation with blackjack consideration
        if advantage <= 0:
            kelly_fraction = 0.05  # Minimum bet when disadvantaged
        else:
            ev = (adjusted_win_prob * 1.0) + (blackjack_prob * 0.5) - ((1 - adjusted_win_prob - blackjack_prob) * 1.0)
            kelly_fraction = ev / 1.0

        # Apply profile multiplier and true count scaling
        kelly_fraction *= profile["kelly_fraction"]

        if true_count > 0:
            tc_multiplier = 1 + (true_count * profile["tc_sensitivity"])
            kelly_fraction *= min(tc_multiplier, profile["max_units"])

        # Enhanced bet sizing with deck penetration consideration
        base_unit = (self.current_bankroll * self.base_unit_percentage) / 100
        bet_size = base_unit * kelly_fraction

        # Penetration bonus (bet more when fewer cards remain)
        penetration_bonus = 1.0 + (max(0, cards_remaining_ratio - 0.5) * 0.2)
        bet_size *= penetration_bonus

        # Apply all limits
        bet_size = max(self.min_bet, min(bet_size, self.max_bet))
        bet_size = min(bet_size, self.current_bankroll * 0.15)  # Slightly reduced max bet

        return round(bet_size, 2)