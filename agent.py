"""
SafetyLens Montgomery — LangGraph Agent
AI-powered multi-dataset city intelligence agent for Montgomery, AL.
"""

import json
import os
from typing import Annotated, Any, TypedDict

import httpx
import pandas as pd
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import DATASETS

# ─── State ───────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ─── Helper: ArcGIS Query ───────────────────────────────────────────────────

def _query_arcgis(dataset_key: str, where: str = "1=1", out_fields: str = "*",
                  result_count: int = 500, order_by: str = "") -> dict:
    """Execute a query against an ArcGIS REST endpoint."""
    ds = DATASETS.get(dataset_key)
    if not ds:
        return {"error": f"Unknown dataset: {dataset_key}"}

    params = {
        "where": where,
        "outFields": out_fields,
        "resultRecordCount": result_count,
        "f": "json",
        "returnGeometry": "false",
    }
    if order_by:
        params["orderByFields"] = order_by

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{ds['url']}/query", params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": str(e)}

    features = data.get("features", [])
    records = [f["attributes"] for f in features]
    return {
        "dataset": dataset_key,
        "description": ds["description"],
        "record_count": len(records),
        "records": records[:50],  # cap for LLM context
        "total_available": data.get("exceededTransferLimit", False),
    }


def _get_dataset_schema(dataset_key: str) -> dict:
    """Get field names and types for a dataset."""
    ds = DATASETS.get(dataset_key)
    if not ds:
        return {"error": f"Unknown dataset: {dataset_key}"}
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(f"{ds['url']}", params={"f": "json"})
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        return {"error": str(e)}

    fields = [{"name": f["name"], "type": f["type"], "alias": f.get("alias", "")}
              for f in data.get("fields", [])]
    return {"dataset": dataset_key, "fields": fields}


# ─── Tools ───────────────────────────────────────────────────────────────────

@tool
def query_911_monthly(where: str = "1=1", result_count: int = 200) -> str:
    """Query Montgomery's monthly 911 call data. Filter with SQL-like WHERE clause.
    Fields: Year, Month, Call_Category (Emergency/Non-Emergency),
    Phone_Service_Provider_Type (Wire-line/Wireless/VoIP/Unknown),
    Call_Count_by_Phone_Service_Pro, Call_Origin (Incoming/Internal/Outgoing/Unknown),
    Call_Count_By_Origin.
    Example: where="Year=2025 AND Call_Category='Emergency'"
    """
    result = _query_arcgis("911_calls_monthly", where=where, result_count=result_count)
    return json.dumps(result, default=str)


@tool
def query_911_daily(where: str = "1=1", result_count: int = 200) -> str:
    """Query Montgomery's daily 911 call data. Filter with SQL-like WHERE clause.
    Fields: Year, Month, Date, F911_Inbound, F911_Outbound, Admin_Inbound,
    Admin_Outbound, NENA, Other, Text_Inbound, Text_Outbound, Total.
    Example: where="Year=2024 AND Month=6"
    """
    result = _query_arcgis("911_calls_daily", where=where, result_count=result_count)
    return json.dumps(result, default=str)


@tool
def query_business_licenses(where: str = "1=1", result_count: int = 200) -> str:
    """Query Montgomery business license data. Use get_dataset_fields first to discover
    available columns. Filter with SQL-like WHERE clause.
    Example: where="1=1" to get sample records.
    """
    result = _query_arcgis("business_licenses", where=where, result_count=result_count)
    return json.dumps(result, default=str)


@tool
def query_code_violations(where: str = "1=1", result_count: int = 200) -> str:
    """Query Montgomery code violation data. Includes locations and violation details.
    Use get_dataset_fields first to discover available columns.
    Example: where="1=1" to get sample records.
    """
    result = _query_arcgis("code_violations", where=where, result_count=result_count)
    return json.dumps(result, default=str)


@tool
def query_311_requests(where: str = "1=1", result_count: int = 200) -> str:
    """Query Montgomery 311 service request data. These are non-emergency citizen
    requests to the city. Use get_dataset_fields first to discover available columns.
    Example: where="1=1" to get sample records.
    """
    result = _query_arcgis("311_requests", where=where, result_count=result_count)
    return json.dumps(result, default=str)


@tool
def get_dataset_fields(dataset_name: str) -> str:
    """Get the schema (field names and types) for a Montgomery dataset.
    Available datasets: 911_calls_monthly, 911_calls_daily, business_licenses,
    code_violations, 311_requests.
    """
    result = _get_dataset_schema(dataset_name)
    return json.dumps(result, default=str)


