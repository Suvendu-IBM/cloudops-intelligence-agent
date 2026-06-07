import json
import logging
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from cost_analyzer import main as analyze_cost_main
from executive_report import main as generate_executive_report_main
from risk_analyzer import main as analyze_risk_main


SERVER_NAME = "cloudops-intelligence-mcp"
SERVER_VERSION = "1.0.0"

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s - %(message)s")
LOGGER = logging.getLogger(SERVER_NAME)

mcp = FastMCP(
    name=SERVER_NAME,
    instructions=(
        "CloudOps Intelligence Agent MCP server for Microsoft 365 Copilot. "
        "Capabilities: "
        "(1) Cloud cost optimization analysis — identifies underutilized resources across Azure, AWS, and GCP and recommends rightsizing actions with savings estimates. "
        "(2) Cloud risk assessment — evaluates backup posture, storage utilization, and public endpoint exposure, producing risk findings and remediation recommendations. "
        "(3) Executive cloud governance reporting — combines cost and risk intelligence into a unified report with cloud health score, maturity level, and top recommendations. "
        "Supports multi-cloud environments: Azure, AWS, and GCP. "
        "Designed for integration with Microsoft 365 Copilot via the Model Context Protocol (MCP)."
    ),
)


@mcp.tool(description="Analyze cloud cost optimization opportunities across Azure, AWS, and GCP.")
def analyze_cost() -> Dict[str, Any]:
    """Return cost analysis with underutilized resources, recommendations, and savings."""
    LOGGER.info("Tool execution started: analyze_cost")
    try:
        result = json.loads(analyze_cost_main())
        LOGGER.info("Tool execution completed: analyze_cost")
        return result
    except Exception as error:
        LOGGER.error("Tool execution failed: analyze_cost — %s", error)
        raise


@mcp.tool(description="Analyze operational and security risk findings across cloud resources.")
def analyze_risk() -> Dict[str, Any]:
    """Return risk findings, recommendations, and executive risk summary."""
    LOGGER.info("Tool execution started: analyze_risk")
    try:
        result = json.loads(analyze_risk_main())
        LOGGER.info("Tool execution completed: analyze_risk")
        return result
    except Exception as error:
        LOGGER.error("Tool execution failed: analyze_risk — %s", error)
        raise


@mcp.tool(description="Generate executive cloud intelligence report from cost and risk analysis.")
def generate_executive_report() -> Dict[str, Any]:
    """Return executive report with cloud health score, maturity level, and top recommendations."""
    LOGGER.info("Tool execution started: generate_executive_report")
    try:
        result = json.loads(generate_executive_report_main())
        LOGGER.info("Tool execution completed: generate_executive_report")
        return result
    except Exception as error:
        LOGGER.error("Tool execution failed: generate_executive_report — %s", error)
        raise


def main() -> None:
    """Startup entry point for running the CloudOps MCP server over stdio."""
    LOGGER.info("CloudOps MCP Server starting — %s v%s", SERVER_NAME, SERVER_VERSION)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
