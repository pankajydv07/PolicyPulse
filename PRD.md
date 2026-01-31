# PolicyPulse — Product Requirements Document

**Version:** 1.0  
**Last Updated:** January 2025  
**Status:** Draft for Development

---

## 1. Executive Summary

### 1.1 One-Line Pitch

PolicyPulse is an AI-powered synthetic population simulator that enables organizations to stress-test policies, business strategies, and social initiatives against virtual citizen populations before real-world implementation.

### 1.2 Product Vision

Transform how organizations make high-stakes decisions by providing a risk-free simulation environment where the impact of policies can be observed across diverse demographic segments, tracked over time, and analyzed from multiple stakeholder perspectives—all before committing resources to implementation.

---

## 2. Problem Statement

### 2.1 The Core Problem

Organizations making significant decisions—governments implementing policies, businesses changing pricing, non-profits launching programs—currently rely on:

1. **Historical data analysis**: Limited applicability to novel situations
2. **Expert opinions**: Subjective, expensive, and often narrow in perspective
3. **Focus groups and surveys**: Slow, costly, small sample sizes, potential bias
4. **Pilot programs**: Require real implementation, risking actual harm
5. **A/B testing**: Only possible after launch, may cause irreversible damage

There is no practical way to ask "What if?" at scale before committing to a decision.

### 2.2 The Consequences

- Policies fail because planners couldn't anticipate demographic-specific reactions
- Business strategies alienate key customer segments unexpectedly
- Resources are wasted on initiatives that generate backlash
- Decision-makers operate with significant blind spots about population diversity

### 2.3 The Opportunity

Modern AI (Large Language Models) can now generate plausible, contextual human reactions. Neural networks can learn from these AI-generated samples to scale predictions to massive populations. This creates an opportunity to build a practical simulation tool that was previously impossible.

---

## 3. Target Users

### 3.1 Primary Users

| User Type | Description | Key Needs |
|-----------|-------------|-----------|
| **Policy Analysts** | Government or think-tank researchers evaluating proposed regulations | Demographic breakdowns, inequality metrics, multi-step impact |
| **Business Strategists** | Product managers, pricing analysts testing market decisions | Customer segment reactions, sentiment tracking |
| **Social Researchers** | Academics studying behavioral economics, social dynamics | Reproducible simulations, exportable data |

### 3.2 Secondary Users

| User Type | Description | Key Needs |
|-----------|-------------|-----------|
| **Non-Profit Program Designers** | Organizations planning community interventions | Impact on vulnerable populations, resource allocation insights |
| **Educators** | Instructors teaching policy analysis or social science | Demonstration tool, student experimentation |
| **Innovation Teams** | Corporate R&D testing new concepts | Rapid iteration, scenario comparison |

### 3.3 User Personas

#### Persona 1: Maya — Policy Analyst
- **Role:** Senior analyst at a state transportation department
- **Goal:** Evaluate public reaction to proposed congestion pricing before City Council vote
- **Pain Point:** Current methods only capture vocal opposition; needs to understand silent majority
- **Success:** Simulation reveals low-income commuters are disproportionately impacted, leading to equity adjustments in policy

#### Persona 2: David — Product Strategist
- **Role:** Pricing manager at a subscription software company
- **Goal:** Test customer reaction to 20% price increase across different segments
- **Pain Point:** Last price increase caused unexpected churn in enterprise segment
- **Success:** Simulation identifies which customer profiles are price-sensitive, enabling targeted retention strategies

#### Persona 3: Dr. Chen — Academic Researcher
- **Role:** Professor of behavioral economics
- **Goal:** Run controlled experiments on policy interventions for publication
- **Pain Point:** IRB approval and participant recruitment are slow and expensive
- **Success:** Rapid hypothesis testing with synthetic populations, publishable methodology

---

## 4. Use Cases

### 4.1 Core Use Cases (MVP)

| ID | Use Case | Description |
|----|----------|-------------|
| UC-1 | **Policy Impact Simulation** | User defines a policy, simulates population reaction over time steps, views aggregated outcomes |
| UC-2 | **Demographic Analysis** | User examines how different segments (income, location, political view) react differently |
| UC-3 | **Scenario Comparison** | User runs multiple simulations with different policies and compares outcomes side-by-side |
| UC-4 | **Individual Citizen Exploration** | User drills into specific synthetic citizen profiles to understand micro-level reactions |
| UC-5 | **Expert Perspective Generation** | System generates AI-authored analysis from economist, activist, and business perspectives |

### 4.2 Extended Use Cases (Post-MVP)

