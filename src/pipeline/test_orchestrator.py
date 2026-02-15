# src/pipeline/test_orchestrator.py

from src.pipeline.orchestrator import Orchestrator


def main():
    orch = Orchestrator()

    descriptions = [
        "Begin from standstill, accelerate to 60 with ACC, then maintain speed.",
        "After that, disable ACC and change to the right lane.",
        "Next, accelerate to 120 and then brake hard.",
        "Finally, change to the left lane and reduce speed to 40.",
    ]

    report = orch.process_test_descriptions(descriptions)

    # Print the final text report
    print("\n===== FINAL REPORT =====\n")
    print(report["text_report"])

    # Print steps for debugging
    print("\n===== STEPS =====\n")
    for i, step in enumerate(report["steps"], start=1):
        print(f"{i:03d}: {step}")

    # Print issues
    print("\n===== ISSUES =====\n")
    if report["issues"]:
        for issue in report["issues"]:
            print(issue)
    else:
        print("No issues detected.")


if __name__ == "__main__":
    main()
