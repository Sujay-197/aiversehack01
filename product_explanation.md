# Product Explanation: Aiversehack01 - The Career Scientist

## 1. Project Essence & Core Philosophy
**"Your Career as a Science Experiment"**

Aiversehack01 reimagines the job search process by transforming it from a linear "apply and hope" methodology into a **scientific loop**. Instead of a standard job board or application bot, this system acts as a "Scientist" that:
1.  **Formulates Hypotheses**: "If I apply to this Senior Backend role, my Python skills will be validated."
2.  **Runs Experiments**: Executes the application process.
3.  **Analyzes Results**: Treats rejections not as failures, but as **data points** to update its internal "Belief State".
4.  **Refines Strategy**: Automatically adjusts future applications based on what it learned (e.g., "downgrade seniority expectations," "highlight different skills").

**Key Differentiator**: The system **learns from failure**. A rejection isn't the end; it's the signal that triggers a "Belief Update," changing the agent's strategy for the next attempt.

## 2. Architecture Review

The system follows a modern **Agentic Architecture**, splitting responsibilities between a "Brain" (Reasoning) and "Limbs" (Execution).

### Backend (The Brain)
-   **Framework**: **FastAPI** (Python) serves as the central nervous system, exposing REST endpoints.
-   **Orchestration**: **LangGraph** (via `backend/brain/graph_v2.py`) manages the stateful flow between agents. It defines nodes like `retrieve`, `filter`, and `reason`, and handles conditional routing based on outcomes.
-   **Data Model**: **Pydantic** is used heavily for structured data exchange (Resumes, Evidence, Beliefs) to ensure strict typing.
-   **Database**: **PostgreSQL** (implied via SQLAlchemy/PsycoPG2) stores the persistent state: Users, Beliefs, Experiments, and Outcomes.
-   **Vector Search**: Uses a **Vector Store** (likely ephemeral or simple in current code) to match opportunities with user beliefs.

### Frontend (The Lab Notebook)
-   **Framework**: **Next.js 15** (App Router) + **React 19**.
-   **Styling**: **Tailwind CSS** for a utility-first, dark-mode-centric design.
-   **Concept**: The UI is designed as a **"Lab Notebook"**, consisting of:
    -   **Passport View**: Visualizes skills as "Beliefs" with confidence intervals (e.g., "Python: 70% Confidence").
    -   **Experiments Dashboard**: Tracks applications as active experiments.
    -   **Insights Log**: A journal of what the AI has learned from each outcome.

## 3. Tools & Technologies

| Category | Tools Used | Purpose |
| :--- | :--- | :--- |
| **Backend Core** | `FastAPI`, `Uvicorn` | High-performance API server. |
| **AI & Agents** | `LangGraph`, `Google GenAI` | Agent orchestration and LLM reasoning. |
| **Data Parsing** | `BeautifulSoup4`, `PyPDF2`, `PyGithub` | Extracting data from web, PDFs, and GitHub. |
| **Validation** | `Pydantic` | Ensuring strict data structure for AI outputs. |
| **Search** | `DuckDuckGo Search` | Finding relevant job opportunities. |
| **Frontend** | `Next.js`, `React`, `Tailwind CSS` | Building the interactive "Lab Notebook" UI. |
| **Visualization** | `Recharts`, `Framer Motion` | Rendering charts and smooth UI transitions. |
| **Database** | `SQLAlchemy`, `PsycoPG2` | ORM and Database connectivity. |

## 4. Novelty of Path

### A. The "Belief State" Model
Unlike traditional ATS scanners that just match keywords, this system maintains a **probabilistic belief state** about the user.
-   *Traditional*: "You have 'Python' on your resume."
-   *Aiversehack01*: "I have 60% confidence in your 'Python' skill based on your GitHub. If you get rejected from a Google role, I will lower this to 55% and recommend a mid-level role next."

### B. Autonomous Replanning
The system features a **rejection-driven feedback loop**. The `Reflection Agent` analyzes failure to update the `Planner Agent`.
-   **Hypothesis Engine**: It explicitly states *why* it is recommending an action (e.g., "Testing fit for ML roles").
-   **Strategic Evolution**: Strategies are versioned objects. If Strategy V1 fails multiple times, the Planner generates Strategy V2 with justified changes (e.g., "Pivot focus to Data Engineering").

## 5. Summary for Analysis & Next Steps

**Current Status**:
-   **Backend**: Core agent logic (`resume`, `github`, `market`) and the reasoning graph (`graph_v2.py`) are implemented. The LangGraph orchestration is active.
-   **Frontend**: The plan is detailed (`frontend_plan.md`), but the implementation seems to be in the early initialization stage.
-   **Missing**: Connection between the running LangGraph backend and the Next.js frontend needs to be solidified.

**Recommendation for Proceeding**:
1.  **Frontend Implementation**: Execute the `frontend_plan.md`. Build the "Passport" and "Experiments" views to visualize the backend's rich data.
2.  **Integration**: Connect the Next.js frontend to the FastAPI `auth` and `graph` endpoints.
3.  **Visualization**: Focus on the "Confidence Interval" visualizations, as this is the key UI differentiator.
4.  **Testing**: Run `test_end_to_end.py` to verify the full loop (Parse -> Plan -> Experiment -> Learn) before building the UI on top.
