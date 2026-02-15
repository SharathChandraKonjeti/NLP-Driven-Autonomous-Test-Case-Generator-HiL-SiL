# src/pipeline/orchestrator.py

from typing import Any, Dict, List

from src.chaining.chaining_engine import ChainingEngine
from src.nlp.nlp_processor import NLPProcessor
from src.optimizer.redundancy_optimizer import RedundancyOptimizer
from src.reasoner.reasoner import Reasoner
from src.reporting.reporting_engine import ReportingEngine
from src.state_machine.state_machine import StateMachine


class Orchestrator:
    """
    End-to-end pipeline:
    NLP → Reasoner → Chaining → Optimizer → StateMachine → Reporting

    Supports BOTH:
    - ["Accelerate to 80.", "Reduce speed to 40."]
    - [{"id": "t01", "description": "Accelerate to 80."}, ...]
    """

    def __init__(self):
        self.nlp = NLPProcessor()
        self.reasoner = Reasoner()
        self.chainer = ChainingEngine()
        self.optimizer = RedundancyOptimizer()
        self.state_machine = StateMachine()
        self.reporting = ReportingEngine()

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------
    def process_test_descriptions(
        self,
        descriptions: List[Any],   # Accepts strings OR dicts
    ) -> Dict[str, Any]:
        """
        descriptions: list of natural language test descriptions
        returns: full report dict
        """

        # ---------------------------------------------------------
        # 1) NLP: parse each test case (supports both formats)
        # ---------------------------------------------------------
        all_raw_steps: List[List[Dict]] = []
        test_ids: List[str] = []
        test_texts: List[str] = []

        for idx, case in enumerate(descriptions):

            # Case is a simple string
            if isinstance(case, str):
                text = case
                case_id = f"case_{idx+1}"

            # Case is a dict with description
            elif isinstance(case, dict):
                text = case.get("description", "")
                case_id = case.get("id", f"case_{idx+1}")

            else:
                raise ValueError(f"Unsupported test case format: {case}")

            test_ids.append(case_id)
            test_texts.append(text)

            steps = self.nlp.process_text(text)
            all_raw_steps.append(steps)

        # ---------------------------------------------------------
        # 2) Reasoner: validate & enrich each test
        # ---------------------------------------------------------
        all_validated: List[List[Dict]] = []
        all_issues: List[Dict] = []

        for steps in all_raw_steps:
            validated, issues = self.reasoner.validate_and_enrich(steps)
            all_validated.append(validated)
            all_issues.extend(issues)

        # ---------------------------------------------------------
        # 3) Chaining: merge all validated tests
        # ---------------------------------------------------------
        chained = self.chainer.chain_tests(all_validated)

        # ---------------------------------------------------------
        # 4) Redundancy Optimizer
        # ---------------------------------------------------------
        optimized = self.optimizer.optimize(chained)

        # ---------------------------------------------------------
        # 5) State Machine: apply steps, collect state trace
        # ---------------------------------------------------------
        state_trace = []
        for step in optimized:
            ok, msg = self.state_machine.apply_step(step)
            state = self.state_machine.get_state()
            state_trace.append(
                {
                    "step": step,
                    "ok": ok,
                    "message": msg,
                    "state": state,
                }
            )

        # ---------------------------------------------------------
        # 6) Reporting
        # ---------------------------------------------------------
        report = self.reporting.build_report(
            steps=optimized,
            issues=all_issues,
            state_trace=state_trace,
        )

        return report