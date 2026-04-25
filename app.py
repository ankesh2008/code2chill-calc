import streamlit as st
import math


st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
)


st.markdown("""
<style>
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #1b1c1f !important;
    color: #e6e6e6 !important;
    font-family: Segoe UI, sans-serif;
}
#MainMenu, header, footer { visibility: hidden; }

/* ── Container ── */
.calc-wrap {
    max-width: 360px;
    margin: auto;
    padding: 10px;
}

/* ── Title ── */
.calc-title {
    font-size: 1.4rem;
    font-weight: 600;
    padding: 10px 0;
}

/* ── Display ── */
.display-box {
    background: #1f2228;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 10px;
}

.display-expr {
    font-size: 0.8rem;
    color: #9aa0a6;
    text-align: right;
}

.display-main {
    font-size: 2.2rem;
    text-align: right;
    font-weight: 500;
}

/* ── Buttons ── */
div[data-testid="column"] button {
    height: 48px !important;
    border-radius: 6px !important;
    font-size: 1rem !important;
    border: none !important;
}

/* numbers */
.num-btn button {
    background: #2a2d33 !important;
    color: white !important;
}

/* operators */
.op-btn button {
    background: #32363f !important;
    color: white !important;
}

/* function */
.fn-btn button {
    background: #23262c !important;
    color: #cfcfcf !important;
    font-size: 0.85rem !important;
}

/* equals */
.eq-btn button {
    background: #4cc2ff !important;
    color: black !important;
    font-weight: bold !important;
}

/* clear */
.clear-btn button {
    background: #3a2b2b !important;
    color: #ff6b6b !important;
}

/* subtle hover */
button:hover {
    filter: brightness(1.15);
}
</style>
""", unsafe_allow_html=True)



