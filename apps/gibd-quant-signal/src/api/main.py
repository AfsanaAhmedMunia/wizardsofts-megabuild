"""
GIBD Quant Signal Service - FastAPI Application

Provides trading signal generation using AdaptiveSignalEngine.
Integrates with Eureka for service discovery.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.signal_engine import AdaptiveSignalEngine
from database.connection import get_db_context

# Eureka registration
try:
    from py_eureka_client import eureka_client

    eureka_client.init(
        eureka_server=os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka"),
        app_name=os.getenv("APP_NAME", "gibd-quant-signal"),
        instance_port=int(os.getenv("APP_PORT", "5001")),
        instance_host=os.getenv("APP_HOST", "gibd-quant-signal")
    )
except Exception as e:
    print(f"Warning: Eureka registration failed: {e}")

app = FastAPI(
    title="GIBD Quant Signal Service",
    description="Trading signal generation with adaptive thresholds",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class SignalRequest(BaseModel):
    ticker: str
    date: Optional[str] = None

class SignalResponse(BaseModel):
    ticker: str
    signal_type: str
    total_score: float
    confidence: float
    rsi_score: float
    macd_score: float
    sma_score: float
    adx_score: float
    volume_score: float
    sector_score: float

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "UP", "service": "gibd-quant-signal"}

@app.post("/api/v1/signals/generate", response_model=SignalResponse)
async def generate_signal(request: SignalRequest):
    """Generate trading signal for a ticker"""
    try:
        engine = AdaptiveSignalEngine()
        signal = engine.generate_signal(request.ticker, request.date)

        return SignalResponse(
            ticker=signal.ticker,
            signal_type=signal.signal_type,
            total_score=signal.total_score,
            confidence=signal.confidence,
            rsi_score=signal.rsi_score,
            macd_score=signal.macd_score,
            sma_score=signal.sma_score,
            adx_score=signal.adx_score,
            volume_score=signal.volume_score,
            sector_score=signal.sector_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/signals/batch")
async def generate_batch_signals(tickers: list[str]):
    """Generate signals for multiple tickers"""
    try:
        engine = AdaptiveSignalEngine()
        results = []

        for ticker in tickers:
            try:
                signal = engine.generate_signal(ticker)
                results.append({
                    "ticker": signal.ticker,
                    "signal_type": signal.signal_type,
                    "total_score": signal.total_score,
                    "confidence": signal.confidence
                })
            except Exception as e:
                results.append({
                    "ticker": ticker,
                    "error": str(e)
                })

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/signals/scan")
async def scan_signals(
    signal_type: str = "BUY",
    threshold: float = 0.4,
    limit: int = 50
):
    """Scan all stocks for signals"""
    try:
        engine = AdaptiveSignalEngine(
            buy_threshold=threshold if signal_type == "BUY" else 0.4,
            sell_threshold=-threshold if signal_type == "SELL" else -0.4
        )

        # Get all active tickers from database
        with get_db_context() as session:
            from database.models import Indicator
            tickers = session.query(Indicator.ticker).distinct().all()
            tickers = [t[0] for t in tickers]

        results = []
        for ticker in tickers[:limit]:  # Limit for performance
            try:
                signal = engine.generate_signal(ticker)
                if signal_type == "all" or signal.signal_type == signal_type:
                    results.append({
                        "ticker": signal.ticker,
                        "signal_type": signal.signal_type,
                        "total_score": signal.total_score,
                        "confidence": signal.confidence
                    })
            except:
                continue

        # Sort by score
        results.sort(key=lambda x: abs(x["total_score"]), reverse=True)
        return {"results": results[:limit]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "5001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
