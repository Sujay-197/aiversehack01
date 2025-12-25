# Frontend Architecture Plan: The Lab Notebook

## Overview
The UI for the Career Scientist system will be a **"Lab Notebook"** interface that visualizes the user's career as a scientific experiment. The design philosophy shifts from traditional job boards to an **experimental dashboard** where users track beliefs, run tests, and learn from outcomes.

---

## Tech Stack

### Core Framework
- **Next.js 15** (App Router)
- **React 19**
- **TypeScript**

### Styling & UI
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **shadcn/ui** - High-quality components (optional, can build custom)

### Data & State
- **React Query / TanStack Query** - Server state management
- **Zustand** - Client state (if needed)

### Visualization
- **Recharts** or **Chart.js** - Confidence graphs, timelines

---

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home/Dashboard
│   ├── passport/
│   │   └── page.tsx         # Belief State (Passport) view
│   ├── experiments/
│   │   ├── page.tsx         # Experiments list
│   │   └── [id]/
│   │       └── page.tsx     # Individual experiment detail
│   ├── insights/
│   │   └── page.tsx         # Learning log / reflection history
│   └── onboarding/
│       └── page.tsx         # Initial profile upload
│
├── components/
│   ├── ui/                  # Reusable primitives (Button, Card, Badge, etc.)
│   ├── passport/
│   │   ├── BeliefCard.tsx
│   │   ├── ConfidenceBar.tsx
│   │   └── SkillGraph.tsx
│   ├── experiments/
│   │   ├── ExperimentCard.tsx
│   │   ├── HypothesisDisplay.tsx
│   │   └── OutcomeTimeline.tsx
│   ├── insights/
│   │   └── ReflectionCard.tsx
│   └── layout/
│       ├── Navbar.tsx
│       └── Sidebar.tsx
│
├── lib/
│   ├── api/
│   │   ├── passport.ts      # API calls for belief state
│   │   ├── experiments.ts   # API calls for experiments
│   │   └── insights.ts      # API calls for reflections
│   ├── types.ts             # TypeScript types (mirror backend models)
│   └── utils.ts             # Helper functions
│
├── public/
│   └── assets/              # Images, icons
│
└── styles/
    └── globals.css          # Tailwind + custom styles
```

---

## Core Views

### 1. **Dashboard (Home)**
**Purpose**: Overview of the user's scientific career journey.

**Layout**:
- Header: User name + confidence score trend
- Left: Quick stats (Total experiments, Win rate, Active hypotheses)
- Center: Timeline of recent experiments & outcomes
- Right: Next suggested experiment

**Key Components**:
- `<StatCard />` - Shows metrics (e.g., "5 Active Tests")
- `<TimelineView />` - Chronological experiment history
- `<SuggestionCard />` - AI-generated next action

---

### 2. **The Failure Passport** (`/passport`)
**Purpose**: Visual representation of the user's belief state (skills, confidence, gaps).

**Layout**:
- Grid of **Belief Cards**, each showing:
  - Attribute name (e.g., "Python")
  - Confidence score (0.0 - 1.0) as a progress bar
  - Basis (e.g., "3 GitHub repos, 2 rejections")
  - History chart (mini line graph showing confidence over time)

**Key Components**:
- `<BeliefCard />` - Individual skill belief
- `<ConfidenceBar />` - Animated bar showing 0-100%
- `<BeliefHistoryGraph />` - Small sparkline of confidence changes

**Color Coding**:
- 🔴 Red (0.0 - 0.3): "Learning Zone"
- 🟡 Yellow (0.3 - 0.7): "Testing Zone"
- 🟢 Green (0.7 - 1.0): "Verification Zone"

---

### 3. **Experiments Dashboard** (`/experiments`)
**Purpose**: Track active and past experiments (applications, projects).

**Layout**:
- Tabs: `Active`, `Pending Outcome`, `Completed`
- Each experiment card shows:
  - Hypothesis (e.g., "Applying to Backend roles will validate Python confidence")
  - Opportunity details (company, role, link)
  - Status: Proposed → Active → Outcome Received
  - Outcome (if complete): Rejection, Interview, Offer

**Key Components**:
- `<ExperimentCard />` - Shows hypothesis + status
- `<HypothesisDisplay />` - Format the "If...then..." statement
- `<OutcomeTag />` - Color-coded badge (Rejection = Red, Interview = Green)

**Interaction**:
- Click card → Drill into `/experiments/[id]` for full details + belief impact

---

### 4. **Insights Log** (`/insights`)
**Purpose**: A "learning journal" showing how beliefs evolved.

**Layout**:
- Feed of reflection entries, each showing:
  - Date
  - Outcome that triggered the insight
  - Old vs New belief (e.g., "Python confidence: 0.6 → 0.4")
  - AI-generated reasoning (e.g., "Resume keyword mismatch detected")

**Key Components**:
- `<ReflectionCard />` - Displays before/after belief state
- `<BeliefDiff />` - Visual diff (e.g., bar chart showing change)

---

### 5. **Onboarding** (`/onboarding`)
**Purpose**: Upload resume → Generate initial Passport v0.

**Flow**:
1. Upload PDF
2. Show loading state ("Analyzing resume...")
3. Display extracted data (skills, experience)
4. Generate initial Belief State
5. Redirect to `/passport`

**Key Components**:
- `<FileUpload />` - Drag-and-drop PDF
- `<LoadingSpinner />` - Animated loader
- `<ExtractionPreview />` - Show what was parsed

---

## Design System

### Color Palette
```css
/* Confidence States */
--learning: #EF4444;    /* Red - Low confidence */
--testing: #F59E0B;     /* Amber - Medium confidence */
--verifying: #10B981;   /* Green - High confidence */

