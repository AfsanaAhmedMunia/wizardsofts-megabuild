"""
GIBD Quant Calibration Service - FastAPI Application

Provides stock parameter calibration and profiling.
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

from profiling.calibrator import StockCalibrator
from database.connection import get_db_context
from database.models import StockProfile

# Eureka registration
try:
    from py_eureka_client import eureka_client

    eureka_client.init(
        eureka_server=os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka"),
        app_name=os.getenv("APP_NAME", "gibd-quant-calibration"),
        instance_port=int(os.getenv("APP_PORT", "5003")),
        instance_host=os.getenv("APP_HOST", "gibd-quant-calibration")
    )
except Exception as e:
    print(f"Warning: Eureka registration failed: {e}")

app = FastAPI(
    title="GIBD Quant Calibration Service",
    description="Stock parameter calibration and profiling",
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

# Response models
class ProfileResponse(BaseModel):
    ticker: str
    rsi_overbought: float
    rsi_oversold: float
    volatility_category: str
    typical_volume: float
    high_volume_threshold: float
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    last_calibrated: Optional[str] = None

class CalibrationResponse(BaseModel):
    ticker: str
    status: str
    message: str
    profile: ProfileResponse

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "UP", "service": "gibd-quant-calibration"}

@app.post("/api/v1/calibrate/{ticker}", response_model=CalibrationResponse)
async def calibrate_stock(ticker: str, force: bool = False):
    """Auto-calibrate stock parameters from historical data"""
    try:
        calibrator = StockCalibrator()

        with get_db_context() as session:
            # Check if already calibrated
            existing = session.query(StockProfile).filter_by(ticker=ticker).first()

            if existing and not force:
                return CalibrationResponse(
                    ticker=ticker,
                    status="skipped",
                    message="Stock already calibrated. Use force=true to recalibrate.",
                    profile=ProfileResponse(
                        ticker=existing.ticker,
                        rsi_overbought=existing.rsi_overbought,
                        rsi_oversold=existing.rsi_oversold,
                        volatility_category=existing.volatility_category,
                        typical_volume=existing.typical_volume,
                        high_volume_threshold=existing.high_volume_threshold,
                        support_level=existing.support_level,
                        resistance_level=existing.resistance_level,
                        last_calibrated=str(existing.last_calibrated) if existing.last_calibrated else None
                    )
                )

            # Perform calibration
            profile = calibrator.calibrate_stock(ticker, session)

            return CalibrationResponse(
                ticker=ticker,
                status="success",
                message="Stock parameters calibrated successfully",
                profile=ProfileResponse(
                    ticker=profile.ticker,
                    rsi_overbought=profile.rsi_overbought,
                    rsi_oversold=profile.rsi_oversold,
                    volatility_category=profile.volatility_category,
                    typical_volume=profile.typical_volume,
                    high_volume_threshold=profile.high_volume_threshold,
                    support_level=profile.support_level,
                    resistance_level=profile.resistance_level,
                    last_calibrated=str(profile.last_calibrated) if profile.last_calibrated else None
                )
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/calibrate/{ticker}/profile", response_model=ProfileResponse)
async def get_stock_profile(ticker: str):
    """Get stock profile parameters"""
    try:
        with get_db_context() as session:
            profile = session.query(StockProfile).filter_by(ticker=ticker).first()

            if not profile:
                raise HTTPException(
                    status_code=404,
                    detail=f"No profile found for ticker {ticker}. Run calibration first."
                )

            return ProfileResponse(
                ticker=profile.ticker,
                rsi_overbought=profile.rsi_overbought,
                rsi_oversold=profile.rsi_oversold,
                volatility_category=profile.volatility_category,
                typical_volume=profile.typical_volume,
                high_volume_threshold=profile.high_volume_threshold,
                support_level=profile.support_level,
                resistance_level=profile.resistance_level,
                last_calibrated=str(profile.last_calibrated) if profile.last_calibrated else None
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/calibrate/{ticker}/profile")
async def update_stock_profile(
    ticker: str,
    rsi_overbought: Optional[float] = None,
    rsi_oversold: Optional[float] = None,
    volatility_category: Optional[str] = None,
    typical_volume: Optional[float] = None,
    high_volume_threshold: Optional[float] = None,
    support_level: Optional[float] = None,
    resistance_level: Optional[float] = None
):
    """Manually update stock profile parameters"""
    try:
        with get_db_context() as session:
            profile = session.query(StockProfile).filter_by(ticker=ticker).first()

            if not profile:
                raise HTTPException(
                    status_code=404,
                    detail=f"No profile found for ticker {ticker}. Run calibration first."
                )

            # Update provided parameters
            if rsi_overbought is not None:
                profile.rsi_overbought = rsi_overbought
            if rsi_oversold is not None:
                profile.rsi_oversold = rsi_oversold
            if volatility_category is not None:
                profile.volatility_category = volatility_category
            if typical_volume is not None:
                profile.typical_volume = typical_volume
            if high_volume_threshold is not None:
                profile.high_volume_threshold = high_volume_threshold
            if support_level is not None:
                profile.support_level = support_level
            if resistance_level is not None:
                profile.resistance_level = resistance_level

            session.commit()
            session.refresh(profile)

            return ProfileResponse(
                ticker=profile.ticker,
                rsi_overbought=profile.rsi_overbought,
                rsi_oversold=profile.rsi_oversold,
                volatility_category=profile.volatility_category,
                typical_volume=profile.typical_volume,
                high_volume_threshold=profile.high_volume_threshold,
                support_level=profile.support_level,
                resistance_level=profile.resistance_level,
                last_calibrated=str(profile.last_calibrated) if profile.last_calibrated else None
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/calibrate/batch")
async def calibrate_batch(tickers: list[str], force: bool = False):
    """Calibrate multiple stocks in batch"""
    try:
        calibrator = StockCalibrator()
        results = []

        with get_db_context() as session:
            for ticker in tickers:
                try:
                    # Check if already calibrated
                    existing = session.query(StockProfile).filter_by(ticker=ticker).first()

                    if existing and not force:
                        results.append({
                            "ticker": ticker,
                            "status": "skipped",
                            "message": "Already calibrated"
                        })
                        continue

                    # Perform calibration
                    profile = calibrator.calibrate_stock(ticker, session)
                    results.append({
                        "ticker": ticker,
                        "status": "success",
                        "message": "Calibrated successfully"
                    })
                except Exception as e:
                    results.append({
                        "ticker": ticker,
                        "status": "error",
                        "message": str(e)
                    })

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "5003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
