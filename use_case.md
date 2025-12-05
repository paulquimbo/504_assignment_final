# Project Overview
# AI-Assisted Self-Triage with Anonymous Intake and Vital Signs

This project provides a **privacy-first cloud workflow** for anonymous health input.  
Users can submit symptoms and vital signs without sharing personal identifiers.  
The system delivers immediate **AI-assisted severity assessment** and **general care guidance**.  

Only minimal demographics (age, sex) are collected to support safe and consistent triage.


**NOTE:** This tool provides general guidance only. It is **NOT** a medical diagnosis or a substitute for professional care.

---

## Problem Statement

### Clinical Challenge
People often struggle to decide if symptoms can be managed at home, need a routine visit, or require urgent care.  
Phone triage lines are resource-heavy and inconsistent.

An anonymous AI-assisted tool can:
- Standardize guidance  
- Reduce uncertainty  
- Route patients appropriately  
- Protect user privacy  

### Users
- **Public users** – Submit symptoms/vitals anonymously and receive instant guidance  
- **Healthcare organizations (optional)** – View de-identified aggregate trends for planning and forecasting  

### Core Goals
- Fully anonymous intake (no personal identifiers)  
- Collect only: symptoms, duration, pain score, fever, blood pressure, pulse, age, sex  
- Provide standardized, rule + AI-enhanced severity estimates  
- Show disclaimers at every step  
- Improve continuously via aggregated (not individual) data  

---

## Data Sources

| Source                   | Fields                                                                 | Notes                        |
|--------------------------|------------------------------------------------------------------------|------------------------------|
| Anonymous intake         | Symptoms, duration, pain score, fever, blood pressure, pulse, age, sex | Submitted via form/JSON      |
| Clinical rules           | Red-flag symptoms, age/sex thresholds for vitals                       | Embedded or configurable     |
| Historical aggregates    | De-identified past submissions                                         | Used for calibration/metrics |

## Basic Workflow
1. **User Input**  
   - Symptoms + vitals submitted via Flask form (age & sex only, no PII).

2. **Data Storage & Processing**  
   - Saved in Azure Blob Storage  
   - Azure Function validates ranges & normalizes units

3. **Database Staging**  
   - Data stored in Azure SQL (staging table)

4. **AI Analysis**  
   - Batch job calls Azure OpenAI / ML  
   - Severity score + rationale saved in `ai_scores`

5. **Results Display**  
   - Flask page shows severity level, guidance, and disclaimer

6. **Feedback Loop**  
   - Optional anonymous feedback collected  
   - Used for model/prompt refinement + clinical rule review