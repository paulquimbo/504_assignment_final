### Confidence and uncertainties

- **Most confident:**  
  - **Anonymous intake design** that minimizes PHI while retaining age/sex for relevance.  
  - **Serverless ETL** with strict validation ranges and clear separation of responsibilities across layers.

- **Least sure:**  
  - **Clinical fidelity** of generalized guidance without personalized context; requires conservative prompts and rule safety nets.  
  - **Edge cases** and multi-symptom interactions; balancing simple thresholds with AI outputs.

### Alternative architecture considered

- **Client-only triage (no backend storage):**  
  - **Why not chosen:** Limits auditability, safety controls, and improvement loops; the cloud pipeline enables controlled AI usage, rate limiting, logging, and iterative refinement.

### Next steps with 4–8 more weeks and unlimited credits

- **Dual-layer decision support:** Combine a **rule engine** (red flags, vital thresholds) with **LLM scoring**; present both to users for transparency and safety.  
- **Governance & observability:** Prompt versioning, inference logs, explainability notes, bias monitoring by age/sex cohorts, periodic clinical reviews.  
- **Localization & accessibility:** Multilingual interfaces, screen-reader support, low-bandwidth modes, and inclusive UI design.  
- **Scalability & reliability:** VNET integration, autoscaling Container Apps, regional failover, robust telemetry and alerting, disaster recovery plans.

---