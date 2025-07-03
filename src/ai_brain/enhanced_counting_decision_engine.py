"""Enhanced decision engine with true count optimizations"""

class EnhancedCountingDecisionEngine:
    def __init__(self, basic_strategy, card_counter):
        self.basic_strategy = basic_strategy
        self.card_counter = card_counter

        # True count deviations (expanded set with more common deviations)
        self.deviations = {
            # Format: (player_total, dealer_upcard): {true_count_threshold: action}
            
            # Hard totals
            (16, 10): {0: "surrender", 4: "stand"},  # 16 vs 10 - surrender at TC 0+, stand at TC 4+
            (15, 10): {0: "surrender", 4: "stand"},  # 15 vs 10 - surrender at TC 0+, stand at TC 4+
            (16, 9): {5: "stand"},                   # 16 vs 9 - stand at TC 5+
            (15, 9): {5: "stand"},                   # 15 vs 9 - stand at TC 5+
            (13, 2): {-1: "stand"},                  # 13 vs 2 - stand at TC -1+
            (13, 3): {-2: "stand"},                  # 13 vs 3 - stand at TC -2+
            (12, 3): {2: "stand"},                   # 12 vs 3 - stand at TC 2+
            (12, 2): {3: "stand"},                   # 12 vs 2 - stand at TC 3+
            (12, 4): {0: "stand"},                   # 12 vs 4 - stand at TC 0+
            (12, 5): {-2: "stand"},                  # 12 vs 5 - stand at TC -2+
            (12, 6): {-1: "stand"},                  # 12 vs 6 - stand at TC -1+
            
            # Soft totals
            (18, 9): {1: "stand"},                   # A,7 vs 9 - stand at TC 1+
            (18, 10): {1: "stand"},                  # A,7 vs 10 - stand at TC 1+
            (18, 1): {1: "stand"},                   # A,7 vs A - stand at TC 1+
            
            # Doubling deviations
            (11, 1): {1: "hit"},                     # 11 vs A - hit instead of double at TC 1+
            (10, 10): {4: "double"},                 # 10 vs 10 - double at TC 4+
            (10, 1): {4: "double"},                  # 10 vs A - double at TC 4+
            (9, 2): {1: "double"},                   # 9 vs 2 - double at TC 1+
            (9, 7): {3: "double"},                   # 9 vs 7 - double at TC 3+
            
            # Insurance (special case)
            ("insurance", 1): {3: "take"},           # Take insurance at TC 3+
            
            # Splitting deviations
            (20, 5): {5: "split"},                   # T,T vs 5 - split at TC 5+ (rare)
            (20, 6): {4: "split"},                   # T,T vs 6 - split at TC 4+ (rare)
        }
        
        # Risk management settings
        self.max_deviation_tc = 6  # Don't deviate beyond this true count
        self.min_confidence_threshold = 0.6

    def make_decision(self, player_hand, dealer_upcard, can_double=True, can_split=False, can_surrender=True):
        """Enhanced decision making with true count deviations"""
        true_count = self.card_counter.get_true_count()
        player_total = self._calculate_hand_total(player_hand)
        
        # Clamp true count for safety
        clamped_tc = max(-self.max_deviation_tc, min(self.max_deviation_tc, true_count))

        # Get basic strategy action first
        basic_action = self.basic_strategy.get_action(player_hand, dealer_upcard)
        
        # Check for true count deviations
        deviation_key = (player_total, dealer_upcard)
        used_deviation = False
        final_action = basic_action

        if deviation_key in self.deviations:
            deviations = self.deviations[deviation_key]
            
            # Sort by true count threshold (ascending)
            for tc_threshold, action in sorted(deviations.items()):
                if clamped_tc >= tc_threshold:
                    # Validate action is available
                    if self._is_action_valid(action, can_double, can_split, can_surrender):
                        if action != basic_action:
                            used_deviation = True
                            final_action = action
                        # For 11 vs A, even choosing hit over double is a deviation
                        elif player_total == 11 and dealer_upcard == 1 and action == "hit":
                            used_deviation = True
                            final_action = action
                        break

        # Calculate confidence and risk metrics
        confidence = self.calculate_confidence(clamped_tc, player_total, dealer_upcard, used_deviation)
        
        return {
            "action": final_action,
            "true_count": true_count,
            "clamped_tc": clamped_tc,
            "confidence": confidence,
            "deviation": used_deviation,
            "advantage": self.card_counter.get_betting_advantage(),
            "risk_level": self._assess_risk_level(clamped_tc, player_total, dealer_upcard)
        }

    def _calculate_hand_total(self, hand):
        """Calculate hand total, handling aces appropriately"""
        if not hand:
            return 0
            
        total = sum(hand)
        aces = hand.count(11)  # Assuming aces are represented as 11
        
        # Convert aces from 11 to 1 if needed
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
            
        return total

    def _is_action_valid(self, action, can_double, can_split, can_surrender):
        """Check if the suggested action is valid in current context"""
        if action == "double" and not can_double:
            return False
        if action == "split" and not can_split:
            return False
        if action == "surrender" and not can_surrender:
            return False
        return True

    def calculate_confidence(self, true_count, player_total, dealer_upcard, used_deviation):
        """Calculate decision confidence based on count and situation"""
        base_confidence = 0.7

        # Higher confidence with stronger counts
        if abs(true_count) >= 4:
            base_confidence += 0.25
        elif abs(true_count) >= 3:
            base_confidence += 0.2
        elif abs(true_count) >= 2:
            base_confidence += 0.1
        elif abs(true_count) >= 1:
            base_confidence += 0.05

        # Adjust for situation clarity
        if player_total in [20, 21]:
            base_confidence += 0.15  # Very clear good situations
        elif player_total >= 17 and dealer_upcard <= 6:
            base_confidence += 0.1   # Clear advantage situations
        elif player_total <= 11:
            base_confidence += 0.05  # Can't bust
        elif player_total in [12, 13, 14, 15, 16] and dealer_upcard >= 7:
            base_confidence -= 0.05  # Difficult situations

        # Slight reduction for deviations (they're riskier)
        if used_deviation:
            base_confidence -= 0.02

        # Cap confidence
        return max(self.min_confidence_threshold, min(0.95, base_confidence))

    def _assess_risk_level(self, true_count, player_total, dealer_upcard):
        """Assess the risk level of the current situation"""
        if abs(true_count) >= 4:
            count_risk = "low" if true_count > 0 else "high"
        elif abs(true_count) >= 2:
            count_risk = "medium"
        else:
            count_risk = "neutral"

        # Situation risk
        if player_total in [20, 21]:
            situation_risk = "low"
        elif player_total <= 11:
            situation_risk = "low"
        elif player_total in [17, 18, 19]:
            situation_risk = "low" if dealer_upcard <= 6 else "medium"
        elif player_total in [12, 13, 14, 15, 16]:
            situation_risk = "high" if dealer_upcard >= 7 else "medium"
        else:
            situation_risk = "medium"

        # Combine risks
        risk_levels = {"low": 1, "medium": 2, "high": 3, "neutral": 2}
        combined_risk = (risk_levels[count_risk] + risk_levels[situation_risk]) / 2

        if combined_risk <= 1.5:
            return "low"
        elif combined_risk <= 2.5:
            return "medium"
        else:
            return "high"

    def should_take_insurance(self, true_count):
        """Determine if insurance should be taken based on true count"""
        return true_count >= 3

    def get_deviation_explanation(self, player_total, dealer_upcard, true_count):
        """Get explanation for why a deviation was made"""
        deviation_key = (player_total, dealer_upcard)
        
        if deviation_key not in self.deviations:
            return "No deviation available for this situation"
            
        explanations = {
            (16, 10): f"With TC {true_count:.1f}, the deck is rich in high cards, making standing more favorable",
            (15, 10): f"High true count ({true_count:.1f}) suggests more 10s remaining, favoring stand",
            (12, 3): f"Positive count ({true_count:.1f}) means more 10s likely, avoid busting",
            (11, 1): f"Low/negative count ({true_count:.1f}) reduces double-down value vs ace",
            (10, 10): f"Very high count ({true_count:.1f}) makes doubling profitable vs 10",
            ("insurance", 1): f"True count {true_count:.1f} >= 3 makes insurance profitable"
        }
        
        return explanations.get(deviation_key, f"Deviation based on true count of {true_count:.1f}")

    # Legacy compatibility methods (in case your existing code uses these)
    def get_decision(self, player_hand, dealer_upcard):
        """Legacy method for backward compatibility"""
        return self.make_decision(player_hand, dealer_upcard)