@tool
def scrape_montgomery_news(query: str = "Montgomery Alabama public safety crime") -> str:
    """Search for recent news about Montgomery, AL using Bright Data's SERP API.
    Useful for comparing public perception with actual city data.
    Returns news headlines and snippets from recent coverage.
    """
    api_key = os.getenv("BRIGHT_DATA_API_KEY", "")
    if not api_key:
        return json.dumps({
            "source": "bright_data",
            "status": "no_api_key",
            "message": "Bright Data API key not configured. Set BRIGHT_DATA_API_KEY in .env",
            "fallback_note": "Without Bright Data, perception analysis uses general knowledge only."
        })

    # Bright Data SERP API
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "query": query,
            "search_engine": "google",
            "country": "us",
            "language": "en",
            "num": 10,
            "type": "news",
        }
        with httpx.Client(timeout=60) as client:
            resp = client.post(
                "https://api.brightdata.com/serp/req",
                json=payload,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()

        results = []
        for item in data.get("organic", data.get("results", []))[:10]:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", item.get("description", "")),
                "link": item.get("link", item.get("url", "")),
                "date": item.get("date", ""),
            })
        return json.dumps({"source": "bright_data", "query": query, "results": results})
    except Exception as e:
        return json.dumps({"source": "bright_data", "error": str(e)})


@tool
def compute_statistics(data_json: str, group_by: str = "", value_field: str = "") -> str:
    """Compute statistics on data previously fetched. Pass the records as a JSON string.
    Optionally group_by a field and aggregate value_field.
    Returns summary statistics (count, sum, mean, min, max).
    """
    try:
        records = json.loads(data_json)
        if isinstance(records, dict) and "records" in records:
            records = records["records"]
        df = pd.DataFrame(records)

        if df.empty:
            return json.dumps({"error": "No data to analyze"})

        result = {"total_records": len(df), "columns": list(df.columns)}

        if group_by and group_by in df.columns:
            if value_field and value_field in df.columns:
                grouped = df.groupby(group_by)[value_field].agg(["count", "sum", "mean", "min", "max"])
                result["grouped_stats"] = grouped.reset_index().to_dict("records")
            else:
                result["value_counts"] = df[group_by].value_counts().head(20).to_dict()
        else:
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                result["numeric_summary"] = df[numeric_cols].describe().to_dict()

        return json.dumps(result, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── All Tools ───────────────────────────────────────────────────────────────

ALL_TOOLS = [
    query_911_monthly,
    query_911_daily,
    query_business_licenses,
    query_code_violations,
    query_311_requests,
    get_dataset_fields,
    scrape_montgomery_news,
    compute_statistics,
]

# ─── LLM ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are SafetyLens, an AI city intelligence analyst for Montgomery, Alabama.
You have access to LIVE data from the City of Montgomery's Open Data Portal, including:
- 911 call records (monthly aggregates and daily counts)
- Business license data
- Code violation records
- 311 service requests

And you can scrape recent news about Montgomery using Bright Data to compare
PUBLIC PERCEPTION with ACTUAL DATA (crime statistics vs media coverage).

YOUR CAPABILITIES:
1. Analyze 911 call patterns (time trends, categories, call types)
2. Cross-reference business license data with code violations
3. Identify patterns in 311 service requests
4. Compare real crime/safety data with news media perception (using Bright Data)
5. Provide actionable recommendations for city officials

GUIDELINES:
- Always fetch real data before making claims. Use the query tools.
- When analyzing 911 data, look for trends across months/years.
- Use get_dataset_fields first if you don't know a dataset's schema.
- When asked about perception vs reality, use scrape_montgomery_news.
- Provide specific numbers and percentages in your analysis.
- Suggest actionable recommendations based on data patterns.
- Format responses with clear headers and bullet points.
- If a query returns an error, explain what happened and suggest alternatives.
"""


def build_agent():
    """Build and return the LangGraph agent."""
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    def should_continue(state: AgentState) -> str:
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    def call_model(state: AgentState) -> dict:
        messages = state["messages"]
        # Ensure system prompt is present
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(ALL_TOOLS)

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


def run_agent(user_message: str, chat_history: list | None = None) -> str:
    """Run the agent with a user message and optional history. Returns the final AI response."""
    agent = build_agent()
    messages = []
    if chat_history:
        messages.extend(chat_history)
    messages.append(HumanMessage(content=user_message))

    result = agent.invoke({"messages": messages})

    # Get the last AI message
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content
    return "I wasn't able to generate a response. Please try a different question."
