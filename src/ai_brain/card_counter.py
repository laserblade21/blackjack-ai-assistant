

class CardCounter:
    """
    Enhanced Hi-Lo card counting system with true count, betting, and strategy deviations
    """
    
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.total_cards = num_decks * 52
        self.running_count = 0
        self.cards_seen = 0
        
        # Strategy deviation table for Hi-Lo (True Count thresholds)
        self.strategy_deviations = {
            # Format: (player_total, dealer_upcard, is_soft): (true_count_threshold, deviation_action)
            (16, 10, False): (0, 'stand'),    # Stand on 16 vs 10 at TC 0+
            (15, 10, False): (4, 'stand'),    # Stand on 15 vs 10 at TC +4
            (13, 2, False): (-1, 'hit'),      # Hit 13 vs 2 at TC -1 or lower
            (12, 3, False): (2, 'stand'),     # Stand on 12 vs 3 at TC +2
            (12, 2, False): (3, 'stand'),     # Stand on 12 vs 2 at TC +3
            (11, 11, False): (1, 'double'),   # Double 11 vs A at TC +1
            (10, 10, False): (4, 'double'),   # Double 10 vs 10 at TC +4
            (10, 11, False): (4, 'double'),   # Double 10 vs A at TC +4
            (9, 2, False): (1, 'double'),     # Double 9 vs 2 at TC +1
            (20, 5, False): (5, 'split'),     # Split 10,10 vs 5 at TC +5 (risky!)
            (20, 6, False): (4, 'split'),     # Split 10,10 vs 6 at TC +4 (risky!)
        }
        
        # Betting ramp based on true count
        self.betting_ramp = {
            -10: 0,    # Don't play at very negative counts
            -2: 1,     # Minimum bet at negative counts
            -1: 1,     # Minimum bet
            0: 1,      # Minimum bet at neutral
            1: 2,      # 2 units at TC +1
            2: 4,      # 4 units at TC +2
            3: 8,      # 8 units at TC +3
            4: 12,     # 12 units at TC +4
            5: 16,     # 16 units at TC +5
        }
    
    def update_count(self, cards):
        """Update running count based on seen cards"""
        for card in cards:
            if 2 <= card <= 6:
                self.running_count += 1
            elif card in [10, 11]:  # 10, J, Q, K, A
                self.running_count -= 1
            # 7, 8, 9 are neutral (count = 0)
            self.cards_seen += 1
    
    def get_running_count(self):
        """Get the current running count"""
        return self.running_count
    
    def get_true_count(self):
        """Calculate true count (running count / decks remaining)"""
        if self.cards_seen == 0:
            return 0
        
        decks_remaining = max(0.5, (self.total_cards - self.cards_seen) / 52)
        return round(self.running_count / decks_remaining, 1)
    
    def get_deck_penetration(self):
        """Get percentage of deck played"""
        if self.total_cards == 0:
            return 0
        return (self.cards_seen / self.total_cards) * 100
    
    def get_betting_units(self, base_bet=10):
        """Get recommended bet size based on true count"""
        true_count = self.get_true_count()
        
        # Find the appropriate betting multiplier
        multiplier = 1
        for tc_threshold, units in sorted(self.betting_ramp.items()):
            if true_count >= tc_threshold:
                multiplier = units
            else:
                break
        
        # Don't play at very negative counts
        if multiplier == 0:
            return 0, "Don't play - count too negative"
        
        recommended_bet = base_bet * multiplier
        return recommended_bet, f"TC: {true_count:+.1f} = {multiplier} units"
    
    def should_deviate_from_basic_strategy(self, player_hand, dealer_upcard):
        """
        Check if we should deviate from basic strategy based on count
        
        Returns:
            tuple: (should_deviate, deviation_action, explanation)
        """
        true_count = self.get_true_count()
        
        # Calculate hand total and type
        total = sum(player_hand)
        is_soft = 11 in player_hand and total <= 21
        
        # Adjust for multiple aces
        aces = player_hand.count(11)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            is_soft = aces > 0
        
        # Check for deviation
        key = (total, dealer_upcard, is_soft)
        if key in self.strategy_deviations:
            threshold, deviation_action = self.strategy_deviations[key]
            
            if true_count >= threshold:
                explanation = f"TC {true_count:+.1f} ≥ {threshold:+.1f}: Deviate to {deviation_action}"
                return True, deviation_action, explanation
        
        return False, None, None
    
    def get_advantage_estimate(self):
        """Estimate player advantage based on true count"""
        true_count = self.get_true_count()
        
        # Rough estimate: each +1 true count = ~0.5% advantage
        advantage = true_count * 0.5
        
        if advantage > 0:
            return advantage, f"Player advantage: +{advantage:.1f}%"
        elif advantage < 0:
            return advantage, f"House advantage: {abs(advantage):.1f}%"
        else:
            return 0, "Neutral game"
    
    def get_count_status(self):
        """Get comprehensive count information"""
        true_count = self.get_true_count()
        penetration = self.get_deck_penetration()
        advantage, advantage_text = self.get_advantage_estimate()
        
        status = {
            'running_count': self.running_count,
            'true_count': true_count,
            'cards_seen': self.cards_seen,
            'penetration': f"{penetration:.1f}%",
            'advantage': advantage,
            'advantage_text': advantage_text,
            'deck_status': self._get_deck_status(true_count)
        }
        
        return status
    
    def _get_deck_status(self, true_count):
        """Get qualitative description of deck status"""
        if true_count >= 3:
            return "🔥 Very Hot - High value cards remaining"
        elif true_count >= 1:
            return "🌡️ Warm - Slightly favorable"
        elif true_count >= -1:
            return "😐 Neutral - Balanced deck"
        elif true_count >= -3:
            return "🧊 Cold - Low cards remaining"
        else:
            return "❄️ Very Cold - Avoid playing"
    
    def reset(self):
        """Reset counter for new shoe"""
        self.running_count = 0
        self.cards_seen = 0
    
    def should_wong_out(self, true_count_threshold=-2):
        """Determine if player should leave table (Wong out)"""
        true_count = self.get_true_count()
        return true_count <= true_count_threshold


