"""
MCP Server für Azure Deployment mit HTTP Transport
"""
from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Server erstellen
mcp = FastMCP("Azure MCP Demo Server")

@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
    """Addiert zwei Zahlen zusammen."""
    return a + b

@mcp.tool()
def get_weather_info(city: str = "Berlin") -> dict:
    """Gibt Wetter-Informationen für eine Stadt zurück (Demo)."""
    return {
        "city": city,
        "temperature": "22°C",
        "condition": "sonnig",
        "timestamp": "2024-01-15 14:30:00"
    }

@mcp.resource("config://server")
def get_server_config() -> dict:
    """Server-Konfigurationsinformationen."""
    return {
        "name": "Azure MCP Demo Server",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "deployed_on": "Azure App Service"
    }

# FastAPI App erstellen
app = FastAPI(title="MCP Azure Demo Server")

# CORS für Client-Verbindungen aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>MCP Server auf Azure</title></head>
        <body>
            <h1>🚀 MCP Server läuft auf Azure!</h1>
            <h2>Verfügbare Endpoints:</h2>
            <ul>
                <li><a href="/health">/health</a> - Health Check</li>
                <li><a href="/mcp">/mcp</a> - MCP HTTP Endpoint</li>
                <li><a href="/docs">/docs</a> - API Dokumentation</li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    """Health Check Endpoint für Azure."""
    return JSONResponse({
        "status": "healthy",
        "service": "mcp-server",
        "version": "1.0.0"
    })

# MCP Server in FastAPI einbinden
app.mount("/mcp", mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
