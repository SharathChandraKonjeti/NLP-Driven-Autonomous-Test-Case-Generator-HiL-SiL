from src.chaining.chaining_engine import ChainingEngine

engine = ChainingEngine()

test1 = [
    {"SET_SPEED": {"value": 0}},
    {"SET_SPEED": {"value": 80}},
    {"ACC_ON": {}},
]

test2 = [
    {"SET_SPEED": {"value": 50}},
    {"LANE_CHANGE_LEFT": {}},
    {"APPLY_BRAKE": {}},
]

test3 = [
    {"SET_SPEED": {"value": 100}},
    {"LANE_CHANGE_RIGHT": {}},
]

chained = engine.chain_tests([test1, test2, test3])

print("CHAINED SEQUENCE:")
for s in chained:
    print(s)
