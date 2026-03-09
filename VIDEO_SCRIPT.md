# 🎬 SafetyLens Montgomery — 5-Minute Pitch Video Script

> **Total Time: 5:00 max**  
> **Recording Tool:** OBS Studio (free) or Loom (free tier)  
> **Screens needed:** Browser (pitch.html) + Browser (Streamlit at localhost:8501)  

---

## 🎤 SETUP BEFORE RECORDING

1. Open **pitch.html** in Chrome (full screen / F11)
2. Open **Streamlit app** in another Chrome tab (`streamlit run app.py` → localhost:8501)
3. Pre-load these Streamlit pages so they're cached:
   - 💬 AI Chat Agent — type a question beforehand so there's a response ready
   - 📊 911 Analytics Dashboard — let it load fully
   - 🏢 Business & Code Analysis
   - 📋 311 Service Requests
   - 📰 Perception vs Reality
4. Set mic volume, close notifications, hide taskbar
5. Screen resolution: 1920×1080 recommended

---

## 📜 FULL SCRIPT (with timings)

---

### ⏱️ 0:00–0:25 — SLIDE 1: Title (25 sec)
**[SCREEN: pitch.html → Slide 1 (Title)]**

> "Hi, I'm presenting SafetyLens Montgomery — an AI-powered city intelligence platform built for the WWV 2026 Hackathon.
>
> SafetyLens is a LangGraph AI agent that turns Montgomery's open data into actionable insights — and reveals the gap between what's actually happening in the city and what people think is happening based on media coverage.
>
> Let me walk you through the problem, the solution, and a live demo."

**[Press → to go to Slide 2]**

---

### ⏱️ 0:25–1:00 — SLIDE 2: Problem & Solution (35 sec)
**[SCREEN: pitch.html → Slide 2 (Problem & Solution)]**

> "Montgomery has rich open data — 911 calls, business licenses, code violations, 311 service requests — but it's spread across multiple portals and hard to access.
>
> Residents can't easily understand safety trends. And here's the key insight: media coverage focuses almost exclusively on violent crime, creating a perception gap. The data tells a different story.
>
> SafetyLens solves this by unifying 5 city datasets behind a single AI agent. You ask a question in plain English — the agent queries the live APIs, analyzes the data, and gives you a clear answer. Plus, it uses Bright Data to scrape news and compare public perception against the actual statistics."

**[Press → to go to Slide 3]**

---

### ⏱️ 1:00–1:20 — SLIDE 3: Challenge Areas (20 sec)
**[SCREEN: pitch.html → Slide 3 (All 4 Challenge Areas)]**

> "SafetyLens addresses all four challenge areas: Public Safety through 911 analytics, Civic Access through natural language AI, Economic Growth through business license analysis, and Smart Cities through 311 infrastructure tracking.
>
> It's not just one track — it connects all four."

**[Press → to go to Slide 4]**

---

### ⏱️ 1:20–1:50 — SLIDE 4: Architecture (30 sec)
**[SCREEN: pitch.html → Slide 4 (Architecture)]**

> "Here's how it works. A user asks a question — the LangGraph agent, using the ReAct pattern, plans which tools to use, queries the relevant API endpoints, reasons over the results, and returns an answer with data.
>
> There are 8 custom tools built into the agent — covering 911 monthly and daily data, business licenses, code violations, 311 requests, dataset schema exploration, statistical computation, and Bright Data news scraping.
>
> All data comes from Montgomery's real ArcGIS open data portal — these are live API calls, not static data."

**[Now switch to Streamlit tab]**

---

### ⏱️ 1:50–3:20 — LIVE STREAMLIT DEMO (90 sec)
**[SCREEN: Streamlit app at localhost:8501]**

#### Page 1: AI Chat Agent (30 sec)
**[Click on "💬 AI Chat Agent" in sidebar]**

> "Let me show you the live app. This is the AI Chat Agent. I can type any question — let me ask: 'What are the 911 call trends in Montgomery?'"

**[If pre-loaded, show the response. If typing live, wait for response]**

> "The agent automatically queried the 911 monthly dataset, analyzed the numbers, and came back with a detailed breakdown — emergency vs non-emergency calls, wireless vs landline trends, and actionable recommendations like a 311 diversion campaign to reduce the 35% of calls that are non-emergencies."

#### Page 2: 911 Dashboard (20 sec)
**[Click on "📊 911 Analytics Dashboard" in sidebar]**

