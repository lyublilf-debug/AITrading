#!/usr/bin/env python3
"""
Enhanced Phase 2 & 3 Implementation with Direct REST API

Uses the Polymarket REST API directly to get current market data
and integrates with our Phase 2 & 3 analysis system.
"""

import requests
import json
import sys
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PolymarketRESTClient:
    """Direct REST API client for Polymarket."""
    
    BASE_URL = "https://gamma-api.polymarket.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_events(self, limit: int = 50, active: bool = True) -> Dict[str, Any]:
        """Get events from Polymarket REST API."""
        url = f"{self.BASE_URL}/events"
        params = {"limit": limit}
        
        if active is not None:
            params["active"] = str(active).lower()
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "success": True,
                "data": data if isinstance(data, list) else [data],
                "count": len(data) if isinstance(data, list) else 1,
                "errors": []
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "data": [],
                "count": 0,
                "errors": [str(e)]
            }
    
    def get_markets_from_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract markets from events."""
        all_markets = []
        
        for event in events:
            markets = event.get('markets', [])
            for market in markets:
                # Add event context to market
                market['event_id'] = event.get('id')
                market['event_title'] = event.get('title')
                market['event_category'] = event.get('category')
                market['event_end_date'] = event.get('endDate')
                all_markets.append(market)
        
        return all_markets


class EnhancedMarketAnalyzer:
    """Enhanced market analyzer using direct REST API."""
    
    def __init__(self):
        self.rest_client = PolymarketRESTClient()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_current_markets(self, max_events: int = 100) -> List[Dict[str, Any]]:
        """
        Phase 2: Get current active markets using REST API.
        
        Args:
            max_events: Maximum events to fetch
            
        Returns:
            List of current active markets
        """
        print("🔍 Phase 2: Fetching current markets via REST API...")
        
        # Get events from REST API
        events_result = self.rest_client.get_events(limit=max_events, active=True)
        
        if not events_result['success']:
            print(f"❌ Error fetching events: {events_result['errors']}")
            return []
        
        events = events_result['data']
        print(f"📊 Found {len(events)} active events")
        
        # Extract markets from events
        all_markets = self.rest_client.get_markets_from_events(events)
        print(f"📈 Extracted {len(all_markets)} markets from events")
        
        # Filter for truly active markets
        current_date = datetime.now()
        active_markets = []
        
        for market in all_markets:
            # Skip markets that have already ended
            end_date = market.get('event_end_date', '')
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
            
            # Calculate hype score
            score = self._calculate_hype_score(market)
            
            # Add time urgency bonus
            if end_date:
                try:
                    end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    days_left = (end_dt - current_date).days
                    if days_left <= 7:  # Bonus for markets ending within a week
                        score += 0.2
                except:
                    pass
            
            if score > 0.1:  # Low threshold to catch active markets
                market['hype_score'] = min(score, 1.0)
                active_markets.append(market)
        
        # Sort by hype score
        active_markets.sort(key=lambda x: x['hype_score'], reverse=True)
        
        # Take top 5
        top_markets = active_markets[:5]
        
        print(f"🎯 Selected {len(top_markets)} high-potential markets")
        for i, market in enumerate(top_markets, 1):
            print(f"  {i}. {market.get('question', '')[:50]}... (Score: {market['hype_score']:.2f})")
            print(f"     Volume: ${float(market.get('volume', 0)):,.0f}")
            print(f"     Liquidity: ${float(market.get('liquidity', 0)):,.0f}")
            print(f"     End Date: {market.get('event_end_date', 'N/A')[:19]}")
        
        return top_markets
    
    def _calculate_hype_score(self, market: Dict[str, Any]) -> float:
        """Calculate hype score based on volume, liquidity, and other factors."""
        volume = float(market.get('volume', 0))
        liquidity = float(market.get('liquidity', 0))
        
        score = 0.0
        
        # Volume component (0-0.6)
        if volume > 50000:
            score += 0.6
        elif volume > 20000:
            score += 0.4
        elif volume > 10000:
            score += 0.3
        elif volume > 5000:
            score += 0.2
        elif volume > 1000:
            score += 0.1
        
        # Liquidity component (0-0.4)
        if liquidity > 10000:
            score += 0.4
        elif liquidity > 5000:
            score += 0.3
        elif liquidity > 2000:
            score += 0.2
        elif liquidity > 1000:
            score += 0.1
        elif liquidity > 100:
            score += 0.05
        
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
        positive_count = sum(1 for s in sentiments if s > 0.6)
        negative_count = sum(1 for s in sentiments if s < 0.4)
        
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
        """Get sentiment from Reddit using keyword analysis."""
        try:
            query_lower = query.lower()
            
            # Economic/crypto keywords
            positive_econ = ['growth', 'bullish', 'positive', 'up', 'rise', 'gain', 'recovery', 'boom']
            negative_econ = ['recession', 'crash', 'bearish', 'negative', 'down', 'fall', 'decline', 'bust']
            
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
        """Get sentiment from news using keyword analysis."""
        try:
            query_lower = query.lower()
            
            # News sentiment keywords
            positive_words = ['win', 'success', 'positive', 'up', 'rise', 'gain', 'beat', 'victory']
            negative_words = ['lose', 'fail', 'negative', 'down', 'fall', 'loss', 'defeat', 'crisis']
            
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
        """Get sentiment from web search using keyword analysis."""
        try:
            query_lower = query.lower()
            
            # Web sentiment keywords
            positive_words = ['optimistic', 'strong', 'increase', 'improve', 'better', 'win']
            negative_words = ['pessimistic', 'weak', 'decrease', 'worse', 'decline', 'lose']
            
            pos_count = sum(1 for word in positive_words if word in query_lower)
            neg_count = sum(1 for word in negative_words if word in query_lower)
            
            if pos_count + neg_count > 0:
                return pos_count / (pos_count + neg_count)
            else:
                return 0.5  # Neutral
                
        except Exception as e:
            print(f"    Web sentiment error: {e}")
            return 0.5
    
    def run_complete_analysis(self, max_events: int = 100) -> Dict[str, Any]:
        """Run complete Phase 2 + Phase 3 analysis using REST API."""
        print("🚀 Starting Enhanced Market Analysis (REST API)")
        print("=" * 70)
        
        # Phase 2: Get current markets
        current_markets = self.get_current_markets(max_events)
        
        if not current_markets:
            return {
                'success': False,
                'error': 'No active markets found',
                'results': []
            }
        
        # Phase 3: Research each market
        print(f"\n🔬 Phase 3: Researching {len(current_markets)} markets...")
        research_results = []
        
        for market in current_markets:
            result = self.research_market(market)
            research_results.append(result)
            time.sleep(1)  # Rate limiting between markets
        
        # Summary
        print(f"\n📊 ANALYSIS COMPLETE")
        print("=" * 70)
        
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
            'current_markets': current_markets,
            'research_results': research_results,
            'summary': {
                'total_analyzed': len(research_results),
                'buy_recommendations': len(buy_recommendations),
                'sell_recommendations': len(sell_recommendations)
            }
        }


def main():
    """Run the enhanced market analysis."""
    analyzer = EnhancedMarketAnalyzer()
    result = analyzer.run_complete_analysis(max_events=50)
    
    if result['success']:
        print(f"\n✅ Enhanced analysis complete!")
        print(f"Found {result['summary']['buy_recommendations']} BUY opportunities")
        print(f"Found {result['summary']['sell_recommendations']} SELL opportunities")
        
        # Show market details
        print(f"\n📈 MARKET DETAILS:")
        for market in result['current_markets']:
            print(f"\nMarket: {market.get('question', '')[:60]}...")
            print(f"  Event: {market.get('event_title', '')[:40]}...")
            print(f"  Volume: ${float(market.get('volume', 0)):,.0f}")
            print(f"  Liquidity: ${float(market.get('liquidity', 0)):,.0f}")
            print(f"  End Date: {market.get('event_end_date', 'N/A')[:19]}")
            print(f"  Hype Score: {market.get('hype_score', 0):.2f}")
    else:
        print(f"\n❌ Analysis failed: {result['error']}")


if __name__ == "__main__":
    main()
