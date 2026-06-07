import json
import logging
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from cost_analyzer import main as analyze_cost_main
from executive_report import main as generate_executive_report_main
from risk_analyzer import main as analyze_risk_main


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger("cloudops-mcp-server")


@dataclass
class ToolDefinition:
    """Defines an MCP tool and the Python handler backing it."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable[[], str]


class CloudOpsMCPServer:
    """A minimal MCP server that communicates via JSON-RPC on stdio."""

    def __init__(self) -> None:
        self.server_info = {"name": "cloudops-intelligence-mcp", "version": "1.0.0"}
        self.tools: Dict[str, ToolDefinition] = {}
        self._register_tools()

    def _register_tools(self) -> None:
        """Register MCP tools exposed to Microsoft 365 Copilot."""
        empty_schema = {"type": "object", "properties": {}, "additionalProperties": False}

        self.tools["analyze_cost"] = ToolDefinition(
            name="analyze_cost",
            description="Analyze cloud cost optimization opportunities.",
            input_schema=empty_schema,
            handler=analyze_cost_main,
        )
        self.tools["analyze_risk"] = ToolDefinition(
            name="analyze_risk",
            description="Analyze operational and security risk findings.",
            input_schema=empty_schema,
            handler=analyze_risk_main,
        )
        self.tools["generate_executive_report"] = ToolDefinition(
            name="generate_executive_report",
            description="Generate executive cloud intelligence report from cost and risk analysis.",
            input_schema=empty_schema,
            handler=generate_executive_report_main,
        )

    def _send_response(self, request_id: Any, result: Dict[str, Any]) -> None:
        payload = {"jsonrpc": "2.0", "id": request_id, "result": result}
        print(json.dumps(payload), flush=True)

    def _send_error(self, request_id: Any, code: int, message: str) -> None:
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
        print(json.dumps(payload), flush=True)

    def _list_tools(self) -> Dict[str, Any]:
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema,
                }
                for tool in self.tools.values()
            ]
        }

    def _call_tool(self, name: str, arguments: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        del arguments

        tool = self.tools.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")

        raw_output = tool.handler()
        parsed_output = json.loads(raw_output)

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(parsed_output, indent=2),
                }
            ],
            "structuredContent": parsed_output,
            "isError": False,
        }

    def handle_request(self, request: Dict[str, Any]) -> None:
        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        try:
            if method == "initialize":
                self._send_response(
                    request_id,
                    {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": self.server_info,
                        "capabilities": {"tools": {}},
                    },
                )
                return

            if method == "tools/list":
                self._send_response(request_id, self._list_tools())
                return

            if method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                self._send_response(request_id, self._call_tool(tool_name, tool_args))
                return

            if method == "notifications/initialized":
                return

            self._send_error(request_id, -32601, f"Method not found: {method}")

        except ValueError as error:
            self._send_error(request_id, -32602, str(error))
        except Exception as error:  # pylint: disable=broad-except
            LOGGER.exception("Server error while handling method '%s'", method)
            self._send_error(request_id, -32000, str(error))

    def run(self) -> None:
        """Start the MCP request loop over stdio."""
        LOGGER.info("CloudOps MCP Server started")

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                self._send_error(None, -32700, "Parse error")
                continue

            if isinstance(request, list):
                for item in request:
                    if isinstance(item, dict):
                        self.handle_request(item)
                continue

            if isinstance(request, dict):
                self.handle_request(request)


def main() -> None:
    """Startup entry point for running the CloudOps MCP server."""
    server = CloudOpsMCPServer()
    server.run()


if __name__ == "__main__":
    main()
