from typing import Dict, List


class RedundancyOptimizer:
    """
    Removes redundant or unnecessary steps from the chained sequence.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def optimize(self, steps: List[Dict]) -> List[Dict]:
        optimized = []
        last_state = {
            "speed": None,
            "acc_on": None,
            "lane": None,
            "indicator": None,
        }
        last_action = None  # NEW: track last action for consecutive checks

        for step in steps:
            action, params = self._unpack(step)

            # 0. Remove consecutive APPLY_BRAKE
            if action == "APPLY_BRAKE" and last_action == "APPLY_BRAKE":
                continue

            # 1. Remove duplicate SET_SPEED
            if action == "SET_SPEED":
                speed = params.get("value")
                if last_state["speed"] == speed:
                    last_action = action
                    continue  # skip duplicate
                last_state["speed"] = speed

            # 2. Remove duplicate ACC_ON / ACC_OFF
            if action == "ACC_ON":
                if last_state["acc_on"] is True:
                    last_action = action
                    continue
                last_state["acc_on"] = True

            if action == "ACC_OFF":
                if last_state["acc_on"] is False:
                    last_action = action
                    continue
                last_state["acc_on"] = False

            # 3. Remove duplicate lane changes
            if action == "LANE_CHANGE_LEFT":
                if last_state["lane"] == "LEFT":
                    last_action = action
                    continue
                last_state["lane"] = "LEFT"

            if action == "LANE_CHANGE_RIGHT":
                if last_state["lane"] == "RIGHT":
                    last_action = action
                    continue
                last_state["lane"] = "RIGHT"

            # 4. Remove duplicate indicators
            if action == "INDICATOR_LEFT":
                if last_state["indicator"] == "LEFT":
                    last_action = action
                    continue
                last_state["indicator"] = "LEFT"

            if action == "INDICATOR_RIGHT":
                if last_state["indicator"] == "RIGHT":
                    last_action = action
                    continue
                last_state["indicator"] = "RIGHT"

            # If not skipped, keep the step
            optimized.append(step)
            last_action = action  # update last action

        return optimized

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _unpack(self, step: Dict):
        [(action, params)] = step.items()
        return action, params or {}
