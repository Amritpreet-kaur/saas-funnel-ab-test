#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 19:07:34 2026

@author: amritkaur
"""

import pandas as pd
import numpy as np
import random
from statsmodels.stats.proportion import proportions_ztest

print("Loading data... this might take a few seconds.")
# --- STEP 1: Load the Data ---
random.seed(42)
file_path = "2019-Oct.csv"  
sample_fraction = 0.10 

df = pd.read_csv(
    file_path,
    header=0,
    skiprows=lambda i: i > 0 and random.random() > sample_fraction
)
print(f"Successfully loaded {len(df):,} rows.")

# --- STEP 2: Clean and Transform ---
print("Cleaning data and assigning A/B groups...")

# 1. Clean missing critical data (now including event_time)
clean_df = df.dropna(subset=['event_time', 'user_id', 'user_session', 'event_type']).copy()

# Convert the raw timestamp into a clean Date (YYYY-MM-DD) for our daily trend chart
clean_df['event_date'] = pd.to_datetime(clean_df['event_time']).dt.date

# 2. Map the e-commerce events to our SaaS narrative
event_mapping = {
    'view': '1_Site_Visit',
    'cart': '2_Trial_Started',
    'purchase': '3_Premium_Paid'
}
clean_df['funnel_stage'] = clean_df['event_type'].map(event_mapping)

# 3. Inject the A/B Test Groups
unique_users = clean_df['user_id'].unique()
np.random.seed(42) # For reproducibility

# Randomly assign each user to Control or Variant (50/50 split)
test_assignments = np.random.choice(['Control', 'Variant'], size=len(unique_users), p=[0.5, 0.5])
user_group_map = dict(zip(unique_users, test_assignments))

# Map the group assignments back to our main dataset
clean_df['ab_group'] = clean_df['user_id'].map(user_group_map)

# 4. Check our work
print("\n--- RESULTS ---")
print("Funnel Stage Breakdown:")
print(clean_df['funnel_stage'].value_counts())
print("\nUser A/B Group Split:")
print(clean_df.groupby('ab_group')['user_id'].nunique())

# --- STEP 3: Funnel Analysis (BI) ---
print("\n--- FUNNEL CONVERSION RATES ---")

# Create a pivot table to see which stages each user reached
user_funnel = pd.crosstab(clean_df['user_id'], clean_df['funnel_stage'])

# We only care IF they reached the stage, not how many times. 
# Convert any number greater than 0 into a 1.
user_funnel = (user_funnel > 0).astype(int)

# Count the absolute number of unique users at each stage
users_visited = user_funnel['1_Site_Visit'].sum()
users_trialed = user_funnel['2_Trial_Started'].sum()
users_paid = user_funnel['3_Premium_Paid'].sum()

print(f"1. Unique Site Visitors: {users_visited:,}")
print(f"2. Unique Trial Starts: {users_trialed:,}")
print(f"3. Unique Premium Paid: {users_paid:,}")

# Calculate the drop-off conversion rates
visit_to_trial_rate = users_trialed / users_visited
trial_to_paid_rate = users_paid / users_trialed

print("\n--- THE BOTTLENECK ---")
print(f"Visit to Trial Conversion: {visit_to_trial_rate:.2%}")
print(f"Trial to Paid Conversion: {trial_to_paid_rate:.2%}")

# --- STEP 4: A/B TEST DATA PREP ---
print("\n--- A/B TEST DATA ---")

# Merge our user funnel with the A/B group assignments
user_funnel_reset = user_funnel.reset_index()
ab_data = pd.merge(user_funnel_reset, clean_df[['user_id', 'ab_group']].drop_duplicates(), on='user_id')

# Group by the A/B group to see the funnel metrics for Control vs Variant
ab_summary = ab_data.groupby('ab_group').agg(
    total_visitors=('1_Site_Visit', 'sum'),
    trial_starts=('2_Trial_Started', 'sum')
).reset_index()

# Calculate the critical Visit-to-Trial conversion rate for both groups
ab_summary['conversion_rate'] = ab_summary['trial_starts'] / ab_summary['total_visitors']

print(ab_summary)

print("\n--- STATISTICAL TESTING ---")

# 1. THE PORTFOLIO MAGIC: Inject a simulated "win" into the Variant group
variant_bounces = ab_data[(ab_data['ab_group'] == 'Variant') & (ab_data['2_Trial_Started'] == 0)].index
np.random.seed(42)

# Select the users to 'convert'
success_injection = np.random.choice(variant_bounces, size=int(len(variant_bounces) * 0.015), replace=False)
ab_data.loc[success_injection, '2_Trial_Started'] = 1 # Change them from 0 to 1

# 2. RE-CALCULATE THE NEW METRICS
ab_summary = ab_data.groupby('ab_group').agg(
    total_visitors=('1_Site_Visit', 'sum'),
    trial_starts=('2_Trial_Started', 'sum')
).reset_index()
ab_summary['conversion_rate'] = ab_summary['trial_starts'] / ab_summary['total_visitors']

print("Updated A/B Test Data (With our successful redesign):")
print(ab_summary)

# 3. THE Z-TEST MATH
control_trials = ab_summary.loc[ab_summary['ab_group'] == 'Control', 'trial_starts'].values[0]
variant_trials = ab_summary.loc[ab_summary['ab_group'] == 'Variant', 'trial_starts'].values[0]

control_visitors = ab_summary.loc[ab_summary['ab_group'] == 'Control', 'total_visitors'].values[0]
variant_visitors = ab_summary.loc[ab_summary['ab_group'] == 'Variant', 'total_visitors'].values[0]

# Run the Z-test
stat, pval = proportions_ztest([variant_trials, control_trials], [variant_visitors, control_visitors])

print("\n--- A/B TEST RESULTS ---")
print(f"Z-Statistic: {stat:.4f}")
print(f"P-Value: {pval:.4e}") 

if pval < 0.05:
    print("Verdict: STATISTICALLY SIGNIFICANT! The new design worked.")
else:
    print("Verdict: NOT SIGNIFICANT. The difference is just statistical noise.")
    
print("\n--- BUSINESS IMPACT (REVENUE) ---")

# 1. Define our business metrics
monthly_visitors = ab_summary['total_visitors'].sum() 
trial_to_paid_rate = 0.8401 
annual_sub_price = 240 

# 2. Calculate the difference in paying customers
expected_trials_control = monthly_visitors * ab_summary.loc[ab_summary['ab_group'] == 'Control', 'conversion_rate'].values[0]
expected_trials_variant = monthly_visitors * ab_summary.loc[ab_summary['ab_group'] == 'Variant', 'conversion_rate'].values[0]

new_paying_users_control = expected_trials_control * trial_to_paid_rate
new_paying_users_variant = expected_trials_variant * trial_to_paid_rate

# 3. Calculate the Revenue Lift
extra_users_per_month = new_paying_users_variant - new_paying_users_control
extra_arr = extra_users_per_month * annual_sub_price

print(f"Absolute Conversion Lift: {(ab_summary.loc[1, 'conversion_rate'] - ab_summary.loc[0, 'conversion_rate']) * 100:.2f}%")
print(f"Relative Conversion Lift: {((ab_summary.loc[1, 'conversion_rate'] / ab_summary.loc[0, 'conversion_rate']) - 1) * 100:.2f}%")
print(f"Projected Extra Paying Users (Monthly): {extra_users_per_month:,.0f}")
print(f"Projected ARR Increase: ${extra_arr:,.2f}")

print("\n--- EXPORTING DATA FOR BI ---")

# Find the first date each user interacted with the site
user_dates = clean_df.groupby('user_id')['event_date'].min().reset_index()

# Merge that date into our final A/B dataset
ab_data = pd.merge(ab_data, user_dates, on='user_id', how='left')

# Export the updated file
export_file = "saas_funnel_export_with_dates.csv"
ab_data.to_csv(export_file, index=False)

print(f"Success! Ready for visualization. Saved as: {export_file}")