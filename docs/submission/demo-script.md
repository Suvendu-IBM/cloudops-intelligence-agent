# CloudOps Intelligence Copilot Demo Script

## Duration

Approximately 2 minutes

---

## Introduction (15 Seconds)

Hello, my name is Suvendu Panda.

This is CloudOps Intelligence Copilot, an Enterprise Agent built for Microsoft 365 Copilot using Declarative Agents and a custom Azure-hosted MCP server.

The solution helps organizations analyze cloud costs, identify risks, and generate executive governance reports across Azure, AWS, and GCP using natural language.

---

## Architecture Overview (20 Seconds)

The user interacts with Microsoft 365 Copilot.

A Declarative Agent invokes a Remote MCP Action.

The action calls a FastMCP server hosted on Azure App Service.

The server executes cloud intelligence tools and returns structured recommendations back to Copilot.

---

## Scenario 1 – Cost Optimization (25 Seconds)

Prompt:

Analyze cloud cost optimization opportunities.

Show:

* Cost analysis response
* Optimization recommendations
* Savings opportunities

Explain:

The MCP server executes the analyze_cost tool and returns structured FinOps recommendations.

---

## Scenario 2 – Risk Analysis (25 Seconds)

Prompt:

Analyze operational and security risks across our cloud estate.

Show:

* Risk findings
* Severity indicators
* Remediation recommendations

Explain:

The analyze_risk MCP tool identifies governance and operational concerns and prioritizes remediation actions.

---

## Scenario 3 – Executive Governance Reporting (25 Seconds)

Prompt:

Generate an executive cloud governance report.

Show:

* Executive summary
* Strategic recommendations
* Governance insights

Explain:

The generate_executive_report tool converts technical findings into leadership-ready intelligence.

---

## MCP Execution Evidence (15 Seconds)

Show Azure App Service logs.

Highlight:

* MCP tool execution
* Request processing
* Successful completion

Explain:

This demonstrates that responses are generated through actual MCP tool execution rather than generic LLM reasoning.

---

## Closing (15 Seconds)

CloudOps Intelligence Copilot combines Microsoft 365 Copilot, Declarative Agents, Azure App Service, and MCP to deliver enterprise-grade cloud governance intelligence.

Thank you for reviewing our submission.
