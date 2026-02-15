# src/reporting/test_reporting.py

from src.reporting.reporting_engine import ReportingEngine

steps = [
    {"SET_SPEED": {"value": 0}},
    {"SET_SPEED": {"value": 80}},
    {"ACC_ON": {}},
    {"INDICATOR_LEFT": {}},
    {"LANE_CHANGE_LEFT": {}},
    {"APPLY_BRAKE": {}},
]

issues = [
    {"type": "warning", "message": "LANE_CHANGE_LEFT while ACC was recently ON."},
]

engine = ReportingEngine()
report = engine.build_report(steps=steps, issues=issues, state_trace=None)

print(report["text_report"])
