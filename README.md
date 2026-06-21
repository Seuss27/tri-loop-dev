# Tri-Loop Dev: Multi-Agent Architecture

A stateful, multi-agent system built on LangGraph, Pydantic, and OpenTofu. This architecture enforces strict data contracts between autonomous personas to manage token spend, prevent hallucination loops, and ensure deterministic system design.

## 🏗 Architecture Overview

The system utilizes a 3-stage progression loop, where data flows downstream into progressively stricter schemas:

1. **The Product Manager (PM) Loop:** Extracts and clarifies raw user intent into a validated Product Requirements Document (PRD).
2. **The Architect Loop:** Consumes the PRD to design system boundaries, API contracts, and infrastructure requirements without writing execution code.
3. **The Coder Loop:** Executes the Architect's design step-by-step, utilizing sandboxed tools and self-correcting debug loops.

## 🛠 Prerequisites

* **Python 3.12+**
* **Hatch** (for strict dependency and environment management)
* **OpenTofu** (for infrastructure provisioning)

## 🚀 Quick Start

1. **Clone and Configure Environment**

   ```bash
   git clone [https://github.com/Seuss27/tri-loop-dev.git](https://github.com/Seuss27/tri-loop-dev.git)
   cd tri-loop-dev
   cp .env.example .env
