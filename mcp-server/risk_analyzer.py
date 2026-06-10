import csv
import json
from pathlib import Path
from typing import Any, Dict, List


DATASET_PATH = Path("/home/site/wwwroot/datasets/risk_data.csv")


def get_overall_risk_rating(overall_risk_score: float) -> str:
	"""Map numeric risk score to a business-friendly rating."""
	if overall_risk_score >= 70:
		return "High"
	if overall_risk_score >= 40:
		return "Medium"
	return "Low"


def load_risk_data(file_path: Path = DATASET_PATH) -> List[Dict[str, str]]:
	"""Load cloud risk data from CSV and return rows as dictionaries."""
	with file_path.open("r", encoding="utf-8", newline="") as csv_file:
		reader = csv.DictReader(csv_file)
		return list(reader)


def analyze_risks(risk_data: List[Dict[str, str]]) -> Dict[str, Any]:
	"""Analyze risks per resource and compute overall risk metrics."""
	findings: List[Dict[str, Any]] = []
	high_risk_count = 0
	medium_risk_count = 0

	for row in risk_data:
		resource_name = row["resource_name"]
		resource_findings: List[Dict[str, Any]] = []

		backup_enabled = row["backup_enabled"].strip().lower()
		storage_utilization = float(row["storage_utilization"])
		public_endpoint = row["public_endpoint"].strip().lower()

		if backup_enabled == "no":
			resource_findings.append(
				{
					"resource_name": resource_name,
					"risk_level": "High",
					"rule": "backup_enabled = no",
					"message": "Backups are disabled.",
				}
			)
			high_risk_count += 1

		if storage_utilization > 85:
			resource_findings.append(
				{
					"resource_name": resource_name,
					"risk_level": "Medium",
					"rule": "storage_utilization > 85",
					"message": "Storage utilization is above recommended threshold.",
				}
			)
			medium_risk_count += 1

		if public_endpoint == "yes":
			resource_findings.append(
				{
					"resource_name": resource_name,
					"risk_level": "High",
					"rule": "public_endpoint = yes",
					"message": "Resource is exposed via a public endpoint.",
				}
			)
			high_risk_count += 1

		findings.extend(resource_findings)

	total_resources = len(risk_data)
	max_possible_score = max(total_resources * 100, 1)

	# High risk contributes 30 points and medium risk contributes 15 points per finding.
	raw_risk_score = (high_risk_count * 30) + (medium_risk_count * 15)
	overall_risk_score = min(round((raw_risk_score / max_possible_score) * 100, 2), 100.0)

	return {
		"findings": findings,
		"high_risk_count": high_risk_count,
		"medium_risk_count": medium_risk_count,
		"overall_risk_score": overall_risk_score,
	}


def generate_recommendations(findings: List[Dict[str, Any]]) -> List[Dict[str, str]]:
	"""Generate remediation recommendations from findings."""
	recommendations: List[Dict[str, str]] = []
	seen = set()

	for finding in findings:
		resource_name = finding["resource_name"]
		rule = finding["rule"]
		key = (resource_name, rule)

		if key in seen:
			continue
		seen.add(key)

		if rule == "backup_enabled = no":
			action = "Enable automated backups and validate restore policies."
		elif rule == "storage_utilization > 85":
			action = "Increase storage capacity or implement data lifecycle cleanup."
		elif rule == "public_endpoint = yes":
			action = "Restrict public access using private endpoints and firewall rules."
		else:
			action = "Review resource configuration and apply security best practices."

		recommendations.append(
			{
				"resource_name": resource_name,
				"risk_level": finding["risk_level"],
				"issue": rule,
				"recommendation": action,
			}
		)

	return recommendations


def generate_executive_summary(
	total_resources: int,
	high_risk_count: int,
	medium_risk_count: int,
	overall_risk_score: float,
) -> Dict[str, Any]:
	"""Build executive-level risk summary metrics."""
	overall_risk_rating = get_overall_risk_rating(overall_risk_score)

	return {
		"total_resources_analyzed": total_resources,
		"total_high_risk_findings": high_risk_count,
		"total_medium_risk_findings": medium_risk_count,
		"overall_risk_score": overall_risk_score,
		"overall_risk_rating": overall_risk_rating,
	}


def main() -> str:
	"""Run risk analysis workflow and return JSON output."""
	risk_data = load_risk_data()
	analysis = analyze_risks(risk_data)
	recommendations = generate_recommendations(analysis["findings"])
	executive_summary = generate_executive_summary(
		total_resources=len(risk_data),
		high_risk_count=analysis["high_risk_count"],
		medium_risk_count=analysis["medium_risk_count"],
		overall_risk_score=analysis["overall_risk_score"],
	)

	result = {
		"risk_score": analysis["overall_risk_score"],
		"overall_risk_rating": get_overall_risk_rating(analysis["overall_risk_score"]),
		"findings": analysis["findings"],
		"recommendations": recommendations,
		"executive_summary": executive_summary,
	}

	return json.dumps(result, indent=2)


if __name__ == "__main__":
	print(main())
