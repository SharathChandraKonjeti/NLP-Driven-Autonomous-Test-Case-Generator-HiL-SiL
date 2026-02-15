from src.optimizer.redundancy_optimizer import RedundancyOptimizer

steps = [
    {"SET_SPEED": {"value": 0}},
    {"SET_SPEED": {"value": 80}},
    {"ACC_ON": {}},
    {"SET_SPEED": {"value": 50}},
    {"ACC_OFF": {}},
    {"SET_SPEED": {"value": 50}},  # duplicate
    {"LANE_CHANGE_LEFT": {}},
    {"APPLY_BRAKE": {}},
    {"SET_SPEED": {"value": 100}},
    {"SET_SPEED": {"value": 100}},  # duplicate
    {"LANE_CHANGE_RIGHT": {}},
]

opt = RedundancyOptimizer()
clean = opt.optimize(steps)

print("OPTIMIZED SEQUENCE:")
for s in clean:
    print(s)
