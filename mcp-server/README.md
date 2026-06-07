# CloudOps MCP Server (HTTP)

This server exposes FastMCP tools over Streamable HTTP at `/mcp` for Microsoft 365 Copilot MCP Actions.

## Tools

- `analyze_cost`
- `analyze_risk`
- `generate_executive_report`

## Install

```powershell
cd "C:\Use cases\cloudops-intelligence-agent\mcp-server"
python -m pip install -r requirements.txt
```

## Local run

```powershell
# Optional: override defaults
$env:HOST = "0.0.0.0"
$env:PORT = "8000"

python server.py
```

MCP endpoint:

- `http://localhost:8000/mcp`

## Local testing

1. Verify the health endpoint:

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/healthz" -Method GET
```

2. Test the MCP endpoint with MCP Inspector:

```powershell
npx -y @modelcontextprotocol/inspector
```

Then connect to `http://localhost:8000/mcp`.

Notes:

- Do not use `GET /mcp` as the primary validation check. MCP Streamable HTTP is meant to be exercised by an MCP client such as Inspector.
- The canonical FastMCP 1.25.0 Starlette pattern is `Mount("/", app=mcp.streamable_http_app())`, which exposes the MCP endpoint at `/mcp`.

## Azure App Service deployment

### App settings

Set these App Settings:

- `PORT` = `8000` (or let platform inject)
- `HOST` = `0.0.0.0`

### Startup command

Use this startup command from the repository root:

```bash
gunicorn --chdir mcp-server --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker server:app
```

This launches the ASGI app exported by `server.py`, with MCP available at `/mcp`.
