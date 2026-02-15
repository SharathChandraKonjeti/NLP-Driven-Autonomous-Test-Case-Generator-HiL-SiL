# 🚗 Autonomous Vehicle Test Case Generator (AVTC)
### Natural Language → Validated, Enriched, and Visualised Test Steps

AVTC is an end‑to‑end pipeline that converts **natural‑language driving instructions** into **validated, enriched, and visualised test steps** for autonomous vehicle testing.

It combines:

- A **hybrid NLP engine**
- A **rule‑based automotive reasoner**
- A **chaining + optimization engine**
- A **state machine**
- A **visualisation module**
- A **reporting engine**

The result is a fully automated, audit‑ready test generation system.

---

## 📦 Features

### 🧠 Hybrid NLP Engine
- Semantic similarity using SentenceTransformer  
- Rule‑based fallback for reliability  
- Multi‑action extraction per sentence  
- Robust speed extraction  
- ACC ON/OFF detection  
- Lane‑change detection  
- Clause splitting (“and”, “then”, “after that”, etc.)

### 🛡 Automotive Reasoner
- OEM‑style safety rule validation  
- ACC minimum speed enforcement  
- Brake insertion before speed reduction  
- Indicator insertion before lane changes  
- ACC_OFF before braking  
- State tracking (speed + ACC + lane)

### 🔗 Chaining + Optimization
- Merges multiple test cases  
- Removes redundant steps  
- Produces a clean, minimal sequence

### 📊 Visualisation
- Speed profile  
- ACC engagement timeline  
- Lane position timeline  
- Clean styling + legends  
- PNG export

### 📁 Reporting
- Raw NLP steps  
- Validated steps  
- Optimized steps  
- Issues (warnings + errors)  
- Markdown report  
- Visualisation images  

---

## 📁 Project Structure

```
AVTC/
│
├── main.py
├── README.md
│
├── src/
│   ├── nlp/
│   │   └── nlp_processor.py
│   ├── reasoner/
│   │   └── reasoner.py
│   ├── pipeline/
│   │   └── orchestrator.py
│   ├── optimizer/
│   │   └── redundancy_optimizer.py
│   ├── state_machine/
│   │   └── state_machine.py
│   ├── chaining/
│   │   └── chaining_engine.py
│   ├── rag/
│   │   └── rag_engine.py
│   └── visualisation/
│       └── visualisations.py
│
├── data/
│   └── test_cases.json
│
└── reports/
    └── <run_name>/
```

---

## ▶️ How to Run

### Run the full pipeline
```
python main.py --file data/test_cases.json --run_name demo_run
```

### Run with a custom test suite
```
python main.py --file tests/test_suite_50.json --run_name suite_50
```

---

## 🧪 Test Case Format

### ✔ Format A — Simple list of strings
```json
{
  "tests": [
    "Accelerate to 80.",
    "Reduce speed to 40."
  ]
}
```

### ✔ Format B — List of objects
```json
{
  "tests": [
    { "id": "t01", "description": "Accelerate to 80." },
    { "id": "t02", "description": "Reduce speed to 40." }
  ]
}
```

Your orchestrator supports both.

---

## 📘 Example (Input → Output)

### Input
```
Accelerate to 100 and then reduce speed to 60.
```

### NLP Output
```json
[
  {"SET_SPEED": {"value": 100}},
  {"SET_SPEED": {"value": 60}}
]
```

### Reasoner Output
```json
[
  {"SET_SPEED": {"value": 100}},
  {"APPLY_BRAKE": {}},
  {"SET_SPEED": {"value": 60}}
]
```

### Visualisation
- Speed rises to 100  
- Brake event  
- Speed drops to 60  

---

## 📊 Output Folder Example

```
reports/
└── suite_50/
    ├── reports/
    │   ├── report.md
    │   ├── steps_raw.json
    │   ├── steps_validated.json
    │   ├── steps_optimized.json
    │   ├── issues.json
    │   ├── speed_profile.png
    │   ├── acc_timeline.png
    │   └── lane_timeline.png
```

---

## 🛠 Development Tools

This project uses:

- **Black** — formatting  
- **isort** — import sorting  
- **Ruff** — linting  

Run all formatters:

```
python -m black .
python -m isort .
python -m ruff check . --fix
```

---

## 👤 Author

**Sharath Chandra Konjeti**  
M.Sc. Mechatronics — TH Rosenheim  
Specializing in NLP‑driven test automation for autonomous vehicles.
