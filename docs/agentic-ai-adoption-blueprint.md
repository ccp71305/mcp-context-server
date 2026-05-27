# 🚀 The Agentic AI Blueprint

## Adopting 100% AI-Powered SDLC Workflows for Product & Development

> *"We're not replacing developers with AI. We're giving every developer a team of tireless, context-aware specialists who never call in sick and never forget what you told them yesterday."*

---

## Table of Contents

1. [The Problem We're Solving](#1-the-problem-were-solving)
2. [What is Agentic AI? (In Plain English)](#2-what-is-agentic-ai-in-plain-english)
3. [Agents vs Skills vs MCP Servers — Demystified](#3-agents-vs-skills-vs-mcp-servers--demystified)
4. [Why MCP Servers Are a Game Changer](#4-why-mcp-servers-are-a-game-changer)
5. [Industry Best Practices (What the Leaders Are Doing)](#5-industry-best-practices)
6. [The Context Window Problem (And How We Solve It)](#6-the-context-window-problem-and-how-we-solve-it)
7. [Our Technology Landscape](#7-our-technology-landscape)
8. [The Adoption Roadmap: From Zero to Agentic](#8-the-adoption-roadmap-from-zero-to-agentic)
9. [Pillar 1: Domain-Specific Skills](#9-pillar-1-domain-specific-skills)
10. [Pillar 2: The MCP Context Server](#10-pillar-2-the-mcp-context-server)
11. [Pillar 3: Custom Agent Orchestration](#11-pillar-3-custom-agent-orchestration)
12. [Workflow Examples: A Day in the Life](#12-workflow-examples-a-day-in-the-life)
13. [Adoption Strategy: Getting the Whole Team On Board](#13-adoption-strategy-getting-the-whole-team-on-board)
14. [Measuring Success](#14-measuring-success)
15. [Risks, Guardrails & Governance](#15-risks-guardrails--governance)
16. [FAQ](#16-faq)

---

## 1. The Problem We're Solving

### The Current Reality

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE DEVELOPER'S DAY (Before)                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  09:00  Read Jira ticket. Wonder what it actually means.           │
│  09:30  Search Confluence for design doc. Find 3 outdated ones.    │
│  10:00  Grep codebase for related patterns. Get 847 results.       │
│  10:30  Ask teammate "how does this work?" They're on PTO.         │
│  11:00  Start coding. Realize you misunderstood the requirement.   │
│  11:30  Re-read Jira. Check acceptance criteria. Ah, THAT's what   │
│         they meant.                                                 │
│  12:00  Lunch. Think about what you should have been doing.        │
│  13:00  Actually write code. The productive 4 hours begin.         │
│  17:00  Context switch to a PDSupport ticket. Lose all context.    │
│  17:30  Try to remember where you left off on the first task.      │
│                                                                     │
│  Actual coding time: ~4 hours                                       │
│  Context gathering: ~4 hours                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Sound familiar?** The problem isn't that our developers aren't skilled. It's that we spend an enormous amount of time on context gathering, requirement interpretation, and repetitive mechanical tasks — time that could be spent on **thinking deeply about customer problems and building elegant solutions**.

### What We Want

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE DEVELOPER'S DAY (After)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  09:00  "Agent, pick up ION-12310. Read the requirements,          │
│          check Confluence for the design doc, review the related   │
│          code, and give me a summary with an implementation plan." │
│                                                                     │
│  09:05  Agent returns: Requirements, acceptance criteria,           │
│          relevant code snippets, design doc summary, and a         │
│          step-by-step implementation plan. Ready to go.            │
│                                                                     │
│  09:10  Start designing and coding with full context.              │
│                                                                     │
│  14:00  "Agent, resume the PDSupport ticket from yesterday."       │
│          Agent loads session context, knows exactly where you      │
│          left off, and picks up from step 4 of 7.                  │
│                                                                     │
│  Actual design & coding time: ~7 hours                              │
│  Context gathering: ~1 hour                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### The Shift: From Code Monkeys to Product Artisans

This isn't just about writing code faster. It's about fundamentally reshaping how we think:

| **Old Mindset** | **New Mindset** |
|---|---|
| "What does the code need to do?" | "What customer problem are we solving?" |
| "How do I implement this method?" | "What's the best architectural approach?" |
| "Let me write tests for this class" | "What scenarios does the customer actually care about?" |
| "Merge and move on" | "Does this solution truly delight the user?" |

**We deeply care about the products we build.** Agentic AI frees us to act on that care.

---

## 2. What is Agentic AI? (In Plain English)

Think of traditional AI assistants like a really smart friend you can text. You ask a question, they give an answer, conversation over.

**Agentic AI** is more like hiring a junior developer with photographic memory and zero ego:

- **Autonomous**: You give it a goal. It figures out the steps, executes them, checks its work, and iterates until done.
- **Tool-Using**: It doesn't just suggest code — it reads your codebase, runs commands, queries APIs, and interacts with your tools.
- **Persistent**: It remembers what happened across sessions (if you give it memory).
- **Composable**: Multiple agents can work together, each specializing in different tasks.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    THE AGENTIC AI STACK                              │
│                                                                     │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │                    YOUR GOAL                              │     │
│   │  "Upgrade Jackson to 2.17.x across all microservices"    │     │
│   └────────────────────────┬─────────────────────────────────┘     │
│                            │                                        │
│                            ▼                                        │
│   ┌──────────────────────────────────────────────────────────┐     │
│   │               AGENT (Claude Opus 4.6)                     │     │
│   │                                                          │     │
│   │  "I'll break this into steps, track progress, and        │     │
│   │   verify each module compiles and tests pass."           │     │
│   └──┬──────────┬──────────┬──────────┬──────────┬──────────┘     │
│      │          │          │          │          │                   │
│      ▼          ▼          ▼          ▼          ▼                   │
│   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│   │ Read │ │Query │ │ Run  │ │Search│ │Track │                    │
│   │ Code │ │ Jira │ │Tests │ │ Docs │ │State │                    │
│   │(Git) │ │      │ │      │ │(KB)  │ │(MCP) │                    │
│   └──────┘ └──────┘ └──────┘ └──────┘ └──────┘                   │
│                                                                     │
│   = Skills     + MCP Tools     + Local Tools     + Filesystem       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Agents vs Skills vs MCP Servers — Demystified

This is the question everyone asks first, and the answer is beautifully simple once you see it.

### The Restaurant Analogy 🍳

Imagine you're opening a restaurant:

| Concept | Restaurant Analogy | What It Is |
|---|---|---|
| **Agent** | The **Chef** | An AI persona with a specific role, personality, and set of instructions. It decides *what* to do and *when*. |
| **Skill** | The **Recipe Book** | A collection of domain knowledge and step-by-step workflows. It tells the agent *how* to do something well. |
| **MCP Server** | The **Kitchen Equipment** | External tools and data sources the agent can use. It provides the *capability* to do things. |
| **Local Tools** | The **Utensils** | Built-in capabilities like reading files, running terminal commands. Always available. |

**The Chef (Agent)** reads a **Recipe (Skill)** and uses the **Kitchen Equipment (MCP Server)** and **Utensils (Local Tools)** to prepare the dish.

### In Technical Terms

```
┌──────────────────────────────────────────────────────────────────┐
│                          AGENTS                                   │
│                                                                  │
│  WHO: A configured AI persona (e.g., "Refactoring Specialist")  │
│  WHAT: Has specific instructions, restricted tool access,        │
│        and behavioral rules                                      │
│  WHERE: Defined in .github/AGENTS.md or agent config files      │
│  WHEN TO USE: When you need the AI to "think" differently       │
│               for a specific type of task                        │
│                                                                  │
│  Example: A "Review Agent" that only reads code and checks      │
│           for issues vs a "Refactoring Agent" that modifies code │
├──────────────────────────────────────────────────────────────────┤
│                          SKILLS                                   │
│                                                                  │
│  WHO: Domain knowledge packaged as markdown instructions        │
│  WHAT: Detailed workflows, checklists, patterns, and            │
│        domain-specific know-how                                  │
│  WHERE: .github/skills/<skill-name>/SKILL.md                    │
│  WHEN TO USE: When the agent needs to know HOW to do            │
│               something specific to your domain                  │
│                                                                  │
│  Example: "Java Refactoring Skill" knows your module            │
│           dependency order and Maven conventions                 │
├──────────────────────────────────────────────────────────────────┤
│                       MCP SERVERS                                 │
│                                                                  │
│  WHO: External tool providers that follow the Model Context     │
│       Protocol standard                                          │
│  WHAT: Expose capabilities (tools) that any agent can call —    │
│        Jira queries, Git operations, file search, etc.          │
│  WHERE: Runs locally as a process, connected via stdio/SSE      │
│  WHEN TO USE: When agents need to reach beyond the IDE into     │
│               external systems and data sources                  │
│                                                                  │
│  Example: Query Jira for ticket details, search Confluence      │
│           for docs, access any Git repo outside the workspace   │
└──────────────────────────────────────────────────────────────────┘
```

### How They Work Together

```
   Developer gives a goal
          │
          ▼
   ┌─────────────┐     reads      ┌───────────────┐
   │    AGENT     │◄──────────────│    SKILLS      │
   │ (The Brain)  │               │ (The Know-How) │
   └──────┬───────┘               └────────────────┘
          │
          │ calls tools from
          ▼
   ┌─────────────────────────────────────────────┐
   │              AVAILABLE TOOLS                  │
   │                                               │
   │  ┌──────────────┐  ┌─────────────────────┐  │
   │  │ Local Tools   │  │    MCP Server(s)     │  │
   │  │              │  │                     │  │
   │  │ • Read files │  │ • Session context   │  │
   │  │ • Edit files │  │ • Jira queries      │  │
   │  │ • Terminal   │  │ • Confluence search  │  │
   │  │ • Search     │  │ • Git operations    │  │
   │  │ • Debug      │  │ • KB file search    │  │
   │  └──────────────┘  └─────────────────────┘  │
   └─────────────────────────────────────────────┘
```

### Key Insight

> **Skills are knowledge. MCP servers are capabilities. Agents are personalities.**
> 
> A Skill says *"When upgrading Jackson, always follow module dependency order and run tests after each module."*
> 
> An MCP server says *"Here's a `jira_get_issue` tool you can call to fetch ticket details."*
> 
> An Agent says *"I am a Java refactoring specialist. I will use the refactoring skill and MCP tools to methodically upgrade this library."*

**The golden rule of where to invest:**

```
   ┌────────────────────────────────────────────────────────────────┐
   │                                                                │
   │  "If GitHub Copilot can already do it well, use it.           │
   │   Don't build a Ferrari from spare parts."                    │
   │                                                                │
   │   Build Skills   → when agents need YOUR domain knowledge     │
   │   Build MCP      → when agents need to reach external systems │
   │   Build Agents   → when you need specialized orchestration    │
   │                      (start here LAST)                        │
   │                                                                │
   └────────────────────────────────────────────────────────────────┘
```

---

## 4. Why MCP Servers Are a Game Changer

### The Problem Before MCP

Before MCP (Model Context Protocol), every AI tool had its own way of connecting to external systems. Want to query Jira? Build a custom integration. Want to read Git history? Different integration. Want to search Confluence? Yet another one.

It was like having a different power plug for every appliance in your kitchen. 🔌

### MCP: The Universal Adapter

**MCP is an open standard** (created by Anthropic, adopted across the industry) that provides a universal protocol for AI agents to discover and use tools from any provider.

```
   ┌──────────────────────────────────────────────────────────────┐
   │                    WITHOUT MCP                                │
   │                                                              │
   │   Copilot ──(custom)──► Jira                                │
   │   Copilot ──(custom)──► Confluence                          │
   │   Copilot ──(custom)──► Git                                 │
   │   Copilot ──(custom)──► Your internal tool                  │
   │                                                              │
   │   4 agents × 4 integrations = 16 custom connectors 😱       │
   ├──────────────────────────────────────────────────────────────┤
   │                     WITH MCP                                  │
   │                                                              │
   │                ┌─────────────┐                               │
   │   Copilot ────►│ MCP Protocol│◄── standard interface         │
   │   Claude  ────►│             │                               │
   │   Cursor  ────►│    ┌───────┤                               │
   │   Any AI  ────►│    │Tools: │                               │
   │                │    │• Jira │                               │
   │                │    │• Conf │                               │
   │                │    │• Git  │                               │
   │                │    │• KB   │                               │
   │                └────┴───────┘                               │
   │                                                              │
   │   Any agents × 1 MCP server = 1 integration to maintain ✨   │
   └──────────────────────────────────────────────────────────────┘
```

### Custom homegrown MCP Context Server: What It Does (in development)

We've built a production-ready MCP server specifically designed for our workflows:

```
┌───────────────────────────────────────────────────────────────────┐
│                   MCP CONTEXT SERVER                               │
│                   (Our Home-Grown Solution)                        │
│                                                                   │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│  │  SESSION CONTEXT     │  │  JIRA INTEGRATION                │  │
│  │                     │  │                                  │  │
│  │  • Create sessions  │  │  • Get issue details             │  │
│  │  • Track decisions  │  │  • JQL search                    │  │
│  │  • Store progress   │  │  • Read/add comments             │  │
│  │  • Resume work      │  │  • Requirements & AC             │  │
│  │  • Search history   │  │                                  │  │
│  └─────────────────────┘  └──────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────┐  ┌──────────────────────────────────┐  │
│  │  CONFLUENCE          │  │  GIT OPERATIONS                  │  │
│  │                     │  │                                  │  │
│  │  • Search docs      │  │  • Log, diff, blame              │  │
│  │  • Read pages       │  │  • File history                  │  │
│  │  • Browse spaces    │  │  • Branch comparison             │  │
│  │  • Find ADRs        │  │  • Multi-repo access             │  │
│  └─────────────────────┘  └──────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────────────┐                                         │
│  │  KNOWLEDGE BASE      │  Transport: stdio (local, secure)     │
│  │                     │  Auth: env vars (API tokens)           │
│  │  • File search      │  Storage: local filesystem             │
│  │  • Pattern grep     │  Language: Python 3.11+                │
│  │  • Cross-project    │                                         │
│  │  • Regex support    │                                         │
│  └─────────────────────┘                                         │
└───────────────────────────────────────────────────────────────────┘
```

---

## 5. Industry Best Practices

### What the Leaders Are Doing

The companies achieving the best results with agentic AI share common patterns:

#### 1. Start with Skills, Not Agents

> **Anthropic's recommendation**: *"Invest in good prompts and tool descriptions before building complex agent orchestration."*

The companies seeing 3-5x productivity gains didn't start by building elaborate multi-agent systems. They started by writing **detailed skill documents** that encode their team's institutional knowledge.

```
┌───────────────────────────────────────────────┐
│         MATURITY MODEL                         │
│                                               │
│  Level 1: AI Autocomplete                     │  ← Most teams are here
│           (Copilot suggestions)               │
│                                               │
│  Level 2: AI Chat + Edit                      │  ← Many teams reach this
│           (Ask Copilot to write code)         │
│                                               │
│  Level 3: Skill-Augmented Agent               │  ← Target for Phase 1
│           (Agent reads your domain knowledge, │
│            follows your workflows)            │
│                                               │
│  Level 4: Tool-Connected Agent                │  ← Target for Phase 2
│           (Agent queries Jira, searches docs, │
│            accesses external systems via MCP) │
│                                               │
│  Level 5: Multi-Agent Orchestration           │  ← Target for Phase 3
│           (Specialized agents collaborate,    │
│            hand off work, review each other)  │
│                                               │
└───────────────────────────────────────────────┘
```

#### 2. Anthropic's Agent Design Patterns (from their research)

Anthropic (creators of Claude) published definitive guidance on building effective agents:

```
┌────────────────────────────────────────────────────────────────┐
│              ANTHROPIC'S AGENT PATTERNS                         │
│                                                                │
│  Pattern 1: AUGMENTED LLM (Start Here)                        │
│  ┌──────────┐                                                 │
│  │   LLM    │──► retrieval (Skills/KB)                        │
│  │          │──► tools (MCP/local)                            │
│  │          │──► memory (Sessions)                            │
│  └──────────┘                                                 │
│  Use when: single agent + good tools is enough                │
│                                                                │
│  Pattern 2: PROMPT CHAINING                                    │
│  ┌───┐   ┌───┐   ┌───┐   ┌───┐                              │
│  │ 1 │──►│ 2 │──►│ 3 │──►│ 4 │                              │
│  └───┘   └───┘   └───┘   └───┘                              │
│  Use when: task has clear sequential steps                    │
│  e.g., Read Jira → Analyze code → Propose changes → Test     │
│                                                                │
│  Pattern 3: ROUTING                                            │
│          ┌──► Specialist A (Java)                             │
│  Input ──┤                                                    │
│          ├──► Specialist B (Testing)                          │
│          │                                                    │
│          └──► Specialist C (Infra)                            │
│  Use when: different task types need different expertise       │
│                                                                │
│  Pattern 4: ORCHESTRATOR-WORKERS                               │
│       ┌──────────┐                                            │
│       │Orchestr. │                                            │
│       └─┬──┬──┬──┘                                            │
│         ▼  ▼  ▼                                               │
│       ┌─┐┌─┐┌─┐                                              │
│       │W││W││W│  (parallel workers)                           │
│       └─┘└─┘└─┘                                              │
│  Use when: tasks can be parallelized                          │
│  e.g., Upgrade library across 5 microservices simultaneously  │
│                                                                │
│  Pattern 5: EVALUATOR-OPTIMIZER                                │
│       ┌──────┐    ┌───────────┐                              │
│       │Agent │◄──►│ Evaluator │                              │
│       └──────┘    └───────────┘                              │
│  Use when: quality matters and criteria are clear             │
│  e.g., Write code → Review agent checks → Iterate            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Key takeaway**: Start with Pattern 1 (Augmented LLM). That's a single Claude Opus 4.6 agent with good skills and MCP tools. It's remarkably effective and requires the least infrastructure.

#### 3. The Claude + VS Code Sweet Spot

The industry consensus for 2025-2026 is converging on:

| Component | Best Practice |
|---|---|
| **IDE** | VS Code with GitHub Copilot |
| **Model** | Claude Opus 4.6 for complex reasoning; Claude Sonnet for routine tasks |
| **Context Management** | MCP servers for external tools + persistent session state |
| **Domain Knowledge** | Skill files in `.github/skills/` within each repository |
| **Code Knowledge** | Local git + filesystem tools (no cloud indexing needed) |
| **Workflow Integration** | Jira/Confluence MCP tools for requirement context |

---

## 6. The Context Window Problem (And How We Solve It)

### The Problem

Every developer using AI agents has hit this wall:

```
   Conversation Start                              Token Limit
   │                                                    │
   │  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
   │  "Agent is sharp, helpful, productive!"           │
   │                                                    │
   │  ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
   │  "Agent is still doing okay..."                   │
   │                                                    │
   │  █████████████████████████████░░░░░░░░░░░░░░░░░░  │
   │  "Wait, agent forgot what I said 10 mins ago"     │
   │                                                    │
   │  ████████████████████████████████████████████████  │
   │  "Agent is hallucinating. Time for a new chat." 😤│
   │                                                    │
```

### Why Claude Opus 4.6 Helps

Claude Opus 4.6 is exceptional at **being given a detailed goal with steps and working autonomously**:

- Creates its own internal todo list
- Iterates until the objective is met
- Uses tokens efficiently (doesn't repeat context back to you)
- Maintains coherence over longer conversations
- Self-corrects when it hits an obstacle

But even Claude Opus has limits. That's where our **multi-pronged strategy** comes in:

### Our Solution: The Context Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  CONTEXT MANAGEMENT STRATEGY                     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LAYER 1: SKILLS (Loaded On-Demand)                      │  │
│  │                                                          │  │
│  │  Skills are ONLY loaded when relevant to the task.       │  │
│  │  A Java refactoring task loads Java skills.              │  │
│  │  A testing task loads QA skills.                         │  │
│  │  This keeps the context window focused.                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LAYER 2: MCP TOOLS (Query, Don't Preload)               │  │
│  │                                                          │  │
│  │  Agent doesn't load entire Jira ticket + all comments    │  │
│  │  + all code + all docs into context.                     │  │
│  │                                                          │  │
│  │  Instead, it QUERIES specific pieces as needed:          │  │
│  │  • jira_get_issue("ION-12310")  → just this ticket      │  │
│  │  • kb_grep("CloudAttribute")    → just matching lines   │  │
│  │  • git_diff(ref_a, ref_b)       → just the changes      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LAYER 3: SESSION PERSISTENCE (Survive Across Chats)     │  │
│  │                                                          │  │
│  │  When context window fills up → start new conversation.  │  │
│  │  Session context preserves:                              │  │
│  │  • Decisions made                                        │  │
│  │  • Files changed                                         │  │
│  │  • Blockers encountered                                  │  │
│  │  • Progress checkpoints                                  │  │
│  │                                                          │  │
│  │  New conversation loads session → picks up where you     │  │
│  │  left off with minimal token usage.                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  LAYER 4: COPILOT MEMORY (Personal Patterns)             │  │
│  │                                                          │  │
│  │  User-level memory files store:                          │  │
│  │  • Personal coding preferences                          │  │
│  │  • Common commands and shortcuts                         │  │
│  │  • Lessons learned from past debugging                   │  │
│  │  • Repository-specific conventions                       │  │
│  │                                                          │  │
│  │  Always available, always tiny, always relevant.         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Math That Matters

```
Without Context Management:
  1 long conversation → 200K tokens → context degradation → poor output

With Context Management:
  Conversation 1: 50K tokens (focused) → session saved
  Conversation 2: 50K tokens (resumes) → session saved
  Conversation 3: 50K tokens (resumes) → task complete
  
  Total work done: 150K tokens of HIGH-QUALITY output
  Each conversation: Sharp, focused, productive
```

---

## 7. Our Technology Landscape

### What We're Working With

```
┌───────────────────────────────────────────────────────────────────┐
│                    OUR TECH ECOSYSTEM                              │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     APPLICATION LAYER                        │ │
│  │                                                             │ │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │   │  Dropwizard   │  │   Python     │  │  Front-End   │    │ │
│  │   │  Microservices│  │   Services   │  │  (if any)    │    │ │
│  │   │  (Java)       │  │              │  │              │    │ │
│  │   └──────┬───────┘  └──────┬───────┘  └──────────────┘    │ │
│  └──────────┼──────────────────┼───────────────────────────────┘ │
│             │                  │                                   │
│  ┌──────────┼──────────────────┼───────────────────────────────┐ │
│  │          │  AWS SERVICES    │                                │ │
│  │          ▼                  ▼                                │ │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │ │
│  │  │ SQS  │ │ SNS  │ │  S3  │ │ SES  │ │Dynamo│ │ SSM  │  │ │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    CI/CD & DEPLOYMENT                        │ │
│  │                                                             │ │
│  │   Jenkins ──► Build & Test ──► Docker ──► AWS ECS           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    WORKFLOW & COLLABORATION                  │ │
│  │                                                             │ │
│  │   Jira (Stories, PDSupport) ◄──► Confluence (Docs, Design) │ │
│  │                      │                                      │ │
│  │                      ▼                                      │ │
│  │              Git (Source Code)                               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### Why This Matters for Agentic AI

Our ecosystem is **perfectly suited** for agentic workflows because:

1. **Dropwizard Microservices** = Well-structured, modular code that agents understand well
2. **AWS Services** = Well-documented APIs with clear patterns agents can follow
3. **Jira + Confluence** = Machine-readable requirements and documentation
4. **Jenkins CI/CD** = Automated verification pipeline agents can trigger
5. **Git** = Full audit trail agents can read and learn from

The agent doesn't need to understand everything. It needs **skills that describe our patterns** and **MCP tools to query our systems**.

---

## 8. The Adoption Roadmap: From Zero to Agentic

### The Three Pillars, Three Phases

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│     PHASE 1 (Weeks 1-4)        PHASE 2 (Weeks 5-12)              │
│     ─────────────────          ──────────────────                 │
│     Foundation                  Integration                       │
│                                                                    │
│     ┌─────────────────┐       ┌─────────────────────────┐        │
│     │  PILLAR 1:       │       │  PILLAR 2:               │        │
│     │  SKILLS           │       │  MCP CONTEXT SERVER     │        │
│     │                   │       │                         │        │
│     │ • Dev Skills      │       │ • Session Management    │        │
│     │ • QA Skills       │       │ • Jira Integration      │        │
│     │ • Product Skills  │       │ • Confluence Access     │        │
│     │ • Copilot Config  │       │ • Git Operations        │        │
│     └─────────────────┘       │ • Knowledge Base        │        │
│                                 └─────────────────────────┘        │
│                                                                    │
│                       PHASE 3 (Weeks 12-20)                       │
│                       ─────────────────────                       │
│                       Orchestration                                │
│                                                                    │
│                       ┌─────────────────────────┐                 │
│                       │  PILLAR 3:               │                 │
│                       │  CUSTOM AGENTS           │                 │
│                       │                          │                 │
│                       │ • Refactoring Agent      │                 │
│                       │ • Review Agent           │                 │
│                       │ • Research Agent          │                 │
│                       │ • PDSupport Agent        │                 │
│                       └─────────────────────────┘                 │
│                                                                    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  ░░░░░░░░░░░░░░░░░░░░  CONTINUOUS: Team Enablement  ░░░░░░░░░░░  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 9. Pillar 1: Domain-Specific Skills

### The Highest ROI Investment

Skills are **the single most impactful thing we can build** because:

- They cost nothing (just markdown files)
- Every developer benefits immediately
- They encode tribal knowledge that would otherwise live only in people's heads
- They make Claude Opus 4.6 behave like a team member who's read every internal doc

### Skills We Should Build

```
┌────────────────────────────────────────────────────────────────────┐
│                      SKILL CATEGORIES                              │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                 DEVELOPMENT SKILLS                            │ │
│  │                                                              │ │
│  │  dropwizard-microservice     System architecture, resource   │ │
│  │                               patterns, health checks,       │ │
│  │                               Dropwizard conventions         │ │
│  │                                                              │ │
│  │  aws-services                SQS/SNS patterns, DynamoDB      │ │
│  │                               table design, S3 conventions,  │ │
│  │                               SSM parameter naming           │ │
│  │                                                              │ │
│  │  java-refactoring ✅          Module dependencies, Maven     │ │
│  │                               conventions, upgrade workflows │ │
│  │  (Already built!)                                            │ │
│  │                                                              │ │
│  │  jenkins-cicd                Pipeline structure, deployment  │ │
│  │                               stages, build configurations   │ │
│  │                                                              │ │
│  │  ecs-deployment              Task definitions, service       │ │
│  │                               configs, scaling patterns      │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    QA & TESTING SKILLS                        │ │
│  │                                                              │ │
│  │  cucumber-testing            Feature files, step definitions,│ │
│  │                               scenario patterns, tagging     │ │
│  │                                                              │ │
│  │  jmeter-performance          Test plans, thread groups,      │ │
│  │                               assertions, reporting          │ │
│  │                                                              │ │
│  │  integration-testing         Test environment setup, AWS     │ │
│  │                               mocking (LocalStack), test     │ │
│  │                               data management                │ │
│  │                                                              │ │
│  │  test-strategy               What to test, coverage targets, │ │
│  │                               regression approach, edge cases│ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                 PRODUCT & DOMAIN SKILLS                       │ │
│  │                                                              │ │
│  │  business-domain-X           Domain terminology, business    │ │
│  │                               rules, data models, customer   │ │
│  │                               workflows                      │ │
│  │                                                              │ │
│  │  business-domain-Y           (Same for each domain area)     │ │
│  │                                                              │ │
│  │  pdsupport-triage            Common customer issues,         │ │
│  │                               diagnostic steps, known fixes, │ │
│  │                               escalation criteria            │ │
│  │                                                              │ │
│  │  product-requirements        How to read AC, user story      │ │
│  │                               patterns, DOD checklist,       │ │
│  │                               non-functional requirements    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                 CROSS-CUTTING SKILLS                          │ │
│  │                                                              │ │
│  │  session-context ✅           Session management workflow    │ │
│  │  git-operations ✅            Git queries and analysis       │ │
│  │  jira-confluence ✅           Jira/Confluence integration    │ │
│  │  knowledge-base ✅            Filesystem search patterns     │ │
│  │  (Already built!)                                            │ │
│  │                                                              │ │
│  │  code-review                 Review checklist, PR standards, │ │
│  │                               security patterns, naming      │ │
│  │                                                              │ │
│  │  incident-response           Runbook access, log analysis,   │ │
│  │                               RCA template, communication    │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

### Skill File Anatomy

Every skill follows a standard structure:

```markdown
---
name: dropwizard-microservice
description: >
  **WORKFLOW SKILL** — Guide development of Dropwizard microservices.
  USE FOR: creating new endpoints; understanding service architecture;
  Dropwizard conventions and patterns; health checks; configuration.
  DO NOT USE FOR: frontend work; infrastructure provisioning.
  INVOKES: session tools, git tools, kb tools, terminal commands.
---

# Dropwizard Microservice Development Skill

## Architecture Overview
[Describe your service architecture, module layout, key patterns]

## Conventions
[Your team's naming conventions, package structure, patterns]

## Common Workflows
### Adding a New Endpoint
1. Step-by-step with specifics about YOUR codebase
2. Including YOUR package naming conventions
3. Including YOUR testing expectations

### Data Flow
[Describe how data flows through SQS → Service → DynamoDB → SNS]

## Known Gotchas
[Things the agent should watch out for — thread safety, etc.]
```

### Who Writes Which Skills?

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  Developers    →  Development Skills                   │
│                   (architecture, code patterns, AWS)   │
│                                                        │
│  QA/Testers    →  Testing Skills                       │
│                   (Cucumber, JMeter, test strategy)    │
│                                                        │
│  Product Owners →  Domain & Product Skills             │
│                   (business rules, customer workflows) │
│                                                        │
│  DevOps        →  Infrastructure Skills                │
│                   (Jenkins, ECS, deployment)           │
│                                                        │
│  Everyone      →  Review & improve each other's skills │
│                                                        │
└────────────────────────────────────────────────────────┘
```

> *Think of it this way: If a new team member joined tomorrow, what would you tell them? Write that down as a skill. The AI is that perpetual new team member who actually reads the docs and remembers everything.* 📚

---

## 10. Pillar 2: The MCP Context Server

### What We've Already Built

Our MCP Context Server is **production-ready** with five integrated capabilities:

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│              MCP CONTEXT SERVER ARCHITECTURE                      │
│                                                                   │
│       VS Code + GitHub Copilot                                   │
│              │                                                    │
│              │ stdio (local, no network needed)                   │
│              ▼                                                    │
│    ┌─────────────────┐                                           │
│    │   FastMCP Server │  Python 3.11+                            │
│    │   (main.py)      │                                           │
│    └────┬──┬──┬──┬──┬┘                                           │
│         │  │  │  │  │                                             │
│    ┌────┘  │  │  │  └────┐                                       │
│    ▼       ▼  │  ▼       ▼                                       │
│ ┌──────┐┌────┐│┌──────┐┌──────┐                                 │
│ │Sessns││Jira│││Conflu││ Git  │                                 │
│ │      ││    │││ence  ││      │                                 │
│ │JSON  ││REST│││REST  ││Local │                                 │
│ │files ││API ││ API   ││repos │                                 │
│ └──────┘└────┘│└──────┘└──────┘                                 │
│               │                                                   │
│               ▼                                                   │
│          ┌──────┐                                                │
│          │  KB  │                                                │
│          │      │                                                │
│          │Local │                                                │
│          │files │                                                │
│          └──────┘                                                │
│                                                                   │
│  30+ tools registered and available to any agent                 │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Tool Inventory

| Module | Tools | What They Enable |
|---|---|---|
| **Sessions** | `session_create`, `session_get`, `session_list`, `session_add_context`, `session_update_status`, `session_search`, `session_delete` | Persistent memory across conversation boundaries |
| **Jira** | `jira_get_issue`, `jira_search`, `jira_get_comments`, `jira_add_comment` | Agent reads requirements without you copy-pasting |
| **Confluence** | `confluence_get_page`, `confluence_search`, `confluence_space_pages`, `confluence_page_children` | Agent reads design docs and architecture decisions |
| **Git** | `git_status`, `git_log`, `git_diff`, `git_blame`, `git_branches`, `git_file_history`, `git_show_file` | Agent understands code evolution across repos outside workspace |
| **KB** | `kb_search`, `kb_read_file`, `kb_list_directory`, `kb_find_files`, `kb_grep` | Agent finds code patterns and docs across all projects |

### The Session Context Superpower

This is the **secret weapon** against context window limitations:

```
┌────────────────────────────────────────────────────────────────┐
│                   SESSION CONTEXT LIFECYCLE                     │
│                                                                │
│  Conversation 1:                                               │
│  ┌────────────────────────────────────────────────────┐       │
│  │ Developer: "Work on ION-12310"                      │       │
│  │                                                    │       │
│  │ Agent:                                             │       │
│  │   1. session_create("ION-12310 DynamoDB Migration")│       │
│  │   2. jira_get_issue("ION-12310") → reads reqs     │       │
│  │   3. confluence_search("DynamoDB migration") → docs│       │
│  │   4. Makes code changes to modules 1-2 of 5       │       │
│  │   5. session_add_context(progress, decisions)      │       │
│  │                                                    │       │
│  │ [Context window getting full → start new chat]     │       │
│  └────────────────────────────────────────────────────┘       │
│                        │                                       │
│                        │  Session persists to disk             │
│                        ▼                                       │
│  Conversation 2:                                               │
│  ┌────────────────────────────────────────────────────┐       │
│  │ Developer: "Continue ION-12310"                     │       │
│  │                                                    │       │
│  │ Agent:                                             │       │
│  │   1. session_get(id) → loads all prior context     │       │
│  │   2. "I see modules 1-2 are done. Picking up at   │       │
│  │       module 3. Previous decision: use new SDK..."  │       │
│  │   3. Continues from exactly where it left off      │       │
│  │   4. session_add_context(progress)                 │       │
│  └────────────────────────────────────────────────────┘       │
│                        │                                       │
│                        ▼                                       │
│  Conversation 3:                                               │
│  ┌────────────────────────────────────────────────────┐       │
│  │ Developer: "Finish ION-12310"                       │       │
│  │                                                    │       │
│  │ Agent:                                             │       │
│  │   1. session_get(id) → all accumulated context     │       │
│  │   2. Completes modules 4-5, runs full test suite   │       │
│  │   3. session_update_status("completed")            │       │
│  │   4. jira_add_comment("ION-12310", "Done: ...")    │       │
│  └────────────────────────────────────────────────────┘       │
│                                                                │
│  Result: Complex task completed across 3 conversations        │
│  with ZERO context loss. 🎯                                   │
└────────────────────────────────────────────────────────────────┘
```

### What's Next for the MCP Server

Potential enhancements based on team needs:

| Enhancement | Benefit |
|---|---|
| **Jenkins Integration** | Agent triggers builds, monitors results |
| **AWS SSM Lookups** | Agent reads config parameters for debugging |
| **Code Review Tools** | Automated review checklist execution |
| **Metrics/Monitoring** | Agent queries DataDog/CloudWatch for incident context |
| **Team Calendar** | Agent knows who to ask about which module |

---

## 11. Pillar 3: Custom Agent Orchestration

### When to Build Custom Agents (Phase 3)

Remember: **don't build a Ferrari from spare parts when Copilot already drives.** 🏎️

Custom agents are warranted when:
- You need the AI to behave *differently* for different task types
- You want to restrict which tools the AI can access (read-only for review, read-write for refactoring)
- You need repeatable multi-step workflows that always follow the same pattern

### Agent Archetypes We Can Build

```
┌────────────────────────────────────────────────────────────────────┐
│                     AGENT ARCHETYPES                               │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  🔧  REFACTORING AGENT                                       │ │
│  │                                                              │ │
│  │  Role: Make code changes methodically                        │ │
│  │  Skills: java-refactoring, dropwizard-microservice           │ │
│  │  Tools: All MCP tools + edit + terminal                      │ │
│  │  Rule: Always compile & test after changes                   │ │
│  │  Rule: Track every step in session context                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  🔍  RESEARCH AGENT                                          │ │
│  │                                                              │ │
│  │  Role: Gather information, never modify                      │ │
│  │  Skills: knowledge-base, git-operations, jira-confluence     │ │
│  │  Tools: Read-only MCP tools (no edit, no terminal)           │ │
│  │  Rule: Produce findings as structured session context        │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  📋  REVIEW AGENT                                            │ │
│  │                                                              │ │
│  │  Role: Check changes against standards                       │ │
│  │  Skills: code-review, test-strategy                          │ │
│  │  Tools: git_diff, git_blame, kb_grep                        │ │
│  │  Rule: Produce actionable feedback, categorized by severity  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  🚨  PDSUPPORT TRIAGE AGENT                                  │ │
│  │                                                              │ │
│  │  Role: Analyze customer issues, suggest fixes                │ │
│  │  Skills: pdsupport-triage, business-domain-X                 │ │
│  │  Tools: jira_get_issue, kb_grep, git_log, session context   │ │
│  │  Rule: Check known issues DB first, include customer impact  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  📊  PRODUCT ANALYST AGENT                                   │ │
│  │                                                              │ │
│  │  Role: Analyze requirements from product lens                │ │
│  │  Skills: product-requirements, business-domain-X             │ │
│  │  Tools: jira_search, confluence_search                       │ │
│  │  Rule: Always consider customer impact and business value    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### The Orchestration Flow

```
   Developer: "Pick up ION-12310 and implement it"
         │
         ▼
   ┌──────────────┐
   │  Copilot +    │    Step 1: Understand
   │  Claude Opus  │◄── Read Jira ticket + Confluence docs
   │               │    (using jira-confluence SKILL)
   └──────┬───────┘
          │
          ▼         Step 2: Research
   ┌──────────────┐
   │  Research     │◄── Find all affected code, assess impact
   │  Sub-Agent    │    (using knowledge-base + git-operations SKILLS)
   └──────┬───────┘
          │
          ▼         Step 3: Plan
   ┌──────────────┐
   │  Copilot +    │◄── Create implementation plan,
   │  Claude Opus  │    track in session context
   └──────┬───────┘
          │
          ▼         Step 4: Implement
   ┌──────────────┐
   │  Copilot +    │◄── Make changes, compile, test
   │  Claude Opus  │    (using java-refactoring SKILL)
   └──────┬───────┘
          │
          ▼         Step 5: Verify
   ┌──────────────┐
   │  Review       │◄── Check against standards
   │  Sub-Agent    │    (using code-review SKILL)
   └──────┬───────┘
          │
          ▼
   Done. Context saved. PR ready.
```

---

## 12. Workflow Examples: A Day in the Life

### Example 1: Developer Working a User Story

```
┌──────────────────────────────────────────────────────────────────┐
│  SCENARIO: Implement ION-12310 — New SQS listener for            │
│            order processing notifications                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DEVELOPER:                                                      │
│  "Pick up ION-12310. Read the requirements, find related         │
│   code patterns for SQS listeners, and create a plan."           │
│                                                                  │
│  AGENT (Claude Opus 4.6):                                        │
│                                                                  │
│  ✅ session_create("ION-12310 SQS Order Notifications")          │
│  ✅ jira_get_issue("ION-12310")                                  │
│      → Requirements: Listen for OrderProcessed events,           │
│        update DynamoDB, send SNS notification on completion      │
│  ✅ confluence_search("order processing architecture")            │
│      → Found: ADR-042 describing event flow                     │
│  ✅ kb_grep("@SQSListener", "*.java")                            │
│      → 3 existing listeners as reference patterns                │
│  ✅ kb_grep("SqsBundle", "*.java")                               │
│      → Dropwizard bundle registration pattern found             │
│                                                                  │
│  AGENT PRODUCES:                                                 │
│  "Here's what I found and my implementation plan:                │
│                                                                  │
│   Requirements from ION-12310:                                   │
│   - [summary of AC items]                                        │
│                                                                  │
│   From confluence ADR-042:                                       │
│   - [key architectural decisions]                                │
│                                                                  │
│   Existing patterns to follow:                                   │
│   - OrderCreatedListener.java (best match)                       │
│   - PaymentProcessedListener.java                                │
│                                                                  │
│   Implementation plan:                                           │
│   1. Create OrderProcessedListener extends BaseSqsListener       │
│   2. Add DynamoDB update in handler                              │
│   3. Add SNS notification publish                                │
│   4. Register in SqsBundle                                       │
│   5. Add Cucumber scenarios                                      │
│   6. Update deployment config for new queue                      │
│                                                                  │
│   Shall I proceed?"                                              │
│                                                                  │
│  DEVELOPER: "Go"                                                 │
│                                                                  │
│  [Agent implements, tests, tracks progress in session]           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Example 2: PDSupport Bug Resolution

```
┌──────────────────────────────────────────────────────────────────┐
│  SCENARIO: Customer reports orders stuck in "processing" state   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DEVELOPER:                                                      │
│  "PDSupport ticket PDS-5678. Customer says orders are stuck.     │
│   Help me diagnose."                                             │
│                                                                  │
│  AGENT:                                                          │
│                                                                  │
│  ✅ jira_get_issue("PDS-5678") → reads customer report           │
│  ✅ session_search("orders stuck processing")                     │
│      → Found! Session from 3 months ago: "Similar issue caused  │
│        by SQS visibility timeout being too short for large       │
│        batches. Fixed by increasing to 300s in ION-11280."      │
│                                                                  │
│  AGENT:                                                          │
│  "I found a historical session matching this issue.              │
│   ION-11280 (3 months ago) had the same symptom. The root       │
│   cause was SQS visibility timeout. Let me check if this        │
│   was deployed to the affected customer's environment..."        │
│                                                                  │
│  ✅ kb_grep("visibilityTimeout", "*.java")                       │
│  ✅ git_log(path="src/.../SqsConfig.java")                       │
│                                                                  │
│  "The fix from ION-11280 was merged to main but the             │
│   customer is on release 4.2.1 which predates it. This is       │
│   a known issue with a known fix. Recommend deploying           │
│   release 4.3.0+ or cherry-picking commit abc1234."             │
│                                                                  │
│  Time to resolution: 5 minutes instead of 2 hours. 🎯           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Example 3: Product Owner Analyzing Requirements

```
┌──────────────────────────────────────────────────────────────────┐
│  SCENARIO: PO preparing sprint planning                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PRODUCT OWNER:                                                  │
│  "Search Jira for all open stories in the Order Management       │
│   domain. Cross-reference with Confluence for any design         │
│   docs. Summarize what's ready for development."                 │
│                                                                  │
│  AGENT:                                                          │
│                                                                  │
│  ✅ jira_search('project=ION AND component="Order Management"    │
│      AND status IN ("To Do","Refined") ORDER BY priority')       │
│  ✅ confluence_search('label="order-management" AND               │
│      label="design-doc"')                                        │
│                                                                  │
│  AGENT PRODUCES:                                                 │
│  "Found 8 stories. Here's the readiness analysis:                │
│                                                                  │
│   READY (has AC + design doc):                                   │
│   • ION-12310: Order notification processing  [P1, 5pts]        │
│   • ION-12315: Bulk order status update API   [P2, 8pts]        │
│                                                                  │
│   NEEDS DESIGN DOC:                                              │
│   • ION-12320: Order archival policy          [P2, 13pts]       │
│   • ION-12325: Multi-currency order support   [P1, 21pts]       │
│                                                                  │
│   NEEDS REFINEMENT (vague AC):                                   │
│   • ION-12330: 'Improve order performance'    [no estimate]     │
│                                                                  │
│   Recommendation: ION-12310 and ION-12315 are sprint-ready.     │
│   ION-12325 is high priority and needs a design session         │
│   before it can be developed."                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Example 4: QA Engineer Writing Test Scenarios

```
┌──────────────────────────────────────────────────────────────────┐
│  SCENARIO: QA writing Cucumber scenarios for a new feature       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  QA ENGINEER:                                                    │
│  "I need Cucumber scenarios for ION-12310. Use the acceptance    │
│   criteria from Jira and follow our existing test patterns."     │
│                                                                  │
│  AGENT:                                                          │
│                                                                  │
│  ✅ jira_get_issue("ION-12310") → reads acceptance criteria      │
│  ✅ kb_find_files("*.feature", root="tests/")                    │
│  ✅ kb_read_file("tests/features/order-creation.feature")        │
│      → learns the team's Gherkin style and patterns             │
│                                                                  │
│  AGENT PRODUCES:                                                 │
│  Feature file matching AC + team conventions, including:        │
│  • Happy path scenarios                                          │
│  • Error scenarios (invalid order, timeout, duplicate)           │
│  • Edge cases (large batch, special characters)                  │
│  • Performance scenario (1000 orders in < 30s)                   │
│                                                                  │
│  All written in the team's established Gherkin style.            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 13. Adoption Strategy: Getting the Whole Team On Board

### The Ripple Approach

Don't try to get everyone to adopt everything at once. Ripple outward from a **core team of champions**.

```
                     ┌─────────────┐
                     │ Champions   │  2-3 developers who are
                     │ (Week 1-2)  │  already excited about AI
                     └──────┬──────┘
                            │
                ┌───────────┴───────────┐
                │    Early Adopters      │  One team, all roles
                │    (Week 3-6)          │  (dev, QA, PO)
                └───────────┬───────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │         Broader Rollout            │  All product teams
          │         (Week 7-16)                │  with training
          └─────────────────┬─────────────────┘
                            │
    ┌───────────────────────┴───────────────────────┐
    │              Full Organization                  │  Standard practice
    │              (Week 16+)                         │
    └─────────────────────────────────────────────────┘
```

### Concrete Steps

#### Week 1-2: Champions Setup

| Step | Action | Owner |
|---|---|---|
| 1 | Install VS Code + GitHub Copilot with Claude Opus 4.6 | Champions |
| 2 | Deploy MCP Context Server locally | Champions |
| 3 | Write first 2-3 development skills | Champions |
| 4 | Document setup guide for team | Champions |

#### Week 3-6: Early Adopter Team

| Step | Action | Owner |
|---|---|---|
| 5 | Onboard one complete team (dev + QA + PO) | Champions + Team |
| 6 | Each role writes skills for their domain | Whole team |
| 7 | Use agent workflow for 2-3 real Jira tickets | Developers |
| 8 | Write Cucumber/JMeter skills | QA |
| 9 | Write product domain skills | PO |
| 10 | Retrospective: what worked, what didn't | Whole team |

#### Week 7-16: Broader Rollout

| Step | Action | Owner |
|---|---|---|
| 11 | Create video tutorials / lunch-and-learns | Champions |
| 12 | Pair programming sessions: AI-assisted | Champions + Teams |
| 13 | Shared skill library across teams | All |
| 14 | MCP server enhancements based on feedback | Platform team |
| 15 | Measure productivity metrics | Leads |

#### Week 16+: Full Organization

| Step | Action | Owner |
|---|---|---|
| 16 | AI agent usage is standard for all development | All |
| 17 | Skills are maintained like code (PRs, reviews) | All |
| 18 | New joiners learn the AI-assisted workflow in onboarding | HR + Leads |

### The Training Playbook

```
┌────────────────────────────────────────────────────────────────┐
│                    TRAINING MODULES                             │
│                                                                │
│  Module 1: "Hey Copilot" (30 min)                             │
│  ─────────────────────────────                                │
│  Basic Copilot Chat usage, inline completions,                │
│  how to write effective prompts.                               │
│  Audience: Everyone                                            │
│                                                                │
│  Module 2: "Give It a Goal" (60 min)                          │
│  ─────────────────────────────────                             │
│  Multi-step tasks with Claude Opus 4.6, todo lists,           │
│  providing context, iterating on output.                       │
│  Audience: All developers & QA                                 │
│                                                                │
│  Module 3: "Skills that Kill" (60 min)                        │
│  ──────────────────────────────────                            │
│  Writing effective skill files, YAML frontmatter,             │
│  skill invocation patterns, testing skills.                    │
│  Audience: Skill authors (all roles)                          │
│                                                                │
│  Module 4: "MCP & Beyond" (90 min)                            │
│  ────────────────────────────────                              │
│  Setting up MCP server, using Jira/Confluence tools,          │
│  session context workflows, troubleshooting.                   │
│  Audience: All developers                                      │
│                                                                │
│  Module 5: "The Product Mindset" (60 min)                     │
│  ────────────────────────────────────                          │
│  Using AI to think about customer problems, not just code.    │
│  Requirement analysis, architecture decisions,                 │
│  writing skills from product perspective.                      │
│  Audience: POs + Tech Leads                                   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 14. Measuring Success

### What to Measure (And What Not To)

> *"Not everything that counts can be counted, and not everything that can be counted counts." — Einstein (probably while debugging)*

#### Quantitative Metrics

| Metric | Baseline | Target | How to Measure |
|---|---|---|---|
| **Context gathering time** | ~4 hrs/day | ~1 hr/day | Developer survey |
| **Time to first commit** (story start → first push) | 2+ days | < 1 day | Git analytics |
| **PDSupport resolution time** | Hours-days | Minutes-hours | Jira metrics |
| **Defect escape rate** | Current baseline | -30% | QA metrics |
| **PR review cycle time** | Days | Hours | Git analytics |
| **Test coverage of new code** | Variable | >80% consistent | CI reports |

#### Qualitative Metrics

| Metric | How to Measure |
|---|---|
| **Developer satisfaction** | Monthly pulse survey |
| **Confidence in changes** | "Do you feel more confident pushing code?" |
| **Product understanding** | "Can you explain why this feature matters to customers?" |
| **Knowledge sharing** | Number and quality of skills contributed |
| **Onboarding speed** | Time for new joiners to make first meaningful PR |

### Success is NOT Measured By

- Lines of code generated (vanity metric)
- Number of AI interactions per day (usage ≠ value)
- Speed of writing code (fast code ≠ good code)
- Reducing headcount (this is about amplifying humans, not replacing them)

---

## 15. Risks, Guardrails & Governance

### Real Risks and Real Mitigations

```
┌────────────────────────────────────────────────────────────────┐
│  RISK                          │  MITIGATION                   │
├────────────────────────────────┼───────────────────────────────┤
│                                │                               │
│  AI generates insecure code    │  Security skills with OWASP  │
│                                │  patterns, PR review process  │
│                                │  unchanged                    │
│                                │                               │
│  Over-reliance on AI           │  Developers must understand   │
│                                │  and approve all changes.     │
│                                │  AI assists, humans decide.   │
│                                │                               │
│  Sensitive data exposure       │  MCP server runs locally.     │
│                                │  No data leaves the machine.  │
│                                │  API tokens in env vars only. │
│                                │                               │
│  Skills become stale           │  Skills live in Git repos.    │
│                                │  Review in retros. Ownership  │
│                                │  assigned like code modules.  │
│                                │                               │
│  Context window exhaustion     │  Session persistence solves   │
│                                │  this. Plus: skill-based      │
│                                │  on-demand loading.           │
│                                │                               │
│  "It works on my machine"      │  Standardized setup guide.    │
│  (AI setup inconsistency)     │  Version-locked MCP server.   │
│                                │  Shared skill definitions.    │
│                                │                               │
│  Token/API cost concerns       │  Claude Opus 4.6 efficient    │
│                                │  with detailed goals. Skills  │
│                                │  reduce redundant queries.    │
│                                │  Sessions prevent re-work.    │
│                                │                               │
└────────────────────────────────┴───────────────────────────────┘
```

### The Golden Rules

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   1. AI ASSISTS. HUMANS DECIDE.                                ║
║      Every code change is reviewed by a human.                 ║
║      Every architecture decision is owned by a human.          ║
║      AI is the world's best intern, not the tech lead.        ║
║                                                                ║
║   2. NO SENSITIVE DATA IN PROMPTS.                             ║
║      Credentials, customer-identifying data, and secrets       ║
║      never go into AI prompts. Period.                         ║
║                                                                ║
║   3. SKILLS ARE CODE. TREAT THEM THAT WAY.                     ║
║      PR review for skill changes.                              ║
║      Version control. Ownership. Testing.                      ║
║                                                                ║
║   4. PRODUCT FIRST, CODE SECOND.                               ║
║      Use AI to understand the WHY before the HOW.              ║
║      A brilliantly coded wrong solution helps nobody.          ║
║                                                                ║
║   5. SHARE WHAT WORKS. DEPRECATE WHAT DOESN'T.                ║
║      We learn together.                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 16. FAQ

### "Isn't this just fancy autocomplete?"

No. Autocomplete predicts the next few tokens. Agentic AI reads your Jira ticket, searches your codebase, references your architecture docs, follows your team's patterns, makes changes across multiple files, compiles, tests, and iterates — all while tracking progress for the next session. That's not autocomplete. That's a colleague.

### "Will this replace developers?"

Absolutely not. It makes developers 2-5x more productive at the parts of their job that are mechanical (boilerplate, context gathering, pattern replication) so they can spend more time on the parts that are creative (design, architecture, customer empathy, solving novel problems). The best chefs don't hand-grind their spices — they spend that time creating new dishes.

### "What about code quality?"

This should *improve* code quality. Skills encode your best patterns. AI generates code that follows those patterns *consistently*, not just when the developer remembers. Plus, the review agent can check every change against your standards — something humans often skip when they're rushed.

### "I tried Copilot and it kept getting things wrong."

That's the difference between using Copilot as autocomplete (Level 1) versus using it as a skill-augmented, context-connected agent (Level 3-4). With detailed skills and MCP tools providing real context, the quality of output improves dramatically. It's the difference between asking someone "write me a function" versus "here's our architecture, our conventions, the requirements, the related code, and our test patterns — now implement this feature."

### "The context window fills up and everything degrades."

That's exactly why we built the session context system. When the window fills up, start a new conversation. The session persists your decisions, progress, and context. The next conversation picks up right where you left off with a fresh, clean context window. Think of it as save points in a video game. 🎮

### "How much time does it take to write skills?"

A good skill takes 1-3 hours to write initially. That skill then saves every developer on the team hours of context gathering on every related task, forever. The ROI is extraordinary. And skills get better over time as you refine them.

### "What if the AI does something destructive?"

The AI always asks for confirmation before destructive actions (dropping tables, force pushing, deleting files). The MCP server runs locally with no cloud access. Skills include guardrails and "DO NOT" rules. And ultimately — humans review and approve all changes before they ship. We trust but verify.

### "What about our interns and junior developers?"

This is where the magic really shines. Junior developers suddenly have access to all the institutional knowledge that would normally take years to absorb. The skills encode senior developers' wisdom. The MCP server gives them access to context they wouldn't know to look for. It's like pair programming with every senior on the team simultaneously.

---

## Appendix A: Quick-Start Setup Guide

### For Every Developer (15 minutes)

```bash
# 1. Ensure VS Code with GitHub Copilot extension is installed.

# 2. Configure Claude Opus 4.6 as the preferred model in Copilot settings.

# 3. Clone and set up the MCP Context Server:
cd "C:\Users\<you>\projects"
git clone <mcp-context-server-repo-url>
cd mcp-context-server
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"

# 4. Configure (minimum viable):
cp .env.example .env
# Edit .env with your Jira email, API token, Confluence URL, 
# and local project paths for KB_ROOTS and GIT_DEFAULT_REPOS

# 5. Add to VS Code workspace (create .vscode/mcp.json):
# Follow template in mcp-config-for-vscode.json

# 6. Verify: Open Copilot Chat and ask 
#    "List all active sessions"
#    If it calls session_list, you're good! 🎉
```

### For Skill Authors (5 minutes per skill)

```bash
# 1. Create skill directory in your repo:
mkdir -p .github/skills/<skill-name>/

# 2. Create SKILL.md with YAML frontmatter:
# See examples in the MCP server repo under .github/skills/

# 3. Test: In Copilot Chat, mention a task that should 
#    trigger your skill. Verify it loads and follows the workflow.
```

---

## Appendix B: The Big Picture — Agentic AI in Our SDLC

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                    THE AGENTIC SDLC                                 │
│                                                                     │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐ │
│  │ DISCOVER  │───►│  DESIGN   │───►│  DEVELOP  │───►│   TEST    │ │
│  │           │    │           │    │           │    │           │ │
│  │ Agent     │    │ Agent     │    │ Agent     │    │ Agent     │ │
│  │ reads     │    │ searches  │    │ reads     │    │ reads AC  │ │
│  │ Jira      │    │ Confluence│    │ skills,   │    │ + test    │ │
│  │ tickets,  │    │ for ADRs, │    │ follows   │    │ skills,   │ │
│  │ searches  │    │ suggests  │    │ patterns, │    │ generates │ │
│  │ historical│    │ patterns  │    │ implements│    │ Cucumber  │ │
│  │ sessions  │    │ from KB   │    │ & tracks  │    │ + JMeter  │ │
│  │           │    │           │    │ progress  │    │ scenarios │ │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘ │
│       │                │                │                │         │
│       ▼                ▼                ▼                ▼         │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐ │
│  │  REVIEW   │───►│  DEPLOY   │───►│  SUPPORT  │───►│  LEARN    │ │
│  │           │    │           │    │           │    │           │ │
│  │ Agent     │    │ Agent     │    │ Agent     │    │ Agent     │ │
│  │ checks    │    │ reads     │    │ searches  │    │ stores    │ │
│  │ git diff, │    │ infra     │    │ sessions  │    │ findings  │ │
│  │ applies   │    │ skills,   │    │ for known │    │ in session│ │
│  │ review    │    │ verifies  │    │ issues,   │    │ context   │ │
│  │ checklist │    │ config    │    │ diagnoses │    │ for next  │ │
│  │ from skill│    │ readiness │    │ quickly   │    │ time      │ │
│  │           │    │           │    │           │    │           │ │
│  └───────────┘    └───────────┘    └───────────┘    └───────────┘ │
│                                                                     │
│                    ◄─── Session Context persists across ───►       │
│                         all phases and conversations               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Appendix C: Additional Ideas & Opportunities

### Things We Haven't Discussed Yet (But Should)

1. **Shared Skill Library**: A central Git repository of skills that all teams contribute to and benefit from. Skills for common patterns (error handling, logging, health checks) benefit everyone.

2. **Skill Quality Scores**: Track which skills produce the best outcomes. Agent track records — which skills are invoked most, which lead to successful outcomes (clean builds, passing tests) and which need refinement.

3. **Onboarding Accelerator**: New team members start with a guided agent workflow that walks them through the codebase, architecture, and team conventions using skills and the knowledge base.

4. **Architecture Decision Records (ADR) Generation**: When the agent helps make architectural decisions, it can automatically draft ADRs in Confluence format.

5. **Sprint Retrospective Intelligence**: Session context accumulated over a sprint can be analyzed for patterns — what types of tasks took longest, what blockers recurred, what skills need updating.

6. **Cross-Team Knowledge Pollination**: When Team A solves a problem, the session context and any new skills become discoverable by Team B through session_search.

7. **Customer Impact Scoring**: Skills that teach the agent to always assess and articulate the customer impact of technical decisions.

8. **Automated Technical Debt Tracking**: Agent identifies and records tech debt as it works through code, creating a living inventory that's always current.

---

## Closing Thoughts

> *"The future is already here — it's just not evenly distributed."* — William Gibson

We have the technology. We have the tools (literally — we *built* the MCP server). We have talented developers who deeply care about the products they create. What we need now is a systematic path to put these pieces together.

The Agentic AI adoption isn't about replacing human judgment with machine speed. It's about **amplifying human creativity by automating the mechanical** — so our developers spend less time copy-pasting between Jira and their IDE, and more time thinking about what truly delights our customers.

Start with Skills. Connect with MCP. Orchestrate with Agents when needed. **And remember: if GitHub Copilot already does it well, just use it. No need to build a Ferrari from spare parts.** 🏎️

The path to 100% agentic workflow isn't a single leap — it's a series of small, additive improvements where each step immediately delivers value. And the best part? The AI gets better as we write more skills and accumulate more session context. It's a virtuous cycle that compounds over time.

Let's build something we're deeply proud of. Together, with our AI teammates.

---

*Document prepared for Product & Development leadership. For questions, feedback, or to volunteer as a champion, reach out to the AI Engineering team.*

*Last updated: March 2026*
