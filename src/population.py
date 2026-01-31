"""
PolicyPulse - Population Generation

Synthetic citizen population generation with configurable demographics.
Reference: PRD.md Feature F1 (Population Generation Engine)

Dependencies: numpy, data_models
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.random import Generator

from src.data_models import (
    Citizen,
    CitizenState,
    CityZone,
    IncomeLevel,
    PoliticalView,
    PopulationConfig,
)


# =============================================================================
# Constants
# =============================================================================

# Profession lists by income level
# Reference: PRD.md - realistic attribute correlation
PROFESSIONS_BY_INCOME: dict[IncomeLevel, list[str]] = {
    IncomeLevel.LOW: [
        "Retail Worker",
        "Food Service Worker",
        "Warehouse Worker",
        "Janitor",
        "Home Health Aide",
        "Cashier",
        "Security Guard",
        "Farm Worker",
    ],
    IncomeLevel.MIDDLE: [
        "Teacher",
        "Nurse",
        "Accountant",
        "Sales Representative",
        "Office Manager",
        "Electrician",
        "Plumber",
        "Police Officer",
        "Firefighter",
        "IT Support",
    ],
    IncomeLevel.HIGH: [
        "Software Engineer",
        "Doctor",
        "Lawyer",
        "Executive",
        "Financial Analyst",
        "Consultant",
        "Architect",
        "Pharmacist",
        "Dentist",
        "Business Owner",
    ],
}

# Income ranges by level (annual, USD)
INCOME_RANGES: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (15_000, 35_000),
    IncomeLevel.MIDDLE: (35_000, 80_000),
    IncomeLevel.HIGH: (80_000, 250_000),
}

# Education years correlation with income (mean, std)
EDUCATION_BY_INCOME: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (11, 2),
    IncomeLevel.MIDDLE: (14, 2),
    IncomeLevel.HIGH: (18, 2),
}

# Base happiness by income level
HAPPINESS_BY_INCOME: dict[IncomeLevel, tuple[float, float]] = {
    IncomeLevel.LOW: (0.45, 0.15),
    IncomeLevel.MIDDLE: (0.60, 0.12),
    IncomeLevel.HIGH: (0.72, 0.10),
}


# =============================================================================
# Population Generation Functions
# =============================================================================

def generate_population(
    config: PopulationConfig,
    rng: "Generator",
) -> list[Citizen]:
    """
    Generate a synthetic population of citizens.
    
    Creates citizens with correlated attributes based on income level.
    
    Args:
        config: Population configuration settings
        rng: Numpy random generator for reproducibility
        
    Returns:
        List of generated Citizen objects
    """
    # TODO: Implement population generation logic
    # - Distribute citizens across income levels per config percentages
    # - Generate correlated attributes (education, profession)
    # - Assign city zones, political views, personality traits
    raise NotImplementedError("Population generation not yet implemented")


def generate_initial_states(
    citizens: list[Citizen],
    rng: "Generator",
) -> list[CitizenState]:
    """
    Generate initial states (step 0) for all citizens.
    
    Initial happiness and income are correlated with income level.
    Initial policy support is neutral (0.0) with small random variance.
    
    Args:
        citizens: List of citizens to generate states for
        rng: Numpy random generator
        
    Returns:
        List of CitizenState objects for step 0
    """
    # TODO: Implement initial state generation
    raise NotImplementedError("Initial state generation not yet implemented")


def _assign_income_level(
    index: int,
    total: int,
    config: PopulationConfig,
) -> IncomeLevel:
    """
    Determine income level for a citizen based on configured distribution.
    
    Uses index-based assignment to ensure exact percentages.
    """
    # TODO: Implement income level assignment
    raise NotImplementedError()


def _generate_citizen_attributes(
    citizen_id: int,
    income_level: IncomeLevel,
    rng: "Generator",
) -> Citizen:
    """
    Generate all attributes for a single citizen.
    
    Attributes are correlated with income level per PRD specifications.
    """
    # TODO: Implement attribute generation
    raise NotImplementedError()
