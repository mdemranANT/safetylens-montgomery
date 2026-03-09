# 🔍 SafetyLens Montgomery

**AI-Powered City Intelligence Platform for Montgomery, Alabama**

> *An intelligent LangGraph agent that turns Montgomery's open data into actionable insights — comparing real city data with public perception using Bright Data.*

Built for the **WWV 2026 Hackathon** | Vibe-Coded with AI

---

## 🎯 Challenge Areas Addressed

| Challenge Area | How SafetyLens Addresses It |
|---|---|
| 🚨 **Public Safety, Emergency Response & City Analytics** | Analyzes 911 call patterns, trends, and response types using live Montgomery data |
| 🏛️ **Civic Access & Community Communication** | Natural language AI interface — ask questions in plain English about any city dataset |
| 💼 **Workforce, Business & Economic Growth** | Business license analytics, cross-referencing with code violations for economic health |
| 🏗️ **Smart Cities, Infrastructure & Public Spaces** | 311 service request analysis, code violation mapping, city service optimization |

**Unique Angle:** SafetyLens doesn't just show data — it reasons about it. The AI agent performs **gap analysis between actual 911/crime data and media perception** using Bright Data, revealing where public perception diverges from reality.

---

## 🏗️ Architecture

```
User Query (Natural Language)
        │
   LangGraph Agent (ReAct Pattern)
        │
   ┌────┼────────────────┬──────────────┐
   │    │                │              │
   ▼    ▼                ▼              ▼
 911 Data    Business     Code        Bright Data
 (ArcGIS)   Licenses    Violations   (News Scraping)
   │    │                │              │
   └────┼────────────────┴──────────────┘
        │
   AI Analysis + Recommendations
        │
   Interactive Streamlit Dashboard
```

---

## 📊 Data Sources

All city data sourced from the **[City of Montgomery Open Data Portal](https://citymgm.maps.arcgis.com)**:

| Dataset | API Endpoint | Update Frequency |
|---|---|---|
| 911 Calls (Monthly) | ArcGIS FeatureServer | Monthly |
| Emergency 911 Calls (Daily) | ArcGIS FeatureServer | Daily |
| Business Licenses | ArcGIS FeatureServer | Weekly |
| Code Violations | ArcGIS FeatureServer | Ongoing |
| 311 Service Requests | ArcGIS MapServer | Continuous |

**Bright Data Integration:** Scrapes real-time news about Montgomery public safety to compare media narrative with actual data.

---

## 🛠️ Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — Multi-step AI agent with tool-calling
- **[OpenAI GPT-4](https://openai.com)** — LLM for reasoning and analysis
- **[Streamlit](https://streamlit.io)** — Interactive web dashboard
- **[ArcGIS REST API](https://developers.arcgis.com)** — Montgomery Open Data
- **[Bright Data](https://brightdata.com)** — Web scraping for news/perception analysis
- **[Plotly](https://plotly.com)** — Interactive charts and visualizations
- **[Pandas](https://pandas.pydata.org)** — Data processing

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/safetylens-montgomery.git
cd safetylens-montgomery
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
# Optionally add Bright Data API key for +3 bonus points
```

### 3. Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🎮 Features

### 💬 AI Chat Agent
Ask questions in natural language:
- *"What are the 911 call trends in Montgomery?"*
- *"How do business licenses compare with code violations?"*
- *"Compare real crime data with media perception"*

### 📊 911 Analytics Dashboard
- Monthly/yearly trend analysis
- Emergency vs. Non-Emergency breakdown
- Phone service provider analysis (Wireless vs Wire-line vs VoIP)

### 🏢 Business & Code Analysis
- Business license data exploration
- Code violation mapping
- Cross-reference analysis

### 📋 311 Service Requests
- Service request categorization
- Volume trends and patterns

### 📰 Perception vs Reality
- Bright Data news scraping
- Side-by-side comparison: actual data vs. media narrative
- AI-powered gap analysis

---

## 🏆 Judging Criteria Alignment

| Criteria | Max Points | Our Score Strategy |
|---|---|---|
| **Relevance to Challenge** | 10 | Addresses ALL 4 challenge areas with live Montgomery data |
| **Quality & Design** | 10 | Production-grade LangGraph agent, Plotly charts, polished Streamlit UI |
| **Originality** | 5 | AI agent that *reasons* (not just displays), perception gap analysis is novel |
| **Social Value/Impact** | 5 | Empowers residents + helps city optimize emergency resources |
| **Commercialization** | 5 | Platform model — reusable for any city's open data portal |
| **Bright Data Bonus** | +3 | ✅ Integrated for real-time news scraping and perception analysis |
| **Total Potential** | **38** | |

---

## 📋 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | OpenAI API key for GPT-4 |
| `BRIGHT_DATA_API_KEY` | Optional | Bright Data API key for news scraping (+3 bonus) |
| `OPENAI_MODEL` | Optional | Model selection (default: `gpt-4o-mini`) |

---

## 📜 License

MIT License — Built for WWV 2026 Hackathon

---

*🔍 SafetyLens Montgomery — See the full picture of your city.*