| ID | Use Case | Description |
|----|----------|-------------|
| UC-6 | **Time-Varying Policies** | Simulate policies that change over time (phased rollout, sunset provisions) |
| UC-7 | **Social Network Effects** | Citizens influence each other's opinions based on connections |
| UC-8 | **Multi-Policy Interaction** | Simulate multiple concurrent policies and their interaction effects |
| UC-9 | **Custom Population Import** | Upload demographic data to create populations matching specific regions |
| UC-10 | **Report Generation** | Export professional PDF reports summarizing simulation findings |

---

## 5. Core Features

### 5.1 MVP Features (v1.0)

#### F1: Population Generation Engine
- Generate synthetic populations of 100 to 50,000 citizens
- Configurable income distribution (low/middle/high percentages)
- Realistic attribute correlation (education correlates with income)
- Reproducible generation with random seed support
- Attributes: age, gender, location, income, education, profession, family size, political view, personality traits

#### F2: Policy Definition Interface
- Preset policy templates for quick starts (economic, education, social, business)
- Custom policy creation with title, description, and domain classification
- Domain categories: Economy, Education, Social, Business/Startup
- Clear policy scope documentation

#### F3: Hybrid AI Simulation Engine
- Three simulation modes:
  - **Precision Mode**: LLM-powered reactions for maximum nuance (slower, API-dependent)
  - **Balanced Mode**: Hybrid LLM sampling + neural network scaling
  - **Speed Mode**: Trained neural network only (fast, no API required)
- Automatic fallback: LLM → Neural Network → Rule-based
- Multi-step simulation (1-10 time steps)
- Training data collection from LLM outputs

#### F4: Neural Network Training System
- Collect labeled samples from LLM during simulations
- Train neural network to approximate LLM behavior
- Persist trained models for reuse across sessions
- Display training progress and model accuracy metrics

#### F5: Analytics Dashboard
- Time-series visualization of key metrics (happiness, policy support, income)
- Demographic breakdown charts (by income level, by location)
- Inequality gap tracking (high vs. low income groups)
- Interactive step selection to explore evolution over time

#### F6: Citizen Browser
- Searchable, filterable list of individual citizens
- Detailed citizen profile view with all attributes
- Individual timeline showing metric changes across steps
- AI-generated "diary entries" explaining citizen's perspective (LLM mode)

#### F7: Expert Perspectives
- AI-generated analysis from three viewpoints:
  - Economist (fiscal impact, market effects, efficiency)
  - Social Activist (equity, vulnerable populations, justice)
  - Business Owner (market opportunities, operational impacts)
- Grounded in actual simulation metrics

#### F8: Scenario Management
- Store multiple simulation runs in session
- Compare any two scenarios side-by-side
- Visual overlay of metrics across scenarios

### 5.2 Post-MVP Features (v1.x+)

#### F9: Data Export
- Export simulation results to CSV
- Export population data for external analysis
- Export training dataset for model portability

#### F10: Custom Citizen Templates
- Create citizen archetypes for targeted testing
- Clone and modify existing citizens

#### F11: Geographic Visualization
- Map-based view of city zones
- Heatmaps of sentiment by location

#### F12: Collaborative Scenarios
- Share simulation configurations via URL
- Compare scenarios across users

---

## 6. Non-Goals (Explicit Exclusions)

The following are explicitly NOT in scope for PolicyPulse:

| Non-Goal | Rationale |
|----------|-----------|
| **Predictive accuracy claims** | This is a thought experiment tool, not a forecasting system. We do not claim to predict real-world behavior. |
| **Real demographic data integration** | MVP uses synthetic, generated data only. No census data, no real PII. |
| **Multi-user collaboration** | MVP is single-user, session-based. No accounts, no shared workspaces. |
| **Historical validation** | We do not validate against past policy outcomes. That would require research-grade datasets. |
| **Regulatory compliance** | No GDPR/HIPAA scope since no real user data is stored. |
| **Mobile optimization** | Desktop-first experience. Responsive is nice-to-have, not required. |
| **Real-time updates** | Simulations run to completion, then display results. No streaming mid-simulation. |
| **Custom LLM fine-tuning** | Use general-purpose LLM. Domain-specific fine-tuning is out of scope. |

---

## 7. Constraints & Assumptions

### 7.1 Technical Constraints

| Constraint | Impact |
|------------|--------|
| **LLM API rate limits** | Free tier: 15 requests/min, 200/day. Shapes simulation size and speed. |
| **Browser-based execution** | All computation happens client-side or on Streamlit server. No dedicated backend. |
| **Session-based persistence** | Data lives in memory during session. Model files persist to local storage. |
| **Single-threaded simulation** | Python GIL limits true parallelism. Async helps but doesn't fully parallelize. |

