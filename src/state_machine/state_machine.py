# src/state_machine/state_machine.py

from typing import Dict, List, Tuple


class StateMachine:
    """
    Tracks vehicle state and validates transitions.
    """

    def __init__(self):
        self.state = {
            "speed": 0,
            "acc_on": False,
            "lane": "CENTER",
            "indicator": "OFF",
            "camera": True,
            "radar": True,
            "lidar": True,
        }

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def apply_step(self, step: Dict) -> Tuple[bool, str]:
        """
        Applies a step to the state machine.
        Returns:
            (success: bool, message: str)
        """
        action, params = self._unpack(step)

        # Validate transition
        ok, msg = self._validate_transition(action, params)
        if not ok:
            return False, msg

        # Apply transition
        self._update_state(action, params)

        return True, f"Applied {action}"

    def get_state(self) -> Dict:
        return self.state.copy()

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _unpack(self, step: Dict):
        [(action, params)] = step.items()
        return action, params or {}

    # ---------------------------------------------------------
    # TRANSITION VALIDATION
    # ---------------------------------------------------------
    def _validate_transition(self, action: str, params: Dict) -> Tuple[bool, str]:

        # 1. Speed transitions
        if action == "SET_SPEED":
            v = params.get("value")
            if v < 0:
                return False, "Speed cannot be negative"
            if v > 250:
                return False, "Speed exceeds vehicle capability"

        # 2. ACC transitions
        if action == "ACC_ON":
            if self.state["speed"] < 30:
                return False, "ACC cannot activate below 30 km/h"
            if not self.state["radar"] or not self.state["camera"]:
                return False, "ACC requires radar + camera"

        if action == "ACC_OFF":
            if not self.state["acc_on"]:
                return False, "ACC is already OFF"

        # 3. Lane changes
        if action == "LANE_CHANGE_LEFT":
            if self.state["lane"] == "LEFT":
                return False, "Already in left lane"
            if self.state["indicator"] != "LEFT":
                return False, "Left indicator must be ON before lane change"

        if action == "LANE_CHANGE_RIGHT":
            if self.state["lane"] == "RIGHT":
                return False, "Already in right lane"
            if self.state["indicator"] != "RIGHT":
                return False, "Right indicator must be ON before lane change"

        # 4. Indicators
        if action == "INDICATOR_LEFT":
            if self.state["indicator"] == "LEFT":
                return False, "Left indicator already ON"

        if action == "INDICATOR_RIGHT":
            if self.state["indicator"] == "RIGHT":
                return False, "Right indicator already ON"

        # 5. Sensors
        if action == "DISABLE_RADAR" and not self.state["radar"]:
            return False, "Radar already disabled"

        if action == "DISABLE_CAMERA" and not self.state["camera"]:
            return False, "Camera already disabled"

        return True, "OK"

    # ---------------------------------------------------------
    # STATE UPDATE
    # ---------------------------------------------------------
    def _update_state(self, action: str, params: Dict):

        if action == "SET_SPEED":
            self.state["speed"] = params.get("value")

        if action == "ACC_ON":
            self.state["acc_on"] = True

        if action == "ACC_OFF":
            self.state["acc_on"] = False

        if action == "INDICATOR_LEFT":
            self.state["indicator"] = "LEFT"

        if action == "INDICATOR_RIGHT":
            self.state["indicator"] = "RIGHT"

        if action == "LANE_CHANGE_LEFT":
            self.state["lane"] = "LEFT"

        if action == "LANE_CHANGE_RIGHT":
            self.state["lane"] = "RIGHT"

        if action == "DISABLE_RADAR":
            self.state["radar"] = False

        if action == "DISABLE_CAMERA":
            self.state["camera"] = False

        if action == "DISABLE_LIDAR":
            self.state["lidar"] = False
