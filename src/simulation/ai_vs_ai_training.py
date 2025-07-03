# Enhanced Bankroll Management with Advanced Analytics
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
import math
from collections import deque
from src.ai_brain.card_counter import CardCounter
from src.ai_brain.basic_strategy import BasicStrategy
from src.simulation.shoe import BlackjackShoe
from src.ai_brain.decision_engine import CountingDecisionEngine  # Import the missing class
from src.ai_brain.EnhancedCardCounter import EnhancedCardCounter
from src.ai_brain.advanced_bankroll_manager import AdvancedBankrollManager
from src.ai_brain.enhanced_counting_decision_engine import EnhancedCountingDecisionEngine
from src.ai_brain.optimized_bankroll_manager import OptimizedBankrollManager  

# Enhanced AI Bot with new bankroll manager
class OptimizedAIBot:
    def __init__(self, strategy, name="AI", initial_bankroll=1000, 
                 risk_level="moderate", unit_percentage=1.0):
        self.name = name
        self.strategy = strategy
        self.bankroll_manager = AdvancedBankrollManager(
            initial_bankroll=initial_bankroll,
            base_unit_percentage=unit_percentage,
            risk_level=risk_level
        )
        
        # Enhanced statistics
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.busts = 0
        self.deviation_count = 0
        self.hands_played = 0
        self.risk_reductions = 0  # Track how many times risk was reduced
        
    def play_hand(self, dealer_upcard, shoe, card_counter=None, active_ais=None):
        if self.bankroll_manager.is_broke():
            if self.name == "EnhancedOptimalAI":
                result = self.play_hand(dealer_upcard, shoe, card_counter, active_ais)
            else:
                result = self.play_hand(dealer_upcard, shoe, card_counter if "Conservative" not in self.name else None, active_ais)
            if result != "broke" and active_ais is not None:
                active_ais.append(self)
            return "broke"
            
        self.hands_played += 1
        player_hand = [shoe.draw_card(), shoe.draw_card()]
        dealer_hand = [dealer_upcard, shoe.draw_card()]

        # Get decision info
        if card_counter:
            decision_info = self.strategy.make_decision(player_hand, dealer_upcard)
            true_count = decision_info.get("true_count", 0)
            confidence = decision_info.get("confidence", 0.5)
        else:
            action, confidence = self.strategy.get_action_with_confidence(player_hand, dealer_upcard)
            true_count = 0
            decision_info = {"action": action, "confidence": confidence}

        # Use enhanced bet sizing with volatility control
        bet_size = self.bankroll_manager.get_bet_size_with_volatility_control(
            true_count=true_count,
            confidence=confidence
        )
        
        # Check if we should reduce risk
        if self.bankroll_manager.should_reduce_risk():
            bet_size *= 0.7  # Emergency risk reduction
            self.risk_reductions += 1

        # Track deviations
        if isinstance(decision_info, dict) and decision_info.get("deviation", False):
            self.deviation_count += 1

        # Simulate hand resolution
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)
        is_blackjack = (len(player_hand) == 2 and player_total == 21)
        
        result = self.resolve_hand(player_total, dealer_total, is_blackjack)
        hand_type = "blackjack" if is_blackjack else "normal"
        
        # Update bankroll with enhanced tracking
        self.bankroll_manager.update_bankroll(result, bet_size, hand_type)

        # Enhanced logging
        stats = self.bankroll_manager.get_advanced_stats()
        risk_indicator = "⚠️" if self.bankroll_manager.should_reduce_risk() else ""
        
        print(f"[{self.name}] {risk_indicator} Hand: {player_hand} vs {dealer_upcard} | "
              f"Bet: ${bet_size:.2f} | Result: {result} | "
              f"Bankroll: ${stats['current_bankroll']:.2f} | "
              f"DD: {stats['current_drawdown']:.1f}% | TC: {true_count:.1f}")

        return result
    
    def resolve_hand(self, player_total, dealer_total, is_blackjack=False):
        """Same resolution logic as before"""
        if player_total > 21:
            self.losses += 1
            self.busts += 1
            return "loss"
        elif is_blackjack and dealer_total != 21:
            self.wins += 1
            self.blackjacks += 1
            return "win"
        elif dealer_total > 21 or player_total > dealer_total:
            self.wins += 1
            return "win"
        elif player_total < dealer_total:
            self.losses += 1
            return "loss"
        else:
            self.pushes += 1
            return "push"
    
    def get_comprehensive_stats(self):
        """Enhanced statistics including new metrics"""
        bankroll_stats = self.bankroll_manager.get_advanced_stats()
        win_rate = (self.wins / max(self.hands_played, 1)) * 100
        
        return {
            "name": self.name,
            "hands_played": self.hands_played,
            "wins": self.wins,
            "losses": self.losses,
            "pushes": self.pushes,
            "win_rate": win_rate,
            "blackjacks": self.blackjacks,
            "busts": self.busts,
            "deviation_count": self.deviation_count,
            "risk_reductions": self.risk_reductions,
            **bankroll_stats
        }
