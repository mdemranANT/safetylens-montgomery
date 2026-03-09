"""
SafetyLens Montgomery — Streamlit App
AI-Powered City Intelligence Platform for Montgomery, AL
"""

import json
import os
from datetime import datetime

import httpx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from config import APP_DESCRIPTION, APP_SUBTITLE, APP_TITLE, CHALLENGE_AREAS, DATASETS

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: #e94560; margin: 0; font-size: 2.2rem; }
    .main-header p { color: #a8b2d1; margin: 0.3rem 0 0 0; font-size: 1.1rem; }
    .metric-card {
        background: #16213e;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #e94560;
        color: white;
    }
    .metric-card h3 { color: #e94560; margin: 0; font-size: 1.8rem; }
    .metric-card p { color: #a8b2d1; margin: 0.2rem 0 0 0; font-size: 0.9rem; }
    .challenge-tag {
        display: inline-block;
        background: #0f3460;
        color: #e94560;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .stChatMessage { border-radius: 12px; }
    div[data-testid="stSidebar"] { background: #1a1a2e; }
    div[data-testid="stSidebar"] .stMarkdown { color: #a8b2d1; }
</style>
""", unsafe_allow_html=True)


# ─── Data Fetching ───────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_dataset(dataset_key: str, where: str = "1=1", count: int = 2000) -> pd.DataFrame:
    """Fetch data from ArcGIS REST API and return as DataFrame."""
    ds = DATASETS.get(dataset_key)
    if not ds:
        return pd.DataFrame()
    params = {
        "where": where,
        "outFields": "*",
        "resultRecordCount": count,
        "f": "json",
        "returnGeometry": "false",
    }
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{ds['url']}/query", params=params)
            resp.raise_for_status()
            data = resp.json()
        features = data.get("features", [])
        records = [f["attributes"] for f in features]
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Error fetching {dataset_key}: {e}")
        return pd.DataFrame()


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🔍 SafetyLens Montgomery")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["💬 AI Chat Agent", "📊 911 Analytics Dashboard", "🏢 Business & Code Analysis",
         "📋 311 Service Requests", "📰 Perception vs Reality", "ℹ️ About"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 🔑 Configuration")
    api_key = st.text_input("OpenAI API Key", type="password",
                            value=os.getenv("OPENAI_API_KEY", ""))
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    bright_key = st.text_input("Bright Data API Key (optional, +3 pts)", type="password",
                               value=os.getenv("BRIGHT_DATA_API_KEY", ""))
    if bright_key:
        os.environ["BRIGHT_DATA_API_KEY"] = bright_key

    model_choice = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"], index=0)
    os.environ["OPENAI_MODEL"] = model_choice

    st.markdown("---")
    st.markdown("### 📊 Data Sources")
    st.markdown("**City of Montgomery Open Data Portal**")
    for name, ds in DATASETS.items():
        st.markdown(f"- {name.replace('_', ' ').title()}")

    st.markdown("---")
    st.caption(f"Built for WWV 2026 Hackathon | {datetime.now().strftime('%Y-%m-%d')}")


# ─── Header ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="main-header">
    <h1>🔍 {APP_TITLE}</h1>
    <p>{APP_SUBTITLE}</p>
    <div style="margin-top: 0.8rem;">
        {''.join(f'<span class="challenge-tag">{area}</span>' for area in CHALLENGE_AREAS)}
    </div>
</div>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: AI Chat Agent
# ═════════════════════════════════════════════════════════════════════════════

if page == "💬 AI Chat Agent":
    st.markdown("### 💬 Ask SafetyLens Anything About Montgomery")
    st.markdown("*Powered by LangGraph + OpenAI — queries live city data in real time*")

    # Suggested questions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📞 911 Call Trends", use_container_width=True):
            st.session_state.setdefault("suggested_q", "")
            st.session_state["suggested_q"] = "What are the trends in Montgomery 911 calls? Compare emergency vs non-emergency calls across months."
    with col2:
        if st.button("🏢 Business vs Violations", use_container_width=True):
            st.session_state["suggested_q"] = "How do business license patterns compare with code violations in Montgomery? Are there concerning trends?"
    with col3:
        if st.button("📰 Perception vs Reality", use_container_width=True):
            st.session_state["suggested_q"] = "Compare the actual 911 and crime data in Montgomery with how the media portrays public safety. Is there a perception gap?"

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # Input
    suggested = st.session_state.pop("suggested_q", "")
    prompt = st.chat_input("Ask about Montgomery's public safety, businesses, 311 requests...") or suggested

    if prompt:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ Please enter your OpenAI API key in the sidebar.")
        else:
            st.session_state.messages.append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🔍 Analyzing Montgomery data..."):
                    try:
                        from agent import run_agent
                        response = run_agent(prompt, st.session_state.messages[:-1])
                        st.markdown(response)
                        st.session_state.messages.append(AIMessage(content=response))
                    except Exception as e:
                        st.error(f"Error: {e}")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: 911 Analytics Dashboard
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📊 911 Analytics Dashboard":
    st.markdown("### 📊 911 Call Analytics Dashboard")
    st.markdown("*Live data from City of Montgomery Emergency Communications*")

    with st.spinner("Loading 911 data..."):
        df_monthly = fetch_dataset("911_calls_monthly", count=2000)
        df_daily = fetch_dataset("911_calls_daily", count=2000)

    if not df_monthly.empty:
        # ── KPI Metrics ──
        col1, col2, col3, col4 = st.columns(4)

        # Total calls from Call_Count_By_Origin (incoming only to avoid double-count)
        incoming = df_monthly[df_monthly["Call_Origin"] == "Incoming"]
        total_calls = incoming["Call_Count_By_Origin"].sum() if "Call_Count_By_Origin" in incoming.columns else 0

        emergency = df_monthly[df_monthly["Call_Category"] == "Emergency"]
        non_emergency = df_monthly[df_monthly["Call_Category"] == "Non-Emergency"]

        with col1:
            st.metric("Total Incoming Calls", f"{total_calls:,.0f}")
        with col2:
            wireless_pct = 0
            if "Call_Count_by_Phone_Service_Pro" in emergency.columns:
                total_e = emergency["Call_Count_by_Phone_Service_Pro"].sum()
                wireless_e = emergency[emergency["Phone_Service_Provider_Type"] == "Wireless"]["Call_Count_by_Phone_Service_Pro"].sum()
                wireless_pct = (wireless_e / total_e * 100) if total_e > 0 else 0
            st.metric("Wireless Calls %", f"{wireless_pct:.1f}%")
        with col3:
            months_count = df_monthly["Month"].nunique()
            st.metric("Months of Data", months_count)
        with col4:
            years = sorted(df_monthly["Year"].unique())
            st.metric("Years Covered", f"{min(years)}–{max(years)}" if years else "N/A")

        st.markdown("---")

        # ── Monthly Trend ──
        tab1, tab2, tab3 = st.tabs(["📈 Monthly Trends", "📊 By Category", "📱 By Provider"])

        with tab1:
            # Aggregate calls by month using Call_Count_by_Phone_Service_Pro
            month_order = ["01 - January", "02 - February", "03 - March", "04 - April",
                          "05 - May", "06 - June", "07 - July", "08 - August",
                          "09 - September", "10 - October", "11 - November", "12 - December"]
            trend = df_monthly.groupby(["Year", "Month", "Call_Category"])["Call_Count_by_Phone_Service_Pro"].sum().reset_index()
            trend.columns = ["Year", "Month", "Category", "Calls"]
            trend["Period"] = trend["Month"].str[:2] + "/" + trend["Year"].astype(str)

            fig = px.line(trend, x="Period", y="Calls", color="Category",
                         title="911 Call Trends by Category",
                         color_discrete_map={"Emergency": "#e94560", "Non-Emergency": "#0f3460"})
            fig.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            cat_totals = df_monthly.groupby("Call_Category")["Call_Count_by_Phone_Service_Pro"].sum().reset_index()
            cat_totals.columns = ["Category", "Total Calls"]
            fig2 = px.pie(cat_totals, values="Total Calls", names="Category",
                         title="Emergency vs Non-Emergency Calls",
                         color_discrete_sequence=["#e94560", "#0f3460"])
            fig2.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e")
            st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            provider = df_monthly.groupby("Phone_Service_Provider_Type")["Call_Count_by_Phone_Service_Pro"].sum().reset_index()
            provider.columns = ["Provider", "Total Calls"]
            fig3 = px.bar(provider, x="Provider", y="Total Calls",
                         title="Calls by Phone Service Provider Type",
                         color="Provider",
                         color_discrete_sequence=["#e94560", "#0f3460", "#533483", "#a8b2d1"])
            fig3.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e")
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.warning("Unable to load 911 monthly data. Please check your connection.")

    # Daily data
    if not df_daily.empty:
        st.markdown("### 📅 Daily Emergency Call Volume")
        daily_agg = df_daily.groupby(["Year", "Month"])["Total"].sum().reset_index()
        daily_agg["Period"] = daily_agg["Month"].astype(str).str.zfill(2) + "/" + daily_agg["Year"].astype(str)
        fig4 = px.bar(daily_agg, x="Period", y="Total",
                     title="Total Daily 911 Calls by Month",
                     color_discrete_sequence=["#e94560"])
        fig4.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e")
        st.plotly_chart(fig4, use_container_width=True)

    # Raw data
    with st.expander("🔍 View Raw 911 Data"):
        st.dataframe(df_monthly.head(100), use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: Business & Code Analysis
# ═════════════════════════════════════════════════════════════════════════════

elif page == "🏢 Business & Code Analysis":
    st.markdown("### 🏢 Business Licenses & Code Violations")
    st.markdown("*Cross-referencing business health with code compliance*")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 Business Licenses")
        with st.spinner("Loading business license data..."):
            df_biz = fetch_dataset("business_licenses", count=500)
        if not df_biz.empty:
            st.metric("Total Business Licenses", f"{len(df_biz):,}")
            st.dataframe(df_biz.head(50), use_container_width=True, height=400)
        else:
            st.info("Business license data is loading or unavailable.")

    with col2:
        st.markdown("#### ⚠️ Code Violations")
        with st.spinner("Loading code violation data..."):
            df_code = fetch_dataset("code_violations", count=500)
        if not df_code.empty:
            st.metric("Total Code Violations", f"{len(df_code):,}")
            st.dataframe(df_code.head(50), use_container_width=True, height=400)
        else:
            st.info("Code violation data is loading or unavailable.")

    # AI Analysis CTA
    st.markdown("---")
    st.info("💡 **Tip:** Use the AI Chat Agent to ask questions like: *'Are there patterns between business types and code violations?'*")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: 311 Service Requests
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📋 311 Service Requests":
    st.markdown("### 📋 311 Service Requests")
    st.markdown("*Citizen requests to City of Montgomery*")

    with st.spinner("Loading 311 data..."):
        df_311 = fetch_dataset("311_requests", count=1000)

    if not df_311.empty:
        st.metric("Total 311 Requests Loaded", f"{len(df_311):,}")

        # Try to find categorical columns for visualization
        str_cols = df_311.select_dtypes(include="object").columns.tolist()
        if str_cols:
            viz_col = st.selectbox("Group by field:", str_cols)
            if viz_col:
                counts = df_311[viz_col].value_counts().head(15)
                fig = px.bar(x=counts.index, y=counts.values,
                            title=f"311 Requests by {viz_col}",
                            labels={"x": viz_col, "y": "Count"},
                            color_discrete_sequence=["#e94560"])
                fig.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e")
                st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_311.head(100), use_container_width=True)
    else:
        st.warning("311 service request data is loading or unavailable.")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: Perception vs Reality
# ═════════════════════════════════════════════════════════════════════════════

elif page == "📰 Perception vs Reality":
    st.markdown("### 📰 Crime Data vs Public Perception")
    st.markdown("*Powered by Bright Data — Compare real 911 data with media coverage*")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 📊 Actual 911 Data (Reality)")
        df_monthly = fetch_dataset("911_calls_monthly", count=2000)
        if not df_monthly.empty:
            emergency = df_monthly[df_monthly["Call_Category"] == "Emergency"]
            total_e = emergency["Call_Count_by_Phone_Service_Pro"].sum()
            non_emergency = df_monthly[df_monthly["Call_Category"] == "Non-Emergency"]
            total_ne = non_emergency["Call_Count_by_Phone_Service_Pro"].sum()

            st.metric("Total Emergency Calls", f"{total_e:,.0f}")
            st.metric("Total Non-Emergency Calls", f"{total_ne:,.0f}")
            st.metric("Emergency Ratio", f"{total_e/(total_e+total_ne)*100:.1f}%" if (total_e+total_ne) > 0 else "N/A")

            # Trend
            trend = emergency.groupby(["Year", "Month"])["Call_Count_by_Phone_Service_Pro"].sum().reset_index()
            trend.columns = ["Year", "Month", "Emergency_Calls"]
            trend["Period"] = trend["Month"].str[:2] + "/" + trend["Year"].astype(str)
            fig = px.area(trend, x="Period", y="Emergency_Calls",
                         title="Emergency Call Trend",
                         color_discrete_sequence=["#e94560"])
            fig.update_layout(template="plotly_dark", paper_bgcolor="#1a1a2e", plot_bgcolor="#16213e",
                            height=300)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📰 Media Coverage (Perception)")
        if os.getenv("BRIGHT_DATA_API_KEY"):
            search_query = st.text_input("News search query:", "Montgomery Alabama crime safety")
            if st.button("🔍 Search News via Bright Data"):
                with st.spinner("Scraping news with Bright Data..."):
                    try:
                        from agent import scrape_montgomery_news
                        result = json.loads(scrape_montgomery_news.invoke(search_query))
                        if "results" in result:
                            for item in result["results"]:
                                st.markdown(f"**{item.get('title', 'N/A')}**")
                                st.caption(item.get("snippet", ""))
                                st.markdown(f"[Read more]({item.get('link', '#')})")
                                st.markdown("---")
                        elif "error" in result:
                            st.error(result["error"])
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Enter your Bright Data API key in the sidebar to enable news scraping.")
            st.markdown("""
            **Without Bright Data, here's what we know about the perception gap:**

            Media coverage of crime in Montgomery tends to:
            - Over-represent violent incidents relative to their % of 911 calls
            - Under-report non-emergency and administrative calls
            - Create perception of increasing crime even when 911 data may show stability

            *Add your Bright Data API key to get real-time news analysis and earn +3 bonus points!*
            """)

    st.markdown("---")
    st.markdown("#### 🤖 AI Gap Analysis")
    st.info("💡 Use the AI Chat Agent and ask: *'Compare the actual 911 and crime data with how media portrays Montgomery public safety'*")

# ═════════════════════════════════════════════════════════════════════════════
# PAGE: About
# ═════════════════════════════════════════════════════════════════════════════

elif page == "ℹ️ About":
    st.markdown("### ℹ️ About SafetyLens Montgomery")

    st.markdown(f"""
    **{APP_TITLE}** is an AI-powered city intelligence platform that transforms Montgomery's
    open data into actionable insights using a LangGraph-based intelligent agent.

    ---

    #### 🎯 Challenge Areas Addressed

    | Challenge Area | How We Address It |
    |---|---|
    | **Public Safety & City Analytics** | 911 call analysis, trend detection, pattern recognition |
    | **Civic Access & Communication** | Natural language interface to city data |
    | **Business & Economic Growth** | Business license analytics, cross-referencing with violations |
    | **Smart Cities & Infrastructure** | 311 request analysis, code violation mapping |

    ---

    #### 🏗️ Architecture

    ```
    User Query (Natural Language)
            │
       LangGraph Agent (ReAct Pattern)
            │
       ┌────┼────────────┬──────────────┐
       │    │             │              │
       ▼    ▼             ▼              ▼
    911 Data  Business    Code        Bright Data
    (ArcGIS)  Licenses   Violations   (News/SERP)
       │    │             │              │
       └────┼────────────┴──────────────┘
            │
       AI Analysis + Visualization
            │
       Actionable Insights & Recommendations
    ```

    ---

    #### 🛠️ Tech Stack

    - **LangGraph** — Multi-step AI agent with tool use
    - **OpenAI GPT-4** — Language model for reasoning
    - **Streamlit** — Interactive web dashboard
    - **ArcGIS REST API** — Montgomery Open Data Portal
    - **Bright Data** — Web scraping for news/perception analysis (+3 bonus)
    - **Plotly** — Interactive data visualizations
    - **Pandas** — Data processing and statistics

    ---

    #### 📊 Data Sources

    All data is sourced from the **City of Montgomery Open Data Portal**
    ([citymgm.maps.arcgis.com](https://citymgm.maps.arcgis.com)):

    | Dataset | Update Frequency | Records |
    |---|---|---|
    | 911 Calls (Monthly) | Monthly | Aggregated by category/provider |
    | Emergency 911 Calls (Daily) | — | Daily call volumes |
    | Business Licenses | Weekly | Active licenses citywide |
    | Code Violations | — | Violation locations & details |
    | 311 Service Requests | Continuous | Citizen service requests |

    ---

    #### 🏆 Judging Criteria Alignment

    | Criteria | Score | Our Approach |
    |---|---|---|
    | **Relevance** | /10 | Directly addresses 4 challenge areas with live Montgomery data |
    | **Quality & Design** | /10 | LangGraph agent architecture, Plotly visualizations, polished UI |
    | **Originality** | /5 | AI agent that *reasons* over data (not just a dashboard) + perception gap analysis |
    | **Social Value** | /5 | Helps residents understand safety, helps city optimize resources |
    | **Commercialization** | /5 | Reusable platform — any city with open data can use it |
    | **Bright Data Bonus** | +3 | Integrated for news perception analysis |

    ---

    *Built for the WWV 2026 Hackathon by Team SafetyLens*
    """)
