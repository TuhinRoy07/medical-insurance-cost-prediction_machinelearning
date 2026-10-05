from string import Template

import altair as alt
import joblib
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------ page setup
st.set_page_config(
    page_title="InsureIQ | Medical Insurance Cost Predictor",
    page_icon="🏥",
    layout="wide",
)

AVG_CHARGES = 13279.12  # average charges in insurance.csv (after removing duplicates)

LIGHT = dict(
    bg="#F5F7FB", card="#FFFFFF", input="#FFFFFF", text="#1F2937", muted="#6B7280",
    border="#E5E7EB", accent="#4F46E5", accent2="#7C3AED", danger="#EF4444",
    shadow="rgba(15,23,42,.07)", grid="#E5E7EB",
    green_bg="#DCFCE7", green_tx="#166534", amber_bg="#FEF3C7", amber_tx="#92400E",
    red_bg="#FEE2E2", red_tx="#991B1B", blue_bg="#DBEAFE", blue_tx="#1E40AF",
)
DARK = dict(
    bg="#0B1220", card="#151E32", input="#1E293B", text="#E5E7EB", muted="#94A3B8",
    border="#2B3A55", accent="#818CF8", accent2="#A78BFA", danger="#F87171",
    shadow="rgba(0,0,0,.45)", grid="#2B3A55",
    green_bg="rgba(34,197,94,.18)", green_tx="#4ADE80", amber_bg="rgba(245,158,11,.18)",
    amber_tx="#FBBF24", red_bg="rgba(239,68,68,.18)", red_tx="#F87171",
    blue_bg="rgba(59,130,246,.2)", blue_tx="#93C5FD",
)

CSS = Template(
    """
<style>
:root {
  --bg:$bg; --card:$card; --input:$input; --text:$text; --muted:$muted; --border:$border;
  --accent:$accent; --accent2:$accent2; --shadow:$shadow;
}
#MainMenu, footer {visibility: hidden;}
.stApp, [data-testid="stAppViewContainer"] {background: var(--bg) !important;}
[data-testid="stHeader"] {background: transparent !important;}
[data-testid="stHeader"] * {color: var(--muted) !important;}
.block-container {padding-top: 1.5rem; max-width: 1150px;}

/* sidebar */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {
  background: var(--card) !important; border-right: 1px solid var(--border);}
[data-testid="stSidebar"] label *, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {color: var(--text) !important;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {color: var(--muted) !important;}

/* inputs */
[data-baseweb="input"], [data-baseweb="input"] > div, [data-baseweb="input"] input,
[data-baseweb="select"] > div, [data-baseweb="select"] div,
[data-testid="stNumberInput"] button {
  background-color: var(--input) !important; color: var(--text) !important;
  border-color: var(--border) !important;}
[data-baseweb="select"] svg, [data-testid="stNumberInput"] svg {fill: var(--text) !important;}
[data-baseweb="popover"], [data-baseweb="popover"] ul, [data-baseweb="popover"] li,
[data-baseweb="menu"] {background: var(--card) !important; color: var(--text) !important;}
[data-baseweb="popover"] li:hover {background: var(--input) !important;}

/* predict button */
button[kind="primary"], button[data-testid="stBaseButton-primary"] {
  background: linear-gradient(120deg, $accent 0%, $accent2 100%) !important;
  color: #fff !important; border: none !important; border-radius: 12px !important;
  font-weight: 700 !important; padding: .65rem 1rem !important; width: 100%;
  box-shadow: 0 8px 20px rgba(79,70,229,.35);}
button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {filter: brightness(1.08);}
button[kind="primary"] *, button[data-testid="stBaseButton-primary"] * {color:#fff !important;}

/* custom components */
.hero {background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 55%, #06B6D4 100%);
  padding: 2rem 2.2rem; border-radius: 18px; box-shadow: 0 10px 30px rgba(79,70,229,.25);
  margin-bottom: 1.4rem;}
.hero h1 {margin:0; font-size:2.1rem; color:#fff !important;}
.hero p {margin:.4rem 0 0 0; font-size:1.02rem; color:#fff !important; opacity:.93;}
.result-card {background: var(--card); border-radius:18px; padding:1.8rem 2rem;
  border:1px solid var(--border); box-shadow:0 6px 22px var(--shadow); text-align:center;
  margin-bottom:1rem;}
.result-label {color: var(--muted); font-size:.85rem; letter-spacing:.08em; text-transform:uppercase;}
.result-value {font-size:3.2rem; font-weight:800; color: var(--accent); line-height:1.15;}
.result-sub {color: var(--muted); font-size:1rem;}
.kpi {background: var(--card); border-radius:14px; padding:1rem 1.2rem;
  border:1px solid var(--border); box-shadow:0 4px 14px var(--shadow); height:100%;}
.kpi .t {color: var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.06em;}
.kpi .v {font-size:1.45rem; font-weight:700; color: var(--text); margin-top:.2rem;}
.kpi .n {font-size:.85rem; color: var(--muted); margin-top:.1rem;}
.section {font-size:1.15rem; font-weight:700; color: var(--text); margin:1.4rem 0 .4rem 0;}
.pill {display:inline-block; padding:.18rem .7rem; border-radius:999px; font-size:.8rem; font-weight:600;}
.green {background:$green_bg; color:$green_tx;} .amber {background:$amber_bg; color:$amber_tx;}
.red {background:$red_bg; color:$red_tx;} .blue {background:$blue_bg; color:$blue_tx;}
.placeholder {background: var(--card); border:2px dashed var(--border); border-radius:18px;
  padding:3.2rem 2rem; text-align:center; color: var(--muted);}
.placeholder .big {font-size:3rem;} .placeholder .h {font-size:1.3rem; font-weight:700;
  color: var(--text); margin:.4rem 0;}
.notice {background:$amber_bg; color:$amber_tx; border-radius:12px; padding:.6rem 1rem;
  font-size:.9rem; margin-bottom:1rem;}
.summary {width:100%; border-collapse:collapse; background: var(--card); border-radius:14px;
  overflow:hidden; border:1px solid var(--border);}
.summary th, .summary td {padding:.65rem 1rem; text-align:left; border-bottom:1px solid var(--border);
  color: var(--text);}
.summary th {color: var(--muted); font-weight:600; width:40%;}
.summary tr:last-child th, .summary tr:last-child td {border-bottom:none;}
.caption {color: var(--muted); font-size:.85rem;}
.disclaimer {color: var(--muted); font-size:.8rem; text-align:center; margin-top:2rem; opacity:.8;}
</style>
"""
)


