from src.ai_brain.basic_strategy import BasicStrategy
from src.ai_brain.card_counter import CardCounter

class CountingDecisionEngine:
    """
    Decision engine that combines basic strategy with card counting deviations.
    """

    def __init__(self, basic_strategy: BasicStrategy, card_counter: CardCounter):
        self.basic_strategy = basic_strategy
        self.card_counter = card_counter

    def make_decision(self, player_hand, dealer_upcard, can_double=True, can_split=True):
        # Get basic strategy recommendation
        base_action = self.basic_strategy.get_action(
            player_hand, dealer_upcard, can_double, can_split
        )

        # Get current true count from counter
        tc = self.card_counter.get_true_count()

        # Check if deviation from basic strategy is recommended
        should_deviate, deviation_action, reason = self.card_counter.should_deviate_from_basic_strategy(
            player_hand, dealer_upcard
        )

        if should_deviate:
            return {
                "action": deviation_action,
                "reason": f"Deviation: {reason} | TC: {tc:+.1f}",
                "tc": tc
            }
        else:
            return {
                "action": base_action,
                "reason": f"Basic Strategy | TC: {tc:+.1f}",
                "tc": tc
            }
