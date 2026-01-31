# PolicyPulse — Design Document

**Version:** 1.0  
**Last Updated:** January 2025  
**Status:** Design Specification

---

## 1. Design Philosophy

### 1.1 Core Principles

PolicyPulse is a **professional analytical tool**, not a consumer application. The design must balance:

1. **Clarity over decoration**: Every visual element must serve a purpose
2. **Data density without overwhelm**: Show comprehensive information in digestible chunks
3. **Progressive disclosure**: Start simple, reveal complexity on demand
4. **Trust through transparency**: Make the AI's role and limitations visible
5. **Actionable insights**: Visualizations should answer questions, not just display data

### 1.2 Design Goals

| Goal | How We Achieve It |
|------|-------------------|
| **Professional credibility** | Clean typography, muted colors, precise alignment |
| **Efficient workflows** | Sidebar always visible, minimal clicks to key actions |
| **Exploration without confusion** | Clear navigation hierarchy, breadcrumb-style context |
| **Responsible AI communication** | Prominent disclaimers, transparent methodology |

### 1.3 Anti-Goals

| Anti-Goal | Why |
|-----------|-----|
| **Gamification** | This is serious analysis, not engagement farming |
| **Dark patterns** | No tricks to increase usage; respect user's time |
| **Feature overload** | Better to do fewer things excellently than many things poorly |
| **Mobile-first** | Desktop is primary; mobile is best-effort |

---

## 2. Layout Architecture

### 2.1 Overall Structure

The application follows a **sidebar + main content** pattern common in analytical dashboards:

```
┌─────────────────────────────────────────────────────────────────────┐
│  HEADER BAR (sticky)                                                │
│  ┌─────────��───────────────────────────────────────────────────┐   │
│  │ 🎯 PolicyPulse                              [Learning Status]│   │
│  └─────────────────────────────────────────────────────────────┘   │
├─────────────┬───────────────────────────────────────────────────────┤
│  SIDEBAR    │  MAIN CONTENT AREA                                    │
│  (fixed)    │                                                       │
│  ┌────────┐ │  ┌──────────────────────────────────────────────────┐ │
│  │Config  │ │  │ [Tab 1] [Tab 2] [Tab 3] [Tab 4] [Tab 5] [Tab 6] │ │
│  │Panel   │ │  ├──────────────────────────────────────────────────┤ │
│  │        │ │  │                                                  │ │
│  │Population│ │                                                  │ │
│  │        │ │  │  TAB CONTENT                                     │ │
│  │Steps   │ │  │  (scrollable)                                    │ │
│  │        │ │  │                                                  │ │
│  │Mode    │ │  │                                                  │ │
│  │        │ │  │                                                  │ │
│  │Policy  │ │  │                                                  │ │
│  │        │ │  │                                                  │ │
│  │        │ │  │                                                  │ │
│  │[RUN]   │ │  │                                                  │ │
│  └────────┘ │  └──────────────────────────────────────────────────┘ │
│             │                                                       │
└─────────────┴───────────────────────────────────────────────────────┘
```

### 2.2 Sidebar Design

The sidebar is the **command center** for simulation configuration. It remains fixed while the user scrolls through results.

**Sidebar Sections (top to bottom):**

1. **Population Configuration**
   - Population size slider (100 to 50,000)
   - Income distribution expander (3 sliders showing percentages)
   - Visual feedback: percentages must sum to 100%

2. **Simulation Settings**
   - Time steps slider (1 to 10)
   - Random seed checkbox + number input
   - Mode selector (Precision / Balanced / Speed)
   - Mode tooltip explaining each option

3. **Policy Configuration**
   - Preset dropdown (includes "Custom" option)
   - Policy title text input
   - Policy description text area (multi-line)
   - Domain selector (Economy / Education / Social / Business)

4. **Scenario Naming**
   - Auto-generated name (can be edited)
   - Format: "{Policy Title (truncated)} - {Mode}"

5. **Action Buttons**
   - **Primary action**: "▶ Run Simulation" (prominent, full-width)
   - **Secondary actions**:
     - "🔄 Generate Population" (regenerate without running)
     - "🧠 Train Neural Network" (visible when samples available)

**Sidebar Visual Characteristics:**
- Background: slightly darker than main content (creates visual separation)
- Width: 300-320px fixed
- Internal padding: 16px
- Section spacing: 24px between major sections
- Labels: small caps, muted color
- Inputs: full-width within sidebar

