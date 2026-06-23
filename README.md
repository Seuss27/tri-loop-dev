# Tri-Loop Dev: Multi-Agent Architecture

A stateful, multi-agent system built on LangGraph, Pydantic, and OpenTofu.
This architecture enforces strict data contracts between autonomous personas
to manage token spend, prevent hallucination loops, and ensure deterministic
system design.

## 🏗 Architecture Overview

The system utilizes a 3-stage progression loop, where data flows downstream
into progressively stricter schemas:

1. **The Product Manager (PM) Loop:** Extracts and clarifies raw user intent
   into a validated Product Requirements Document (PRD). Uses lightweight LLMs
   to optimize costs.
2. **The Architect Loop:** Consumes the PRD to design system boundaries, API
   contracts, and infrastructure requirements without writing execution code.
   Uses heavy reasoning LLMs.
3. **The Coder Loop:** Executes the Architect's design step-by-step, utilizing
   sandboxed tools and self-correcting debug loops.

## 🔌 Pluggable LLM Backend

Tri-Loop features a provider-agnostic factory pattern. You can seamlessly swap
the intelligence engine driving the agents without altering the core graph logic.
The active provider and models are managed entirely via environment variables
(`PRIMARY_LLM_PROVIDER`), currently supporting Anthropic, Google Gemini, and
AWS Bedrock.

## 🛠 Prerequisites

* **Python 3.12+**
* **Hatch** (for strict dependency and environment management)
* **OpenTofu** (for infrastructure provisioning)

## 🚀 Quick Start & Local MVP

1. **Clone and Configure Environment**

   ```bash
   git clone [https://github.com/Seuss27/tri-loop-dev.git](https://github.com/Seuss27/tri-loop-dev.git)
   cd tri-loop-dev
   cp .env.example .env
   ```

2. **Set API Credentials**
   Edit your `.env` file to set your `PRIMARY_LLM_PROVIDER` and paste the
   corresponding API key (e.g., Anthropic or Google).

3. **Run the Local MVP**
   Execute the local state-routing test via Hatch. This will initialize the
   graph, prompt the PM agent, pause for human approval, and complete the loop.

   ```bash

   hatch run python run_mvp.py
   ```
