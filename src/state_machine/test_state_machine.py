from src.state_machine.state_machine import StateMachine

sm = StateMachine()

steps = [
    {"SET_SPEED": {"value": 50}},
    {"ACC_ON": {}},
    {"INDICATOR_LEFT": {}},
    {"LANE_CHANGE_LEFT": {}},
]

for step in steps:
    ok, msg = sm.apply_step(step)
    print(step, ok, msg)

print("\nFinal State:", sm.get_state())