### 2.3 Header Area

The header provides persistent context and status information.

**Header Contents:**
- **Left**: Application logo/name "🎯 PolicyPulse"
- **Center**: Current scenario name (when simulation is active)
- **Right**: Learning status indicator (training samples count, NN status)

**Header Visual Characteristics:**
- Height: 48-56px
- Background: white with subtle bottom border
- Logo: gradient text effect (purple to blue)
- Sticky positioning (stays visible on scroll)

### 2.4 Main Content Area

The main content uses a **tabbed interface** to organize different analysis views.

**Tab Structure:**

| Tab | Icon | Purpose |
|-----|------|---------|
| Overview | 📊 | Population-wide trends, time-series charts |
| Demographics | 👥 | Breakdown by income level, location |
| Individuals | 👤 | Citizen browser, individual timelines |
| Experts | 🎓 | AI-generated stakeholder perspectives |
| AI Insights | 🧠 | Neural network analytics, performance metrics |
| Compare | 📂 | Scenario management and comparison |

**Tab Design Principles:**
- Active tab is clearly highlighted (underline + color)
- Inactive tabs are muted but readable
- Tab bar is sticky below header during scroll
- Each tab has its own scroll context

---

## 3. Component Specifications

### 3.1 Welcome State

When no simulation has been run, the main area displays a welcome message.

**Welcome State Layout:**
```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│     👋 Welcome to PolicyPulse                                  │
│                                                                │
│     Get started in three steps:                                │
│                                                                │
│     1. Select or create a policy in the sidebar               │
│     2. Choose a simulation mode                                │
│     3. Click "Run Simulation"                                  │
│                                                                │
│     ┌───────────────────────────────────────────────────────┐ │
│     │ 💡 Tip: Start with Precision Mode to collect          │ │
│     │ training data, then switch to Speed Mode for          │ │
│     │ faster large-scale simulations                        │ │
│     └───────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Characteristics:**
- Centered content
- Large, friendly typography
- Numbered steps for clarity
- Tip box with light background highlighting hybrid workflow

### 3.2 Responsible AI Disclaimer

A prominent warning appears at the top of the main content area (below tabs).

**Disclaimer Design:**
- Yellow/amber warning box
- Icon: ⚠️
- Text: Clear statement that this is synthetic simulation, not prediction
- Collapsible after first view (user can dismiss but it remains accessible)

**Example Text:**
> ⚠️ **Synthetic Simulation Disclaimer**
> This tool creates fictional scenarios for exploratory purposes. Results do not predict real-world behavior. Use as a thought experiment to identify potential blind spots—not as a substitute for real data, surveys, or expert analysis.

### 3.3 Metrics Cards

Key metrics are displayed in card format at the top of the Overview tab.

**Card Layout:**
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Avg        │ │  Avg        │ │  Avg        │ │  Happiness  │
│  Happiness  │ │  Support    │ │  Income     │ │  Gap        │
│             │ │             │ │             │ │             │
│    0.67     │ │   +23%      │ │  $48,500    │ │   0.12      │
│             │ │             │ │             │ │             │
│   ▲ 0.05    │ │   ▼ -5%     │ │   ▲ $2,100  │ │   ▲ 0.02    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

**Card Characteristics:**
- Equal-width cards in a row (4 columns on desktop)
- Primary value: large, bold
- Change indicator: smaller, with colored arrow (green up, red down)
- Label: small, muted, above value
- Subtle shadow for elevation
- Rounded corners (8px)

### 3.4 Time-Series Charts

Line charts showing metrics over simulation steps.

**Chart Design Principles:**
- X-axis: Simulation step (0, 1, 2, ... N)
- Y-axis: Metric value with appropriate range
- Line: 2px stroke with markers at data points
- Grid: Light horizontal lines only (reduces visual noise)
- Legend: Below chart when multiple series

**Specific Charts:**
| Chart | Y-Range | Notes |
|-------|---------|-------|
| Happiness Over Time | 0 to 1 | Green color scheme |
| Policy Support Over Time | -1 to 1 | Blue color scheme, zero line highlighted |
| Average Income Over Time | Auto | Currency formatting |

**Interactivity:**
- Hover shows exact values at each point
- Click on legend item toggles visibility (in multi-series)
- Zoom: not required for 1-10 step range

### 3.5 Bar Charts (Demographic Breakdowns)

Used in Demographics tab to show per-group metrics.

**Chart Layout:**
```
Happiness by Income Level          Support by Income Level
┌───────────────────────────┐     ┌───────────────────────────┐
│    ▓▓▓▓▓▓▓▓   Low         │     │    ▓▓▓▓▓▓▓▓▓▓   Low      │
│    ▓▓▓▓▓▓▓▓▓  Middle      │     │    ▓▓▓▓▓▓▓     Middle    │
│    ▓▓▓▓▓▓▓▓▓▓ High        │     │    ▓▓▓         High      │
└───────────────────────────┘     └───────────────────────────┘
```

**Bar Chart Characteristics:**
- Horizontal bars for category labels (easier to read)
- Consistent color per category across all charts (low=orange, middle=blue, high=green)
- Value labels at end of each bar
- Consistent width scales for comparison

### 3.6 Citizen Browser

A data table with filtering for individual citizen exploration.

**Table Columns:**
| Column | Width | Notes |
|--------|-------|-------|
| ID | 60px | Numeric, clickable |
| Age | 50px | Numeric |
| Profession | 150px | Text, truncate with ellipsis |
| Income Level | 80px | Badge style (colored) |
| City Zone | 100px | Text |
| Happiness | 80px | Number with 2 decimals |
| Support | 80px | Percentage with sign |
| Income | 100px | Currency formatted |
| Diary | 50px | ✅/❌ indicator |

**Filter Controls:**
- Multi-select for Income Level (Low, Middle, High)
- Multi-select for City Zone (Downtown, Industrial, Suburban, Rural)
- Filters appear above table in a collapsible row

**Pagination:**
- Show 100 rows per page
- Note explaining total population vs. displayed

**Citizen Detail View:**
- Triggered by clicking a row or entering ID
- Expands below table (or in side panel)
- Shows full attribute list, personal timeline charts, diary entries

### 3.7 Expert Perspectives Panel

Three-column layout showing AI-generated viewpoints.

**Layout:**
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 💼 Economist    │ │ ✊ Activist      │ │ 🏪 Business     │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│                 │ │                 │ │                 │
│  The policy     │ │  This policy    │ │  From a market  │
│  demonstrates   │ │  reveals        │ │  perspective,   │
│  fiscal...      │ │  concerning...  │ │  the changes... │
│                 │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

**Characteristics:**
- Equal-width columns
- Icon + title header with colored accent
- Paragraph text below (3-5 sentences each)
- Light background differentiation per column
- Loading state: skeleton text animation

### 3.8 Scenario Comparison

Side-by-side comparison of two saved scenarios.

**Comparison Layout:**
```
┌───────────────────────────────────────────────────────────────────┐
│  Scenario A: [Dropdown ▼]          Scenario B: [Dropdown ▼]       │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────┐   ┌────────────────────────┐         │
│  │ Happiness Comparison   │   │ Support Comparison     │         │
│  │ ───A                   │   │ ───A                   │         │
│  │ ───B                   │   │ ───B                   │         │
│  └────────────────────────┘   └────────────────────────┘         │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