> "Here's the 911 Dashboard — interactive Plotly charts showing call volume trends, emergency vs non-emergency breakdown, and phone service provider analysis. All of this is pulled live from the city's API."

#### Page 3: Business & Code (15 sec)
**[Click on "🏢 Business & Code Analysis" in sidebar]**

> "The Business and Code Analysis page cross-references business license data with code violations — helping identify areas where economic development and enforcement intersect."

#### Page 4: 311 Requests (10 sec)
**[Click on "📋 311 Service Requests" in sidebar]**

> "311 Service Requests shows infrastructure and maintenance patterns across the city."

#### Page 5: Perception vs Reality (15 sec)
**[Click on "📰 Perception vs Reality" in sidebar]**

> "And this is the key differentiator — the Perception vs Reality page. Using Bright Data's SERP API, we scrape recent news articles about Montgomery and compare the media narrative against what the 911 data actually shows. The gap is significant — media focuses on violent crime while the data shows most calls are medical, administrative, and welfare-related."

**[Switch back to pitch.html tab]**

---

### ⏱️ 3:20–3:50 — SLIDE 6: Perception Gap (30 sec)
**[SCREEN: pitch.html → Slide 6 (Perception Gap)]**
**[Press → until you reach Slide 6 if needed]**

> "This perception gap is our core insight. On the left — reality from the data: most 911 calls are non-violent, trends are stable, 86% of calls come from wireless devices, and the city has active 311 and Code Enforcement services.
>
> On the right — media perception: almost all coverage focuses on violent crime, implies an escalating crisis, and never mentions the non-emergency calls or city services that are actually working.
>
> Our recommendation to the city: publish a monthly data-driven safety dashboard to close this gap and rebuild public confidence."

**[Press → to go to Slide 7]**

---

### ⏱️ 3:50–4:15 — SLIDE 7: Tech Stack (25 sec)
**[SCREEN: pitch.html → Slide 7 (Tech Stack)]**

> "On the technology side — the agent is built with LangGraph using the ReAct reasoning pattern, powered by OpenAI GPT-4. The frontend is Streamlit with Plotly visualizations. Data comes from 5 live ArcGIS REST API endpoints. And Bright Data provides the news scraping capability for the perception analysis.
>
> Everything is open source on GitHub — the full codebase, documentation, and a self-contained demo page on GitHub Pages."

**[Press → to go to Slide 8]**

---

### ⏱️ 4:15–4:45 — SLIDE 8: Scoring Alignment (30 sec)
**[SCREEN: pitch.html → Slide 8 (Scoring)]**

> "Let me map to the judging criteria. For Challenge Consistency — we cover all 4 tracks with live Montgomery data. For Quality — this is a production-grade agent with 8 tools, interactive charts, and a polished UI. For Originality — an AI that reasons over city data and compares it to media sentiment is new. For Social Value — we empower residents and help the city optimize resources. For Commercialization — any city with an open data portal can deploy SafetyLens as a SaaS product. And we've integrated Bright Data for the bonus 3 points."

**[Press → to go to Slide 9]**

---

### ⏱️ 4:45–5:00 — SLIDE 9: Close (15 sec)
**[SCREEN: pitch.html → Slide 9 (Thank You / CTA)]**

> "SafetyLens Montgomery — see the full picture of your city. Data-driven. AI-powered. Perception-aware.
>
> You can try the live demo right now on GitHub Pages, and the full source code is on GitHub. Thank you for watching."

**[Hold on final slide for 3 seconds]**

---

## ✅ POST-RECORDING CHECKLIST

- [ ] Video is under 5 minutes
- [ ] Audio is clear, no background noise
- [ ] All Streamlit pages loaded properly on camera
- [ ] Pitch slides are readable (no glare/blur)
- [ ] Upload to **YouTube (Unlisted)** or **Loom (public link)**
- [ ] Copy the public URL → paste into hackathon submission
- [ ] Test the URL in an incognito browser to confirm public access

## 🎥 RECORDING TIPS

- **Speed:** Practice once before recording — aim for calm, confident pacing
- **Cursor:** Move your mouse slowly and deliberately to guide the viewer's eye
- **Transitions:** Pause 1 second when switching between pitch.html and Streamlit
- **Errors:** If the AI agent takes too long, just say "while that loads..." and move on
- **Face cam:** Optional — bottom-left corner if you want. Not required.
- **Resolution:** Record at 1080p minimum
- **Upload:** YouTube Unlisted = instant public link. Loom also works.
