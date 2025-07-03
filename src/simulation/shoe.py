import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random

class Shoe:
    def __init__(self, num_decks=6, penetration_threshold=0.75):
        self.num_decks = num_decks
        self.penetration_threshold = penetration_threshold
        self._generate_shoe()
    
    def _generate_shoe(self):
        self.cards = []
        for _ in range(self.num_decks):
            # Add 4 suits of each card value per deck (Ace = 11)
            self.cards.extend([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4)
        random.shuffle(self.cards)
        self.total_cards = len(self.cards)
        self.cards_dealt = 0

    def deal_card(self):
        if self.penetration() >= self.penetration_threshold:
            print("\n🔁 Reshuffling shoe due to penetration threshold.\n")
            self._generate_shoe()
        
        card = self.cards.pop()
        self.cards_dealt += 1
        return card

    def penetration(self):
        return self.cards_dealt / self.total_cards

    def cards_remaining(self):
        return len(self.cards)
    
    def cards_seen(self):
        return self.cards_dealt


class BlackjackShoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = self._create_shoe()
        random.shuffle(self.cards)

    def _create_shoe(self):
        # Standard 52-card deck, face cards and 10s are all 10, Ace = 11
        single_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        return single_deck * self.num_decks

    def draw_card(self):
        if not self.cards:
            self.cards = self._create_shoe()
            random.shuffle(self.cards)
        return self.cards.pop()

    def penetration(self):
        total = self.num_decks * 52
        seen = total - len(self.cards)
        return (seen / total) * 100

    def shuffle(self):
        self.cards = self._create_shoe()
        random.shuffle(self.cards)
