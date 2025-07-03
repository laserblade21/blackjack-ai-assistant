import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from src.ai_brain.EnhancedCardCounter import EnhancedCardCounter
from src.ai_brain.enhanced_counting_decision_engine import EnhancedCountingDecisionEngine
from src.ai_brain.basic_strategy import BasicStrategy

class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.counter = EnhancedCardCounter(num_decks=6)
        self.strategy = BasicStrategy()
        self.engine = EnhancedCountingDecisionEngine(self.strategy, self.counter)

    def test_basic_decision(self):
        self.counter.reset()
        self.counter.update_count([10, 6, 10])
        result = self.engine.make_decision([10, 6], 10)
        self.assertIn(result['action'], ['hit', 'stand', 'surrender'])

    def test_deviation(self):
        print("=== TEST DEVIATION ===")
        self.counter.running_count = 24  # Simulate high count
        print(f"DEBUG: Set running_count = {self.counter.running_count}")
        print(f"DEBUG: True count should be = {self.counter.get_true_count()}")
        
        # Use proper card representation - cards that total 16
        result = self.engine.make_decision([10, 6], 10)
        print(f"DEBUG: Result = {result}")
        
        # Check if deviation key exists and is True
        self.assertIn('deviation', result, "Result should contain 'deviation' key")
        self.assertTrue(result['deviation'], f"Expected deviation=True, got {result}")

    def test_16_vs_10_deviation(self):
        print("=== TEST 16 vs 10 DEVIATION ===")
        self.counter.running_count = 24  # TC = 4 for 6 decks
        print(f"DEBUG: Running count = {self.counter.running_count}")
        print(f"DEBUG: True count = {self.counter.get_true_count()}")
        
        result = self.engine.make_decision([10, 6], 10)  # Cards that total 16
        print(f"DEBUG: Result = {result}")
        
        self.assertTrue(result.get('deviation', False), "Should deviate from basic strategy")
        self.assertIn(result['action'], ["stand", "surrender"], "Should stand or surrender on 16 vs 10 with high count")

    def test_15_vs_10_deviation(self):
        print("=== TEST 15 vs 10 DEVIATION ===")
        self.counter.running_count = 24  # TC = 4 for 6 decks
        print(f"DEBUG: Running count = {self.counter.running_count}")
        print(f"DEBUG: True count = {self.counter.get_true_count()}")
        
        result = self.engine.make_decision([10, 5], 10)  # Cards that total 15
        print(f"DEBUG: Result = {result}")
        
        self.assertTrue(result.get('deviation', False), "Should deviate from basic strategy")
        self.assertEqual(result['action'], "stand", "Should stand on 15 vs 10 with high count")

    def test_12_vs_3_deviation(self):
        print("=== TEST 12 vs 3 DEVIATION ===")
        self.counter.running_count = 12  # TC = 2 for 6 decks
        print(f"DEBUG: Running count = {self.counter.running_count}")
        print(f"DEBUG: True count = {self.counter.get_true_count()}")
        
        result = self.engine.make_decision([10, 2], 3)  # Cards that total 12
        print(f"DEBUG: Result = {result}")
        
        self.assertTrue(result.get('deviation', False), "Should deviate from basic strategy")
        self.assertEqual(result['action'], "stand", "Should stand on 12 vs 3 with positive count")

    def test_12_vs_2_deviation(self):
        print("=== TEST 12 vs 2 DEVIATION ===")
        self.counter.running_count = 18  # TC = 3 for 6 decks
        print(f"DEBUG: Running count = {self.counter.running_count}")
        print(f"DEBUG: True count = {self.counter.get_true_count()}")
        
        result = self.engine.make_decision([10, 2], 2)  # Cards that total 12
        print(f"DEBUG: Result = {result}")
        
        self.assertTrue(result.get('deviation', False), "Should deviate from basic strategy")
        self.assertEqual(result['action'], "stand", "Should stand on 12 vs 2 with high count")

    def test_11_vs_ace_deviation(self):
        print("=== TEST 11 vs ACE DEVIATION ===")
        self.counter.running_count = 6  # TC = 1 for 6 decks
        print(f"DEBUG: Running count = {self.counter.running_count}")
        print(f"DEBUG: True count = {self.counter.get_true_count()}")
        
        result = self.engine.make_decision([6, 5], 1)  # Cards that total 11, dealer has Ace
        print(f"DEBUG: Result = {result}")
        
        self.assertTrue(result.get('deviation', False), "Should deviate from basic strategy")
        self.assertEqual(result['action'], "hit", "Should hit 11 vs Ace with positive count")

if __name__ == '__main__':
    unittest.main()