# Advanced Performance Analysis and Future Enhancements
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class AIPerformanceMetrics:
    """Data class for AI performance metrics"""
    name: str
    final_bankroll: float
    roi: float
    sharpe_ratio: float
    max_drawdown: float
    volatility: float
    win_rate: float
    risk_reductions: int
    hands_played: int
    
    def efficiency_score(self) -> float:
        """Calculate overall efficiency score"""
        # Weighted score: ROI (40%) + Sharpe (30%) + Low Drawdown (20%) + Win Rate (10%)
        normalized_roi = min(self.roi / 100, 1.0)  # Cap at 100%
        normalized_sharpe = min(self.sharpe_ratio / 200, 1.0)  # Cap at 200
        normalized_drawdown = max(0, 1 - (self.max_drawdown / 50))  # Penalty for high drawdown
        normalized_win_rate = self.win_rate / 50  # Normalize around 50%
        
        return (normalized_roi * 0.4 + 
                normalized_sharpe * 0.3 + 
                normalized_drawdown * 0.2 + 
                normalized_win_rate * 0.1) * 100


class PerformanceAnalyzer:
    """Advanced performance analysis for AI trading results"""
    
    def __init__(self):
        self.results = []
    
    def add_result(self, metrics: AIPerformanceMetrics):
        """Add AI performance result"""
        self.results.append(metrics)
    
    def analyze_results(self) -> Dict[str, Any]:
        """Comprehensive analysis of all AI performances"""
        if not self.results:
            return {}
        
        analysis = {
            "best_roi": max(self.results, key=lambda x: x.roi),
            "best_sharpe": max(self.results, key=lambda x: x.sharpe_ratio),
            "lowest_risk": min(self.results, key=lambda x: x.max_drawdown),
            "most_efficient": max(self.results, key=lambda x: x.efficiency_score()),
            "risk_vs_return": self._analyze_risk_return_tradeoff(),
            "betting_efficiency": self._analyze_betting_patterns(),
            "recommendations": self._generate_recommendations()
        }
        
        return analysis
    
    def _analyze_risk_return_tradeoff(self) -> Dict[str, Any]:
        """Analyze risk vs return characteristics"""
        risk_return_data = []
        
        for result in self.results:
            efficiency = result.roi / max(result.max_drawdown, 1)  # ROI per unit of risk
            risk_return_data.append({
                "name": result.name,
                "roi": result.roi,
                "risk": result.max_drawdown,
                "efficiency": efficiency,
                "sharpe": result.sharpe_ratio
            })
        
        # Find optimal risk-return profile
        best_efficiency = max(risk_return_data, key=lambda x: x["efficiency"])
        
        return {
            "data": risk_return_data,
            "optimal_profile": best_efficiency,
            "risk_return_correlation": self._calculate_correlation()
        }
    
    def _analyze_betting_patterns(self) -> Dict[str, str]:
        """Analyze betting pattern effectiveness"""
        patterns = {}
        
        for result in self.results:
            if result.risk_reductions > 0:
                pattern = "Aggressive with Emergency Controls"
                effectiveness = "High Risk, Moderate Return"
            elif result.sharpe_ratio > 150:
                pattern = "Optimal Kelly-Based Scaling"
                effectiveness = "Excellent Risk-Adjusted Returns"
            elif result.volatility < 0.35:
                pattern = "Conservative Unit Scaling"
                effectiveness = "Steady Growth, Lower Risk"
            else:
                pattern = "Standard Progressive Betting"
                effectiveness = "Moderate Risk and Return"
            
            patterns[result.name] = {
                "pattern": pattern,
                "effectiveness": effectiveness
            }
        
        return patterns
    
    def _calculate_correlation(self) -> float:
        """Calculate correlation between risk and return"""
        if len(self.results) < 2:
            return 0.0
        
        risks = [r.max_drawdown for r in self.results]
        returns = [r.roi for r in self.results]
        
        # Simple correlation calculation
        n = len(risks)
        sum_risks = sum(risks)
        sum_returns = sum(returns)
        sum_risk_return = sum(r * ret for r, ret in zip(risks, returns))
        sum_risks_sq = sum(r * r for r in risks)
        sum_returns_sq = sum(ret * ret for ret in returns)
        
        numerator = n * sum_risk_return - sum_risks * sum_returns
        denominator = ((n * sum_risks_sq - sum_risks * sum_risks) * 
                      (n * sum_returns_sq - sum_returns * sum_returns)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Find best performer
        best_ai = max(self.results, key=lambda x: x.sharpe_ratio)
        
        recommendations.append(f"🎯 Optimal Strategy: {best_ai.name} achieved the best risk-adjusted returns")
        recommendations.append(f"   → Sharpe Ratio: {best_ai.sharpe_ratio:.1f} with {best_ai.roi:.1f}% ROI")
        
        # Risk management insights
        high_risk_ais = [r for r in self.results if r.max_drawdown > 25]
        if high_risk_ais:
            recommendations.append("⚠️  High-Risk Alert: Consider reducing unit sizes for aggressive strategies")
        
        # Efficiency insights
        most_efficient = max(self.results, key=lambda x: x.efficiency_score())
        recommendations.append(f"🏆 Most Efficient: {most_efficient.name} (Efficiency Score: {most_efficient.efficiency_score():.1f})")
        
        # Betting recommendations
        avg_sharpe = sum(r.sharpe_ratio for r in self.results) / len(self.results)
        if best_ai.sharpe_ratio > avg_sharpe * 1.5:
            recommendations.append("📈 Recommendation: Scale up the optimal strategy for better returns")
        
        return recommendations
    
    def print_comprehensive_report(self):
        """Print detailed performance analysis report"""
        analysis = self.analyze_results()
        
        print("\n" + "="*80)
        print("🔍 COMPREHENSIVE PERFORMANCE ANALYSIS REPORT 🔍")
        print("="*80)
        
        # Best performers in each category
        print(f"\n🏆 CATEGORY LEADERS:")
        print(f"   Best ROI: {analysis['best_roi'].name} ({analysis['best_roi'].roi:.1f}%)")
        print(f"   Best Risk-Adjusted: {analysis['best_sharpe'].name} (Sharpe: {analysis['best_sharpe'].sharpe_ratio:.1f})")
        print(f"   Lowest Risk: {analysis['lowest_risk'].name} ({analysis['lowest_risk'].max_drawdown:.1f}% max drawdown)")
        print(f"   Most Efficient: {analysis['most_efficient'].name} (Score: {analysis['most_efficient'].efficiency_score():.1f})")
        
        # Risk-Return Analysis
        print(f"\n📊 RISK-RETURN ANALYSIS:")
        optimal = analysis['risk_vs_return']['optimal_profile']
        print(f"   Optimal Risk-Return Profile: {optimal['name']}")
        print(f"   → ROI per Unit Risk: {optimal['efficiency']:.2f}")
        print(f"   → Risk Level: {optimal['risk']:.1f}% | Return: {optimal['roi']:.1f}%")
        
        # Betting Pattern Analysis
        print(f"\n💰 BETTING PATTERN EFFECTIVENESS:")
        for name, pattern_info in analysis['betting_efficiency'].items():
            print(f"   {name}: {pattern_info['pattern']}")
            print(f"   └─ Result: {pattern_info['effectiveness']}")
        
        # Recommendations
        print(f"\n🎯 STRATEGIC RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
        
        # Advanced Metrics Table
        print(f"\n📈 DETAILED PERFORMANCE MATRIX:")
        print(f"{'AI Name':<20} {'ROI%':<8} {'Sharpe':<8} {'MaxDD%':<8} {'Efficiency':<10} {'Grade':<6}")
        print("-" * 70)
        
        for result in sorted(self.results, key=lambda x: x.sharpe_ratio, reverse=True):
            grade = self._calculate_grade(result)
            print(f"{result.name:<20} {result.roi:<8.1f} {result.sharpe_ratio:<8.1f} "
                  f"{result.max_drawdown:<8.1f} {result.efficiency_score():<10.1f} {grade:<6}")
    
    def _calculate_grade(self, metrics: AIPerformanceMetrics) -> str:
        """Calculate letter grade based on overall performance"""
        score = metrics.efficiency_score()
        
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        else:
            return "C"


# Analysis of your results
def analyze_your_results():
    """Analyze the specific results from your simulation"""
    analyzer = PerformanceAnalyzer()
    
    # Add your AI results
    analyzer.add_result(AIPerformanceMetrics(
        name="OptimalAI",
        final_bankroll=1604.75,
        roi=60.48,
        sharpe_ratio=179.127,
        max_drawdown=17.98,
        volatility=0.34,
        win_rate=46.38,
        risk_reductions=0,
        hands_played=5000
    ))
    
    analyzer.add_result(AIPerformanceMetrics(
        name="ConservativeAI", 
        final_bankroll=1374.75,
        roi=37.48,
        sharpe_ratio=101.559,
        max_drawdown=17.74,
        volatility=0.37,
        win_rate=45.96,
        risk_reductions=0,
        hands_played=5000
    ))
    
    analyzer.add_result(AIPerformanceMetrics(
        name="ControlledAggressiveAI",
        final_bankroll=1231.75,
        roi=23.18,
        sharpe_ratio=50.433,
        max_drawdown=27.38,
        volatility=0.46,
        win_rate=45.74,
        risk_reductions=226,
        hands_played=5000
    ))
    
    # Generate comprehensive report
    analyzer.print_comprehensive_report()
    
    # Specific insights for your results
    print(f"\n🔬 SPECIFIC INSIGHTS FROM YOUR SIMULATION:")
    print(f"   1. OptimalAI achieved a Sharpe ratio of 179 - this is EXCEPTIONAL")
    print(f"   2. Kelly Criterion betting proved superior to aggressive scaling")
    print(f"   3. Risk reduction triggers saved ControlledAggressiveAI from bankruptcy")
    print(f"   4. Moderate risk strategy outperformed both conservative and aggressive")
    print(f"   5. Card counting + optimal betting = 60.5% ROI with controlled risk")
    
    print(f"\n💡 NEXT OPTIMIZATION OPPORTUNITIES:")
    print(f"   → Test different Kelly fractions (0.25x, 0.5x, 0.75x)")
    print(f"   → Experiment with dynamic risk level adjustment")
    print(f"   → Add more sophisticated counting deviations") 
    print(f"   → Implement bankroll stop-loss and take-profit levels")
    print(f"   → Test performance across different deck penetrations")


if __name__ == "__main__":
    analyze_your_results()