# speed_test_runner.py

from src.nlp.nlp_processor import NLPProcessor
from src.reasoner.reasoner import Reasoner

# ---------------------------------------------------------
# SPEED TEST CASES (increase + decrease)
# ---------------------------------------------------------
TEST_CASES = [
    "Accelerate to 100 and then reduce speed to 60.",
    "Speed up to 120, then slow down to 80.",
]


# ---------------------------------------------------------
# RUN TESTS
# ---------------------------------------------------------
def run_speed_tests():
    nlp = NLPProcessor()
    reasoner = Reasoner()

    print("\n================ SPEED TEST RUNNER ================\n")

    for idx, text in enumerate(TEST_CASES, start=1):
        print(f'\n--- Test {idx}: "{text}" ---')

        # NLP extraction
        nlp_steps = nlp.process_text(text)
        print("\nNLP Output:")
        for s in nlp_steps:
            print("  ", s)

        # Reasoner enrichment
        enriched, issues = reasoner.validate_and_enrich(nlp_steps)

        print("\nReasoner Output:")
        for s in enriched:
            print("  ", s)

        if issues:
            print("\nIssues:")
            for issue in issues:
                print("  ", issue)

        print("\n----------------------------------------------")

    print("\n================== DONE ==================\n")


if __name__ == "__main__":
    run_speed_tests()
