from src.reasoner.reasoner import Reasoner

reasoner = Reasoner()

steps = [
    {"SET_SPEED": {"value": 0}},
    {"SET_SPEED": {"value": 20}},
    {"ACC_ON": {}},
    {"LANE_CHANGE_LEFT": {}},
    {"APPLY_BRAKE": {}},
    {"SET_SPEED": {"value": 200}},
]

validated, issues = reasoner.validate_and_enrich(steps)

print("VALIDATED SEQUENCE:")
for s in validated:
    print(s)

print("\nISSUES:")
for i in issues:
    print(f"[{i['type'].upper()}] {i['message']}")