/* Background */
--bg-primary: #0F172A;   /* Dark slate */
--bg-secondary: #1E293B; /* Lighter slate */

/* Text */
--text-primary: #F1F5F9;
--text-secondary: #94A3B8;

/* Accents */
--accent: #3B82F6;       /* Blue for actions */
```

### Typography
- **Headings**: `Inter` or `Outfit` (Google Fonts)
- **Body**: `Inter`
- **Mono (code/data)**: `JetBrains Mono`

### Animations
- **Micro-interactions**: Confidence bars fill on mount
- **Transitions**: Smooth page transitions with Framer Motion
- **Hover states**: Scale + glow effects on cards

---

## API Integration

### Backend Communication
All API calls will target the FastAPI backend (assumed to run on `http://localhost:8000`).

**Example endpoints** (to be implemented in backend):
```
GET  /api/passport/{user_id}          # Get belief state
GET  /api/experiments/{user_id}       # List experiments
POST /api/experiments                 # Create new experiment
GET  /api/insights/{user_id}          # Get reflection history
POST /api/upload-resume               # Onboarding
```

### Data Flow
```
Frontend (React Query) 
   ↓
FastAPI Backend
   ↓
PostgreSQL (belief_state, experiments, outcomes)
```

---

## Accessibility & UX

- **Dark Mode**: Default (matches "Lab Notebook" aesthetic)
- **Responsive**: Mobile-first, works on tablets/phones
- **Keyboard Navigation**: All actions accessible via keyboard
- **Screen Readers**: Proper ARIA labels on all components

---

## Next Steps (Pending Approval)

1. **Initialize Next.js project** in `frontend/` directory
2. **Install dependencies** (Tailwind, Framer Motion, etc.)
3. **Build design system** (`components/ui/`)
4. **Implement Passport view** (highest priority)
5. **Connect to backend** (stub API for now if backend not ready)

---

## Design Decisions - All Confirmed ✅

1. **Color scheme**: Dark mode only - simple yet modern aesthetic
2. **Component approach**: Custom-built components for full control and simplicity
3. **Chart library**: Recharts (React-native compatible, clean API)
4. **Authentication**: Universal login placeholder - proper auth deferred to later phase
5. **Deployment**: Netlify (linked with Git for auto-deployment)

---

## Ready to Build

All architectural decisions are locked in. Next step: Initialize the Next.js project in `frontend/` directory.
