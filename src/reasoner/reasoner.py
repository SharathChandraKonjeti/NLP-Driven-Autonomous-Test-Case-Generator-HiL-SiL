# src/reasoner/reasoner.py

from typing import Dict, List, Tuple
from src.rag.rag_engine import RAGEngine


class Reasoner:
    """
    Hybrid Reasoner:
    - Validates NLP actions against OEM + safety rules (from RAG)
    - Inserts only necessary safety steps
    - Preserves user intent (e.g., SET_SPEED 40)
    - Avoids duplicate or unnecessary braking
    """

    def __init__(self):
        self.rag = RAGEngine()
        self.rag.build_index()

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def validate_and_enrich(self, steps: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        issues: List[Dict] = []
        enriched: List[Dict] = []

        current_speed = None
        acc_on = False

        for step in steps:
            action, params = self._unpack(step)
            previous_speed = current_speed

            # Rule checks
            step_issues = self._check_action_rules(
                action=action,
                params=params,
                current_speed=current_speed,
                acc_on=acc_on,
            )
            issues.extend(step_issues)

            # Hybrid enrichment
            enriched_steps = self._enrich_sequence(
                action=action,
                params=params,
                current_speed=current_speed,
                previous_speed=previous_speed,
                acc_on=acc_on,
            )

            # Update state
            for es in enriched_steps:
                a, p = self._unpack(es)
                if a == "ACC_ON":
                    acc_on = True
                elif a == "ACC_OFF":
                    acc_on = False
                elif a == "SET_SPEED":
                    current_speed = p.get("value")

            enriched.extend(enriched_steps)

        return enriched, issues

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _unpack(self, step: Dict):
        if not step:
            return None, {}
        [(action, params)] = step.items()
        return action, params or {}

    # ---------------------------------------------------------
    # RULE CHECKS
    # ---------------------------------------------------------
    def _check_action_rules(
        self,
        action: str,
        params: Dict,
        current_speed: int,
        acc_on: bool,
    ) -> List[Dict]:

        issues: List[Dict] = []

        # ACC minimum speed
        if action == "ACC_ON":
            if current_speed is not None and current_speed < 30:
                issues.append(
                    {
                        "type": "error",
                        "message": f"ACC_ON at {current_speed} km/h violates ACC_MIN_SPEED (>= 30 km/h).",
                    }
                )

        # Speed max limit
        if action == "SET_SPEED":
            v = params.get("value")
            if v is not None and v > 180:
                issues.append(
                    {
                        "type": "error",
                        "message": f"SET_SPEED {v} km/h violates SPEED_MAX_LIMIT (<= 180 km/h).",
                    }
                )

        # Lane change with ACC ON → warning
        if action in ["LANE_CHANGE_LEFT", "LANE_CHANGE_RIGHT"] and acc_on:
            issues.append(
                {
                    "type": "warning",
                    "message": f"{action} while ACC is ON. Check LANE_CHANGE + ACC interaction.",
                }
            )

        return issues

    # ---------------------------------------------------------
    # ENRICHMENT ENGINE (FINAL FIXED VERSION)
    # ---------------------------------------------------------
    def _enrich_sequence(
        self,
        action: str,
        params: Dict,
        current_speed: int,
        previous_speed: int,
        acc_on: bool,
    ) -> List[Dict]:

        result: List[Dict] = []

        # 1) Brake overrides ACC → insert ACC_OFF before APPLY_BRAKE
        if action == "APPLY_BRAKE" and acc_on:
            return [{"ACC_OFF": {}}, {"APPLY_BRAKE": {}}]

        # 2) Lane change → indicator only
        if action == "LANE_CHANGE_LEFT":
            return [{"INDICATOR_LEFT": {}}, {"LANE_CHANGE_LEFT": {}}]

        if action == "LANE_CHANGE_RIGHT":
            return [{"INDICATOR_RIGHT": {}}, {"LANE_CHANGE_RIGHT": {}}]

        # ---------------------------------------------------------
        # 3) SPEED LOGIC (SAFE + FINAL)
        # ---------------------------------------------------------
        if action == "SET_SPEED":
            v = params.get("value")

            # If NLP produced SET_SPEED with no value → ignore
            if v is None:
                return []

            # First speed ever → accept
            if previous_speed is None:
                return [{"SET_SPEED": {"value": v}}]

            # Speed reduction → brake + set_speed
            if v < previous_speed:
                return [{"APPLY_BRAKE": {}}, {"SET_SPEED": {"value": v}}]

            # Speed increase → just set_speed
            return [{"SET_SPEED": {"value": v}}]

        # Default: no enrichment
        return [{action: params}]