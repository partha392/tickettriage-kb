"""
FastAPI wrapper for TicketTriage+KB Multi-Agent System
Production-ready REST API with error handling, retries, and monitoring
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
import time
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.triage_agent import triage_agent
from core.memory import memory_bank

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TicketTriage+KB API",
    description="Enterprise-grade multi-agent customer support system",
    version="1.0.0"
)

# Request/Response models
class TicketRequest(BaseModel):
    id: str = Field(..., description="Unique ticket identifier")
    description: str = Field(..., description="Ticket description/content")
    user_id: Optional[str] = Field(None, description="Customer user ID")
    priority: Optional[str] = Field(None, description="Initial priority hint")

class TicketResponse(BaseModel):
    ok: bool
    ticket_id: str
    status: str
    reply: str
    processing_time_ms: float
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float

# Metrics
start_time = time.time()
request_count = 0
error_count = 0

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    global request_count
    request_count += 1
    
    start = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        logger.info(f"Response: {response.status_code} ({duration:.2f}ms)")
        return response
    except Exception as e:
        global error_count
        error_count += 1
        logger.error(f"Request failed: {str(e)}")
        raise

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "service": "TicketTriage+KB API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime_seconds=time.time() - start_time
    )

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint"""
    return {
        "requests_total": request_count,
        "errors_total": error_count,
        "uptime_seconds": time.time() - start_time,
        "tickets_processed": len(memory_bank.data.get("tickets", [])),
        "tickets_escalated": sum(1 for t in memory_bank.data.get("tickets", []) if t.get("escalated", False))
    }

@app.post("/process", response_model=TicketResponse)
async def process_ticket(ticket: TicketRequest):
    """
    Process a customer support ticket
    
    Returns classification, KB search results, and AI-generated response or escalation
    """
    start = time.time()
    
    try:
        logger.info(f"Processing ticket {ticket.id}")
        
        # Build ticket dict
        ticket_data = {
            "id": ticket.id,
            "description": ticket.description,
            "user_id": ticket.user_id or "unknown"
        }
        
        # Process with triage agent
        result = triage_agent.process_ticket(ticket_data)
        
        processing_time = (time.time() - start) * 1000
        
        logger.info(f"Ticket {ticket.id} processed: {result.get('status')} ({processing_time:.2f}ms)")
        
        return TicketResponse(
            ok=True,
            ticket_id=ticket.id,
            status=result.get("status", "unknown"),
            reply=result.get("reply", ""),
            processing_time_ms=processing_time,
            metadata={
                "category": result.get("category"),
                "severity": result.get("severity")
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing ticket {ticket.id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process ticket: {str(e)}"
        )

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Retrieve a processed ticket by ID"""
    ticket = memory_bank.get_ticket(ticket_id)
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {"ok": True, "ticket": ticket}

@app.get("/tickets")
async def list_tickets(limit: int = 10, category: Optional[str] = None):
    """List processed tickets"""
    tickets = memory_bank.data.get("tickets", [])
    
    if category:
        tickets = [t for t in tickets if t.get("category") == category]
    
    return {
        "ok": True,
        "total": len(tickets),
        "tickets": tickets[-limit:]
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"ok": False, "error": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