# ------------------------------------------------------------------ helpers
@st.cache_resource
def load_model():
    return joblib.load("insurance_model.joblib")


def make_row(age, sex, bmi, children, smoker, region):
    return pd.DataFrame(
        [{"age": age, "sex": sex, "bmi": bmi, "children": children,
          "smoker": smoker, "region": region}]
    )


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "blue"
    if bmi < 25:
        return "Normal weight", "green"
    if bmi < 30:
        return "Overweight", "amber"
    return "Obese", "red"


def style_chart(chart, P):
    return (
        chart.configure(background="rgba(0,0,0,0)")
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor=P["text"], titleColor=P["text"], gridColor=P["grid"],
            domainColor=P["grid"], tickColor=P["grid"],
        )
    )


def show_chart(chart):
    try:
        st.altair_chart(chart, width="stretch", theme=None)
    except TypeError:  # older Streamlit versions
        st.altair_chart(chart, use_container_width=True, theme=None)


# ------------------------------------------------------------------ sidebar
toggle = getattr(st, "toggle", st.checkbox)
with st.sidebar:
    dark = toggle("🌙 Dark mode", value=False, key="dark_mode")
    P = DARK if dark else LIGHT
    st.markdown("## 👤 Customer Profile")
    age = st.slider("Age", 18, 64, 35)
    sex = st.radio("Sex", ["male", "female"], horizontal=True)
    bmi = st.slider("BMI", 15.0, 55.0, 27.0, 0.1)
    children = st.number_input("Children covered", min_value=0, max_value=5, value=0, step=1)
    smoker = st.radio("Smoker", ["no", "yes"], horizontal=True)
    region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])
    predict_clicked = st.button("🔮 Predict", type="primary")
    st.caption("Ranges match the training data (age 18-64, BMI 16-53, 0-5 children).")

st.markdown(CSS.safe_substitute(P), unsafe_allow_html=True)

