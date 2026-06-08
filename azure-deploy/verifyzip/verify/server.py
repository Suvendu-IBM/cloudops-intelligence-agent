import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from cost_analyzer import main as analyze_cost_main
from executive_report import main as generate_executive_report_main
from risk_analyzer import main as analyze_risk_main


SERVER_NAME = "cloudops-intelligence-mcp"
SERVER_VERSION = "1.0.0"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(name)s - %(message)s",
)

LOGGER = logging.getLogger(SERVER_NAME)

mcp = FastMCP(
    name=SERVER_NAME,
    stateless_http=True,
    json_response=True,

    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "cloudops-mcp-suvendu.azurewebsites.net",
            "localhost:*",
            "127.0.0.1:*",
        ],
        allowed_origins=[
            "https://cloudops-mcp-suvendu.azurewebsites.net",
            "http://localhost:*",
            "http://127.0.0.1:*",
        ],
    ),

    instructions=(
        "CloudOps Intelligence Agent MCP server for Microsoft 365 Copilot. "
        "Capabilities: "
        "(1) Cloud cost optimization analysis — identifies underutilized resources "
        "across Azure, AWS, and GCP and recommends rightsizing actions with savings estimates. "
        "(2) Cloud risk assessment — evaluates backup posture, storage utilization, "
        "and public endpoint exposure, producing risk findings and remediation recommendations. "
        "(3) Executive cloud governance reporting — combines cost and risk intelligence "
        "into a unified report with cloud health score, maturity level, and top recommendations. "
        "Supports multi-cloud environments: Azure, AWS, and GCP. "
        "Designed for integration with Microsoft 365 Copilot via the Model Context Protocol (MCP)."
    ),
)


@mcp.tool(
    description="Analyze cloud cost optimization opportunities across Azure, AWS, and GCP."
)
def analyze_cost() -> Dict[str, Any]:
    LOGGER.info("Tool execution started: analyze_cost")

    try:
        result = json.loads(analyze_cost_main())
        LOGGER.info("Tool execution completed: analyze_cost")
        return result

    except Exception:
        LOGGER.exception("Tool execution failed: analyze_cost")
        raise


@mcp.tool(
    description="Analyze operational and security risk findings across cloud resources."
)
def analyze_risk() -> Dict[str, Any]:
    LOGGER.info("Tool execution started: analyze_risk")

    try:
        result = json.loads(analyze_risk_main())
        LOGGER.info("Tool execution completed: analyze_risk")
        return result

    except Exception:
        LOGGER.exception("Tool execution failed: analyze_risk")
        raise


@mcp.tool(
    description="Generate executive cloud intelligence report from cost and risk analysis."
)
def generate_executive_report() -> Dict[str, Any]:
    LOGGER.info("Tool execution started: generate_executive_report")

    try:
        result = json.loads(generate_executive_report_main())
        LOGGER.info("Tool execution completed: generate_executive_report")
        return result

    except Exception:
        LOGGER.exception("Tool execution failed: generate_executive_report")
        raise


async def health_check(request):
    return JSONResponse(
        {
            "status": "healthy",
            "service": SERVER_NAME,
            "version": SERVER_VERSION,
        }
    )


@asynccontextmanager
async def app_lifespan(_: Starlette):
    LOGGER.info("Starting MCP session manager")

    async with mcp.session_manager.run():
        yield

    LOGGER.info("Stopping MCP session manager")


app = Starlette(
    routes=[
        Route("/healthz", health_check),

        # FastMCP internally exposes /mcp
        # Therefore mount at root.
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=app_lifespan,
)


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    LOGGER.info(
        "CloudOps MCP Server starting — %s v%s",
        SERVER_NAME,
        SERVER_VERSION,
    )

    LOGGER.info(
        "Health endpoint: http://%s:%s/healthz",
        host,
        port,
    )

    LOGGER.info(
        "MCP endpoint: http://%s:%s/mcp",
        host,
        port,
    )

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()