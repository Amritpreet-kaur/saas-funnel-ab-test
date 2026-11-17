# 📈 SaaS Subscription Funnel & 1-Click Sign-Up A/B Test

[**🔗 View the Interactive Tableau Executive Dashboard Here**](https://public.tableau.com:9443/views/SaaSABTest/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## 📌 Executive Summary

Analyzed over 4.2 million user events to map a SaaS subscription funnel and identified a severe 94.6% top-of-funnel drop-off rate. Designed and analyzed an A/B test for a "1-Click" sign-up flow, proving with >99.99% statistical significance that the new variant increases trial sign-ups by a relative 27.4%. Based on current conversion metrics, deploying this variant to 100% of traffic is projected to generate **\$4,001,792 in additional Annual Recurring Revenue (ARR)**.

## 🏢 The Business Problem: "The Leaky Bucket"

An analysis of 1.36 million unique site visitors revealed extreme behavioral polarization:

* **The Good (Product-Market Fit):** Once users start a trial, the product sells itself. The Trial-to-Paid conversion rate is an exceptional **84.01%**.

* **The Bad (Activation Friction):** The onboarding flow was fundamentally broken. Only **5.32%** of site visitors successfully started a trial.

Because downstream conversion is so efficient, fixing this top-of-funnel bottleneck became the highest-leverage opportunity for the business.

## 🛠️ Data & Methodology

* **Dataset:** 4.2 million raw e-commerce clickstream events, cleaned and mapped to a simulated SaaS subscription model (Site Visit ➡️ Trial Started ➡️ Premium Paid).

* **Experimental Design:** 1,363,325 unique users were randomly assigned to a 50/50 A/B split.

  * **Control:** Legacy multi-field sign-up page.

  * **Variant:** Streamlined 1-click email sign-up.

* **Statistical Testing:** Two-Sample Z-Test for Proportions (Alpha = 0.05).

* **Tech Stack:** Python (Pandas, NumPy) for data engineering and time-series extraction, `statsmodels` for inferential statistics, and Tableau for BI visualization.

## 📊 Phase 1: Funnel Analysis (Baseline BI)

* **Total Unique Visitors:** 1,363,325

* **Unique Trial Starts:** 72,482

* **Unique Premium Paid:** 60,895

* **Visit-to-Trial Conversion:** 5.32% *(Identified Bottleneck)*

* **Trial-to-Paid Conversion:** 84.01%

## 🧪 Phase 2: A/B Testing Results (Data Science)

* **Null Hypothesis (H0):** The 1-click sign-up flow has no effect on Visit-to-Trial conversion rates compared to the legacy flow.

* **Alternative Hypothesis (H1):** The 1-click sign-up flow increases Visit-to-Trial conversions.

**The Metrics:**

* **Control Group Conversion:** 5.31% (36,214 trials / 681,612 visitors)

* **Variant Group Conversion:** 6.77% (46,144 trials / 681,713 visitors)

**The Math:**

* **Z-Statistic:** 35.6747

* **P-Value:** 9.76e-279

* **Verdict:** Statistically Significant. We reject the null hypothesis. There is a near-zero probability that this lift was due to random chance.

## 📈 Phase 3: Visual Analytics

To communicate these findings to stakeholders, a multi-chart Executive Dashboard was built in Tableau:

* **Funnel Comparison:** A side-by-side bar chart visualizing the exact volume drop-off between the Control and Variant groups at each stage.

* **Daily Conversion Trend:** A time-series line chart proving that the Variant group's conversion rate consistently outperformed the Control group every single day of the month-long test, validating that the result was not affected by day-of-week seasonality.

## 💡 Business Translation & ROI

Moving beyond statistical significance, this test generated massive financial viability:

* **Absolute Conversion Lift:** +1.46%

* **Relative Conversion Lift:** +27.40%

* **Projected Extra Paying Users:** 16,674 per month (accounting for the 84% trial-to-paid rate).

Assuming a standard SaaS price point of \$20/month ($240/year), rolling this feature out to 100% of site traffic yields a **Projected ARR Increase of \$4,001,792.29**.

## 📁 Repository Structure

```
├── data/
│   ├── 2019-Oct.csv                      # Raw Kaggle dataset (Excluded from repo due to size)
│   └── saas_funnel_export_with_dates.csv # Cleaned BI export for Tableau
├── scripts/
│   └── saas_ab_test_analysis.py          # Full EDA, cleaning, and statistical testing code (Spyder/Anaconda)
├── images/
│   └── dashboard_screenshot.png          # High-res image of the multi-chart Tableau dashboard
└── README.md

```

## 🚀 How to Run the Project

1. Clone this repository to your local machine.

2. Ensure you have Anaconda installed, utilizing an environment with `pandas`, `numpy`, and `statsmodels`.

3. Open `scripts/saas_ab_test_analysis.py` in **Spyder** (or your preferred Python IDE) and run the file to step through the data cleaning, time-series extraction, A/B group assignments, and statistical Z-test.

4. Download the raw data from [Kaggle's eCommerce Behavior Data](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store) if you wish to re-run the complete pipeline from scratch.