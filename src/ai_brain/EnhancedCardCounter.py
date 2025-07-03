import math
from collections import deque

class EnhancedCardCounter:
    """Enhanced card counter with true count and advanced analytics"""
    def __init__(self, num_decks=6, penetration_threshold=0.75):
        self.num_decks = num_decks
        self.penetration_threshold = penetration_threshold
        self.reset()
        self.count_history = deque(maxlen=100)
        self.accuracy_tracking = []
        self.bet_correlation_history = []

    def check_for_deviation(self, player_hand, dealer_card):
        player_total = sum(player_hand)
        true_count = self.get_true_count()
        print(f"DEVIATION CHECK: {player_total} vs {dealer_card}, TC={true_count}")
        # 11 vs Ace deviation
        if player_total == 11 and dealer_card == 1:
            if true_count >= 1:
                print("DEVIATION: 11 vs Ace - Hit instead of double")
                return True
        # Other deviation logic...
        return False

    def reset(self):
        """Reset all counts and tracking"""
        self.running_count = 0
        self.cards_seen = 0
        self.total_cards = self.num_decks * 52
        self.aces_seen = 0
        self.tens_seen = 0

    def update_count(self, cards):
        """Update running count with Hi-Lo system"""
        for card in cards:
            self.cards_seen += 1
            # Hi-Lo values
            if card in [2, 3, 4, 5, 6]:
                self.running_count += 1
            elif card in [10, 11, 12, 13, 1]:  # 10, J, Q, K, A
                self.running_count -= 1
                if card == 1:  # Ace
                    self.aces_seen += 1
                else:
                    self.tens_seen += 1
            # 7, 8, 9 are neutral (0)
        self.count_history.append(self.get_true_count())

    def get_true_count(self):
        """Calculate true count (running count / decks remaining)"""
        decks_remaining = max(1, (self.total_cards - self.cards_seen) / 52)
        true_count = self.running_count / decks_remaining
        return round(true_count, 1)

    def get_betting_advantage(self):
        """Calculate betting advantage based on true count"""
        true_count = self.get_true_count()
        advantage = true_count * 0.005
        if self.cards_seen > 52:
            expected_aces = self.cards_seen * (4 / 52)
            expected_tens = self.cards_seen * (16 / 52)
            ace_richness = (expected_aces - self.aces_seen) / max(1, self.cards_seen / 52)
            ten_richness = (expected_tens - self.tens_seen) / max(1, self.cards_seen / 52)
            advantage += (ace_richness + ten_richness) * 0.001
        return max(-0.02, min(0.05, advantage))

    def get_insurance_decision(self):
        """Determine if insurance is profitable"""
        true_count = self.get_true_count()
        return true_count >= 3.0

    def penetration(self):
        """Get deck penetration percentage"""
        return (self.cards_seen / self.total_cards) * 100
    
