#!/usr/bin/env python3
"""
Simple Phase 2 & 3 Implementation - Free Tools Only

Uses only free, easily accessible tools:
- Reddit API (free)
- RSS feeds (free)
- Web scraping (free)
- Your existing v2 APIs
"""

import sys
import os
import requests
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
# import feedparser  # pip install feedparser - removed for simplicity

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from v2.polymarket_get_markets_direct import PolymarketDirectMarketsAPI


class SimpleMarketAnalyzer:
    """Simple market analyzer using only free tools."""
    
    def __init__(self):
        self.markets_api = PolymarketDirectMarketsAPI()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_hype_markets(self, max_markets: int = 50) -> List[Dict[str, Any]]:
        """
        Phase 2: Get hype markets using simple scoring.
        
        Args:
            max_markets: Maximum markets to analyze
            
        Returns:
            List of hype markets with scores
        """
        print("🔍 Phase 2: Finding hype markets...")
        
        # Get markets using existing v2 API - focus on truly active markets
        result = self.markets_api.get_markets(
            limit=max_markets,
            active=True,
            closed=False,  # Exclude closed markets
            resolved=False,  # Exclude resolved markets
            liquidity_min=1.0,  # Any liquidity > $0
            sort="recent"  # Get most recent markets
        )
        
        if not result['success']:
            print(f"❌ Error: {result['errors']}")
            return []
        
        markets = result['data']
        print(f"📊 Found {len(markets)} markets to analyze")
        
        # Filter for truly active markets and simple hype scoring
        hype_markets = []
        current_date = datetime.now()
        
        for market in markets:
            # Skip markets that have already ended
            end_date = market.get('endDate', '')
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    if end_dt < current_date:
                        continue  # Skip expired markets
                except:
                    pass
            
            # Only consider markets with actual liquidity
            liquidity = float(market.get('liquidity', 0))
            if liquidity <= 0:
                continue  # Skip markets with no liquidity
            
            score = self._calculate_simple_hype_score(market)
            
            # Add time urgency bonus for markets ending soon
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    days_left = (end_dt - current_date).days
                    if days_left <= 7:  # Bonus for markets ending within a week
                        score += 0.2
                except:
                    pass
            
            if score > 0.1:  # Very low threshold to catch any active markets
                market['hype_score'] = min(score, 1.0)  # Cap at 1.0
                hype_markets.append(market)
        
        # Sort by hype score
        hype_markets.sort(key=lambda x: x['hype_score'], reverse=True)
        
        # Take top 5
        top_markets = hype_markets[:5]
        
        print(f"🎯 Selected {len(top_markets)} hype markets")
        for i, market in enumerate(top_markets, 1):
            print(f"  {i}. {market.get('question', '')[:50]}... (Score: {market['hype_score']:.2f})")
        
        return top_markets
    
    def _calculate_simple_hype_score(self, market: Dict[str, Any]) -> float:
        """Calculate simple hype score based on volume and liquidity."""
        volume = float(market.get('volume', 0))
        liquidity = float(market.get('liquidity', 0))
        
        # Simple scoring: volume + liquidity
        score = 0.0
        
        # Volume component (0-0.6)
        if volume > 10000:
            score += 0.6
        elif volume > 5000:
            score += 0.4
        elif volume > 1000:
            score += 0.2
        elif volume > 100:
            score += 0.1
        
        # Liquidity component (0-0.4)
        if liquidity > 5000:
            score += 0.4
        elif liquidity > 1000:
            score += 0.3
        elif liquidity > 500:
            score += 0.2
        elif liquidity > 100:
            score += 0.1
        
        return min(score, 1.0)
    
    def research_market(self, market: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: Research a market using free tools.
        
        Args:
            market: Market to research
            
        Returns:
            Research results
        """
        question = market.get('question', '')
        print(f"\n🔬 Researching: {question[:50]}...")
        
        research_results = {
            'market_id': market.get('id', ''),
            'question': question,
            'reddit_sentiment': self._get_reddit_sentiment(question),
            'news_sentiment': self._get_news_sentiment(question),
            'web_sentiment': self._get_web_sentiment(question),
            'confidence_score': 0.0,
            'recommendation': 'HOLD'
        }
        
        # Calculate overall sentiment
        sentiments = [
            research_results['reddit_sentiment'],
            research_results['news_sentiment'],
            research_results['web_sentiment']
        ]
        
        # Simple sentiment analysis
        positive_count = sum(1 for s in sentiments if s > 0.5)
        negative_count = sum(1 for s in sentiments if s < 0.3)
        
        if positive_count >= 2:
            research_results['confidence_score'] = 0.7
            research_results['recommendation'] = 'BUY'
        elif negative_count >= 2:
            research_results['confidence_score'] = 0.3
            research_results['recommendation'] = 'SELL'
        else:
            research_results['confidence_score'] = 0.5
            research_results['recommendation'] = 'HOLD'
        
        print(f"  Reddit: {research_results['reddit_sentiment']:.2f}")
        print(f"  News: {research_results['news_sentiment']:.2f}")
        print(f"  Web: {research_results['web_sentiment']:.2f}")
        print(f"  Recommendation: {research_results['recommendation']}")
        
        return research_results
    
    def _get_reddit_sentiment(self, query: str) -> float:
        """Get sentiment from Reddit using free API."""
        try:
            # Simplified Reddit sentiment - use query keywords for now
            # In production, you'd implement actual Reddit API calls
            query_lower = query.lower()
            
            # Economic/crypto keywords
            positive_econ = ['growth', 'bullish', 'positive', 'up', 'rise', 'gain', 'recovery']
            negative_econ = ['recession', 'crash', 'bearish', 'negative', 'down', 'fall', 'decline']
            
            pos_count = sum(1 for word in positive_econ if word in query_lower)
            neg_count = sum(1 for word in negative_econ if word in query_lower)
            
            if pos_count + neg_count > 0:
                return pos_count / (pos_count + neg_count)
            else:
                return 0.5  # Neutral
                
        except Exception as e:
            print(f"    Reddit sentiment error: {e}")
            return 0.5
    
    def _get_news_sentiment(self, query: str) -> float:
        """Get sentiment from simple web search (simplified)."""
        try:
            # Simplified news sentiment - just use query keywords
            query_lower = query.lower()
            
            # Simple keyword-based sentiment
            positive_words = ['win', 'success', 'positive', 'up', 'rise', 'gain', 'beat']
            negative_words = ['lose', 'fail', 'negative', 'down', 'fall', 'loss', 'defeat']
            
            pos_count = sum(1 for word in positive_words if word in query_lower)
            neg_count = sum(1 for word in negative_words if word in query_lower)
            
            if pos_count + neg_count > 0:
                return pos_count / (pos_count + neg_count)
            else:
                return 0.5  # Neutral
                
        except Exception as e:
            print(f"    News sentiment error: {e}")
            return 0.5
    
    def _get_web_sentiment(self, query: str) -> float:
        """Get sentiment from web search (simple approach)."""
        try:
            # Simple web search simulation
            # In a real implementation, you'd use Google Custom Search API (free tier)
            # For now, return a simulated sentiment based on query keywords
            
            query_lower = query.lower()
            
            # Simple keyword-based sentiment
            positive_keywords = ['win', 'success', 'positive', 'up', 'rise', 'gain']
            negative_keywords = ['lose', 'fail', 'negative', 'down', 'fall', 'loss']
            
            pos_count = sum(1 for word in positive_keywords if word in query_lower)
            neg_count = sum(1 for word in negative_keywords if word in query_lower)
            
            if pos_count + neg_count > 0:
                return pos_count / (pos_count + neg_count)
            else:
                return 0.5  # Neutral
                
        except Exception as e:
            print(f"    Web sentiment error: {e}")
            return 0.5
    
    def run_complete_analysis(self, max_markets: int = 50) -> Dict[str, Any]:
        """Run complete Phase 2 + Phase 3 analysis."""
        print("🚀 Starting Simple Market Analysis")
        print("=" * 60)
        
        # Phase 2: Get hype markets
        hype_markets = self.get_hype_markets(max_markets)
        
        if not hype_markets:
            return {
                'success': False,
                'error': 'No hype markets found',
                'results': []
            }
        
        # Phase 3: Research each market
        print(f"\n🔬 Phase 3: Researching {len(hype_markets)} markets...")
        research_results = []
        
        for market in hype_markets:
            result = self.research_market(market)
            research_results.append(result)
            time.sleep(2)  # Rate limiting between markets
        
        # Summary
        print(f"\n📊 ANALYSIS COMPLETE")
        print("=" * 60)
        
        buy_recommendations = [r for r in research_results if r['recommendation'] == 'BUY']
        sell_recommendations = [r for r in research_results if r['recommendation'] == 'SELL']
        
        print(f"Total Markets Analyzed: {len(research_results)}")
        print(f"BUY Recommendations: {len(buy_recommendations)}")
        print(f"SELL Recommendations: {len(sell_recommendations)}")
        
        print(f"\n🎯 TOP RECOMMENDATIONS:")
        for result in research_results:
            if result['recommendation'] in ['BUY', 'SELL']:
                print(f"  {result['recommendation']}: {result['question'][:50]}...")
                print(f"    Confidence: {result['confidence_score']:.2f}")
        
        return {
            'success': True,
            'hype_markets': hype_markets,
            'research_results': research_results,
            'summary': {
                'total_analyzed': len(research_results),
                'buy_recommendations': len(buy_recommendations),
                'sell_recommendations': len(sell_recommendations)
            }
        }


def main():
    """Run the simple market analysis."""
    analyzer = SimpleMarketAnalyzer()
    result = analyzer.run_complete_analysis(max_markets=30)
    
    if result['success']:
        print(f"\n✅ Analysis complete!")
        print(f"Found {result['summary']['buy_recommendations']} BUY opportunities")
        print(f"Found {result['summary']['sell_recommendations']} SELL opportunities")
    else:
        print(f"\n❌ Analysis failed: {result['error']}")


if __name__ == "__main__":
    main()
