"""Unified nutrition data schema for macro-sync."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class NutritionEntry:
    """Represents a single food entry with macro and micronutrient data."""

    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    date: date
    source: str  # 'myfitnesspal' or 'cronometer'
    serving_size: Optional[str] = None
    fiber_g: Optional[float] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    meal: Optional[str] = None  # breakfast, lunch, dinner, snack

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "calories": self.calories,
            "protein_g": self.protein_g,
            "carbs_g": self.carbs_g,
            "fat_g": self.fat_g,
            "date": self.date.isoformat(),
            "source": self.source,
            "serving_size": self.serving_size,
            "fiber_g": self.fiber_g,
            "sugar_g": self.sugar_g,
            "sodium_mg": self.sodium_mg,
            "meal": self.meal,
        }


@dataclass
class DailySummary:
    """Aggregated nutrition totals for a single day across all sources."""

    date: date
    total_calories: float = 0.0
    total_protein_g: float = 0.0
    total_carbs_g: float = 0.0
    total_fat_g: float = 0.0
    total_fiber_g: float = 0.0
    total_sugar_g: float = 0.0
    total_sodium_mg: float = 0.0
    entries: list = field(default_factory=list)

    @classmethod
    def from_entries(cls, date: date, entries: list["NutritionEntry"]) -> "DailySummary":
        summary = cls(date=date, entries=entries)
        for entry in entries:
            summary.total_calories += entry.calories
            summary.total_protein_g += entry.protein_g
            summary.total_carbs_g += entry.carbs_g
            summary.total_fat_g += entry.fat_g
            summary.total_fiber_g += entry.fiber_g or 0.0
            summary.total_sugar_g += entry.sugar_g or 0.0
            summary.total_sodium_mg += entry.sodium_mg or 0.0
        return summary

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "total_calories": round(self.total_calories, 2),
            "total_protein_g": round(self.total_protein_g, 2),
            "total_carbs_g": round(self.total_carbs_g, 2),
            "total_fat_g": round(self.total_fat_g, 2),
            "total_fiber_g": round(self.total_fiber_g, 2),
            "total_sugar_g": round(self.total_sugar_g, 2),
            "total_sodium_mg": round(self.total_sodium_mg, 2),
            "entry_count": len(self.entries),
        }