def init_state():
    defaults = {
        "expr": "",
        "display": "0",
        "history": [],
        "angle": "DEG",
        "just_evaluated": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
ss = st.session_state



def to_rad(x):
    return x if ss.angle == "RAD" else math.radians(x)

def evaluate(expr: str):

    expr = (expr
        .replace("×", "*")
        .replace("÷", "/")
        .replace("^", "**")
        .replace("π", str(math.pi))
        .replace("e", str(math.e))
    )
    allowed = {
        "__builtins__": {},
        "sin": lambda x: math.sin(to_rad(x)),
        "cos": lambda x: math.cos(to_rad(x)),
        "tan": lambda x: math.tan(to_rad(x)),
        "asin": lambda x: (math.degrees(math.asin(x)) if ss.angle == "DEG" else math.asin(x)),
        "acos": lambda x: (math.degrees(math.acos(x)) if ss.angle == "DEG" else math.acos(x)),
        "atan": lambda x: (math.degrees(math.atan(x)) if ss.angle == "DEG" else math.atan(x)),
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "abs": abs,
        "factorial": math.factorial,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
    }
    result = eval(expr, allowed)
    if isinstance(result, float):
        if result == int(result) and abs(result) < 1e15:
            result = int(result)
        else:
            result = round(result, 10)
    return result


def press(val: str):
    if ss.just_evaluated:

        if val not in ("+", "−", "×", "÷", "^", "%"):
            ss.expr = ""
        ss.just_evaluated = False

    if val == "C":
        ss.expr = ""
        ss.display = "0"
    elif val == "CE":

        ss.expr = ss.expr[:-1]
        ss.display = ss.expr if ss.expr else "0"
    elif val == "=":
        if ss.expr:
            try:
                result = evaluate(ss.expr)
                ss.history.append(f"{ss.expr} = {result}")
                if len(ss.history) > 20:
                    ss.history = ss.history[-20:]
                ss.display = str(result)
                ss.expr = str(result)
                ss.just_evaluated = True
            except ZeroDivisionError:
                ss.display = "Division by Zero"
                ss.expr = ""
            except Exception:
                ss.display = "Syntax Error"
                ss.expr = ""
    elif val == "+/-":
        if ss.expr:
            try:
                result = evaluate(ss.expr)
                ss.expr = str(-result)
                ss.display = ss.expr
            except Exception:
                pass
    elif val in ("sin(", "cos(", "tan(", "asin(", "acos(", "atan(",
                 "log(", "ln(", "sqrt(", "abs(", "factorial(", "exp("):
        ss.expr += val
        ss.display = ss.expr
    else:
        ss.expr += val
        ss.display = ss.expr



st.markdown('<div class="calc-wrap">', unsafe_allow_html=True)


st.markdown('<p class="calc-title">SCI<span>CALC</span> · v1</p>', unsafe_allow_html=True)


col_deg, col_rad = st.columns(2)
with col_deg:
    if st.button("DEG", key="mode_deg", use_container_width=True):
        ss.angle = "DEG"
with col_rad:
    if st.button("RAD", key="mode_rad", use_container_width=True):
        ss.angle = "RAD"


err = ss.display in ("Division by Zero", "Syntax Error")
expr_show = ss.expr if not ss.just_evaluated else ""
st.markdown(f"""
<div class="display-box">
  <div class="display-expr">{expr_show or "&nbsp;"}</div>
  <div class="display-main {'error' if err else ''}">{ss.display}</div>
</div>
""", unsafe_allow_html=True)



def btn(label, key, css_class="num-btn", cols_context=None):
    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
    clicked = st.button(label, key=key, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked


r0 = st.columns(5)
pairs0 = [
    ("sin", "b_sin", "fn-btn"),
    ("cos", "b_cos", "fn-btn"),
    ("tan", "b_tan", "fn-btn"),
    ("log", "b_log", "fn-btn"),
    ("ln",  "b_ln",  "fn-btn"),
]
for col, (lbl, key, cls) in zip(r0, pairs0):
    with col:
        if btn(lbl, key, cls): press(lbl + "(")


r1 = st.columns(5)
pairs1 = [
    ("√",       "b_sqrt",    "fn-btn"),
    ("x²",      "b_sq",      "fn-btn"),
    ("xʸ",      "b_pow",     "fn-btn"),
    ("π",       "b_pi",      "fn-btn"),
    ("e",       "b_euler",   "fn-btn"),
]
for col, (lbl, key, cls) in zip(r1, pairs1):
    with col:
        if btn(lbl, key, cls):
            if lbl == "√": press("sqrt(")
            elif lbl == "x²": press("^2")
            elif lbl == "xʸ": press("^")
            elif lbl == "π": press("π")
            elif lbl == "e": press("e")


r2 = st.columns(5)
pairs2 = [
    ("(",    "b_lp",   "fn-btn"),
    (")",    "b_rp",   "fn-btn"),
    ("n!",   "b_fact", "fn-btn"),
    ("%",    "b_mod",  "fn-btn"),
    ("|x|",  "b_abs",  "fn-btn"),
]
for col, (lbl, key, cls) in zip(r2, pairs2):
    with col:
        if btn(lbl, key, cls):
            if lbl == "n!": press("factorial(")
            elif lbl == "|x|": press("abs(")
            elif lbl == "%": press("%")
            else: press(lbl)

st.markdown('<hr style="border-color:#1e2434;margin:10px 0;">', unsafe_allow_html=True)


r3 = st.columns(4)
with r3[0]:
    if btn("C",   "b_c",   "clear-btn"): press("C")
with r3[1]:
    if btn("⌫",   "b_ce",  "clear-btn"): press("CE")
with r3[2]:
    if btn("+/-", "b_neg", "fn-btn"):    press("+/-")
with r3[3]:
    if btn("÷",   "b_div", "op-btn"):   press("÷")


r4 = st.columns(4)
for lbl, key, cls in [("7","b7","num-btn"),("8","b8","num-btn"),("9","b9","num-btn"),("×","b_mul","op-btn")]:
    with r4[["7","8","9","×"].index(lbl)]:
        if btn(lbl, key, cls): press(lbl)


r5 = st.columns(4)
for lbl, key, cls in [("4","b4","num-btn"),("5","b5","num-btn"),("6","b6","num-btn"),("−","b_sub","op-btn")]:
    with r5[["4","5","6","−"].index(lbl)]:
        if btn(lbl, key, cls): press(lbl)


r6 = st.columns(4)
for lbl, key, cls in [("1","b1","num-btn"),("2","b2","num-btn"),("3","b3","num-btn"),("+","b_add","op-btn")]:
    with r6[["1","2","3","+"].index(lbl)]:
        if btn(lbl, key, cls): press(lbl)


r7 = st.columns([2, 1, 1])
with r7[0]:
    if btn("0", "b0", "num-btn"): press("0")
with r7[1]:
    if btn(".", "b_dot", "num-btn"): press(".")
with r7[2]:
    if btn("=", "b_eq", "eq-btn"): press("=")


if ss.history:
    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    hist_html = '<div class="history-box"><h5>History</h5>'
    for entry in reversed(ss.history[-10:]):
        parts = entry.split(" = ")
        if len(parts) == 2:
            hist_html += f'<div class="history-entry">{parts[0]} = <span class="hist-res">{parts[1]}</span></div>'
    hist_html += '</div>'
    st.markdown(hist_html, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c2:
        if st.button("Clear History", key="clr_hist", use_container_width=True):
            ss.history = []
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)