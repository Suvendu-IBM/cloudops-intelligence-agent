import csv
import json
from pathlib import Path
from typing import Any, Dict, List


DATASET_PATH = Path(__file__).resolve().parents[1] / "datasets" / "azure_cost.csv"


def get_optimization_priority(cpu_utilization: float) -> str:
	"""Return optimization priority based on CPU utilization thresholds."""
	if cpu_utilization <= 5:
		return "P1"
	if cpu_utilization <= 6:
		return "P2"
	return "P3"


def get_cloud_recommendation(cloud: str) -> str:
	"""Return provider-specific cost optimization guidance."""
	provider = cloud.strip().lower()

	if provider == "azure":
		return "Use Azure Advisor rightsizing recommendations."
	if provider == "aws":
		return "Use AWS Savings Plans or Reserved Instances."
	if provider == "gcp":
		return "Use GCP Committed Use Discounts."

	return "Review rightsizing and commitment discount options for this provider."


def load_cost_data(file_path: Path = DATASET_PATH) -> List[Dict[str, str]]:
	"""Load cloud cost data from CSV and return rows as dictionaries."""
	with file_path.open("r", encoding="utf-8", newline="") as csv_file:
		reader = csv.DictReader(csv_file)
		return list(reader)


def find_underutilized_resources(cost_data: List[Dict[str, str]]) -> List[Dict[str, float]]:
	"""Return resources with CPU utilization below 10%."""
	underutilized = []

	for row in cost_data:
		cpu_utilization = float(row["cpu_utilization"])
		if cpu_utilization < 10:
			cloud = row.get("cloud", "Unknown")
			monthly_cost = float(row["monthly_cost"])
			estimated_savings = round(monthly_cost * 0.30, 2)
			annual_savings = round(estimated_savings * 12, 2)

			underutilized.append(
				{
					"resource_name": row["resource_name"],
					"cloud": cloud,
					"monthly_cost": monthly_cost,
					"cpu_utilization": cpu_utilization,
					"optimization_priority": get_optimization_priority(cpu_utilization),
					"estimated_savings": estimated_savings,
					"estimated_annual_savings": annual_savings,
				}
			)

	return underutilized


def generate_recommendations(underutilized_resources: List[Dict[str, float]]) -> List[Dict[str, Any]]:
	"""Generate optimization recommendations for underutilized resources."""
	recommendations = []

	for resource in underutilized_resources:
		cloud = str(resource.get("cloud", "Unknown"))
		recommendations.append(
			{
				"resource_name": resource["resource_name"],
				"cloud": cloud,
				"optimization_priority": resource["optimization_priority"],
				"action": get_cloud_recommendation(cloud),
				"secondary_action": "Right-size to a smaller instance or schedule shutdown during off-hours.",
				"current_monthly_cost": resource["monthly_cost"],
				"estimated_savings": resource["estimated_savings"],
				"estimated_annual_savings": resource["estimated_annual_savings"],
			}
		)

	return recommendations


def main() -> str:
	"""Run the cost analysis and return JSON output."""
	cost_data = load_cost_data()
	underutilized_resources = find_underutilized_resources(cost_data)
	recommendations = generate_recommendations(underutilized_resources)

	analysis_result = {
		"underutilized_resources": underutilized_resources,
		"recommendations": recommendations,
		"executive_summary": {
			"total_monthly_savings": round(
				sum(item["estimated_savings"] for item in underutilized_resources),
				2,
			),
			"total_annual_savings": round(
				sum(item["estimated_annual_savings"] for item in underutilized_resources),
				2,
			),
			"optimization_candidates": len(underutilized_resources),
		},
		"summary": {
			"total_underutilized_resources": len(underutilized_resources),
			"total_estimated_savings": round(
				sum(item["estimated_savings"] for item in underutilized_resources),
				2,
			),
			"total_estimated_annual_savings": round(
				sum(item["estimated_annual_savings"] for item in underutilized_resources),
				2,
			),
		},
	}

	return json.dumps(analysis_result, indent=2)


if __name__ == "__main__":
	print(main())
