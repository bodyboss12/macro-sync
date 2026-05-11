# macro-sync

> Aggregate nutrition data from MyFitnessPal and Cronometer into a unified schema.

[![PyPI version](https://badge.fury.io/py/macro-sync.svg)](https://badge.fury.io/py/macro-sync)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

**macro-sync** is a Python library that pulls nutrition data from MyFitnessPal and Cronometer and normalizes it into a single, consistent schema — making it easy to analyze, compare, or store your nutrition logs regardless of which app you use.

---

## Installation

```bash
pip install macro-sync
```

---

## Usage

```python
from macro_sync import MacroSync

client = MacroSync(
    myfitnesspal_credentials={"username": "user", "password": "pass"},
    cronometer_credentials={"email": "user@example.com", "password": "pass"},
)

# Fetch and unify nutrition logs for a date range
logs = client.fetch(start_date="2024-01-01", end_date="2024-01-07")

for entry in logs:
    print(entry.date, entry.source, entry.calories, entry.protein, entry.carbs, entry.fat)
```

### Unified Schema

Each returned `NutritionEntry` object contains:

| Field       | Type    | Description                        |
|-------------|---------|------------------------------------|
| `date`      | `str`   | ISO 8601 date string               |
| `source`    | `str`   | `"myfitnesspal"` or `"cronometer"` |
| `calories`  | `float` | Total calories (kcal)              |
| `protein`   | `float` | Protein (g)                        |
| `carbs`     | `float` | Carbohydrates (g)                  |
| `fat`       | `float` | Fat (g)                            |

---

## Requirements

- Python 3.8+
- Valid credentials for MyFitnessPal and/or Cronometer

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss any significant changes.

---

## License

This project is licensed under the [MIT License](LICENSE).