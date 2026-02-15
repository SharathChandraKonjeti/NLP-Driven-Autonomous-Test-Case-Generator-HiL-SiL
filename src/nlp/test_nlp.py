from src.nlp.nlp_processor import NLPProcessor

nlp = NLPProcessor()

tests = [
    # Basic
    "Start at 0, accelerate to 80, enable ACC, then change to the left lane and brake.",
    "Begin at 20, speed up to 60, move to the right lane, then slow down to 30 and stop.",
    "Drive at 50, engage ACC, shift to left lane, then disengage ACC and come to a halt.",
    "Start at 0 and reach 100 km/h, then hit the brakes.",
    "Accelerate to 40, lane change right, then apply brake.",
    # Additional tests
    "Start at 10 and increase speed to 90.",
    "Go to speed 70 and then slow down to 20.",
    "Move to the left lane and then move back to the right lane.",
    "Enable ACC, accelerate to 120, then disable ACC.",
    "Start at 0, accelerate to 30, accelerate to 60, accelerate to 90.",
    "Decelerate to 40 and then brake.",
    "Shift to the right lane and stop.",
    "Reach 50 mph and maintain speed.",
    "Start at 0, go to 50, then go to 100, then brake hard.",
]

for t in tests:
    print("\nINPUT:", t)
    print("OUTPUT:", nlp.process_text(t))
