"""
PolicyPulse - Simulation Engine

Rule-based simulation engine for policy impact modeling.
Reference: PRD.md Feature F3 (Hybrid AI Simulation Engine)

This implementation provides deterministic, reproducible simulations
using rule-based logic. AI/ML integration will be added later.

Dependencies: data_models, utils
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from numpy.random import Generator

from src.data_models import (
    Citizen,
    CitizenState,
    IncomeLevel,
    Policy,
    PolicyDomain,
    PoliticalView,
    CityZone,
    PopulationConfig,
    SimulationConfig,
    SimulationResult,
    StepMetrics,
    ReactionMethod,
)
from src.stats import calculate_step_metrics
from src.utils import clamp, create_rng


# =============================================================================
# Policy Impact Rules
# =============================================================================

@dataclass(frozen=True)
class PolicyImpactRules:
    """
    Defines how a policy domain affects different demographic groups.
    
    All values are base multipliers that get adjusted by citizen attributes.
    Positive values indicate beneficial impact, negative indicate harmful.
    """
    # Base impact on happiness (before demographic adjustments)
    happiness_base: float
    
    # Impact modifiers by income level
    happiness_by_income: dict[IncomeLevel, float]
    
    # Base impact on income (percentage change)
    income_change_pct: float
    
    # Income change modifiers by income level
    income_change_by_income: dict[IncomeLevel, float]
    
    # Base policy support shift
    support_base: float
    
    # Support modifiers by political view
    support_by_politics: dict[PoliticalView, float]


# Define impact rules for each policy domain
POLICY_DOMAIN_RULES: dict[PolicyDomain, PolicyImpactRules] = {
    PolicyDomain.ECONOMY: PolicyImpactRules(
        happiness_base=0.02,
        happiness_by_income={
            IncomeLevel.LOW: -0.03,      # Economic policies often favor wealthy
            IncomeLevel.MIDDLE: 0.01,
            IncomeLevel.HIGH: 0.05,
        },
        income_change_pct=0.02,
        income_change_by_income={
            IncomeLevel.LOW: 0.005,
            IncomeLevel.MIDDLE: 0.015,
            IncomeLevel.HIGH: 0.03,
        },
        support_base=0.0,
        support_by_politics={
            PoliticalView.PROGRESSIVE: -0.05,
            PoliticalView.MODERATE: 0.02,
            PoliticalView.CONSERVATIVE: 0.08,
        },
    ),
    PolicyDomain.EDUCATION: PolicyImpactRules(
        happiness_base=0.03,
        happiness_by_income={
            IncomeLevel.LOW: 0.05,       # Education helps lower income most
            IncomeLevel.MIDDLE: 0.03,
            IncomeLevel.HIGH: 0.01,
        },
        income_change_pct=0.01,
        income_change_by_income={
            IncomeLevel.LOW: 0.02,
            IncomeLevel.MIDDLE: 0.01,
            IncomeLevel.HIGH: 0.005,
        },
        support_base=0.05,
        support_by_politics={
            PoliticalView.PROGRESSIVE: 0.10,
            PoliticalView.MODERATE: 0.05,
            PoliticalView.CONSERVATIVE: -0.02,
        },
    ),
    PolicyDomain.SOCIAL: PolicyImpactRules(
        happiness_base=0.04,
        happiness_by_income={
            IncomeLevel.LOW: 0.06,       # Social policies help vulnerable
            IncomeLevel.MIDDLE: 0.03,
            IncomeLevel.HIGH: -0.01,
        },
        income_change_pct=0.005,
        income_change_by_income={
            IncomeLevel.LOW: 0.015,
            IncomeLevel.MIDDLE: 0.005,
            IncomeLevel.HIGH: -0.005,    # May include taxes
        },
        support_base=0.03,
        support_by_politics={
            PoliticalView.PROGRESSIVE: 0.12,
            PoliticalView.MODERATE: 0.03,
            PoliticalView.CONSERVATIVE: -0.08,
        },
    ),
    PolicyDomain.BUSINESS: PolicyImpactRules(
        happiness_base=0.01,
        happiness_by_income={
            IncomeLevel.LOW: -0.02,
            IncomeLevel.MIDDLE: 0.02,
            IncomeLevel.HIGH: 0.06,      # Business policies favor wealthy
        },
        income_change_pct=0.025,
        income_change_by_income={
            IncomeLevel.LOW: 0.01,
            IncomeLevel.MIDDLE: 0.02,
            IncomeLevel.HIGH: 0.04,
        },
        support_base=-0.02,
        support_by_politics={
            PoliticalView.PROGRESSIVE: -0.10,
            PoliticalView.MODERATE: 0.0,
            PoliticalView.CONSERVATIVE: 0.10,
        },
    ),
}

# Zone-based modifiers (urban areas see faster change)
ZONE_CHANGE_MULTIPLIER: dict[CityZone, float] = {
    CityZone.DOWNTOWN: 1.3,
    CityZone.INDUSTRIAL: 1.1,
    CityZone.SUBURBAN: 1.0,
    CityZone.RURAL: 0.8,
}


# =============================================================================
# Simulation Engine
# =============================================================================

def run_simulation(
    policy: Policy,
    citizens: list[Citizen],
    initial_states: list[CitizenState],
    config: SimulationConfig,
    population_config: PopulationConfig,
    scenario_name: str,
    rng: Generator | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> SimulationResult:
    """
    Run a complete rule-based simulation.
    
    Simulates how citizens react to a policy over multiple time steps.
    Each step builds on the previous, creating a temporal evolution.
    
    Args:
        policy: The policy being simulated
        citizens: Generated population (immutable)
        initial_states: Initial citizen states (step 0)
        config: Simulation configuration
        population_config: Population configuration
        scenario_name: Name for this simulation run
        rng: Random number generator for reproducibility
        progress_callback: Optional callback(step, total) for progress updates
        
    Returns:
        Complete simulation results with metrics per step
    """
    if rng is None:
        rng = create_rng(population_config.random_seed)
    
    # Initialize storage
    states_by_step: dict[int, list[CitizenState]] = {0: initial_states}
    metrics_by_step: list[StepMetrics] = []
    method_counts: dict[int, dict[ReactionMethod, int]] = {}
    
    # Calculate initial metrics
    initial_metrics = calculate_step_metrics(citizens, initial_states, step=0)
    metrics_by_step.append(initial_metrics)
    method_counts[0] = {ReactionMethod.RULE_BASED: len(citizens)}
    
    # Create citizen lookup for efficient access
    citizen_by_id = {c.id: c for c in citizens}
    
    # Run simulation steps
    for step in range(1, config.steps + 1):
        if progress_callback:
            progress_callback(step, config.steps)
        
        # Get previous states
        previous_states = states_by_step[step - 1]
        
        # Calculate new states
        new_states = _run_step(
            citizens=citizens,
            citizen_by_id=citizen_by_id,
            previous_states=previous_states,
            policy=policy,
            step=step,
            rng=rng,
        )
        
        # Store states
        states_by_step[step] = new_states
        
        # Calculate metrics
        step_metrics = calculate_step_metrics(citizens, new_states, step)
        metrics_by_step.append(step_metrics)
        
        # Track method counts (all rule-based for now)
        method_counts[step] = {ReactionMethod.RULE_BASED: len(citizens)}
    
    return SimulationResult(
        scenario_name=scenario_name,
        policy=policy,
        config=config,
        population_config=population_config,
        citizens=citizens,
        states_by_step=states_by_step,
        metrics_by_step=metrics_by_step,
        method_counts=method_counts,
    )


def _run_step(
    citizens: list[Citizen],
    citizen_by_id: dict[int, Citizen],
    previous_states: list[CitizenState],
    policy: Policy,
    step: int,
    rng: Generator,
) -> list[CitizenState]:
    """
    Run a single simulation step for all citizens.
    
    Each citizen's new state is computed from their previous state
    and the policy's impact on their demographic profile.
    
    Args:
        citizens: All citizens (for reference)
        citizen_by_id: Lookup dict for citizens
        previous_states: States from previous step
        policy: The policy being simulated
        step: Current step number
        rng: Random number generator
        
    Returns:
        List of new CitizenState objects for this step
    """
    new_states: list[CitizenState] = []
    
    for prev_state in previous_states:
        citizen = citizen_by_id[prev_state.citizen_id]
        
        # Calculate deltas using rule-based logic
        delta_happiness, delta_support, delta_income = apply_rule_based_reaction(
            citizen=citizen,
            current_state=prev_state,
            policy=policy,
            step=step,
            rng=rng,
        )
        
        # Apply deltas to create new state (immutable pattern)
        new_happiness = clamp(prev_state.happiness + delta_happiness, 0.0, 1.0)
        new_support = clamp(prev_state.policy_support + delta_support, -1.0, 1.0)
        new_income = max(0.0, prev_state.income + delta_income)
        
        new_state = CitizenState(
            citizen_id=citizen.id,
            step=step,
            happiness=new_happiness,
            policy_support=new_support,
            income=new_income,
            reaction_method=ReactionMethod.RULE_BASED,
            diary_entry=None,
        )
        new_states.append(new_state)
    
    return new_states


def apply_rule_based_reaction(
    citizen: Citizen,
    current_state: CitizenState,
    policy: Policy,
    step: int,
    rng: Generator,
) -> tuple[float, float, float]:
    """
    Apply rule-based reaction logic to compute state deltas.
    
    Uses policy domain rules, citizen demographics, and personality
    to determine how the citizen reacts to the policy.
    
    Args:
        citizen: The citizen reacting
        current_state: Their current state
        policy: The policy being reacted to
        step: Current simulation step
        rng: Random number generator for variance
        
    Returns:
        Tuple of (delta_happiness, delta_support, delta_income)
    """
    # Get policy rules
    rules = POLICY_DOMAIN_RULES[policy.domain]
    
    # Base impacts
    happiness_delta = rules.happiness_base
    support_delta = rules.support_base
    income_delta_pct = rules.income_change_pct
    
    # Apply income level modifiers
    happiness_delta += rules.happiness_by_income[citizen.income_level]
    income_delta_pct += rules.income_change_by_income[citizen.income_level]
    
    # Apply political view modifiers
    support_delta += rules.support_by_politics[citizen.political_view]
    
    # Apply zone multiplier (urban areas change faster)
    zone_mult = ZONE_CHANGE_MULTIPLIER[citizen.city_zone]
    happiness_delta *= zone_mult
    support_delta *= zone_mult
    
    # Apply personality modifiers
    # - High openness to change amplifies positive effects
    # - High risk tolerance amplifies all effects
    openness_factor = 0.5 + citizen.openness_to_change * 0.5  # 0.5 to 1.0
    risk_factor = 0.7 + citizen.risk_tolerance * 0.6  # 0.7 to 1.3
    
    if happiness_delta > 0:
        happiness_delta *= openness_factor
    happiness_delta *= risk_factor
    support_delta *= risk_factor
    
    # Apply step decay (impact diminishes over time)
    decay_factor = 1.0 / (1.0 + step * 0.1)  # Gradual decay
    happiness_delta *= decay_factor
    support_delta *= decay_factor
    
    # Add small random variance for realism
    variance = 0.01
    happiness_delta += rng.normal(0, variance)
    support_delta += rng.normal(0, variance)
    
    # Calculate income change in dollars
    income_delta = current_state.income * income_delta_pct * decay_factor
    
    # Education slightly amplifies positive outcomes
    education_bonus = (citizen.education_years - 12) * 0.002  # +/- based on education
    if happiness_delta > 0:
        happiness_delta += education_bonus
    
    # Family size affects sensitivity (larger families more cautious)
    family_sensitivity = 1.0 - (citizen.family_size - 1) * 0.05
    family_sensitivity = max(0.7, family_sensitivity)
    happiness_delta *= family_sensitivity
    
    return happiness_delta, support_delta, income_delta


def get_simulation_summary(result: SimulationResult) -> dict:
    """
    Generate a summary of simulation results.
    
    Args:
        result: Completed simulation result
        
    Returns:
        Dictionary with summary statistics
    """
    if not result.metrics_by_step:
        return {}
    
    initial = result.metrics_by_step[0]
    final = result.metrics_by_step[-1]
    
    return {
        "scenario_name": result.scenario_name,
        "policy_title": result.policy.title,
        "policy_domain": result.policy.domain.value,
        "steps": result.config.steps,
        "population_size": len(result.citizens),
        "initial_happiness": initial.avg_happiness,
        "final_happiness": final.avg_happiness,
        "happiness_change": final.avg_happiness - initial.avg_happiness,
        "initial_support": initial.avg_support,
        "final_support": final.avg_support,
        "support_change": final.avg_support - initial.avg_support,
        "initial_income": initial.avg_income,
        "final_income": final.avg_income,
        "income_change": final.avg_income - initial.avg_income,
        "initial_gap": initial.happiness_gap,
        "final_gap": final.happiness_gap,
        "gap_change": final.happiness_gap - initial.happiness_gap,
    }
