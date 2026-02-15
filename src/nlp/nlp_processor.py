import re
from sentence_transformers import SentenceTransformer, util


class NLPProcessor:
    """
    Hybrid NLP engine:
    - Semantic similarity for flexible phrasing
    - Rule-based fallback for reliability
    - Multi-action extraction per sentence
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Canonical keyword actions
        self.keyword_templates = {
            "SET_SPEED": [
                "accelerate to",
                "speed up to",
                "go to speed",
                "reach speed",
                "start at",
                "begin at",
                "drive at",
                "set speed to",
                "increase speed to",
                "slow down to",
                "decelerate to",
                "reduce speed to",
                "go at",
                "move at",
                "maintain speed at",
                "keep speed at",
                "cruise at",
                "target speed of",
                "reach a speed of",
                "achieve speed of",
                "attain speed of",
                "adjust speed to",
                "change speed to",
                "lower speed to",
                "bring speed down to",
                "decrease speed to",
            ],
            "APPLY_BRAKE": [
                "brake",
                "apply brake",
                "stop",
                "slow down",
                "decelerate",
                "reduce speed",
                "apply brakes",
                "hit the brakes",
                "press the brake",
                "step on the brake",
                "come to a stop",
                "bring vehicle to a halt",
            ],
            "ACC_ON": [
                "enable acc",
                "turn on acc",
                "activate acc",
                "switch on acc",
                "engage acc",
                "start acc",
                "use acc",
                "turn acc on",
                "enable adaptive cruise control",
                "activate adaptive cruise control",
                "switch on adaptive cruise control",
                "engage adaptive cruise control",
                "start adaptive cruise control",
                "use adaptive cruise control",
                "with acc",
                "with adaptive cruise control",
                "acc enabled",
                "acc active",
                "acc engaged",
            ],
            "ACC_OFF": [
                "disable acc",
                "turn off acc",
                "deactivate acc",
                "switch off acc",
                "disengage acc",
                "stop acc",
                "turn acc off",
                "disable adaptive cruise control",
                "deactivate adaptive cruise control",
                "switch off adaptive cruise control",
                "disengage adaptive cruise control",
                "stop adaptive cruise control",
            ],
            "LANE_CHANGE_LEFT": [
                "change to left lane",
                "change to the left lane",
                "move to left lane",
                "lane change left",
                "shift to left lane",
            ],
            "LANE_CHANGE_RIGHT": [
                "change to right lane",
                "change to the right lane",
                "move to right lane",
                "lane change right",
                "shift to right lane",
            ],
        }

        # Precompute embeddings
        self.template_phrases = []
        self.template_actions = []

        for action, phrases in self.keyword_templates.items():
            for p in phrases:
                self.template_phrases.append(p)
                self.template_actions.append(action)

        self.template_embeddings = self.model.encode(
            self.template_phrases, convert_to_tensor=True
        )

    # ---------------------------------------------------------
    # PARAMETER EXTRACTION
    # ---------------------------------------------------------
    def extract_speed(self, text: str):
        t = text.lower()

        # Standstill → 0
        if any(
            phrase in t for phrase in ["standstill", "from rest", "from zero", "from 0"]
        ):
            return 0

        # Strong patterns for speed reduction
        reduction_patterns = [
            r"(?:reduce|decrease|lower|slow\s*down\s*to|bring\s*speed\s*down\s*to)\s+(\d+)",
        ]
        for pattern in reduction_patterns:
            m = re.search(pattern, t)
            if m:
                return int(m.group(1))

        # Generic numeric extraction
        match = re.search(r"(\d+)\s?(km/h|kph|kmh|mph)?", t)
        if match:
            return int(match.group(1))

        return None

    # ---------------------------------------------------------
    # SEMANTIC ACTION DETECTION
    # ---------------------------------------------------------
    def detect_action_semantic(self, text: str):
        text_emb = self.model.encode(text, convert_to_tensor=True)
        scores = util.cos_sim(text_emb, self.template_embeddings)[0]

        best_idx = int(scores.argmax())
        best_score = float(scores[best_idx])
        action_candidate = self.template_actions[best_idx]

        # Lower threshold for short actions
        if action_candidate in ["APPLY_BRAKE", "LANE_CHANGE_LEFT", "LANE_CHANGE_RIGHT"]:
            if best_score >= 0.30:
                return action_candidate

        if best_score >= 0.40:
            return action_candidate

        return None

    # ---------------------------------------------------------
    # RULE-BASED FALLBACKS
    # ---------------------------------------------------------
    def detect_action_fallback(self, text: str):
        t = text.lower()

        # Lane changes
        if "left lane" in t:
            return "LANE_CHANGE_LEFT"
        if "right lane" in t:
            return "LANE_CHANGE_RIGHT"

        # Braking
        if "brake" in t or "stop" in t or "halt" in t:
            return "APPLY_BRAKE"

        # ACC fallback
        if "with acc" in t or "acc on" in t or "acc enabled" in t or "acc active" in t:
            return "ACC_ON"

        # Standstill → SET_SPEED
        if any(
            phrase in t for phrase in ["standstill", "from rest", "from zero", "from 0"]
        ):
            return "SET_SPEED"

        # Speed
        if self.extract_speed(t) is not None:
            return "SET_SPEED"

        return None

    # ---------------------------------------------------------
    # MULTI-ACTION PARSING (FINAL FIXED VERSION)
    # ---------------------------------------------------------
    def parse_sentence(self, sentence: str):
        actions = []
        sentence = sentence.strip()
        if not sentence:
            return actions

        # Split into clauses
        clauses = re.split(
            r"\band\b|\bthen\b|\bafter that\b|\bnext\b|\bwith\b|,|;",
            sentence,
            flags=re.IGNORECASE,
        )

        for clause in clauses:
            clause = clause.strip()
            if not clause:
                continue

            # 1. Semantic detection
            action = self.detect_action_semantic(clause)

            # 2. Fallback detection
            if not action:
                action = self.detect_action_fallback(clause)

            if not action:
                continue

            # ---------------------------------------------------------
            # 3. FINAL SPEED LOGIC (NO MORE SET_SPEED(None))
            # ---------------------------------------------------------
            if action == "SET_SPEED":
                speed = self.extract_speed(clause)

                # Only add SET_SPEED if a number exists
                if speed is not None:
                    actions.append({"SET_SPEED": {"value": speed}})
                # No number → skip
                continue

            # APPLY_BRAKE logic
            if action == "APPLY_BRAKE":
                speed = self.extract_speed(clause)

                # If numeric speed exists → convert to SET_SPEED
                if speed is not None:
                    actions.append({"SET_SPEED": {"value": speed}})
                    continue

                # Otherwise → brake
                actions.append({"APPLY_BRAKE": {}})
                continue

            # 4. Normal action
            actions.append({action: {}})

        return actions

    # ---------------------------------------------------------
    # FULL TEXT PROCESSING
    # ---------------------------------------------------------
    def process_text(self, text: str):
        sentences = re.split(r"[.]", text)
        steps = []

        for s in sentences:
            parsed = self.parse_sentence(s)
            steps.extend(parsed)

        return steps