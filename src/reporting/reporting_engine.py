# src/reporting/reporting_engine.py

from typing import Any, Dict, List


class ReportingEngine:
    """
    Builds human-readable and machine-usable reports
    from the final test sequence, issues, and state trace.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def build_report(
        self,
        steps: List[Dict],  # optimized steps
        issues: List[Dict],  # warnings + errors
        state_trace: List[Dict] | None = None,
        raw_steps: List[List[Dict]] | None = None,
        validated_steps: List[List[Dict]] | None = None,
    ) -> Dict[str, Any]:
        """
        steps: final optimized sequence
        issues: list of {"type": "warning"/"error", "message": str}
        state_trace: list of state snapshots (optional)
        raw_steps: NLP output before reasoning
        validated_steps: output after Reasoner before chaining
        """

        report: Dict[str, Any] = {}

        # Summary
        report["summary"] = self._build_summary(steps, issues)

        # Steps (formatted)
        report["steps"] = self._format_steps(steps)

        # Raw + validated steps (machine readable)
        report["steps_raw"] = raw_steps or []
        report["steps_validated"] = validated_steps or []

        # Issues + state trace
        report["issues"] = issues
        report["state_trace"] = state_trace or []

        # Human-readable text report
        report["text_report"] = self._build_text_report(
            summary=report["summary"],
            steps=report["steps"],
            issues=issues,
            raw_steps=raw_steps,
            validated_steps=validated_steps,
        )

        return report

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _build_summary(self, steps: List[Dict], issues: List[Dict]) -> Dict[str, Any]:
        total_steps = len(steps)
        errors = [i for i in issues if i.get("type") == "error"]
        warnings = [i for i in issues if i.get("type") == "warning"]

        return {
            "total_steps": total_steps,
            "num_errors": len(errors),
            "num_warnings": len(warnings),
            "status": "FAILED" if errors else "OK",
        }

    def _format_steps(self, steps: List[Dict]) -> List[Dict[str, Any]]:
        formatted = []
        for idx, step in enumerate(steps, start=1):
            action, params = self._unpack(step)
            formatted.append(
                {
                    "index": idx,
                    "action": action,
                    "params": params,
                }
            )
        return formatted

    def _unpack(self, step: Dict):
        [(action, params)] = step.items()
        return action, params or {}

    # ---------------------------------------------------------
    # TEXT REPORT GENERATION
    # ---------------------------------------------------------
    def _build_text_report(
        self,
        summary: Dict[str, Any],
        steps: List[Dict[str, Any]],
        issues: List[Dict],
        raw_steps: List[List[Dict]] | None,
        validated_steps: List[List[Dict]] | None,
    ) -> str:

        lines: List[str] = []

        # Header
        lines.append("=== AUTONOMOUS VEHICLE TEST CAMPAIGN REPORT ===")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-------")
        lines.append(f"Total steps : {summary['total_steps']}")
        lines.append(f"Errors      : {summary['num_errors']}")
        lines.append(f"Warnings    : {summary['num_warnings']}")
        lines.append(f"Status      : {summary['status']}")
        lines.append("")

        # Raw NLP steps
        if raw_steps:
            lines.append("RAW NLP STEPS")
            lines.append("-------------")
            for i, test in enumerate(raw_steps, start=1):
                lines.append(f"Test {i}:")
                for step in test:
                    a, p = self._unpack(step)
                    lines.append(f"  - {a} {p}")
                lines.append("")
        else:
            lines.append("RAW NLP STEPS: Not provided")
            lines.append("")

        # Validated steps
        if validated_steps:
            lines.append("VALIDATED + ENRICHED STEPS")
            lines.append("---------------------------")
            for i, test in enumerate(validated_steps, start=1):
                lines.append(f"Test {i}:")
                for step in test:
                    a, p = self._unpack(step)
                    lines.append(f"  - {a} {p}")
                lines.append("")
        else:
            lines.append("VALIDATED STEPS: Not provided")
            lines.append("")

        # Final optimized steps
        lines.append("FINAL OPTIMIZED STEPS")
        lines.append("----------------------")
        for s in steps:
            lines.append(f"{s['index']:03d}: {s['action']} {s['params']}")
        lines.append("")

        # Issues
        lines.append("ISSUES")
        lines.append("------")
        if issues:
            for i in issues:
                lines.append(f"[{i['type'].upper()}] {i['message']}")
        else:
            lines.append("No issues detected.")
        lines.append("")

        return "\n".join(lines)
