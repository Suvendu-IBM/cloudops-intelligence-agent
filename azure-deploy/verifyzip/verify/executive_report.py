import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from cost_analyzer import main as cost_analyzer_main
from risk_analyzer import main as risk_analyzer_main


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_COST_ANALYSIS_PATH = BASE_DIR / "cost_analysis_output.json"
DEFAULT_RISK_ANALYSIS_PATH = BASE_DIR / "risk_analysis_output.json"


def load_cost_analysis(file_path: Optional[Path] = None) -> Dict[str, Any]:
	"""Load cost analysis JSON from file, or generate it from the analyzer module."""
	path = file_path or DEFAULT_COST_ANALYSIS_PATH
	if path.exists():
		with path.open("r", encoding="utf-8") as input_file:
			return json.load(input_file)

	return json.loads(cost_analyzer_main())


def load_risk_analysis(file_path: Optional[Path] = None) -> Dict[str, Any]:
	"""Load risk analysis JSON from file, or generate it from the analyzer module."""
	path = file_path or DEFAULT_RISK_ANALYSIS_PATH
	if path.exists():
		with path.open("r", encoding="utf-8") as input_file:
			return json.load(input_file)

	return json.loads(risk_analyzer_main())


def calculate_cloud_health_score(high_risk_findings: int, medium_risk_findings: int) -> float:
	"""Calculate cloud health score using the required executive formula."""
	score = 100 - (high_risk_findings * 10) - (medium_risk_findings * 5)
	return max(float(score), 0.0)


def get_cloud_maturity_level(cloud_health_score: float) -> str:
	"""Map cloud health score to a cloud maturity level."""
	if cloud_health_score >= 85:
		return "Optimized"
	if cloud_health_score >= 70:
		return "Managed"
	if cloud_health_score >= 50:
		return "Developing"
	return "Initial"


def generate_executive_summary(
	cloud_health_score: float,
	cloud_maturity_level: str,
	annual_savings_opportunity: float,
	overall_risk_rating: str,
	high_risk_findings: int,
	medium_risk_findings: int,
) -> Dict[str, Any]:
	"""Build an executive summary block for leadership consumption."""
	return {
		"cloud_health_score": cloud_health_score,
		"cloud_maturity_level": cloud_maturity_level,
		"annual_savings_opportunity": annual_savings_opportunity,
		"overall_risk_rating": overall_risk_rating,
		"total_high_risk_findings": high_risk_findings,
		"total_medium_risk_findings": medium_risk_findings,
		"summary": (
			f"Cloud health score is {cloud_health_score}. "
			f"Cloud maturity level is {cloud_maturity_level}. "
			f"Estimated annual savings opportunity is {annual_savings_opportunity}. "
			f"Overall risk rating is {overall_risk_rating}."
		),
	}


def generate_report(
	cost_analysis: Dict[str, Any],
	risk_analysis: Dict[str, Any],
) -> Dict[str, Any]:
	"""Generate an executive cloud intelligence report from cost and risk analyses."""
	risk_exec = risk_analysis.get("executive_summary", {})
	high_risk_findings = int(risk_exec.get("total_high_risk_findings", 0))
	medium_risk_findings = int(risk_exec.get("total_medium_risk_findings", 0))
	cloud_health_score = calculate_cloud_health_score(high_risk_findings, medium_risk_findings)
	cloud_maturity_level = get_cloud_maturity_level(cloud_health_score)

	cost_exec = cost_analysis.get("executive_summary", {})
	cost_summary = cost_analysis.get("summary", {})
	annual_savings_opportunity = float(
		cost_exec.get(
			"total_annual_savings",
			cost_summary.get("total_estimated_annual_savings", 0.0),
		)
	)

	overall_risk_rating = str(
		risk_analysis.get("overall_risk_rating", risk_exec.get("overall_risk_rating", "Unknown"))
	)

	risk_recommendations = risk_analysis.get("recommendations", [])
	cost_recommendations = cost_analysis.get("recommendations", [])

	top_recommendations: List[Dict[str, Any]] = []
	for recommendation in risk_recommendations[:3]:
		top_recommendations.append({"category": "risk", **recommendation})
	for recommendation in cost_recommendations[:3]:
		top_recommendations.append({"category": "cost", **recommendation})

	executive_summary = generate_executive_summary(
		cloud_health_score=cloud_health_score,
		cloud_maturity_level=cloud_maturity_level,
		annual_savings_opportunity=annual_savings_opportunity,
		overall_risk_rating=overall_risk_rating,
		high_risk_findings=high_risk_findings,
		medium_risk_findings=medium_risk_findings,
	)

	return {
		"cloud_health_score": cloud_health_score,
		"cloud_maturity_level": cloud_maturity_level,
		"annual_savings_opportunity": annual_savings_opportunity,
		"overall_risk_rating": overall_risk_rating,
		"executive_summary": executive_summary,
		"top_recommendations": top_recommendations,
	}


def main() -> str:
	"""Run executive report generation and return JSON output."""
	cost_analysis = load_cost_analysis()
	risk_analysis = load_risk_analysis()
	report = generate_report(cost_analysis, risk_analysis)
	return json.dumps(report, indent=2)


if __name__ == "__main__":
	print(main())
