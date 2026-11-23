import re
import datetime as dt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

import data, ml, chain, security, crops
import assistant
import irrigation

try:
    from streamlit_geolocation import streamlit_geolocation
except Exception:
    streamlit_geolocation = None

st.set_page_config(page_title="Secure Climate Intelligence", page_icon="🌦️", layout="wide", initial_sidebar_state="expanded")

pio.templates.default = "plotly_white"
# ---------- Premium Dark Design System ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #F1F8FF;
    --sidebar: #E8F4FF;
    --card: #FFFFFF;
    --border: #D6E8F7;
    --primary: #38BDF8;
    --purple: #6366F1;
    --success: #10B981;
    --text: #183B56;
    --muted: #647C91;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(56,189,248,.13), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(147,197,253,.18), transparent 28%),
        linear-gradient(135deg, #F8FCFF 0%, #EFF8FF 50%, #F5FAFF 100%);
    color: var(--text);
}


.block-container {
    max-width: 1650px;
    padding-top: 1.8rem;
    padding-bottom: 3.5rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

[data-testid="stVerticalBlock"] {
    gap: 1.1rem;
}



[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E0F2FE 0%, #F0F9FF 55%, #FFFFFF 100%);
    border-right: 1px solid #D6E8F7;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    line-height: 1.5;
}


[data-testid="stSidebar"] * {
    color: #183B56;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 11px 13px;
    border-radius: 10px;
    transition: all .2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(59,130,246,.15);
}


/* Premium Sidebar Navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 11px;
    padding: 11px 14px;
    transition: all .2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #E0F2FE;
    border-color: #BAE6FD;
    transform: translateX(3px);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(100deg, #BAE6FD, #DBEAFE);
    border-color: #7DD3FC;
    box-shadow: 0 4px 15px rgba(56,189,248,.12);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #075985 !important;
    font-weight: 700;
}


h1, h2, h3, h4 {
    color: #183B56 !important;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
}

h1 {
    letter-spacing: -0.8px;
}

h2, h3 {
    letter-spacing: -0.4px;
}

p, label, .stMarkdown {
    color: #36566F;
}

.hero {
    padding: 32px;
    border-radius: 22px;
    color: white;
    background: linear-gradient(120deg, #142B4B, #1D4ED8 65%, #6D43C8);
    box-shadow: 0 15px 45px rgba(0,0,0,.25);
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,.10);
}

.hero h1 {
    color: white !important;
    font-size: 2.15rem;
    margin-bottom: 8px;
}

.hero p {
    color: #DCEAFE;
    font-size: 1rem;
}

.eyebrow {
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .15em;
    color: #BFDBFE;
    margin-bottom: 10px;
}


.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #F1F5FF;
    margin: 18px 0 8px;
    padding-left: 12px;
    border-left: 3px solid #3B82F6;
}

.section-sub {
    color: #9FB0C8;
    font-size: .9rem;
    margin-bottom: 20px;
    line-height: 1.6;
}



.kpi {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, #FFFFFF, #F5FAFF);
    border: 1px solid #D6E8F7;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 22px rgba(56, 126, 170, .08);
    min-height: 125px;
    transition: all .25s ease;
}

.kpi::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #38BDF8, #2563EB);
}

.kpi:hover {
    transform: translateY(-5px);
    border-color: #7DD3FC;
    box-shadow: 0 12px 28px rgba(56, 126, 170, .14);
}

.kpi .label {
    color: #647C91;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .5px;
}

.kpi .value {
    font-family: 'Space Grotesk', sans-serif;
    color: #0284C7;
    font-size: 2rem;
    font-weight: 700;
    margin-top: 10px;
}

.kpi .hint {
    color: #7890A5;
    font-size: .76rem;
    margin-top: 5px;
}



.panel {
    position: relative;
    background: linear-gradient(145deg, #FFFFFF, #F5FAFF);
    border: 1px solid #D6E8F7;
    border-radius: 18px;
    padding: 23px;
    box-shadow: 0 8px 25px rgba(56, 126, 170, .08);
    transition: all .25s ease;
}

.panel:hover {
    border-color: #7DD3FC;
    box-shadow: 0 12px 30px rgba(56, 126, 170, .14);
}


.small-note {
    color: #94A3B8;
    font-size: .82rem;
}

div[data-testid="stMetric"] {
    background: #17243A;
    border: 1px solid var(--border);
    padding: 15px;
    border-radius: 15px;
}

div[data-testid="stMetric"] label {
    color: #94A3B8;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #60A5FA;
}


.stButton > button,
.stDownloadButton > button {
    min-height: 42px;
    border-radius: 11px;
    font-weight: 700;
    border: 1px solid #BAE6FD;
    background: linear-gradient(145deg, #FFFFFF, #EAF6FF);
    color: #075985;
    transition: all .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #38BDF8;
    color: #0369A1;
    background: #E0F2FE;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(56,189,248,.15);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #0EA5E9, #2563EB);
    border: none;
    color: white;
    box-shadow: 0 5px 15px rgba(56,189,248,.22);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(100deg, #0284C7, #1D4ED8);
    color: white;
}



.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #FFFFFF !important;
    color: #183B56 !important;
    border: 1px solid #CFE5F5 !important;
    border-radius: 11px !important;
    padding: 10px 12px;
    transition: all .2s ease;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,.16);
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94A3B8 !important;
}



.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CFE5F5 !important;
    border-radius: 10px !important;
    color: #183B56 !important;
}

.stSelectbox svg,
.stMultiSelect svg {
    fill: #647C91 !important;
}

.stSelectbox div[data-baseweb="select"] *,
.stMultiSelect div[data-baseweb="select"] * {
    color: #183B56 !important;
}

[data-baseweb="popover"] {
    background: #FFFFFF !important;
    border: 1px solid #D6E8F7 !important;
}

[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[data-baseweb="option"]:hover {
    background: #E0F2FE !important;
}


.stTabs [data-baseweb="tab"] {
    color: #A9BAD0;
}

.stTabs [aria-selected="true"] {
    color: #60A5FA !important;
}

hr {
    border-color: #263650;
}

[data-testid="stDataFrame"] {
    border: 1px solid #263650;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}


/* Premium Sky Blue Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #EFF8FF;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #38BDF8, #60A5FA);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #0284C7;
}


@media (max-width: 768px) {
    .hero {
        padding: 22px;
    }

    .hero h1 {
        font-size: 1.55rem;
    }

    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)



def hero(kicker, title, subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">{kicker}</div><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def heading(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle: st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

def kpi(label, value, hint=""):
    st.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>', unsafe_allow_html=True)

def safe_float(v, default=0):
    try: return float(v) if v is not None else default
    except (TypeError, ValueError): return default

# ---------- Authentication ----------
security.init()
if "user" not in st.session_state: st.session_state.user = None
if not st.session_state.user:
    left, right = st.columns([1.15, .85], gap="large")
    with left:
        hero("CLIMATE • AGRICULTURE • RESEARCH", "Secure Climate Intelligence", "One workspace for weather intelligence, climate research and smarter agricultural decisions.")
        st.markdown("### Welcome to your climate research workspace")
        st.write("Sign in to explore live conditions, long-term climate signals, crop suitability screening and research-ready datasets.")
        st.markdown("- 🌦️ Live weather and environmental indicators\n- 🌱 Weather-informed crop screening\n- 📈 Climate trends and ML experiments\n- 🔐 Auditable data snapshots")
    with right:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Sign in")
        tab1, tab2 = st.tabs(["Login", "Create account"])
        with tab1:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("Login to workspace", type="primary", use_container_width=True):
                ok, msg = security.login(u, p)
                if ok: st.session_state.user = (u, msg); st.rerun()
                else: st.error(msg)
        with tab2:
            nu = st.text_input("Choose username", key="reg_u")
            npw = st.text_input("Choose password (8+ characters)", type="password", key="reg_p")
            if st.button("Create account", use_container_width=True):
                ok, msg = security.register(nu, npw)
                (st.success if ok else st.error)(msg)
        st.caption("First run demo admin: admin / Admin@123 — change it after initial access.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

user, role = st.session_state.user

# ---------- Sidebar and location ----------

with st.sidebar:
    st.markdown("""
    <div style="
        padding: 18px 12px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1D4ED8, #6D43C8);
        margin-bottom: 18px;
        border: 1px solid rgba(255,255,255,.12);
    ">
        <div style="font-size: 30px;">🌦️</div>
        <div style="
            font-size: 21px;
            font-weight: 800;
            color: white;
            letter-spacing: .5px;
        ">SCI Platform</div>
        <div style="
            font-size: 9px;
            color: #DBEAFE;
            letter-spacing: 1.5px;
            margin-top: 5px;
        ">SECURE CLIMATE INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #FFFFFF, #EAF6FF);
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(56,189,248,.08);
    ">
        <div style="font-size:11px;color:#647C91;font-weight:700;">
            SIGNED IN AS
        </div>
        <div style="font-weight:700;color:#183B56;margin-top:4px;">
            👤 {user}
        </div>
        <div style="font-size:11px;color:#0284C7;margin-top:3px;">
            {role.title()}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("↪ Log out", use_container_width=True):
        st.session_state.user = None
        st.rerun()

    st.divider()
    st.markdown("### 🧭 WORKSPACE")

    st.markdown(f"**Signed in:** {user}  ·  {role.title()}")
    if st.button(
        "↪ Log out",
        use_container_width=True,
        key="sidebar_logout"
):
        st.session_state.user = None
        st.rerun()
    st.divider()
    st.markdown("### WORKSPACE")
    pages = [
    "Overview",
    "Live Weather",
    "Smart Agriculture",
    "Crop Calendar",
    "Climate Research",
    "AI / ML Lab",
    "AI Climate Assistant",
    "Smart Irrigation Advisor",
    "Anomaly Detection",
    "Blockchain Ledger",
    "Security & Audit",
    "Research Export"
]
    page = st.radio(
    "Navigate",
    pages,
    label_visibility="collapsed",
    key="main_navigation"
    )
    st.divider()
    st.markdown("### 📍 Study location")
    loc = streamlit_geolocation() if streamlit_geolocation else None
    gps_lat = gps_lon = None
    if loc and loc.get("latitude") is not None and loc.get("longitude") is not None:
        gps_lat, gps_lon = float(loc["latitude"]), float(loc["longitude"])
        try: gps_name = data.reverse_coords(gps_lat, gps_lon)
        except Exception: gps_name = f"GPS ({gps_lat:.3f}, {gps_lon:.3f})"
        st.success(gps_name)
    else:
        st.caption("Allow browser location or choose a city manually.")
    city = st.text_input("City", value=st.session_state.get("study_city", "Asansol"), key="city_input")
    use_gps = st.checkbox("Use detected GPS", value=bool(gps_lat is not None and gps_lon is not None), disabled=gps_lat is None)
    years = st.select_slider("Historical window", options=[5, 10, 15, 20, 25, 30], value=20)
    if use_gps:
        lat, lon = gps_lat, gps_lon; place = gps_name
    else:
        if not re.fullmatch(r"[A-Za-z .\-]{2,40}", city or ""):
            st.error("Enter a valid city name."); st.stop()
        try:
            lat, lon, resolved = data.coords(city); place = resolved
            st.session_state.study_city = city
        except Exception as e:
            st.error(f"Location lookup failed: {e}"); st.stop()
    st.caption(f"Coordinates: {lat:.4f}, {lon:.4f}")

# ---------- Shared data ----------
end = dt.date.today() - dt.timedelta(days=7)
start = dt.date(end.year - years, 1, 1)
try:
    hist = data.history(lat, lon, str(start), str(end))
    current, forecast = data.live(lat, lon)
except Exception as e:
    st.error(f"Weather data could not be loaded: {e}")
    st.info("Check internet connectivity, then refresh the app.")
    st.stop()
if hist.empty or len(hist) < 40:
    st.error("Not enough historical observations for the selected analysis."); st.stop()
security.log(user, f"view {page} | {place}")

# ---------- Pages ----------
if page == "Overview":
    hero("YOUR RESEARCH COMMAND CENTRE", f"Climate intelligence for {place}", "Understand today's conditions, explore long-term patterns and turn weather signals into better-informed decisions.")
    try: air = data.aqi(lat, lon); aqi_val = air.get("us_aqi")
    except Exception: air = {}; aqi_val = None
    c = st.columns(5)
    vals = [("TEMPERATURE", f"{safe_float(current.get('temperature_2m')):.1f}°C", "Current air temperature"), ("HUMIDITY", f"{safe_float(current.get('relative_humidity_2m')):.0f}%", "Relative humidity"), ("WIND SPEED", f"{safe_float(current.get('wind_speed_10m')):.1f}", "km/h"), ("PRESSURE", f"{safe_float(current.get('surface_pressure')):.0f}", "hPa"), ("US AQI", str(aqi_val) if aqi_val is not None else "N/A", "Air quality index")]
    for col, item in zip(c, vals):
        with col: kpi(*item)
    st.write("")
    a, b = st.columns([1.5, 1])
    with a:
        heading("7-day weather outlook", "Forecast supplied by Open-Meteo; this is distinct from the platform's experimental ML forecast.")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast.time, y=forecast.tmax, name="Max temp", mode="lines+markers", line=dict(color="#e28b45", width=3)))
        fig.add_trace(go.Scatter(x=forecast.time, y=forecast.tmin, name="Min temp", mode="lines+markers", line=dict(color="#398bba", width=3), fill="tonexty", fillcolor="rgba(57,139,186,.08)"))
        fig.update_layout(height=320, margin=dict(l=10,r=10,t=25,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig, use_container_width=True)
    with b:
        heading("Environmental watch", "Simple threshold flags from the available forecast.")
        flags = []
        for _, r in forecast.iterrows():
            if r.tmax >= 40: flags.append(("High temperature", f"{r.time}: {r.tmax:.1f}°C", "warning"))
            if r.rain >= 64.5: flags.append(("Heavy rainfall", f"{r.time}: {r.rain:.1f} mm", "warning"))
        if aqi_val is not None and aqi_val > 150: flags.append(("Poor air quality", f"US AQI {aqi_val}", "warning"))
        if not flags: st.success("No configured high-temperature / heavy-rain / AQI threshold flags in the current snapshot.")
        for title, detail, _ in flags: st.warning(f"**{title}**  ·  {detail}")
        st.markdown("<div class='small-note'>Threshold flags are screening indicators, not official emergency alerts.</div>", unsafe_allow_html=True)
    st.divider()
    heading("Climate snapshot", f"Daily archive from {start} to {end} · {len(hist):,} observations")
    x, y, z = st.columns(3)
    with x: kpi("MEAN TEMPERATURE", f"{hist.tmean.mean():.1f}°C", "Across selected historical window")
    with y: kpi("TOTAL RAINFALL", f"{hist.rain.sum():,.0f} mm", "Accumulated archive rainfall")
    with z: kpi("HOT DAYS ≥ 40°C", f"{(hist.tmax >= 40).sum():,}", "Count in selected archive")
    st.caption("Data source: Open-Meteo historical archive, forecast and air-quality services. Availability and coverage can vary by location.")

elif page == "Live Weather":
    hero("WEATHER MONITOR", f"Live conditions · {place}", "Current observations, forecast context and environmental indicators.")
    try: air = data.aqi(lat, lon)
    except Exception: air = {}
    cols = st.columns(5)
    for col, (label, value, unit) in zip(cols, [("Temperature",current.get("temperature_2m"),"°C"),("Humidity",current.get("relative_humidity_2m"),"%"),("Wind",current.get("wind_speed_10m"),"km/h"),("Pressure",current.get("surface_pressure"),"hPa"),("US AQI",air.get("us_aqi"),"")]):
        col.metric(label, f"{value}{unit}" if value is not None else "N/A")
    heading("7-day forecast")
    f1, f2 = st.columns(2)
    with f1: st.plotly_chart(px.line(forecast, x="time", y=["tmax","tmin"], markers=True, title="Daily temperature range", color_discrete_sequence=["#e28b45","#398bba"]), use_container_width=True)
    with f2: st.plotly_chart(px.bar(forecast, x="time", y="rain", title="Forecast precipitation (mm)", color="rain", color_continuous_scale="Teal"), use_container_width=True)
    st.dataframe(forecast, use_container_width=True, hide_index=True)
    if air: st.json(air)

elif page == "Smart Agriculture":
    hero("AGRICULTURE INTELLIGENCE", "Weather-informed crop screening", "A transparent first-pass shortlist using current temperature, humidity, forecast rainfall and month.")
    st.warning("This is an indicative screening tool, not a validated agronomic prescription. It does not yet use field soil tests, variety, irrigation access, pests or local sowing advisories.")
    temp = safe_float(current.get("temperature_2m"), hist.tmean.tail(7).mean())
    humidity = safe_float(current.get("relative_humidity_2m"), 50)
    rain7 = safe_float(forecast.rain.sum())
    a,b,c = st.columns(3)
    a.metric("Current temperature", f"{temp:.1f}°C"); b.metric("Relative humidity", f"{humidity:.0f}%"); c.metric("7-day forecast rain", f"{rain7:.1f} mm")
    recs = crops.recommend(temp, humidity, rain7, dt.date.today().month)
    category = st.selectbox("Crop group", ["All", "Field crop", "Vegetable", "Fruit"])
    view = [r for r in recs if category == "All" or r["Category"] == category]
    st.subheader("Suitability shortlist")
    if view:
        top = view[:3]; cc = st.columns(3)
        for col, r in zip(cc, top):
            with col:
                st.markdown(f"<div class='panel'><div class='small-note'>{r['Category'].upper()}</div><h3 style='color:#153943;margin:5px 0'>{r['Crop']}</h3><div style='font-size:2rem;font-weight:700;color:#147c75'>{r['Suitability']}<span style='font-size:1rem'>/100</span></div><p class='small-note'>{r['Reason']}</p></div>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(view), use_container_width=True, hide_index=True)
    st.caption("Scores are heuristic rule-based scores, not probabilities or measured yield predictions. Validate locally before planting.")

elif page == "Crop Calendar":
    hero("SEASONAL PLANNING", "Crop calendar explorer", "Explore indicative crop windows by month and crop group; local calendars and varieties take priority.")
    month = st.select_slider("Select planning month", options=list(range(1,13)), value=dt.date.today().month, format_func=lambda m: dt.date(2026,m,1).strftime("%B"))
    group = st.selectbox("Crop group", ["All", "Field crop", "Vegetable", "Fruit"])
    rows=[]
    for crop, cat, months, lo, hi, rain_target, note in crops.CROPS:
        if (group == "All" or cat == group): rows.append({"Crop":crop,"Category":cat,"Indicative window": "In season" if month in months else "Outside listed window", "Temperature band":f"{lo}–{hi}°C", "Monthly rainfall guide":f"~{rain_target} mm", "Notes":note})
    cal = pd.DataFrame(rows)
    st.dataframe(cal, use_container_width=True, hide_index=True)
    st.info("Calendar windows are broad illustrative month ranges embedded in the starter crop catalogue. They are not district-specific sowing dates.")

elif page == "Climate Research":
    hero("LONG-TERM CLIMATE ANALYSIS", "Climate research workspace", "Explore observed historical variability and non-parametric trend signals.")
    annual = hist.assign(year=hist.time.dt.year).groupby("year").agg(mean_temp=("tmean","mean"), total_rain=("rain","sum"), hot_days=("tmax",lambda s:int((s>=40).sum())), max_rain=("rain","max")).reset_index()
    if len(annual)>3: annual = annual.iloc[:-1]
    z,p,slope = ml.mann_kendall(annual.mean_temp)
    a,b,c,d = st.columns(4)
    with a: kpi("MK Z-STATISTIC", f"{z:.2f}", "Mann–Kendall test")
    with b: kpi("P-VALUE", f"{p:.4f}", "Two-sided normal approximation")
    with c: kpi("SEN SLOPE", f"{slope*10:+.2f}°C", "Approx. per decade")
    with d: kpi("YEARS ANALYSED", f"{len(annual)}", "Completed annual records")
    st.markdown("**Interpretation:** " + ("Statistically significant monotonic trend at α = 0.05." if p < .05 else "No statistically significant monotonic trend at α = 0.05."))
    l,r = st.columns(2)
    with l: st.plotly_chart(px.scatter(annual, x="year", y="mean_temp", trendline="ols", title="Annual mean temperature", labels={"year":"Year","mean_temp":"°C"}), use_container_width=True)
    with r: st.plotly_chart(px.bar(annual, x="year", y="total_rain", title="Annual total rainfall", labels={"year":"Year","total_rain":"mm"}), use_container_width=True)
    st.plotly_chart(px.line(annual, x="year", y="hot_days", markers=True, title="Days with Tmax ≥ 40°C"), use_container_width=True)
    st.subheader("Monthly climatology")
    monthly = hist.assign(month=hist.time.dt.month).groupby("month").agg(temp=("tmean","mean"),rain=("rain","mean")).reset_index()
    q1,q2 = st.columns(2)
    with q1: st.plotly_chart(px.bar(monthly,x="month",y="temp",title="Mean temperature by calendar month"),use_container_width=True)
    with q2: st.plotly_chart(px.bar(monthly,x="month",y="rain",title="Mean daily rainfall by calendar month"),use_container_width=True)
    st.dataframe(annual, use_container_width=True, hide_index=True)
    st.caption("Trend results depend on selected period, missing-data coverage and serial dependence. Treat this as exploratory analysis, not attribution of climate change.")

elif page == "AI / ML Lab":
    hero("EXPERIMENT WORKBENCH", "Machine-learning laboratory", "Time-ordered model evaluation, baseline comparison and experimental forecast outputs.")
    with st.spinner("Training models on the selected historical series..."):
        try:
            metrics, models, test = ml.compare(hist)
            best = metrics.iloc[0]["Model"]
            st.success(f"Lowest test RMSE in this run: {best}")
            st.dataframe(metrics.round(3), use_container_width=True, hide_index=True)
            candidates = [m for m in models if m in test.columns]
            show = st.selectbox("Model prediction series", candidates, index=candidates.index(best) if best in candidates else 0)
            fig = go.Figure(); fig.add_trace(go.Scatter(x=test.time.tail(150),y=test.y.tail(150),name="Observed",line=dict(color="#183f4b",width=2.5))); fig.add_trace(go.Scatter(x=test.time.tail(150),y=test[show].tail(150),name=show,line=dict(color="#159b88",width=2)))
            fig.update_layout(title="Held-out test segment · observed vs model",height=350)
            st.plotly_chart(fig,use_container_width=True)
            forecast_ml = ml.forecast7(models[show], hist)
            st.plotly_chart(px.line(forecast_ml,x="time",y="pred_tmean",markers=True,title=f"Experimental recursive 7-day temperature forecast · {show}"),use_container_width=True)
            if hasattr(models[show],"feature_importances_"):
                st.plotly_chart(px.bar(x=models[show].feature_importances_,y=ml.FEATS,orientation="h",title="Feature importance (tree model)"),use_container_width=True)
            acc,f1,cm,_ = ml.rain_clf(hist)
            st.subheader("Rain occurrence classification")
            x,y = st.columns(2); x.metric("Accuracy",f"{acc:.1%}"); y.metric("F1 score",f"{f1:.3f}")
            st.plotly_chart(px.imshow(cm,text_auto=True,x=["Dry","Wet"],y=["Dry","Wet"],labels=dict(x="Predicted",y="Observed"),title="Confusion matrix"),use_container_width=True)
        except Exception as e: st.error(f"Model experiment failed: {e}")
    st.info("The ML forecast is a recursive statistical experiment trained on historical temperatures. It is not the same as the Open-Meteo meteorological forecast and should not be used as an operational warning.")

elif page == "Anomaly Detection":
    hero("DATA QUALITY & EXTREMES", "Anomaly detection", "Use Isolation Forest to flag unusual combinations in the historical weather archive.")
    contamination = st.slider("Expected anomaly fraction",0.5,5.0,1.0,0.5)/100
    flagged = ml.anomalies(hist, contamination)
    count = int(flagged.anomaly.sum())
    a,b,c = st.columns(3)
    with a: kpi("FLAGGED OBSERVATIONS",f"{count}","Model-identified unusual rows")
    with b: kpi("TOTAL OBSERVATIONS",f"{len(flagged):,}","Input archive")
    with c: kpi("FLAG RATE",f"{count/len(flagged):.2%}","Configured contamination is approximate")
    st.plotly_chart(px.scatter(flagged,x="time",y="tmax",color="anomaly",color_discrete_map={True:"#d85d55",False:"#9fb7bd"},title="Maximum temperature anomalies"),use_container_width=True)
    st.dataframe(flagged[flagged.anomaly].drop(columns="anomaly"),use_container_width=True,hide_index=True)
    st.caption("An anomaly is not necessarily an error or a climate extreme. Investigate source quality and local context.")

elif page == "Blockchain Ledger":
    hero("DATA PROVENANCE", "Climate snapshot ledger", "Hash-linked records make stored analysis snapshots tamper-evident; this is a local demonstration ledger, not a public blockchain.")
    st.write("A SHA-256 digest is calculated from each snapshot, linked to the previous block and sealed with a small proof-of-work step.")
    if st.button("⛏️ Add current climate snapshot",type="primary"):
        block = chain.add(place,lat,lon,str(start),str(end),hist)
        security.log(user,f"mined climate block {block['index']}")
        st.success(f"Snapshot stored · block #{block['index']} · {block['hash'][:24]}…")
    ledger = chain.load()
    if ledger:
        valid, idx, msg = chain.verify(ledger)
        (st.success if valid else st.error)(msg)
        st.dataframe(pd.DataFrame(ledger)[["index","city","start","end","rows","mean_temp","nonce","hash","prev"]],use_container_width=True,hide_index=True)
        with st.expander("Integrity demonstration"):
            st.caption("The test below changes only an in-memory copy; it does not alter the saved ledger.")
            ix = st.number_input("Block index",0,len(ledger)-1,0)
            if st.button("Simulate tampering"):
                altered=[dict(x) for x in ledger]; altered[int(ix)]["mean_temp"] += 5
                ok, bad_i, message = chain.verify(altered)
                st.error(f"Tampering detected at block {bad_i}: {message}" if not ok else "No mismatch found")
    else: st.info("No snapshots stored yet. Add the current snapshot to create the first block.")

elif page == "Security & Audit":
    hero("ACCOUNT & PLATFORM SECURITY", "Security and audit centre", "Account controls, input plausibility checks and admin-only activity review.")
    st.markdown("<div class='panel'><b>Session</b><br>Authenticated user: " + user + "<br>Role: " + role + "<br>Database: local SQLite</div>",unsafe_allow_html=True)
    st.subheader("Weather input plausibility demo")
    if st.button("Run synthetic invalid-reading test"):
        sample=hist.copy(); mid=len(sample)//2; sample.loc[mid,["tmax","tmin","rain","wind"]]=[80,70,900,20]
        invalid=sample[~sample.apply(security.plausible,axis=1)]
        st.error(f"Range validation flagged {len(invalid)} invalid record(s).")
        st.dataframe(invalid,use_container_width=True,hide_index=True)
    if role == "admin":
        st.subheader("Recent audit events · admin only")
        st.dataframe(pd.DataFrame(security.audit_log(),columns=["Timestamp","User","Action"]),use_container_width=True,hide_index=True)
    else: st.info("Audit event history is restricted to administrators.")
    st.caption("Use a strong unique password and change the demo administrator password before deployment. This local demo is not a substitute for production security review.")


elif page == "AI Climate Assistant":
    hero(
        "AI CLIMATE ASSISTANT",
        "Your intelligent climate companion",
        "Ask questions about weather, rainfall, crops and agriculture."
    )

    st.caption(f"📍 Current study location: {place}")

    # Build context using actual application data
    try:
        climate_context = assistant.build_climate_context(
            place, current, forecast, hist
        )

        # Initialize chat history
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        # Clear conversation button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()

        # Suggested questions
        st.markdown("#### What would you like to know?")

        col1, col2 = st.columns(2)

        if col1.button("🌧️ Rainfall forecast"):
            st.session_state.pending_question = (
                "Explain the rainfall forecast for my location."
            )

        if col2.button("🌱 Best crops"):
            st.session_state.pending_question = (
                "Which crops are suitable for my current weather?"
            )

        if col1.button("🌡️ Weather analysis"):
            st.session_state.pending_question = (
                "Analyze my current weather conditions."
            )

        if col2.button("💧 Soil moisture"):
            st.session_state.pending_question = (
                "Explain soil moisture conditions and irrigation guidance. "
                "Tell me if actual soil moisture data is available."
            )

        # Display previous messages
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user question
        question = st.chat_input(
            "Ask anything about climate or agriculture..."
        )

        # Handle suggested questions
        if "pending_question" in st.session_state:
            question = st.session_state.pop("pending_question")

        if question:
            st.session_state.chat_messages.append({
                "role": "user",
                "content": question
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("🌦️ Analyzing your climate data..."):
                    answer = assistant.get_ai_response(
                        question,
                        st.session_state.chat_messages[:-1],
                        climate_context
                    )
                    st.markdown(answer)

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": answer
            })

    except Exception as e:
        st.error(f"AI Assistant Error: {e}")
        st.info("Please check your Groq API key and internet connection.")


elif page == "Smart Irrigation Advisor":
    hero(
        "SMART IRRIGATION ADVISOR",
        "Intelligent water management for agriculture",
        "Analyze rainfall, temperature and field conditions to plan irrigation."
    )

    st.caption(f"📍 Study location: {place}")

    st.markdown("### 🌱 Field Information")

    col1, col2 = st.columns(2)

    crop_names = [item[0] for item in crops.CROPS]

    with col1:
        selected_crop = st.selectbox(
            "Select your crop",
            crop_names
        )

    with col2:
        soil_status = st.selectbox(
            "Current soil condition",
            ["dry", "moist", "wet"],
            format_func=lambda x: {
                "dry": "🏜️ Dry",
                "moist": "🌿 Moist",
                "wet": "💧 Wet"
            }[x]
        )

    st.info(
        "Soil condition is based on your field observation. "
        "A live soil-moisture sensor is not connected."
    )

    if st.button("🔍 Analyze Irrigation Requirement", type="primary"):
        try:
            result = irrigation.assess_irrigation(
                selected_crop,
                current,
                forecast,
                soil_status
            )

            st.markdown("---")
            st.markdown("### 📊 Irrigation Analysis")

            st.subheader(result["headline"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Irrigation Priority",
                result["priority"]
            )

            col2.metric(
                "First 2 Forecast Days",
                f'{result["rain_48h"]} mm',
                help="Approximate rainfall from the first two daily forecast entries."
            )

            col3.metric(
                "7-Day Forecast Rain",
                f'{result["rain_7d"]} mm'
            )

            if result["max_temp"] is not None:
                st.metric(
                    "Maximum Forecast Temperature",
                    f'{result["max_temp"]} °C'
                )

            st.markdown("### 🌦️ Weather Analysis")
            for reason in result["reasons"]:
                st.write("•", reason)

            st.markdown("### 💡 Recommended Actions")
            for action in result["actions"]:
                st.write("✅", action)

            st.markdown("### ⚠️ Important Data Note")
            st.warning(result["data_note"])

            st.caption(
                f"Selected crop: {result['crop']} | "
                f"Reported soil condition: {result['soil_status'].title()}"
            )

        except Exception as e:
            st.error(f"Irrigation analysis failed: {e}")


elif page == "Research Export":
    hero("REPRODUCIBLE RESEARCH", "Dataset & report export", "Download the current location's archive observations and a compact research summary with source and method notes.")
    st.metric("Archive rows",f"{len(hist):,}")
    st.dataframe(hist.tail(12),use_container_width=True,hide_index=True)
    csv = hist.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download historical dataset (CSV)",csv,file_name=f"{re.sub('[^A-Za-z0-9_-]','_',place)}_climate_history.csv",mime="text/csv",type="primary")
    annual = hist.assign(year=hist.time.dt.year).groupby("year").agg(mean_temp=("tmean","mean"),rainfall=("rain","sum"),hot_days=("tmax",lambda s:int((s>=40).sum()))).reset_index()
    z,p,slope=ml.mann_kendall(annual.mean_temp.iloc[:-1] if len(annual)>3 else annual.mean_temp)
    report = ["SECURE CLIMATE INTELLIGENCE PLATFORM — RESEARCH SNAPSHOT",f"Location: {place}",f"Coordinates: {lat:.5f}, {lon:.5f}",f"Period: {start} to {end}",f"Rows: {len(hist)}",f"Mean temperature: {hist.tmean.mean():.2f} °C",f"Total archive rainfall: {hist.rain.sum():.1f} mm",f"Mann-Kendall Z: {z:.3f}",f"Mann-Kendall p-value: {p:.5f}",f"Sen slope: {slope*10:.4f} °C/decade","Source: Open-Meteo historical archive API.","Methods: descriptive daily statistics; annual aggregation; Mann-Kendall trend test and Sen slope.","Limitations: observational coverage, missingness, serial dependence and source revisions may affect results. Trend association is not causal attribution."]
    st.download_button("⬇️ Download research summary (TXT)","\n".join(report).encode("utf-8"),file_name="climate_research_summary.txt",mime="text/plain")
    st.download_button("⬇️ Download annual summary (CSV)",annual.to_csv(index=False).encode("utf-8"),file_name="annual_climate_summary.csv",mime="text/csv")
    st.caption("Exports include source/method notes, but do not yet provide full dataset versioning or a formal reproducibility manifest.")

st.markdown("---")
st.markdown(f"<div class='small-note'>SCI Platform · Study location: <b>{place}</b> · Data window: {start} — {end} · Signed in as {user}</div>",unsafe_allow_html=True)