**Characteristics:**
- Two dropdowns for scenario selection (can't select same scenario twice)
- Overlaid line charts with distinct colors for A and B
- Legend clearly indicates which line is which
- Summary table below charts with delta values

### 3.9 AI/Neural Network Analytics

Performance dashboard for the hybrid AI system.

**Metrics Displayed:**
- Training samples collected (progress bar toward 500 minimum)
- Model training status (Not Trained / Training / Ready)
- Last training accuracy (MAE, MSE)
- Current simulation breakdown (pie chart: LLM / NN / Rule-based)
- Speed comparison (LLM vs NN inference times)
- Cost savings estimate

**Visual Design:**
- Dashboard card layout
- Progress indicators with percentage
- Stacked bar chart for method breakdown per step
- Performance metrics in highlighted boxes

---

## 4. Interaction Philosophy

### 4.1 User Control vs. Observation

| User Controls | System Provides |
|---------------|-----------------|
| Population configuration | Generated citizen attributes |
| Policy definition | Simulated reactions |
| Simulation mode | Method selection logic |
| Step navigation | Aggregated statistics |
| Citizen selection | Individual timelines |
| Scenario selection | Comparison visualizations |

The user **configures and observes**. The system **generates and analyzes**.

### 4.2 Progressive Disclosure

**Level 1 (Immediate visibility):**
- Population size
- Policy presets
- Run button
- Key metrics cards

**Level 2 (One click away):**
- Income distribution sliders (in expander)
- Detailed policy editing
- Tab content

**Level 3 (Exploration-driven):**
- Individual citizen details
- AI methodology explanation
- Raw data export

### 4.3 Feedback Patterns

| Action | Feedback |
|--------|----------|
| Click Run Simulation | Spinner with progress message |
| Simulation completes | Success toast + automatic tab switch to Overview |
| Error occurs | Error banner with actionable message |
| NN training starts | Progress bar in sidebar |
| NN training completes | Success toast + status update |

### 4.4 Keyboard Accessibility

- Tab navigation through all interactive elements
- Enter key triggers buttons
- Escape closes modals/expanders
- Arrow keys navigate dropdowns

---

## 5. Visual Design System

### 5.1 Color Palette

**Primary Colors:**
| Name | Hex | Usage |
|------|-----|-------|
| Deep Purple | #667EEA | Primary actions, links, active states |
| Violet | #764BA2 | Gradient partner, accents |
| Coral | #FF6B6B | Warnings, negative indicators |
| Teal | #4ECDC4 | Success, positive indicators |
| Mint | #95E1D3 | Secondary positive, backgrounds |

**Neutral Colors:**
| Name | Hex | Usage |
|------|-----|-------|
| Charcoal | #262730 | Primary text |
| Slate | #666666 | Secondary text, labels |
| Silver | #CCCCCC | Borders, dividers |
| Pearl | #F0F8FF | Sidebar background, cards |
| White | #FFFFFF | Main background |

**Semantic Colors:**
| Meaning | Color |
|---------|-------|
| Positive change | Teal (#4ECDC4) |
| Negative change | Coral (#FF6B6B) |
| Neutral | Slate (#666666) |
| Warning | Amber (#FFC107) |
| Error | Red (#DC3545) |
| Info | Blue (#17A2B8) |

### 5.2 Typography

**Font Family:**
- Primary: `Inter` (system fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
- Monospace: `JetBrains Mono` (for code, IDs, numbers)

**Type Scale:**
| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 (Page title) | 32px | 700 | 1.2 |
| H2 (Section) | 24px | 600 | 1.3 |
| H3 (Subsection) | 18px | 600 | 1.4 |
| Body | 14px | 400 | 1.6 |
| Small | 12px | 400 | 1.5 |
| Caption | 11px | 500 | 1.4 |
| Metric Value | 28px | 700 | 1.2 |

### 5.3 Spacing System

Use an 8px base unit:

| Token | Value | Usage |
|-------|-------|-------|
| xs | 4px | Tight spacing (icon-text gap) |
| sm | 8px | Element internal padding |
| md | 16px | Component spacing |
| lg | 24px | Section separation |
| xl | 32px | Major section gaps |
| 2xl | 48px | Page-level separation |

### 5.4 Border Radius

| Element | Radius |
|---------|--------|
| Buttons | 6px |
| Cards | 8px |
| Inputs | 4px |
| Badges | 12px (pill) |
| Modals | 12px |

### 5.5 Shadows

| Level | Usage | CSS |
|-------|-------|-----|
| Subtle | Cards, inputs | `0 1px 3px rgba(0,0,0,0.08)` |
| Medium | Dropdowns, popovers | `0 4px 12px rgba(0,0,0,0.12)` |
| Strong | Modals | `0 8px 24px rgba(0,0,0,0.16)` |

### 5.6 Icons

Use emoji icons for simplicity and universal rendering:
- 📊 Overview
- 👥 Demographics
- 👤 Individuals
- 🎓 Experts
- 🧠 AI Insights
- 📂 Compare
- ▶️ Run
- 🔄 Refresh
- ⚠️ Warning
- ✅ Success
- ❌ Error

For future refinement, consider Phosphor Icons (open source, consistent style).

---

## 6. Responsive Behavior

### 6.1 Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Desktop (default) | ≥1200px | Full layout with sidebar |
| Laptop | 992-1199px | Narrower sidebar (280px) |
| Tablet | 768-991px | Collapsible sidebar, 2-column metric cards |
| Mobile | <768px | Stack all elements, hamburger menu for sidebar |

### 6.2 Critical Behavior

**Desktop/Laptop (primary target):**
- All features fully functional
- Sidebar always visible
- Charts render at full detail

**Tablet:**
- Sidebar collapses to hamburger menu
- Metric cards go 2x2 grid
- Charts remain interactive

**Mobile (best-effort):**
- Single column layout
- Simplified charts (may reduce interactivity)
- Prominent warning that desktop is recommended

---

## 7. Accessibility

### 7.1 WCAG 2.1 AA Compliance Targets

| Requirement | Implementation |
|-------------|----------------|
| Color contrast | All text meets 4.5:1 ratio against background |
| Focus indicators | Visible focus ring on all interactive elements |
| Keyboard navigation | All actions achievable via keyboard |
| Screen reader | Semantic HTML, ARIA labels where needed |
| Motion | Respect `prefers-reduced-motion` |

### 7.2 Specific Considerations

- Charts have text alternatives (summary below chart)
- Color is never the only indicator (always paired with text/icon)
- Loading states announced to screen readers
- Form inputs have associated labels
- Error messages are linked to their inputs

---

## 8. Loading & Empty States

### 8.1 Loading States

**Simulation Running:**
```
┌──────────────────────────────────────┐
│                                      │
│        ⏳ Running Simulation...      │
│                                      │
│        Step 2 of 5                   │
│        [▓▓▓▓▓▓░░░░░░░░░░░░░░] 40%    │
│                                      │
│        This may take a few minutes   │
│        with Precision Mode           │
│                                      │
└──────────────────────────────────────┘
```

**Chart Loading:**
- Skeleton animation matching chart dimensions
- Subtle pulse effect

**Expert Perspectives Loading:**
- "Generating expert analysis..." message
- Skeleton text blocks

### 8.2 Empty States

**No Simulation Run:**
- Welcome message with getting started steps (see Section 3.1)

**No Scenarios to Compare:**
- Message: "Run at least two simulations to compare scenarios"
- Button: "Run Your First Simulation" (scrolls to sidebar)

**Citizen Browser - No Results:**
- Message: "No citizens match your filters"
- Button: "Clear Filters"

---

## 9. Error States

### 9.1 Error Display Patterns

**API Error:**
```
┌──────────────────────────────────────────────────┐
│ ❌ API Error                                [×]  │
├────────────────────────��─────────────────────────┤
│ Unable to connect to AI service. The simulation  │
│ will continue with rule-based reactions.         │
│                                                  │
│ Details: Rate limit exceeded (429)               │
│                                                  │
│ [Retry]  [Continue Without AI]                   │
└──────────────────────────────────────────────────┘
```

**Validation Error:**
- Inline error below affected input
- Red border on input
- Error text in small, red font

**Catastrophic Error:**
- Full-page error with refresh option
- Error details in collapsible section

### 9.2 Error Recovery

| Error Type | Recovery Action |
|------------|-----------------|
| API rate limit | Automatic retry after delay, or key rotation |
| API quota exceeded | Fall back to NN or rule-based |
| Invalid input | Highlight field, show validation message |
| Session timeout | Offer to reload |

---

## 10. Animation & Transitions

### 10.1 Principles

- **Purposeful**: Animation serves understanding (shows connection between actions and results)
- **Subtle**: No flashy effects; professional environment
- **Fast**: Most transitions complete in 150-250ms
- **Respect preferences**: Honor `prefers-reduced-motion`

### 10.2 Specific Animations

| Element | Animation | Duration |
|---------|-----------|----------|
| Tab switch | Fade content | 150ms |
| Card hover | Subtle lift (shadow) | 150ms |
| Expander open/close | Height slide | 200ms |
| Toast notification | Slide in from top | 250ms |
| Chart data update | Line morph | 300ms |
| Progress bar | Width transition | Continuous |

---

## 11. Design Rationale Summary

| Design Decision | Rationale |
|-----------------|-----------|
| Sidebar for config | Config is always needed; keeps main area for results |
| Tabs for analysis views | Progressive disclosure; don't overwhelm with all data at once |
| Metric cards at top | Answer "what happened?" immediately |
| Three-column expert layout | Equal visual weight to each perspective |
| Muted color palette | Professional tool, not consumer app |
| Emoji icons | Universal rendering, no icon library dependency |
| Prominent disclaimer | Responsible AI; set correct expectations |
| Skeleton loading | Better perceived performance than spinners |
| Scenario comparison in tab | Distinct workflow from single-simulation analysis |

---

*This design document provides the foundation for PolicyPulse's user interface. Developers should interpret specifications with judgment, prioritizing user experience over rigid adherence.*