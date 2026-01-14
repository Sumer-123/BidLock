from fastapi import FastAPI
from ingestion.routes import bids

app = FastAPI(title="BidLock Ingestion Engine")

# Include the routes
app.include_router(bids.router, prefix="/api/v1", tags=["bids"])

@app.get("/")
def health_check():
    return {"status": "active", "service": "BidLock Ingestion"}