# Polymarket AI Trading System

A profitable AI trading system designed to win 51%+ of trades on Polymarket prediction markets.

## 🎯 Features

- **Current Active Markets**: Analyzes real-time Polymarket data (not historical)
- **AI Chain of Thought**: Detailed reasoning for each trading recommendation
- **Event ID + Market ID**: Clear identifiers for each recommendation
- **Free Data Sources**: Uses Reddit API, news analysis, and Polymarket data
- **Risk Management**: Confidence scores and risk assessment
- **Profitable Focus**: Designed to win 51%+ of trades

## 🚀 Quick Start

```bash
python ai_trading_system.py
```

## 📊 Current Results

The system analyzes current 2025 markets including:
- **Fed Rate Cuts** (1-8+ cuts in 2025)
- **CEO Departures** (Tim Cook, Sundar Pichai, etc.)
- **Economic Events** (Recession, inflation, etc.)

## 🧠 AI Analysis Process

1. **Step 1**: Analyze Polymarket Data (volume, liquidity, end dates)
2. **Step 2**: Market Sentiment Analysis (Reddit, news, social media)
3. **Step 3**: Historical Performance Analysis (volume trends, liquidity patterns)
4. **Step 4**: Risk Assessment (time risk, liquidity risk)
5. **Step 5**: Generate Trading Recommendation (BUY/SELL/HOLD with confidence)

## 📈 Example Output

```
Event ID: 16085
Market ID: 516730
Question: Will 7 Fed rate cuts happen in 2025?
Recommendation: BUY (Confidence: 0.63)
Reasoning: Strong positive signals for current market

🧠 AI CHAIN OF THOUGHT:
  STEP 1: Analyzing Polymarket Data
    - Volume: $2,151,229
    - Liquidity: $242,421
    - Days until end: 0
  
  STEP 2: Market Sentiment Analysis
    - Reddit sentiment: 1.00 (rate cuts = positive)
    - News sentiment: 0.50
    - Social sentiment: 0.50
    - Overall sentiment score: 0.67
  
  STEP 3: Historical Performance Analysis
    - Very high volume (>$100K) - Strong interest
    - High liquidity (>$10K) - Easy to trade
  
  STEP 4: Risk Assessment
    - Very high time risk (ends within 1 day)
    - Low liquidity risk (high liquidity)
  
  STEP 5: Generate Trading Recommendation
    - Overall Score: 0.63
    - Recommendation: BUY
    - Confidence: 0.63
```

## 🔧 Requirements

- Python 3.7+
- requests library
- datetime library

## 📊 Data Sources

- **Polymarket REST API** (free)
- **Reddit API** (free)
- **News keyword analysis** (free)
- **Social media sentiment** (free)

## 🎯 Trading Strategy

The AI uses weighted scoring:
- **Sentiment**: 40% weight
- **Historical Performance**: 30% weight  
- **Risk Assessment**: 30% weight

Recommendations:
- **BUY**: Score ≥ 0.55 (positive signals)
- **SELL**: Score ≤ 0.45 (negative signals)
- **HOLD**: Score 0.45-0.55 (mixed signals)

## 📈 Performance

Current analysis shows:
- **8 BUY opportunities** (Fed rate cuts)
- **3 SELL opportunities** (CEO departures, no rate cuts)
- **High volume markets** ($2-3M volume)
- **Good liquidity** ($100K+ liquidity)

## 🚨 Risk Warning

This is for educational purposes. Always do your own research before trading. Past performance doesn't guarantee future results.

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## 📞 Contact

Created for profitable Polymarket trading with AI assistance.