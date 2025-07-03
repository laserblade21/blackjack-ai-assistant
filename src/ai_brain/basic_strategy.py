# src/ai_brain/basic_strategy.py

class BasicStrategy:
    """
    Core Blackjack Basic Strategy Engine
    Implements mathematically optimal play for standard blackjack rules
    """
    
    def __init__(self):
        """Initialize strategy tables"""
        self.hard_strategy = self._create_hard_strategy_table()
        self.soft_strategy = self._create_soft_strategy_table()
        self.pair_strategy = self._create_pair_strategy_table()
        
    def _create_hard_strategy_table(self):
        """Hard totals strategy (no Aces counted as 11)"""
        # Player total vs Dealer upcard (2,3,4,5,6,7,8,9,10,A)
        return {
            5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
            9: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
            10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
            11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
            12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
            17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
            21: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
        }
    
    def _create_soft_strategy_table(self):
        """Soft totals strategy (Ace counted as 11)"""
        # A,2 through A,9 vs Dealer upcard
        return {
            13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,2
            14: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,3
            15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,4
            16: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,5
            17: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A,6
            18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],  # A,7
            19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A,8
            20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A,9
        }
    
    def _create_pair_strategy_table(self):
        """Pair splitting strategy"""
        return {
            'A,A': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            '2,2': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
            '3,3': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
            '4,4': ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
            '5,5': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
            '6,6': ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
            '7,7': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
            '8,8': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            '9,9': ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
            '10,10': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        }
    
    def get_action(self, player_hand, dealer_upcard, can_double=True, can_split=True):
        """
        Get the optimal action for given game state
        
        Args:
            player_hand (list): List of card values [2-11]
            dealer_upcard (int): Dealer's upcard value [2-11]
            can_double (bool): Whether doubling is allowed
            can_split (bool): Whether splitting is allowed
            
        Returns:
            str: Recommended action ('hit', 'stand', 'double', 'split')
        """
        # Convert dealer upcard to index (2-11 -> 0-9)
        dealer_index = min(dealer_upcard - 2, 9) if dealer_upcard <= 10 else 9
        
        # Check for pairs first
        if can_split and len(player_hand) == 2 and player_hand[0] == player_hand[1]:
            pair_key = f"{player_hand[0]},{player_hand[1]}"
            if pair_key == "1,1":  # Aces
                pair_key = "A,A"
            if pair_key in self.pair_strategy:
                action = self.pair_strategy[pair_key][dealer_index]
                if action == 'P':
                    return 'split'
        
        # Calculate hand value and check for soft/hard
        total, is_soft = self._calculate_hand_value(player_hand)
        
        # Soft totals (Ace counted as 11)
        if is_soft and total in self.soft_strategy:
            action = self.soft_strategy[total][dealer_index]
        # Hard totals
        elif total in self.hard_strategy:
            action = self.hard_strategy[total][dealer_index]
        else:
            # Default action for edge cases
            action = 'S' if total >= 17 else 'H'
        
        # Convert action codes to full names
        action_map = {
            'H': 'hit',
            'S': 'stand',
            'D': 'double' if can_double else 'hit',
            'P': 'split'
        }
        
        return action_map.get(action, 'stand')
    
    def _calculate_hand_value(self, hand):
        """
        Calculate hand value and determine if it's soft
        
        Returns:
            tuple: (total_value, is_soft)
        """
        total = sum(hand)
        aces = hand.count(11)
        is_soft = False
        
        # Handle Aces
        while total > 21 and aces > 0:
            total -= 10  # Convert Ace from 11 to 1
            aces -= 1
        
        # Check if we have a soft total (Ace counted as 11)
        if aces > 0 and total <= 21:
            is_soft = True
            
        return total, is_soft
    
    def get_action_with_confidence(self, player_hand, dealer_upcard, can_double=True, can_split=True):
        """
        Get action with confidence score
        
        Returns:
            tuple: (action, confidence_score)
        """
        action = self.get_action(player_hand, dealer_upcard, can_double, can_split)
        
        # Calculate confidence based on how "obvious" the decision is
        total, is_soft = self._calculate_hand_value(player_hand)
        
        # High confidence scenarios
        if total >= 17 and not is_soft:
            confidence = 0.95  # Always stand on hard 17+
        elif total <= 11:
            confidence = 0.95  # Always hit on 11 or less
        elif total == 21:
            confidence = 1.0   # Always stand on 21
        elif len(player_hand) == 2 and player_hand[0] == player_hand[1] and player_hand[0] in [1, 8]:
            confidence = 0.98  # Always split Aces and 8s
        else:
            confidence = 0.85  # Standard confidence for basic strategy
            
        return action, confidence

    def make_decision(self, player_hand, dealer_upcard, can_double=True, can_split=True):
        """
        Returns a dict with action, reasoning, and confidence
        to fit AI training interface
        """
        action, confidence = self.get_action_with_confidence(player_hand, dealer_upcard, can_double, can_split)
        return {
            'action': action,
            'reasoning': 'Basic Strategy',
            'confidence': confidence
        }


# Example usage and testing
if __name__ == "__main__":
    bs = BasicStrategy()
    
    # Test cases
    test_cases = [
        ([10, 6], 10, "Player 16 vs Dealer 10"),
        ([11, 7], 6, "Player A,7 vs Dealer 6"),
        ([8, 8], 9, "Player 8,8 vs Dealer 9"),
        ([10, 11], 5, "Player Blackjack vs Dealer 5"),
        ([2, 3, 6], 7, "Player 11 vs Dealer 7"),
    ]
    
    print("Basic Strategy Test Results:")
    print("-" * 50)
    
    for hand, dealer, description in test_cases:
        decision = bs.make_decision(hand, dealer)
        print(f"{description}")
        print(f"  Recommended Action: {decision['action'].upper()}")
        print(f"  Reasoning: {decision['reasoning']}")
        print(f"  Confidence: {decision['confidence']:.1%}")
        print()
