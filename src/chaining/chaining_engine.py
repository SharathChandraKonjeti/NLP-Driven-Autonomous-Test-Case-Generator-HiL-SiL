# src/chaining/chaining_engine.py

from typing import Dict, List, Tuple


class ChainingEngine:
    """
    ChainingEngine:
    - Takes multiple validated test sequences
    - Produces one continuous, coherent sequence
    - Inserts minimal transitions between tests
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def chain_tests(
        self,
        test_cases: List[List[Dict]],
    ) -> List[Dict]:
        """
        test_cases: list of test sequences
            [
              [ {"SET_SPEED": {"value": 0}}, {"SET_SPEED": {"value": 80}}, ... ],
              [ {"SET_SPEED": {"value": 50}}, {"LANE_CHANGE_LEFT": {}}, ... ],
              ...
            ]

        returns: single chained sequence (list of steps)
        """
        chained: List[Dict] = []
        current_state = {
            "speed": None,
            "acc_on": False,
            "lane": "CENTER",  # simple placeholder
        }

        for idx, case in enumerate(test_cases):
            if idx == 0:
                # First test: just append, and update state
                for step in case:
                    self._update_state(current_state, step)
                    chained.append(step)
                continue

            # For subsequent tests: insert transition if needed
            transition = self._build_transition(
                from_state=current_state,
                to_case=case,
            )
            chained.extend(transition)

            # Then append the case itself, updating state
            for step in case:
                self._update_state(current_state, step)
                chained.append(step)

        return chained

    # ---------------------------------------------------------
    # STATE TRACKING
    # ---------------------------------------------------------
    def _update_state(self, state: Dict, step: Dict):
        action, params = self._unpack(step)

        if action == "SET_SPEED":
            v = params.get("value")
            if v is not None:
                state["speed"] = v

        if action == "ACC_ON":
            state["acc_on"] = True

        if action == "ACC_OFF":
            state["acc_on"] = False

        if action == "LANE_CHANGE_LEFT":
            state["lane"] = "LEFT"

        if action == "LANE_CHANGE_RIGHT":
            state["lane"] = "RIGHT"

    def _unpack(self, step: Dict):
        [(action, params)] = step.items()
        return action, params or {}

    # ---------------------------------------------------------
    # TRANSITION LOGIC
    # ---------------------------------------------------------
    def _build_transition(
        self,
        from_state: Dict,
        to_case: List[Dict],
    ) -> List[Dict]:
        """
        Build minimal steps to move from end of previous case
        into the starting conditions of the next case.
        """
        transition: List[Dict] = []

        # Determine starting conditions of next case
        target_speed = self._get_first_speed(to_case)

        # 1) Speed alignment
        if target_speed is not None and from_state.get("speed") != target_speed:
            transition.append({"SET_SPEED": {"value": target_speed}})
            from_state["speed"] = target_speed

        # 2) ACC alignment (simple version: ensure ACC is off before new case)
        if from_state.get("acc_on"):
            transition.append({"ACC_OFF": {}})
            from_state["acc_on"] = False

        # 3) Lane alignment (optional: here we keep it simple and do nothing)

        return transition

    def _get_first_speed(self, case: List[Dict]):
        for step in case:
            action, params = self._unpack(step)
            if action == "SET_SPEED":
                return params.get("value")
        return None
