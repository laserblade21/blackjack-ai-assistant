from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.ai_brain.EnhancedCardCounter import EnhancedCardCounter
from src.ai_brain.enhanced_counting_decision_engine import EnhancedCountingDecisionEngine
from src.ai_brain.basic_strategy import BasicStrategy

app = FastAPI(title="Blackjack AI Assistant", description="AI-powered blackjack decision making with card counting", version="1.0.0")

class HandRequest(BaseModel):
    player_hand: list
    dealer_upcard: int
    running_count: int
    cards_dealt: int
    num_decks: int

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blackjack AI Assistant</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #e2e8f0;
                min-height: 100vh;
            }
            .container {
                background: rgba(30, 41, 59, 0.8);
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            h1 {
                color: #10b981;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            .subtitle {
                text-align: center;
                color: #94a3b8;
                margin-bottom: 40px;
                font-size: 1.2em;
            }
            .status {
                background: linear-gradient(45deg, #10b981, #059669);
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            }
            .endpoint {
                background: rgba(55, 65, 81, 0.6);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 5px solid #10b981;
                transition: transform 0.2s ease;
            }
            .endpoint:hover {
                transform: translateX(5px);
            }
            .method {
                color: white;
                padding: 5px 12px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #059669; }
            .post { background: #dc2626; }
            code {
                background: rgba(75, 85, 99, 0.8);
                padding: 3px 8px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                color: #fbbf24;
            }
            .example {
                background: rgba(17, 24, 39, 0.8);
                padding: 15px;
                border-radius: 8px;
                margin-top: 15px;
                overflow-x: auto;
                border: 1px solid rgba(75, 85, 99, 0.3);
            }
            pre {
                margin: 0;
                color: #e5e7eb;
                font-size: 14px;
            }
            .links {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 30px;
            }
            .link-card {
                background: rgba(55, 65, 81, 0.6);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                transition: all 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .link-card:hover {
                background: rgba(75, 85, 99, 0.8);
                transform: translateY(-5px);
            }
            .link-card a {
                color: #10b981;
                text-decoration: none;
                font-weight: bold;
                font-size: 16px;
            }
            .link-card a:hover {
                color: #34d399;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature {
                background: rgba(55, 65, 81, 0.4);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            .feature-icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🃏 Blackjack AI Assistant</h1>
            <p class="subtitle">Advanced AI-powered blackjack decision making with enhanced card counting</p>
            
            <div class="status">
                ✅ API is running successfully!
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🧠</div>
                    <h3>Enhanced Card Counter</h3>
                    <p>Advanced counting algorithms for optimal play</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <h3>Decision Engine</h3>
                    <p>Real-time strategic decision making</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <h3>Basic Strategy</h3>
                    <p>Mathematically optimal base strategy</p>
                </div>
            </div>
            
            <h2>API Endpoints:</h2>
            
            <div class="endpoint">
                <p><span class="method get">GET</span> <code>/</code></p>
                <p>This welcome page with API information</p>
            </div>
            
            <div class="endpoint">
                <p><span class="method post">POST</span> <code>/ai_decision</code></p>
                <p>Get AI recommendation for a blackjack hand using enhanced counting and strategy</p>
                
                <h4>Request Body Example:</h4>
                <div class="example">
                    <pre>{
  "player_hand": [10, 7],
  "dealer_upcard": 6,
  "running_count": 2,
  "cards_dealt": 26,
  "num_decks": 6
}</pre>
                </div>
                
                <h4>Response Example:</h4>
                <div class="example">
                    <pre>{
  "action": "stand",
  "confidence": 0.92,
  "reasoning": "Basic strategy + positive count suggests standing"
}</pre>
                </div>
            </div>
            
            <h2>API Documentation:</h2>
            <div class="links">
                <div class="link-card">
                    <a href="/docs">📚 Swagger UI</a>
                    <p>Interactive API documentation</p>
                </div>
                <div class="link-card">
                    <a href="/redoc">📖 ReDoc</a>
                    <p>Alternative documentation view</p>
                </div>
                <div class="link-card">
                    <a href="/openapi.json">⚙️ OpenAPI Schema</a>
                    <p>Raw API specification</p>
                </div>
            </div>
            
            <div style="margin-top: 40px; text-align: center; color: #64748b;">
                <p>🎯 Ready to make optimal blackjack decisions with AI-powered card counting!</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/eyobsai_decision")
def ai_decision(req: HandRequest):
    counter = EnhancedCardCounter(num_decks=req.num_decks)
    counter.running_count = req.running_count
    counter.cards_seen = req.cards_dealt
    strategy = BasicStrategy()
    engine = EnhancedCountingDecisionEngine(strategy, counter)
    result = engine.make_decision(req.player_hand, req.dealer_upcard)
    return result