# src/simulation/realtime_simulation.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
from src.simulation.shoe import Shoe
from src.ai_brain.basic_strategy import BasicStrategy
from src.ai_brain.card_counter import CardCounter, CountingDecisionEngine

class BlackjackSimulator:
    def __init__(self, num_decks=6, starting_bankroll=1000):
        self.basic_strategy = BasicStrategy()
        self.card_counter = CardCounter(num_decks=num_decks)
        self.engine = CountingDecisionEngine(self.basic_strategy, self.card_counter)
        self.bankroll = starting_bankroll
        self.stats = {"wins": 0, "losses": 0, "pushes": 0}

    def deal_card(self):
        return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11])  # includes J, Q, K as 10

    def play_round(self):
        # Reset count if penetration is high
        if self.card_counter.get_deck_penetration() > 75:
            self.card_counter.reset()

        player_hand = [self.deal_card(), self.deal_card()]
        dealer_hand = [self.deal_card(), self.deal_card()]
        dealer_upcard = dealer_hand[0]

        self.card_counter.update_count(player_hand + dealer_hand)

        decision = self.engine.make_decision(player_hand, dealer_upcard)
        action = decision["action"]
        bet = decision["bet_recommendation"]

        dealer_total = sum(dealer_hand)
        while dealer_total < 17:
            dealer_hand.append(self.deal_card())
            dealer_total = sum(dealer_hand)

        player_total = sum(player_hand)
        if action == "hit":
            player_hand.append(self.deal_card())
            player_total = sum(player_hand)
        elif action == "double":
            player_hand.append(self.deal_card())
            player_total = sum(player_hand)
            bet *= 2
        elif action == "split":
            # We'll treat split as regular hand for now
            pass

        # Final outcome
        result = ""
        if player_total > 21:
            self.stats["losses"] += 1
            self.bankroll -= bet
            result = "LOSS"
        elif dealer_total > 21 or player_total > dealer_total:
            self.stats["wins"] += 1
            self.bankroll += bet
            result = "WIN"
        elif player_total == dealer_total:
            self.stats["pushes"] += 1
            result = "PUSH"
        else:
            self.stats["losses"] += 1
            self.bankroll -= bet
            result = "LOSS"

        print(f"===== NEW ROUND =====")
        print(f"Player hand: {player_hand}")
        print(f"Dealer shows: {dealer_upcard}")
        print(f"AI Decision: {action.upper()} | Reason: {decision['reasoning']} | Bet: ${bet}")
        print(f"Dealer final hand: {dealer_hand} => total: {dealer_total}")
        print(f"Count Status: {decision['count_status']['deck_status']} | {decision['count_status']['advantage_text']}")
        print(f"Outcome: {result}")
        print(f"Bankroll: ${self.bankroll:.2f}")
        print()

    def simulate(self, rounds=100):
        for _ in range(rounds):
            self.play_round()

        print("=" * 40)
        print("📊 SIMULATION RESULTS")
        print(f"Rounds Played: {rounds}")
        print(f"Wins: {self.stats['wins']}")
        print(f"Losses: {self.stats['losses']}")
        print(f"Pushes: {self.stats['pushes']}")
        print(f"Final Bankroll: ${self.bankroll:.2f}")
        print("=" * 40)


if __name__ == "__main__":
    sim = BlackjackSimulator()
    sim.simulate(rounds=100)