### 7.2 Assumptions

| Assumption | If Invalid... |
|------------|---------------|
| LLM can generate plausible citizen reactions | Core value prop fails; would need custom fine-tuned model |
| Neural network can learn LLM patterns | Hybrid architecture fails; would fall back to pure rule-based |
| Users understand this is simulation, not prediction | Ethical/liability concerns; must reinforce disclaimers |
| 50,000 citizens is sufficient scale for insights | May need distributed computing for larger simulations |
| Policy domains (Economy, Education, Social, Business) cover use cases | May need to add domains (Healthcare, Environment, Technology) |

### 7.3 Dependencies

| Dependency | Risk Level | Mitigation |
|------------|------------|------------|
| Google Gemini API | Medium | Support API key rotation; implement fallback to rule-based |
| Streamlit framework | Low | Stable, well-maintained; core team is active |
| Scikit-learn | Low | Industry standard, extremely stable |

---

## 8. Success Metrics

### 8.1 Product Success Metrics

| Metric | Target (v1.0) | Measurement Method |
|--------|---------------|---------------------|
| **Simulation completion rate** | >95% of started simulations complete without error | Error logging |
| **User engagement** | Average session duration >15 minutes | Session analytics |
| **Scenario creation** | Average 3+ scenarios per session | Usage tracking |
| **Training adoption** | >50% of multi-session users train neural network | Feature usage tracking |

### 8.2 Technical Performance Metrics

| Metric | Target | Measurement Method |
|--------|--------|---------------------|
| **LLM call success rate** | >99% after retries | API logging |
| **NN inference speed** | <1ms per citizen | Timing instrumentation |
| **Population generation** | <3s for 50,000 citizens | Timing instrumentation |
| **Memory usage** | <500MB for 50,000 citizen simulation | Memory profiling |

### 8.3 Quality Metrics

| Metric | Target | Measurement Method |
|--------|--------|---------------------|
| **NN approximation quality** | MAE < 0.1 for happiness/support deltas | Training metrics |
| **UI responsiveness** | All interactions respond in <200ms | Performance testing |
| **Zero data loss** | No simulation results lost during session | Session state verification |

---

## 9. Scope Boundaries

### 9.1 In Scope for MVP

- Single-user, browser-based application
- Synthetic population generation with configurable distributions
- Three simulation modes (Precision, Balanced, Speed)
- Five policy domains (Economy, Education, Social, Business, Custom)
- Time-series analytics with demographic breakdowns
- Individual citizen exploration with AI-generated narratives
- Expert perspective generation
- Scenario comparison (two at a time)
- Local model persistence

### 9.2 Out of Scope for MVP

- User authentication and accounts
- Cloud storage of simulations
- API for external integration
- Custom LLM model training
- Real demographic data import
- Multi-user collaboration
- Mobile-optimized interface
- Automated report generation
- Real-time streaming results
- Historical validation against real policies

### 9.3 Decision Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Use Streamlit, not React | Rapid prototyping, built-in state management, easy deployment | Jan 2025 |
| Gemini over GPT-4 | Free tier available, sufficient quality for simulation | Jan 2025 |
| MLP over deep learning | Simple enough for small datasets, no GPU required | Jan 2025 |
| File-based persistence | No database setup, works with Streamlit Cloud | Jan 2025 |
| No user auth | Reduces complexity, aligns with demo/research use case | Jan 2025 |

---

## 10. Appendix

### 10.1 Glossary

| Term | Definition |
|------|------------|
| **Citizen** | A synthetic individual in the simulated population with demographic and personality attributes |
| **Citizen State** | The condition of a citizen at a specific simulation step (happiness, support, income) |
| **Policy** | A defined intervention (government policy, business decision, program) being simulated |
| **Simulation Step** | A discrete time unit in the simulation; citizens react at each step |
| **Knowledge Distillation** | Training a smaller model (NN) to approximate a larger model (LLM) |
| **Precision Mode** | Simulation mode using LLM for maximum quality (slower) |
| **Speed Mode** | Simulation mode using only trained neural network (faster) |
| **Balanced Mode** | Hybrid mode combining LLM sampling with NN scaling |

### 10.2 Related Documents

- DESIGN_DOC.md — UI/UX design system and patterns
- TECH_STACK.md — Technology and architecture decisions

---

*This PRD establishes the foundation for PolicyPulse. All implementation should align with these requirements.*