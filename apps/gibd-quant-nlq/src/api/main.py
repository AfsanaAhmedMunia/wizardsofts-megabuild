"""
GIBD Quant NLQ Service - FastAPI Application

Provides natural language query interface for stock analysis.
Integrates with Eureka for service discovery.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlq.api import NLQueryEngine
from database.connection import get_db_context

# Eureka registration
try:
    from py_eureka_client import eureka_client

    eureka_client.init(
        eureka_server=os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka"),
        app_name=os.getenv("APP_NAME", "gibd-quant-nlq"),
        instance_port=int(os.getenv("APP_PORT", "5002")),
        instance_host=os.getenv("APP_HOST", "gibd-quant-nlq")
    )
except Exception as e:
    print(f"Warning: Eureka registration failed: {e}")

app = FastAPI(
    title="GIBD Quant NLQ Service",
    description="Natural language query interface for stock analysis",
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
class QueryRequest(BaseModel):
    query: str
    tickers: Optional[List[str]] = None
    limit: Optional[int] = 50

class ParseRequest(BaseModel):
    query: str

class QueryResult(BaseModel):
    ticker: str
    value: float
    additional_info: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    query_type: str
    results: List[QueryResult]
    total_results: int

class ParseResponse(BaseModel):
    query_type: str
    indicator: Optional[str] = None
    threshold: Optional[float] = None
    days: Optional[int] = None
    direction: Optional[str] = None
    limit: Optional[int] = None
    confidence: float

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "UP", "service": "gibd-quant-nlq"}

@app.post("/api/v1/nlq/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute natural language query"""
    try:
        engine = NLQueryEngine()
        result = engine.query(
            query=request.query,
            tickers=request.tickers,
            limit=request.limit
        )

        return QueryResponse(
            query=request.query,
            query_type=result.query_type,
            results=[
                QueryResult(
                    ticker=r.get("ticker", ""),
                    value=r.get("value", 0.0),
                    additional_info={k: v for k, v in r.items() if k not in ["ticker", "value"]}
                )
                for r in result.results
            ],
            total_results=len(result.results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/nlq/parse", response_model=ParseResponse)
async def parse_query(request: ParseRequest):
    """Parse query without executing (for testing/debugging)"""
    try:
        engine = NLQueryEngine()
        parsed = engine.parse(request.query)

        return ParseResponse(
            query_type=parsed.query_type,
            indicator=parsed.indicator,
            threshold=parsed.threshold,
            days=parsed.days,
            direction=parsed.direction,
            limit=parsed.limit,
            confidence=parsed.confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/nlq/examples")
async def get_examples():
    """Get example queries for each supported type"""
    return {
        "examples": {
            "trend": [
                "stocks with increasing RSI for 5 days",
                "decreasing SMA_20 for 3 days",
                "stocks with rising price"
            ],
            "threshold": [
                "stocks with RSI above 70",
                "volume above average",
                "overbought stocks",
                "oversold stocks"
            ],
            "ranking": [
                "top 20 stocks by volume",
                "show 10 stocks with highest RSI",
                "stocks with lowest price",
                "show 10 Bank sector stocks with highest volume"
            ],
            "comparison": [
                "stocks outperforming their sector",
                "stocks underperforming sector"
            ],
            "crossover": [
                "MACD bullish crossover",
                "MACD bearish crossover"
            ],
            "support_resistance": [
                "price near support",
                "price near resistance"
            ]
        },
        "supported_indicators": [
            "RSI_14",
            "SMA_20",
            "SMA_50",
            "SMA_200",
            "MACD_histogram",
            "MACD_line",
            "MACD_signal",
            "ADX_14",
            "ATR_14",
            "volume",
            "price/close"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "5002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
