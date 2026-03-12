import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="LLM Red-Team Safety Dashboard", layout="wide")

st.title("Automated AI Red-Teaming & Safety Evaluation Dashboard")

DATA_DIR = "dashboard_data"

summary_by_defense_path = os.path.join(DATA_DIR, "summary_by_defense.csv")
summary_by_family_path = os.path.join(DATA_DIR, "summary_by_family.csv")
summary_by_category_path = os.path.join(DATA_DIR, "summary_by_category.csv")
risk_summary_path = os.path.join(DATA_DIR, "risk_summary.csv")
merged_path = os.path.join(DATA_DIR, "merged_results.csv")

required_files = [
    summary_by_defense_path,
    summary_by_family_path,
    summary_by_category_path,
    risk_summary_path,
    merged_path
]

missing = [p for p in required_files if not os.path.exists(p)]

if missing:
    st.error("Missing required dashboard data files:")
    for m in missing:
        st.write(m)
    st.stop()

summary_by_defense = pd.read_csv(summary_by_defense_path)
summary_by_family = pd.read_csv(summary_by_family_path)
summary_by_category = pd.read_csv(summary_by_category_path)
risk_summary = pd.read_csv(risk_summary_path)
merged_df = pd.read_csv(merged_path)

st.sidebar.header("Filters")

defense_options = sorted(merged_df["defense_name"].dropna().unique().tolist())
category_options = sorted(merged_df["category"].dropna().unique().tolist())
family_options = sorted(merged_df["attack_family"].dropna().unique().tolist())

selected_defenses = st.sidebar.multiselect("Defense", defense_options, default=defense_options)
selected_categories = st.sidebar.multiselect("Category", category_options, default=category_options)
selected_families = st.sidebar.multiselect("Attack Family", family_options, default=family_options)

filtered_df = merged_df[
    merged_df["defense_name"].isin(selected_defenses) &
    merged_df["category"].isin(selected_categories) &
    merged_df["attack_family"].isin(selected_families)
].copy()

if len(filtered_df) == 0:
    st.warning("No rows match the selected filters.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

harmful_rate = (filtered_df["compliance_label"] == "harmful_compliance").mean()
refusal_rate = (filtered_df["refusal_label"] == "full_refusal").mean()
avg_severity = filtered_df["severity_score"].mean()
total_runs = len(filtered_df)

col1.metric("Total Runs", int(total_runs))
col2.metric("Harmful Compliance Rate", f"{harmful_rate:.2%}")
col3.metric("Refusal Rate", f"{refusal_rate:.2%}")
col4.metric("Avg Severity", f"{avg_severity:.2f}")

st.subheader("Harmful Compliance by Defense")
defense_chart_df = filtered_df.groupby("defense_name").agg(
    harmful_rate=("compliance_label", lambda x: (x == "harmful_compliance").mean())
).reset_index()

fig1 = px.bar(defense_chart_df, x="defense_name", y="harmful_rate")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Average Severity by Attack Family")
family_chart_df = filtered_df.groupby(["defense_name", "attack_family"]).agg(
    avg_severity=("severity_score", "mean")
).reset_index()

fig2 = px.bar(
    family_chart_df,
    x="attack_family",
    y="avg_severity",
    color="defense_name",
    barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Harmful Compliance by Category")
category_chart_df = filtered_df.groupby(["defense_name", "category"]).agg(
    harmful_rate=("compliance_label", lambda x: (x == "harmful_compliance").mean())
).reset_index()

fig3 = px.bar(
    category_chart_df,
    x="category",
    y="harmful_rate",
    color="defense_name",
    barmode="group"
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Risk Level Distribution")
if "risk_level" in filtered_df.columns:
    risk_chart_df = filtered_df.groupby(["defense_name", "risk_level"]).size().reset_index(name="count")
    fig4 = px.bar(
        risk_chart_df,
        x="risk_level",
        y="count",
        color="defense_name",
        barmode="group"
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("No risk_level column found in merged_results.csv.")

st.subheader("Detailed Results")
display_cols = [
    c for c in [
        "run_id", "model_name", "defense_name", "attack_id", "category", "attack_family",
        "severity_score", "refusal_label", "compliance_label", "failure_mode", "prompt", "response"
    ] if c in filtered_df.columns
]
st.dataframe(filtered_df[display_cols], use_container_width=True)