# Enhanced Decision Engine that integrates counting
class CountingDecisionEngine:
    """
    Decision engine that combines basic strategy with card counting
    """
    
    def __init__(self, basic_strategy, card_counter):
        self.basic_strategy = basic_strategy
        self.card_counter = card_counter
    
    def make_decision(self, player_hand, dealer_upcard, can_double=True, can_split=True):
        """
        Make decision combining basic strategy and counting deviations
        
        Returns:
            dict: Complete decision with reasoning
        """
        # Get basic strategy recommendation
        basic_action = self.basic_strategy.get_action(
            player_hand, dealer_upcard, can_double, can_split
        )
        
        # Check for counting-based deviations
        should_deviate, deviation_action, deviation_explanation = \
            self.card_counter.should_deviate_from_basic_strategy(player_hand, dealer_upcard)
        
        # Determine final action
        if should_deviate:
            final_action = deviation_action
            reasoning = f"Count Deviation: {deviation_explanation}"
            confidence = 0.9  # High confidence in count-based decisions
        else:
            final_action = basic_action
            reasoning = "Basic Strategy"
            confidence = 0.85
        
        # Get betting recommendation
        bet_amount, bet_reasoning = self.card_counter.get_betting_units()
        
        # Get count status
        count_status = self.card_counter.get_count_status()
        
        return {
            'action': final_action,
            'reasoning': reasoning,
            'confidence': confidence,
            'basic_strategy_action': basic_action,
            'deviated': should_deviate,
            'bet_recommendation': bet_amount,
            'bet_reasoning': bet_reasoning,
            'count_status': count_status
        }


# Test the enhanced system
if __name__ == "__main__":
    print("🃏 ENHANCED CARD COUNTING SYSTEM TEST")
    print("=" * 60)
    
    # Simulate a game scenario
    counter = CardCounter(num_decks=6)
    
    # Simulate cards being dealt (lots of small cards = positive count)
    print("Simulating cards dealt: 2, 3, 4, 5, 6, 7, 10, K, A")
    counter.update_count([2, 3, 4, 5, 6, 7, 10, 10, 11])
    
    status = counter.get_count_status()
    print(f"\nCount Status:")
    print(f"  Running Count: {status['running_count']:+d}")
    print(f"  True Count: {status['true_count']:+.1f}")
    print(f"  Deck Status: {status['deck_status']}")
    print(f"  {status['advantage_text']}")
    
    # Test betting recommendation
    bet, bet_reason = counter.get_betting_units(base_bet=25)
    print(f"\nBetting Recommendation:")
    print(f"  Recommended Bet: ${bet}")
    print(f"  Reason: {bet_reason}")
    
    # Test strategy deviation
    print(f"\nStrategy Deviation Test:")
    print(f"Player 16 vs Dealer 10 (normally hit):")
    
    should_deviate, action, explanation = counter.should_deviate_from_basic_strategy([10, 6], 10)
    if should_deviate:
        print(f"  ✨ DEVIATION: {explanation}")
    else:
        print(f"  📖 Stick to basic strategy")
    
    print(f"\nWong Out Check:")
    if counter.should_wong_out():
        print("  🚪 Consider leaving table - count too negative")
    else:
        print("  💺 Stay at table - count acceptable")