# ------------------------------------------------------------------ header
st.markdown(
    """
    <div class="hero">
        <h1>🏥 InsureIQ</h1>
        <p>Machine-learning powered medical insurance cost estimator.
        Fill in the profile on the left and click <b>Predict</b>.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "`insurance_model.joblib` not found. Run the last cell of the notebook "
        "first, and keep the file in the same folder as app.py."
    )
    st.stop()

# ------------------------------------------------------------------ remember the prediction
current = dict(age=age, sex=sex, bmi=bmi, children=children, smoker=smoker, region=region)
if predict_clicked:
    st.session_state["result"] = current

res = st.session_state.get("result")

if res is None:
    st.markdown(
        """
        <div class="placeholder">
            <div class="big">🔮</div>
            <div class="h">No prediction yet</div>
            <div>Enter the customer details in the sidebar and click <b>Predict</b>
            to see the estimated cost, comparisons and charts.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    if res != current:
        st.markdown(
            '<div class="notice">⚠️ You changed the inputs. Click <b>Predict</b> '
            "to update the results below.</div>",
            unsafe_allow_html=True,
        )

    r = res  # everything below uses the inputs from the last Predict click
    prediction = float(model.predict(make_row(**r))[0])
    alt_smoker = "no" if r["smoker"] == "yes" else "yes"
    alt_prediction = float(model.predict(make_row(**{**r, "smoker": alt_smoker}))[0])
    smoker_cost = prediction if r["smoker"] == "yes" else alt_prediction
    nonsmoker_cost = alt_prediction if r["smoker"] == "yes" else prediction
    diff_avg = prediction - AVG_CHARGES
    cat, cat_color = bmi_category(r["bmi"])

    # ---- result + KPI cards
    left, right = st.columns([1.15, 1])
    with left:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Estimated yearly insurance charges</div>
                <div class="result-value">${prediction:,.2f}</div>
                <div class="result-sub">≈ ${prediction / 12:,.2f} per month</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        k1, k2 = st.columns(2)
        k1.markdown(
            f"""<div class="kpi"><div class="t">BMI category</div>
            <div class="v">{r['bmi']:.1f}</div>
            <div class="n"><span class="pill {cat_color}">{cat}</span></div></div>""",
            unsafe_allow_html=True,
        )
        direction = "above" if diff_avg >= 0 else "below"
        pill_color = "red" if diff_avg >= 0 else "green"
        k2.markdown(
            f"""<div class="kpi"><div class="t">Vs. dataset average</div>
            <div class="v">${abs(diff_avg):,.0f}</div>
            <div class="n"><span class="pill {pill_color}">{direction} average</span></div></div>""",
            unsafe_allow_html=True,
        )
        st.write("")
        k3, k4 = st.columns(2)
        k3.markdown(
            f"""<div class="kpi"><div class="t">If non-smoker</div>
            <div class="v">${nonsmoker_cost:,.0f}</div>
            <div class="n">same profile</div></div>""",
            unsafe_allow_html=True,
        )
        k4.markdown(
            f"""<div class="kpi"><div class="t">If smoker</div>
            <div class="v">${smoker_cost:,.0f}</div>
            <div class="n">same profile</div></div>""",
            unsafe_allow_html=True,
        )

    # ---- charts
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section">🚬 Smoking impact</div>', unsafe_allow_html=True)
        smoke_df = pd.DataFrame(
            {"Profile": ["Non-smoker", "Smoker"], "Charges": [nonsmoker_cost, smoker_cost]}
        )
        bar = (
            alt.Chart(smoke_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=80)
            .encode(
                x=alt.X("Profile:N", sort=None, axis=alt.Axis(labelAngle=0, title=None)),
                y=alt.Y("Charges:Q", axis=alt.Axis(format="$,.0f", title=None)),
                color=alt.Color(
                    "Profile:N",
                    scale=alt.Scale(domain=["Non-smoker", "Smoker"], range=[P["accent"], P["danger"]]),
                    legend=None,
                ),
                tooltip=["Profile", alt.Tooltip("Charges:Q", format="$,.2f")],
            )
            .properties(height=300)
        )
        show_chart(style_chart(bar, P))
        st.markdown(
            f'<div class="caption">For this profile, smoking adds about '
            f"<b>${smoker_cost - nonsmoker_cost:,.0f}</b> per year.</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown('<div class="section">📈 Cost by age (same profile)</div>', unsafe_allow_html=True)
        ages = list(range(18, 65))
        age_rows = pd.concat(
            [make_row(**{**r, "age": a}) for a in ages], ignore_index=True
        )
        age_df = pd.DataFrame({"Age": ages, "Charges": model.predict(age_rows)})
        line = (
            alt.Chart(age_df)
            .mark_line(color=P["accent2"], strokeWidth=3)
            .encode(
                x=alt.X("Age:Q", scale=alt.Scale(zero=False), axis=alt.Axis(title="Age")),
                y=alt.Y("Charges:Q", axis=alt.Axis(format="$,.0f", title=None)),
                tooltip=["Age", alt.Tooltip("Charges:Q", format="$,.2f")],
            )
        )
        here = (
            alt.Chart(pd.DataFrame({"Age": [r["age"]], "Charges": [prediction]}))
            .mark_point(size=140, filled=True, color=P["danger"])
            .encode(x="Age:Q", y="Charges:Q",
                    tooltip=["Age", alt.Tooltip("Charges:Q", format="$,.2f")])
        )
        show_chart(style_chart((line + here).properties(height=300), P))
        st.markdown(
            '<div class="caption">The red dot is this customer. All other inputs are kept fixed.</div>',
            unsafe_allow_html=True,
        )

    # ---- summary table
    st.markdown('<div class="section">🧾 Profile summary</div>', unsafe_allow_html=True)
    items = {
        "Age": r["age"], "Sex": r["sex"].title(), "BMI": f"{r['bmi']:.1f}",
        "Children": r["children"], "Smoker": r["smoker"].title(),
        "Region": r["region"].title(), "Estimated yearly charges": f"${prediction:,.2f}",
    }
    rows = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in items.items())
    st.markdown(f'<table class="summary">{rows}</table>', unsafe_allow_html=True)

st.markdown(
    '<div class="disclaimer">Model: Random Forest with log-transformed target, trained on the '
    "public US insurance dataset. Estimates are for learning purposes only and are not "
    "real insurance quotes.</div>",
    unsafe_allow_html=True,
)