# SaaS Subscription Funnel & 1-Click Sign-Up A/B Test

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/Statsmodels-Hypothesis_Testing-blueviolet.svg)](https://www.statsmodels.org/)

**[View the Interactive Tableau Executive Dashboard](https://public.tableau.com:9443/views/SaaSABTest/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)** 

## Executive Summary
This project analyzes 4.2 million raw e-commerce clickstream events mapped to a SaaS subscription funnel. Baseline analysis identified a 94.6% top-of-funnel drop-off rate. A simulated A/B test for a "1-Click" sign-up flow was modeled and analyzed. The variant increased trial sign-ups by a relative 27.4% (p-value: 9.76e-279). Deploying this variant to 100% of site traffic projects an estimated **$4,001,792 increase in Annual Recurring Revenue (ARR)**.

![Tableau Executive Dashboard](images/SaaS%20Dashboard%20A_B.png)

## Business Context
Analysis of 1.36 million unique site visitors revealed a distinct activation bottleneck:
* **Downstream Efficiency:** The Trial-to-Paid conversion rate is 84.01%.
* **The Bottleneck:** Only 5.32% of site visitors successfully started a trial under the legacy onboarding flow. 

Given the high downstream retention, optimizing the top-of-funnel drop-off presented the highest-leverage opportunity for revenue growth.

## Data & Methodology
* **Dataset:** 4.2 million events cleaned and mapped to a SaaS funnel (Site Visit -> Trial Started -> Premium Paid).
* **Experimental Design:** 1,363,325 unique users randomly assigned to a 50/50 A/B split. 
  * **Control:** Legacy multi-field sign-up page.
  * **Variant:** Streamlined 1-click email sign-up.
* **Statistical Testing:** Two-Sample Z-Test for Proportions ($\alpha = 0.05$).
* **Tech Stack:** Python (Pandas, NumPy) for data engineering, `statsmodels` for inferential statistics, and Tableau for BI visualization.

## Phase 1: Baseline Funnel Analysis
* **Total Unique Visitors:** 1,363,325
* **Unique Trial Starts:** 72,482
* **Unique Premium Paid:** 60,895
* **Visit-to-Trial Conversion:** 5.32% 
* **Trial-to-Paid Conversion:** 84.01%

## Phase 2: A/B Testing Results
* **Null Hypothesis (H0):** The 1-click sign-up flow has no effect on Visit-to-Trial conversion rates.
* **Alternative Hypothesis (H1):** The 1-click sign-up flow increases Visit-to-Trial conversions.

**Metrics:**
* **Control Group Conversion:** 5.31% (36,214 trials / 681,612 visitors)
* **Variant Group Conversion:** 6.77% (46,144 trials / 681,713 visitors)

**Statistical Output:**
* **Z-Statistic:** 35.6747
* **P-Value:** 9.76e-279
* **Verdict:** Statistically Significant. The null hypothesis is rejected.

## Phase 3: Visual Analytics
The Tableau Executive Dashboard includes:
* **Funnel Comparison:** Side-by-side bar chart detailing exact volume drop-off between Control and Variant groups.
* **Daily Conversion Trend:** Time-series line chart demonstrating Variant group outperformance across the month-long test, controlling for day-of-week seasonality.

## Revenue Impact
* **Absolute Conversion Lift:** +1.46%
* **Relative Conversion Lift:** +27.40%
* **Projected Extra Paying Users:** 16,674 per month (applying the 84% trial-to-paid rate).

Assuming a standard SaaS price point of $20/month ($240/year), rolling this feature out to 100% of site traffic yields a **Projected ARR Increase of $4,001,792.29**.

## Repository Structure
```text
├── data/
│   ├── 2019-Oct.csv                      # Raw dataset (Excluded from repo due to size)
│   └── saas_funnel_export_with_dates.csv # Cleaned BI export for Tableau
├── scripts/
│   └── saas_ab_test_analysis.py          # EDA, cleaning, and statistical testing code (Spyder)
├── images/
│   └── SaaS Dashboard A_B.png            # High-res image of the Tableau dashboard
└── README.md
```

## Execution
1. Clone this repository.
2. Ensure Anaconda is installed with an environment containing `pandas`, `numpy`, and `statsmodels`.
3. Open `scripts/saas_ab_test_analysis.py` in Spyder and execute to reproduce the data cleaning, time-series extraction, A/B group assignments, and Z-test calculations.

## Caveats & Business Assumptions
* **Simulated Environment:** While baseline volume and timestamps are derived from real-world clickstream data, the A/B group assignments and Variant lift were synthetically modeled in Python to demonstrate experimental evaluation frameworks. 
* **Lead Quality Degradation:** The ARR projection assumes the Trial-to-Paid rate remains constant at 84.01%. In a live production environment, drastically reducing top-of-funnel friction (1-click sign-up) often introduces lower-intent users, which would likely depress the downstream Trial-to-Paid conversion rate. 
* **Statistical Power:** A real-world deployment of this test would require an upfront Power Analysis to define the Minimum Detectable Effect (MDE) and strict time horizons to prevent p-value hacking.

---
*Designed & Analyzed by **Amrit Preet Kaur***  
*M.S. Data Science & Business Intelligence | [Connect on LinkedIn](https://www.linkedin.com/in/amritpreetkaur-)*