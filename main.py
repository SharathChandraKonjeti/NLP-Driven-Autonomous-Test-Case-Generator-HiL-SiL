# main.py

import argparse
import json
import os
from datetime import datetime

from src.pipeline.orchestrator import Orchestrator
from src.visualisation.visualisations import generate_all_visualisations


# ---------------------------------------------------------
# LOAD TEST CASES
# ---------------------------------------------------------
def load_test_cases(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["tests"]


# ---------------------------------------------------------
# SAVE TEXT REPORT
# ---------------------------------------------------------
def save_text_report(report_text: str, out_dir: str):
    path = os.path.join(out_dir, "report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"[OK] Saved text report → {path}")


# ---------------------------------------------------------
# SAVE JSON ARTIFACTS
# ---------------------------------------------------------
def save_json(name: str, data, out_dir: str):
    path = os.path.join(out_dir, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[OK] Saved {name} → {path}")


# ---------------------------------------------------------
# MAIN PIPELINE ENTRY POINT
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", default="data/test_cases.json", help="Path to test cases JSON"
    )
    parser.add_argument("--run_name", default=None, help="Name of the test run folder")
    args = parser.parse_args()

    # 1. Load test cases
    test_cases = load_test_cases(args.file)

    # 2. Run orchestrator
    orch = Orchestrator()
    report = orch.process_test_descriptions(test_cases)

    # 3. Prepare output directory
    if args.run_name:
        run_folder = args.run_name
    else:
        run_folder = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")

    base_dir = os.path.join("reports", run_folder)
    reports_dir = os.path.join(base_dir, "reports")

    os.makedirs(reports_dir, exist_ok=True)

    # 4. Save readable report
    save_text_report(report["text_report"], reports_dir)

    # 5. Save raw + validated + optimized steps
    save_json("steps_raw", report.get("steps_raw", []), reports_dir)
    save_json("steps_validated", report.get("steps_validated", []), reports_dir)
    save_json("steps_optimized", report.get("steps", []), reports_dir)

    # 6. Save issues
    save_json("issues", report.get("issues", []), reports_dir)

    # 7. Generate visualisations (rich colours + legends)
    generate_all_visualisations(report["steps"], reports_dir)

    print("\n[✓] All outputs generated successfully.")
    print(f"Saved in folder: {reports_dir}")


if __name__ == "__main__":
    main()