class EnhancedOptimalAI(OptimizedAIBot):
    def __init__(self, strategy, name="EnhancedOptimalAI", initial_bankroll=1000, risk_level="moderate", unit_percentage=1.0):
        super().__init__(strategy, name, initial_bankroll, risk_level, unit_percentage)
        self.bankroll_manager = OptimizedBankrollManager(
            initial_bankroll=initial_bankroll,
            base_unit_percentage=unit_percentage,
            risk_level=risk_level
        )

def run_optimized_simulation(rounds=60000, log_interval=1000):
    """Run simulation with optimized bankroll management"""
    print("\n🚀 OPTIMIZED AI SIMULATION WITH ADVANCED BANKROLL MANAGEMENT 🚀\n")

    basic_strategy = BasicStrategy()

    # Initialize enhanced components
    enhanced_counter = EnhancedCardCounter(num_decks=6)
    basic_strategy = BasicStrategy()
    enhanced_decision_engine = EnhancedCountingDecisionEngine(basic_strategy, enhanced_counter)

    
    # Create optimized AI bots
    conservative_ai = OptimizedAIBot(
        basic_strategy, 
        name="ConservativeAI", 
        initial_bankroll=1000,
        risk_level="ultra_conservative",
        unit_percentage=0.75
    )

    counter = CardCounter(num_decks=6)
    smart_strategy = CountingDecisionEngine(basic_strategy, counter)
    
    optimal_ai = OptimizedAIBot(
        smart_strategy, 
        name="OptimalAI",
        initial_bankroll=1000,
        risk_level="moderate", 
        unit_percentage=1.0
    )
    
    aggressive_ai = OptimizedAIBot(
        smart_strategy,
        name="ControlledAggressiveAI",
        initial_bankroll=1000,
        risk_level="aggressive",
        unit_percentage=1.25

    )
    enhanced_ai = EnhancedOptimalAI(
    enhanced_decision_engine,
    name="EnhancedOptimalAI",
    initial_bankroll=1000,
    risk_level="moderate",
    unit_percentage=1.0
)

    shoe = BlackjackShoe(num_decks=6)
    all_ais = [conservative_ai, optimal_ai, aggressive_ai, enhanced_ai]

    for round_num in range(1, rounds + 1):
        if shoe.penetration() > 75:
            shoe.shuffle()
            counter.reset()

        dealer_upcard = shoe.draw_card()
        counter.update_count([dealer_upcard])

        if round_num % 50 == 0:  # Reduced logging frequency
            print(f"\n=== Round {round_num}/{rounds} ===")

        # Play hands
        active_ais = []
        for ai in all_ais:
            if not ai.bankroll_manager.is_broke():
                result = ai.play_hand(dealer_upcard, shoe, counter if "Conservative" not in ai.name else None, active_ais)
                if result != "broke":
                    active_ais.append(ai)

        # Progress logging
        if round_num % log_interval == 0:
            print(f"\n{'='*60}")
            print(f"ADVANCED ANALYTICS - ROUND {round_num}")
            print(f"{'='*60}")
            
            for ai in all_ais:
                stats = ai.get_comprehensive_stats()
                print(f"\n[{stats['name']}] - Performance Dashboard")
                print(f"  💰 Bankroll: ${stats['current_bankroll']:.2f} (ROI: {stats['roi_percentage']:.1f}%)")
                print(f"  📊 Record: {stats['wins']}W-{stats['losses']}L-{stats['pushes']}P ({stats['win_rate']:.1f}%)")
                print(f"  🎯 Risk Metrics: Max DD {stats['max_drawdown']:.1f}% | Volatility {stats['volatility']:.1f}%")
                print(f"  📈 Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
                print(f"  💸 Current Unit: ${stats['current_unit_size']:.2f} | Avg Recent Bet: ${stats['avg_recent_bet']:.2f}")
                if stats['risk_reductions'] > 0:
                    print(f"  ⚠️  Risk Reductions Triggered: {stats['risk_reductions']}")

    # Final advanced analysis
    print(f"\n{'='*70}")
    print("🏆 FINAL ADVANCED PERFORMANCE ANALYSIS 🏆")
    print(f"{'='*70}")
    
    # Rank by risk-adjusted returns (Sharpe ratio)
    final_stats = [ai.get_comprehensive_stats() for ai in all_ais]
    ranked_ais = sorted(final_stats, key=lambda x: x['sharpe_ratio'], reverse=True)
    
    for i, stats in enumerate(ranked_ais, 1):
        print(f"\n🥇 RANK #{i}: [{stats['name']}]")
        print(f"  Final Bankroll: ${stats['current_bankroll']:.2f}")
        print(f"  Total Return: ${stats['profit_loss']:.2f} ({stats['roi_percentage']:.2f}% ROI)")
        print(f"  Risk-Adjusted Return (Sharpe): {stats['sharpe_ratio']:.3f}")
        print(f"  Maximum Drawdown: {stats['max_drawdown']:.2f}%")
        print(f"  Win Rate: {stats['win_rate']:.2f}%")
        print(f"  Volatility: {stats['volatility']:.2f}%")
        print(f"  Total Hands: {stats['hands_played']}")
        if stats['deviation_count'] > 0:
            print(f"  Counting Deviations: {stats['deviation_count']}")
        if stats['risk_reductions'] > 0:
            print(f"  Emergency Risk Reductions: {stats['risk_reductions']}")


if __name__ == "__main__":
    run_optimized_simulation(rounds=60000, log_interval=1000)