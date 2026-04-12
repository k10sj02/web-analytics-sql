import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Web Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:       #f9f9f8;
    --surface:  #ffffff;
    --border:   #e8e6e1;
    --ink:      #1a1a1a;
    --muted:    #888580;
    --accent:   #2563eb;
    --accent-lt:#eff4ff;
    --green:    #16a34a;
    --amber:    #d97706;
    --red:      #dc2626;
    --teal:     #0d9488;
    --purple:   #7c3aed;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--ink);
}
.stApp { background-color: var(--bg); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
    border-right: 1px solid #2a2a2a;
}
section[data-testid="stSidebar"] * { color: #e5e5e5 !important; }
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 400;
}
section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #555 !important;
}

/* ── Hero ── */
.hero {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.05;
    margin: 0 0 1rem 0;
    letter-spacing: -0.02em;
}
.hero-title span { color: var(--accent); }
.hero-desc {
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.6;
    max-width: 580px;
    font-weight: 300;
}

/* ── Section headers ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.01em;
    margin: 0 0 0.25rem 0;
}
.section-desc {
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
    line-height: 1.5;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    margin: 1.5rem 0 2rem 0;
}
.kpi-card {
    background: var(--surface);
    padding: 1.25rem 1.5rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.kpi-delta {
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 0.2rem;
}
.delta-up   { color: var(--green); }
.delta-down { color: var(--red); }

/* ── How to read ── */
.how-to-read {
    background: var(--accent-lt);
    border: 1px solid #bfdbfe;
    border-radius: 6px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 1.2rem;
    font-size: 0.84rem;
    color: #1e40af;
    line-height: 1.55;
}
.how-to-read strong { color: #1e3a8a; }

/* ── Insight box ── */
.insight {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.1rem 1.3rem;
    margin-top: 1rem;
    font-size: 0.88rem;
    line-height: 1.65;
    color: var(--ink);
}
.insight-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.tag {
    display: inline-block;
    background: var(--accent-lt);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.05em;
    padding: 0.15rem 0.45rem;
    border-radius: 3px;
    margin-right: 0.3rem;
    font-weight: 500;
}
.tag-green  { background: #f0fdf4; color: var(--green); }
.tag-amber  { background: #fffbeb; color: var(--amber); }
.tag-red    { background: #fef2f2; color: var(--red); }

/* ── SQL block ── */
.sql-wrap details {
    margin-bottom: 1rem;
}
.sql-block {
    background: #0f172a;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    white-space: pre-wrap;
    line-height: 1.7;
    margin: 0;
}
.sql-kw  { color: #7dd3fc; }
.sql-fn  { color: #a5f3fc; }
.sql-str { color: #86efac; }
.sql-cm  { color: #475569; font-style: italic; }

/* ── Divider ── */
.div-line {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ── Footer ── */
.footer {
    border-top: 1px solid var(--border);
    padding: 1.5rem 0;
    margin-top: 3rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# ─── Database ────────────────────────────────────────────────────────────────
@st.cache_resource
def get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute(
        "CREATE TABLE page_views (page_view_id BIGINT, user_id BIGINT, page_view_date DATE, page TEXT, referrer TEXT)"
    )
    conn.execute(
        "CREATE TABLE conversions (donation_id BIGINT, page_view_id BIGINT, conversion_amount NUMERIC, device TEXT)"
    )
    pv = [
        (1, 164712223553, "2022-02-04", "homepage", "twitter"),
        (2, 165208065721, "2020-10-28", "blog", "twitter"),
        (3, 161104192180, "2020-10-31", "issues", "bing"),
        (4, 164004039360, "2021-07-30", "news", "google"),
        (5, 160911292746, "2021-03-10", "homepage", "google"),
        (6, 160812124626, "2021-10-12", "blog", "google"),
        (7, 161008251066, "2020-03-30", "issues", "google"),
        (8, 163803101033, "2021-03-26", "news", "google"),
        (9, 162903296602, "2021-02-23", "homepage", "google"),
        (10, 167404014693, "2020-10-09", "blog", "google"),
        (11, 165411018996, "2020-06-04", "issues", "facebook"),
        (12, 164608019073, "2020-04-04", "news", "google"),
        (13, 165209223147, "2020-11-22", "homepage", "google"),
        (14, 165005293716, "2021-06-09", "blog", "google"),
        (15, 162411208396, "2020-10-19", "issues", "facebook"),
        (16, 165601256729, "2020-05-26", "news", "google"),
        (17, 162003183973, "2021-08-13", "homepage", "google"),
        (18, 166605158176, "2020-12-09", "blog", "google"),
        (19, 166009235638, "2020-09-10", "issues", "instagram"),
        (20, 167706147530, "2021-07-03", "news", "yahoo"),
        (21, 164904200849, "2021-09-09", "homepage", "twitter"),
        (22, 169404014954, "2021-09-02", "blog", "twitter"),
        (23, 168502259859, "2021-01-19", "issues", "bing"),
        (24, 165203216261, "2020-11-18", "news", "google"),
        (25, 165111292941, "2020-11-26", "homepage", "google"),
        (26, 166308059622, "2022-02-23", "blog", "google"),
        (27, 169805112464, "2020-08-17", "issues", "google"),
        (28, 168905207786, "2021-08-19", "news", "google"),
        (29, 168901284094, "2020-04-30", "homepage", "google"),
        (30, 165304294993, "2020-10-26", "blog", "google"),
        (31, 169812097997, "2020-12-25", "issues", "facebook"),
        (32, 161611026988, "2022-02-12", "news", "google"),
        (33, 167305029774, "2020-11-30", "homepage", "google"),
        (34, 161404019570, "2021-07-19", "blog", "google"),
        (35, 162205135169, "2020-11-05", "issues", "facebook"),
        (36, 161707190011, "2020-08-31", "news", "google"),
        (37, 161305091074, "2020-09-04", "homepage", "google"),
        (38, 165603055871, "2021-09-20", "blog", "google"),
        (39, 160107178170, "2020-10-11", "issues", "instagram"),
        (40, 168603280432, "2020-05-14", "news", "yahoo"),
        (41, 169304294482, "2021-05-07", "homepage", "twitter"),
        (42, 169908028872, "2021-08-22", "blog", "twitter"),
        (43, 160712204569, "2022-03-21", "issues", "bing"),
        (44, 160201248739, "2021-03-04", "news", "google"),
        (45, 165904256475, "2022-01-28", "homepage", "google"),
        (46, 168104088615, "2021-07-20", "blog", "google"),
        (47, 160910097831, "2020-10-24", "issues", "google"),
        (48, 168801033559, "2020-08-29", "news", "google"),
        (49, 167803132658, "2021-08-11", "homepage", "google"),
        (50, 166205306563, "2020-07-23", "blog", "google"),
        (51, 164502014444, "2020-12-30", "issues", "facebook"),
        (52, 160403155146, "2021-08-08", "news", "google"),
        (53, 169702112476, "2021-12-22", "homepage", "google"),
        (54, 161707055529, "2021-10-16", "blog", "google"),
        (55, 168610271705, "2021-01-05", "issues", "facebook"),
        (56, 160411032626, "2020-10-15", "news", "google"),
        (57, 160411226947, "2021-09-29", "homepage", "google"),
        (58, 163910119514, "2020-12-13", "blog", "google"),
        (59, 168008309075, "2021-08-26", "issues", "instagram"),
        (60, 162509281495, "2020-05-18", "news", "yahoo"),
        (61, 164210047942, "2021-07-17", "homepage", "twitter"),
        (62, 162009239753, "2021-05-04", "blog", "twitter"),
        (63, 168210255850, "2020-08-22", "issues", "bing"),
        (64, 162012060055, "2021-11-02", "news", "google"),
        (65, 163106032513, "2020-06-30", "homepage", "google"),
        (66, 167012309196, "2021-06-18", "blog", "google"),
        (67, 160009082157, "2021-06-18", "issues", "google"),
        (68, 168209033060, "2021-08-01", "news", "google"),
        (69, 166702266096, "2020-10-23", "homepage", "google"),
        (70, 164107211221, "2021-04-16", "blog", "google"),
        (71, 169811092882, "2020-08-08", "issues", "facebook"),
        (72, 167206080694, "2022-01-21", "news", "google"),
        (73, 169308158113, "2021-04-10", "homepage", "google"),
        (74, 160003225463, "2021-01-31", "blog", "google"),
        (75, 161012148829, "2021-11-28", "issues", "facebook"),
        (76, 166909232420, "2022-01-18", "news", "google"),
        (77, 161411226226, "2021-08-26", "homepage", "google"),
        (78, 161310018351, "2022-01-14", "blog", "google"),
        (79, 168204093549, "2021-05-12", "issues", "instagram"),
        (80, 162309205512, "2021-09-04", "news", "yahoo"),
        (81, 161402040644, "2020-04-21", "homepage", "twitter"),
        (82, 168602251301, "2021-01-05", "blog", "twitter"),
        (83, 161610055152, "2021-07-01", "issues", "bing"),
        (84, 162011092810, "2020-06-16", "news", "google"),
        (85, 166609150526, "2020-07-17", "homepage", "google"),
        (86, 162106215912, "2021-04-26", "blog", "google"),
        (87, 165102307500, "2021-09-20", "issues", "google"),
        (88, 163102298985, "2021-07-22", "news", "google"),
        (89, 166408208855, "2022-02-24", "homepage", "google"),
        (90, 167903198997, "2021-10-29", "blog", "google"),
        (91, 169109090564, "2021-05-29", "issues", "facebook"),
        (92, 166002295712, "2021-12-20", "news", "google"),
        (93, 165307043645, "2020-11-18", "homepage", "google"),
        (94, 166312010850, "2021-04-16", "blog", "google"),
        (95, 169610058654, "2020-10-19", "issues", "facebook"),
        (96, 164606086801, "2020-04-02", "news", "google"),
        (97, 164910184375, "2020-10-05", "homepage", "google"),
        (98, 165802111780, "2021-03-14", "blog", "google"),
        (99, 169703056052, "2021-05-02", "issues", "instagram"),
        (100, 166209019717, "2021-07-23", "news", "yahoo"),
        (101, 164712223553, "2022-01-14", "news", "twitter"),
        (102, 165208065721, "2021-05-12", "news", "twitter"),
        (103, 161104192180, "2021-09-04", "news", "bing"),
        (104, 164004039360, "2020-04-21", "news", "google"),
        (105, 160911292746, "2021-01-05", "news", "google"),
        (106, 160812124626, "2021-07-01", "news", "google"),
        (107, 161008251066, "2020-06-16", "news", "google"),
        (108, 163803101033, "2020-07-17", "news", "google"),
        (109, 162903296602, "2021-04-26", "news", "google"),
        (110, 167404014693, "2021-09-20", "news", "google"),
        (111, 165411018996, "2021-07-22", "news", "facebook"),
        (112, 164608019073, "2022-02-24", "news", "google"),
        (113, 165209223147, "2021-10-29", "news", "google"),
        (114, 165005293716, "2021-05-29", "news", "google"),
        (115, 162411208396, "2021-12-20", "news", "facebook"),
        (116, 165601256729, "2020-11-18", "news", "google"),
        (117, 162003183973, "2021-04-16", "issues", "google"),
        (118, 166605158176, "2020-10-19", "issues", "google"),
        (119, 166009235638, "2020-04-02", "issues", "instagram"),
        (120, 167706147530, "2020-10-05", "issues", "yahoo"),
        (121, 164904200849, "2021-03-14", "issues", "twitter"),
        (122, 169404014954, "2021-05-02", "issues", "twitter"),
        (123, 168502259859, "2021-07-23", "issues", "bing"),
        (124, 165203216261, "2022-01-14", "issues", "google"),
        (125, 166209019717, "2021-05-12", "issues", "google"),
        (126, 164712223553, "2021-09-04", "issues", "google"),
        (127, 165208065721, "2020-04-21", "issues", "google"),
        (128, 161104192180, "2021-01-05", "issues", "google"),
        (129, 164004039360, "2021-07-01", "issues", "google"),
        (130, 160911292746, "2020-06-16", "issues", "google"),
        (131, 160812124626, "2020-07-17", "issues", "facebook"),
        (132, 161008251066, "2021-04-26", "issues", "google"),
        (133, 163803101033, "2021-09-20", "issues", "google"),
        (134, 162903296602, "2021-07-22", "issues", "google"),
        (135, 167404014693, "2022-02-24", "homepage", "facebook"),
        (136, 165411018996, "2021-10-29", "homepage", "google"),
        (137, 164608019073, "2021-05-29", "homepage", "google"),
        (138, 165209223147, "2021-12-20", "homepage", "google"),
        (139, 165005293716, "2020-11-18", "homepage", "instagram"),
        (140, 162411208396, "2021-04-16", "homepage", "yahoo"),
        (141, 165601256729, "2020-10-19", "homepage", "twitter"),
        (142, 162003183973, "2020-04-02", "homepage", "twitter"),
        (143, 166605158176, "2020-10-05", "homepage", "bing"),
        (144, 166009235638, "2021-03-14", "homepage", "google"),
        (145, 167706147530, "2021-05-02", "homepage", "google"),
        (146, 164904200849, "2021-07-23", "homepage", "google"),
        (147, 169404014954, "2021-09-02", "homepage", "google"),
        (148, 168502259859, "2021-01-19", "homepage", "google"),
        (149, 165203216261, "2020-11-18", "homepage", "google"),
    ]
    cv = [
        (343212, 1, 10, "ios"),
        (3432123, 2, 15, "android"),
        (6521034, 3, 20, "windows"),
        (9609945, 4, 40, "ios"),
        (12698856, 5, 200, "android"),
        (15787767, 6, 10, "windows"),
        (18876678, 7, 30, "ios"),
        (21965589, 8, 1, "android"),
        (25054500, 9, 35, "windows"),
        (28143411, 10, 45, "ios"),
        (31232322, 11, 100, "android"),
        (34321233, 12, 10, "windows"),
        (37410144, 13, 15, "ios"),
        (40499055, 14, 20, "android"),
        (43587966, 15, 40, "windows"),
        (46676877, 16, 200, "ios"),
        (49765788, 17, 10, "android"),
        (52854699, 18, 30, "windows"),
        (55943610, 19, 1, "ios"),
        (59032521, 20, 35, "android"),
        (62121432, 21, 45, "windows"),
        (65210343, 22, 100, "ios"),
        (68299254, 23, 45, "android"),
        (71388165, 24, 100, "windows"),
        (74477076, 25, 10, "ios"),
        (77565987, 26, 15, "android"),
        (80654898, 27, 45, "windows"),
        (83743809, 28, 100, "ios"),
        (86832720, 29, 10, "android"),
        (89921631, 30, 15, "windows"),
        (93010542, 31, 0, "ios"),
        (96099453, 32, 30, "android"),
        (99188364, 33, 1, "windows"),
        (102277275, 34, 35, "ios"),
        (105366186, 35, 45, "android"),
        (108455097, 36, 100, "windows"),
        (111544008, 37, 45, "ios"),
        (114632919, 60, 100, "windows"),
        (117721830, 61, 10, "ios"),
        (130077474, 65, 10, "ios"),
        (133166385, 66, 15, "android"),
        (136255296, 67, 0, "windows"),
        (139344207, 68, 30, "ios"),
        (142433118, 69, 1, "android"),
        (145522029, 70, 35, "windows"),
        (148610940, 71, 45, "ios"),
        (151699851, 72, 100, "android"),
        (154788762, 73, 45, "windows"),
        (157877673, 74, 100, "windows"),
        (160966584, 75, 10, "ios"),
        (164055495, 76, 15, "android"),
        (167144406, 77, 45, "windows"),
        (170233317, 78, 100, "ios"),
        (173322228, 79, 10, "android"),
        (176411139, 80, 15, "windows"),
        (179500050, 81, 100, "ios"),
        (182588961, 82, 10, "android"),
        (185677872, 83, 15, "windows"),
        (188766783, 84, 20, "ios"),
        (191855694, 85, 40, "android"),
        (194944605, 86, 200, "windows"),
        (198033516, 87, 10, "ios"),
        (201122427, 88, 5, "android"),
        (204211338, 89, 5, "windows"),
        (207300249, 90, 5, "ios"),
        (210389160, 114, 10, "ios"),
        (213478071, 115, 200, "ios"),
        (216566982, 116, 10, "ios"),
        (219655893, 117, 5, "ios"),
        (222744804, 118, 5, "ios"),
        (225833715, 119, 5, "ios"),
        (228922626, 120, 10, "ios"),
        (232011537, 121, 200, "ios"),
        (235100448, 122, 10, "ios"),
        (238189359, 123, 5, "ios"),
        (241278270, 124, 5, "ios"),
        (244367181, 125, 5, "ios"),
        (247456092, 126, 10, "ios"),
        (250545003, 127, 45, "ios"),
        (253633914, 128, 100, "ios"),
        (256722825, 129, 10, "ios"),
        (259811736, 130, 15, "ios"),
        (262900647, 131, 100, "ios"),
        (265989558, 132, 10, "ios"),
        (269078469, 133, 20, "ios"),
        (272167380, 134, 10, "ios"),
        (275256291, 135, 20, "ios"),
        (296878668, 142, 100, "ios"),
        (299967579, 143, 10, "ios"),
        (303056490, 144, 20, "ios"),
        (306145401, 145, 10, "ios"),
        (309234312, 146, 15, "ios"),
        (312323223, 147, 100, "ios"),
        (315412134, 148, 10, "ios"),
        (318501045, 149, 20, "ios"),
    ]
    conn.executemany("INSERT INTO page_views VALUES (?,?,?,?,?)", pv)
    conn.executemany("INSERT INTO conversions VALUES (?,?,?,?)", cv)
    conn.commit()
    return conn


def query(sql):
    return pd.read_sql_query(sql, get_db())


# ─── Palette & Template ───────────────────────────────────────────────────────
COLORS = {
    "ios": "#2563eb",
    "windows": "#0d9488",
    "android": "#d1d5db",
    "homepage": "#2563eb",
    "issues": "#7c3aed",
    "blog": "#0d9488",
    "news": "#16a34a",
    "google": "#2563eb",
    "twitter": "#0d9488",
    "facebook": "#7c3aed",
    "yahoo": "#d97706",
    "bing": "#16a34a",
    "instagram": "#db2777",
}
PT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#1a1a1a", size=12),
    xaxis=dict(gridcolor="#f0eeea", linecolor="#e8e6e1", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#f0eeea", linecolor="#e8e6e1", tickfont=dict(size=11)),
    margin=dict(t=16, b=16, l=8, r=8),
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
    <div style='padding:1.5rem 0 0.5rem 0;'>
      <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#fff;letter-spacing:-0.01em;'>Web Analytics</div>
      <div style='font-family:JetBrains Mono,monospace;font-size:0.6rem;letter-spacing:0.14em;color:#555;margin-top:4px;text-transform:uppercase;'>SQL Portfolio Dashboard</div>
    </div>
    <hr style='border-color:#2a2a2a;margin:1rem 0;'>
    """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigate",
        [
            "📊 Overview",
            "📱 Device Analysis",
            "🔗 Referral Sources",
            "📄 Page Performance",
            "💰 Donor Value",
            "⏰ Time Patterns",
            "🔍 Query Explorer",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        """
    <hr style='border-color:#2a2a2a;margin:1.2rem 0;'>
    <div style='font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#555;line-height:2;text-transform:uppercase;letter-spacing:0.08em;'>
    Period<br><span style='color:#aaa;'>Mar 2020 – Mar 2022</span><br>
    Records<br><span style='color:#aaa;'>149 views · 98 gifts</span><br>
    Stack<br><span style='color:#aaa;'>SQLite · Pandas · Plotly</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
  <div class="hero-eyebrow">Web Analytics · SQL · Mar 2020 – Mar 2022</div>
  <h1 class="hero-title">Digital Engagement<br><span>& Donor Analytics</span></h1>
  <p class="hero-desc">An end-to-end SQL analysis of website traffic, referral channels, device behavior, and donation patterns — queried live from an embedded SQLite database.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">High-level snapshot of traffic and revenue across the full data period. Use this page to orient yourself before drilling into any specific dimension.</div>',
        unsafe_allow_html=True,
    )

    total_views = query("SELECT COUNT(*) FROM page_views").iloc[0, 0]
    unique_users = query("SELECT COUNT(DISTINCT user_id) FROM page_views").iloc[0, 0]
    total_rev = query("SELECT SUM(conversion_amount) FROM conversions").iloc[0, 0]
    total_gifts = query("SELECT COUNT(*) FROM conversions").iloc[0, 0]
    conv_rate = round(total_gifts / total_views * 100, 1)

    st.markdown(
        f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">{total_views}</div>
        <div class="kpi-label">Page Views</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{unique_users}</div>
        <div class="kpi-label">Unique Users</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${total_rev:,.0f}</div>
        <div class="kpi-label">Total Revenue</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{total_gifts}</div>
        <div class="kpi-label">Gifts Made</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{conv_rate}%</div>
        <div class="kpi-label">Conversion Rate</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="how-to-read"><strong>How to read this chart:</strong> Each bar shows the total number of visits to that page. Taller bars mean more user interest. The most-visited page is where your audience is spending their time — and where calls-to-action will have the highest reach.</div>',
            unsafe_allow_html=True,
        )
        df = query(
            "SELECT page, COUNT(*) as visits FROM page_views GROUP BY page ORDER BY visits DESC"
        )
        fig = px.bar(
            df,
            x="page",
            y="visits",
            color="page",
            color_discrete_map=COLORS,
            labels={"page": "", "visits": "Visits"},
        )
        fig.update_layout(**PT, showlegend=False, height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(
            '<div class="how-to-read"><strong>How to read this chart:</strong> Each slice shows what share of total revenue came from each device type. A larger slice means that platform\'s users collectively donated more. Note this reflects <em>volume × frequency</em>, not necessarily generosity per gift.</div>',
            unsafe_allow_html=True,
        )
        df2 = query(
            "SELECT device, SUM(conversion_amount) as revenue FROM conversions GROUP BY device ORDER BY revenue DESC"
        )
        fig2 = px.pie(
            df2,
            values="revenue",
            names="device",
            color="device",
            color_discrete_map=COLORS,
            hole=0.5,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
            margin=dict(t=16, b=16, l=8, r=8),
            height=280,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
    <div class="insight">
      <div class="insight-title">Key Takeaways</div>
      <span class="tag">Issues</span> is the highest-traffic page — embed your primary CTA here for maximum reach.<br>
      <span class="tag">iOS</span> drives the largest revenue share despite mid-range gift sizes, due to high donation frequency.<br>
      <span class="tag">Google</span> is the dominant acquisition channel — organic search is the growth lever to prioritize.<br>
      <span class="tag tag-green">Friday</span> is peak day for both visits and gifts — time campaigns to land Thursday–Friday.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# DEVICE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📱 Device Analysis":
    st.markdown(
        '<div class="section-title">Device Analysis</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-desc">Understanding which devices your donors use tells you both <em>how</em> to reach them and <em>what</em> to say. Different devices often proxy for different demographics with different giving behaviors.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">SELECT device,
       SUM(conversion_amount)        AS revenue,
       ROUND(AVG(conversion_amount), 2) AS avg_gift_size,
       COUNT(*)                      AS donation_count
FROM conversions
GROUP BY device
ORDER BY revenue DESC;</div>""",
            unsafe_allow_html=True,
        )

    df = query(
        """SELECT device, SUM(conversion_amount) AS revenue,
                  ROUND(AVG(conversion_amount),2) AS avg_gift_size,
                  COUNT(*) AS donation_count
                  FROM conversions GROUP BY device ORDER BY revenue DESC"""
    )

    st.markdown(
        """
    <div class="how-to-read"><strong>How to read these charts:</strong>
    Revenue = total dollars raised. Avg Gift = typical donation per transaction. Count = number of individual gifts.
    A device can rank high on revenue (many small gifts) or high on avg gift (few large gifts) — both are valuable but require different engagement strategies.
    </div>""",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    for col, metric, label in zip(
        [col1, col2, col3],
        ["revenue", "avg_gift_size", "donation_count"],
        ["Total Revenue ($)", "Avg Gift Size ($)", "# of Gifts"],
    ):
        with col:
            st.markdown(f"**{label}**")
            fig = px.bar(
                df,
                x="device",
                y=metric,
                color="device",
                color_discrete_map=COLORS,
                labels={"device": "", metric: label},
            )
            fig.update_layout(**PT, showlegend=False, height=260)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown(
        "**Top page visited per device** — reveals content affinity by platform"
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">WITH ranked AS (
    SELECT p.page, c.device,
           COUNT(p.page_view_id) AS page_visits,
           ROW_NUMBER() OVER (
               PARTITION BY c.device
               ORDER BY COUNT(p.page_view_id) DESC
           ) AS rn
    FROM page_views p
    INNER JOIN conversions c ON p.page_view_id = c.page_view_id
    GROUP BY p.page, c.device
)
SELECT page, device, page_visits
FROM ranked WHERE rn = 1
ORDER BY page_visits DESC;</div>""",
            unsafe_allow_html=True,
        )

    df2 = query(
        """WITH dps AS (
        SELECT p.page, c.device, COUNT(p.page_view_id) AS page_visits,
               ROW_NUMBER() OVER (PARTITION BY c.device ORDER BY COUNT(p.page_view_id) DESC) AS rn
        FROM page_views p INNER JOIN conversions c ON p.page_view_id = c.page_view_id
        GROUP BY p.page, c.device
    ) SELECT page, device, page_visits FROM dps WHERE rn=1 ORDER BY page_visits DESC"""
    )

    st.markdown(
        '<div class="how-to-read"><strong>How to read this chart:</strong> For each device, this shows the single most-visited page. Use this to personalize content by platform — if iOS users consistently land on Issues, that page\'s mobile experience deserves the most investment.</div>',
        unsafe_allow_html=True,
    )

    fig3 = px.bar(
        df2,
        x="device",
        y="page_visits",
        color="page",
        color_discrete_map=COLORS,
        labels={"device": "", "page_visits": "Visits", "page": "Top Page"},
    )
    fig3.update_layout(**PT, height=280)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
    <div class="insight">
      <div class="insight-title">Interpretation & Next Steps</div>
      <span class="tag">iOS</span> Highest total revenue ($2,066) with frequent mid-size gifts — these users donate on the go. 
      Prioritize frictionless mobile checkout and consider SMS/iMessage donation options to lower the barrier further.<br><br>
      <span class="tag">Windows</span> Highest avg gift ($45) — likely older, higher-net-worth donors on desktops. 
      Fewer but larger gifts. Target with deeper mission content (blog, annual reports) and recurring giving prompts.<br><br>
      <span class="tag tag-amber">Android</span> Lowest on both dimensions. Audit the Android donation flow for UX friction — 
      slow load times or payment issues may be suppressing conversions that demographics would otherwise support.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# REFERRAL SOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔗 Referral Sources":
    st.markdown(
        '<div class="section-title">Referral Sources</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-desc">Where your visitors come from before they arrive. Referral data tells you which acquisition channels are working and where to invest (or cut) marketing spend.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">SELECT referrer,
       COUNT(*) AS referral_count
FROM page_views
GROUP BY referrer
ORDER BY referral_count DESC;</div>""",
            unsafe_allow_html=True,
        )

    df = query(
        "SELECT referrer, COUNT(*) AS referrals FROM page_views GROUP BY referrer ORDER BY referrals DESC"
    )
    total_ref = df["referrals"].sum()
    df["share"] = (df["referrals"] / total_ref * 100).round(1)

    st.markdown(
        '<div class="how-to-read"><strong>How to read these charts:</strong> The bar chart ranks channels by raw volume. The donut shows share of total traffic. A channel that is large in volume but low in conversion rate (not shown here) would be a candidate for re-evaluation — high referrals alone are not enough.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(
            df,
            x="referrals",
            y="referrer",
            orientation="h",
            color="referrer",
            color_discrete_map=COLORS,
            labels={"referrals": "Referrals", "referrer": ""},
            text="share",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(**PT, showlegend=False, height=320)
        fig.update_yaxes(categoryorder="total ascending", gridcolor="#f0eeea")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.pie(
            df,
            values="referrals",
            names="referrer",
            color="referrer",
            color_discrete_map=COLORS,
            hole=0.5,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"),
            margin=dict(t=16, b=16, l=8, r=8),
            height=320,
        )
        st.plotly_chart(fig2, use_container_width=True)

    google_share = df.loc[df["referrer"] == "google", "share"].values[0]
    st.markdown(
        f"""
    <div class="insight">
      <div class="insight-title">Interpretation & Next Steps</div>
      <span class="tag">Google</span> accounts for {google_share}% of all referrals — organic search is by far the dominant channel.
      Double down with SEO: optimize page titles, meta descriptions, and structured data especially on high-traffic pages.<br><br>
      <span class="tag">Twitter / Facebook</span> contribute marginally (≈10% combined). Before scaling spend here, 
      measure their downstream conversion rate — social referrals often have lower intent than search.<br><br>
      <span class="tag tag-amber">Instagram</span> drives the fewest referrals despite strong youth reach. 
      The platform's link-in-bio friction and lifestyle-first content feed suppress advocacy clicks. 
      A short-form video or influencer pilot could test whether this channel can be unlocked cost-effectively.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Page Performance":
    st.markdown(
        '<div class="section-title">Page Performance</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-desc">How traffic is distributed across pages and how it changes over time. Spot seasonal patterns, measure the impact of campaigns, and identify which pages need more attention.</div>',
        unsafe_allow_html=True,
    )

    q1 = query(
        "SELECT COUNT(DISTINCT user_id) FROM page_views WHERE page='homepage' AND page_view_date BETWEEN '2021-01-01' AND '2021-03-31'"
    ).iloc[0, 0]
    q2 = query(
        "SELECT COUNT(DISTINCT user_id) FROM page_views WHERE page='homepage' AND page_view_date BETWEEN '2021-04-01' AND '2021-06-30'"
    ).iloc[0, 0]
    pct = (q2 - q1) * 100.0 / q1
    arrow = "▲" if pct > 0 else "▼"
    color = "#16a34a" if pct > 0 else "#dc2626"

    st.markdown(
        f"""
    <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);">
      <div class="kpi-card">
        <div class="kpi-value">{q1}</div>
        <div class="kpi-label">Homepage · Q1 2021</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{q2}</div>
        <div class="kpi-label">Homepage · Q2 2021</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value" style="color:{color};">{arrow} {abs(pct):.0f}%</div>
        <div class="kpi-label">Quarter-over-Quarter</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="how-to-read"><strong>How to read the Q-o-Q stat:</strong> This counts <em>unique</em> users (not page views) on the homepage in each quarter. A +25% jump means 25% more individual people visited in Q2 vs Q1 — it is not inflated by repeat visits from the same user.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL — Q1/Q2 comparison"):
        st.markdown(
            """<div class="sql-block">WITH Q1 AS (
    SELECT DISTINCT user_id FROM page_views
    WHERE page = 'homepage'
      AND page_view_date BETWEEN '2021-01-01' AND '2021-03-31'
),
Q2 AS (
    SELECT DISTINCT user_id FROM page_views
    WHERE page = 'homepage'
      AND page_view_date BETWEEN '2021-04-01' AND '2021-06-30'
)
SELECT
    (COUNT(DISTINCT Q2.user_id) - COUNT(DISTINCT Q1.user_id))
    * 100.0 / COUNT(DISTINCT Q1.user_id) AS pct_change
FROM Q1 LEFT JOIN Q2 ON 1=1;</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown("**Monthly page views by page — 2021**")
    st.markdown(
        '<div class="how-to-read"><strong>How to read this chart:</strong> Each line tracks one page over the course of 2021. Peaks indicate months with high campaign activity or external events driving traffic. Flat or declining lines suggest content is staling. Crossovers between lines show shifts in audience priority.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">SELECT strftime('%m', page_view_date) AS month,
       page,
       COUNT(page_view_id) AS views
FROM page_views
WHERE strftime('%Y', page_view_date) = '2021'
GROUP BY month, page
ORDER BY month;</div>""",
            unsafe_allow_html=True,
        )

    df = query(
        """SELECT strftime('%m', page_view_date) AS month, page, COUNT(*) AS views
                  FROM page_views WHERE strftime('%Y', page_view_date)='2021'
                  GROUP BY month, page ORDER BY month"""
    )
    mnames = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }
    df["month"] = df["month"].map(mnames)
    fig = px.line(
        df,
        x="month",
        y="views",
        color="page",
        color_discrete_map=COLORS,
        markers=True,
        labels={"month": "", "views": "Views", "page": "Page"},
        category_orders={"month": list(mnames.values())},
    )
    fig.update_layout(**PT, height=340)
    fig.update_traces(line_width=2)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
    <div class="insight">
      <div class="insight-title">Interpretation & Next Steps</div>
      <span class="tag tag-green">+25% Q1→Q2</span> homepage growth suggests a spring campaign landed well or 
      a high-profile external event drove discovery. Correlate with campaign calendars to confirm the driver.<br><br>
      Mid-year spikes on Issues and News point to event-driven traffic — content published around real-world moments 
      pulls outsized visits. <strong>Build an editorial calendar</strong> that anticipates high-interest periods and has 
      content ready to publish.<br><br>
      Blog traffic is relatively flat — consider whether it's serving a SEO/retention role (acceptable) or 
      whether it's being neglected as a conversion tool (opportunity).
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# DONOR VALUE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Donor Value":
    st.markdown('<div class="section-title">Donor Value</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Lifetime value (LTV) ranks donors by total giving across the period. A small number of high-value donors typically drive a disproportionate share of revenue — identifying and retaining them is critical.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">SELECT p.user_id,
       SUM(c.conversion_amount) AS lifetime_value,
       COUNT(c.donation_id)     AS num_gifts
FROM conversions c
LEFT JOIN page_views p ON c.page_view_id = p.page_view_id
GROUP BY p.user_id
ORDER BY lifetime_value DESC
LIMIT 10;</div>""",
            unsafe_allow_html=True,
        )

    df = query(
        """SELECT p.user_id, SUM(c.conversion_amount) AS ltv, COUNT(c.donation_id) AS gifts
                  FROM conversions c LEFT JOIN page_views p ON c.page_view_id=p.page_view_id
                  GROUP BY p.user_id ORDER BY ltv DESC LIMIT 10"""
    )

    total_rev = query("SELECT SUM(conversion_amount) FROM conversions").iloc[0, 0]
    top10_rev = df["ltv"].sum()
    top10_pct = top10_rev / total_rev * 100
    top_ltv = df["ltv"].iloc[0]
    top_id = str(df["user_id"].iloc[0])[-8:]

    st.markdown(
        f"""
    <div class="kpi-grid" style="grid-template-columns:repeat(3,1fr);">
      <div class="kpi-card">
        <div class="kpi-value">${top_ltv:,.0f}</div>
        <div class="kpi-label">Top Donor LTV (…{top_id})</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${top10_rev:,.0f}</div>
        <div class="kpi-label">Top 10 Combined LTV</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{top10_pct:.0f}%</div>
        <div class="kpi-label">Share of Total Revenue</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="how-to-read"><strong>How to read this chart:</strong> Each bar is one donor, sorted by total giving. User IDs are truncated for readability. The gap between the top donor and the rest reveals how concentrated giving is. A steep drop-off suggests heavy reliance on a few individuals — a retention risk.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        df["uid"] = "…" + df["user_id"].astype(str).str[-6:]
        fig = px.bar(
            df,
            x="uid",
            y="ltv",
            color="ltv",
            color_continuous_scale=["#dbeafe", "#2563eb"],
            labels={"uid": "", "ltv": "Lifetime Value ($)"},
            text="ltv",
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_layout(**PT, coloraxis_showscale=False, height=340)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Top 10 donors**")
        st.dataframe(
            df[["user_id", "ltv", "gifts"]].rename(
                columns={"user_id": "User ID", "ltv": "LTV ($)", "gifts": "# Gifts"}
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown(
        f"""
    <div class="insight">
      <div class="insight-title">Interpretation & Next Steps</div>
      The top 10 donors represent <strong>{top10_pct:.0f}% of all revenue</strong> — a high concentration that 
      creates meaningful churn risk if even one or two lapse.<br><br>
      <span class="tag">Action</span> Build donor personas for the top cohort: what device do they use? 
      What page did they first visit? What referral source brought them? Replicate those acquisition paths.<br><br>
      <span class="tag tag-green">Retention</span> Implement a VIP engagement track for donors above a threshold LTV — 
      personalized updates, impact reports, and early access to campaigns can meaningfully reduce churn.<br><br>
      <span class="tag tag-amber">Expansion</span> Look for donors in positions 11–25 with high gift frequency but moderate LTV — 
      these are upgrade candidates who already have strong affinity.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TIME PATTERNS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⏰ Time Patterns":
    st.markdown(
        '<div class="section-title">Time Patterns</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-desc">When your audience is most active. Knowing peak days lets you schedule campaigns, emails, and content drops to land when users are already engaged and primed to act.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("View SQL"):
        st.markdown(
            """<div class="sql-block">-- Page views by day of week
SELECT strftime('%w', page_view_date) AS dow,
       COUNT(*) AS views
FROM page_views
GROUP BY dow ORDER BY dow;

-- Donations by day of week
SELECT strftime('%w', p.page_view_date) AS dow,
       COUNT(c.donation_id) AS gifts
FROM conversions c
LEFT JOIN page_views p ON c.page_view_id = p.page_view_id
GROUP BY dow ORDER BY dow;</div>""",
            unsafe_allow_html=True,
        )

    df_v = query(
        "SELECT strftime('%w', page_view_date) AS dow, COUNT(*) AS views FROM page_views GROUP BY dow ORDER BY dow"
    )
    df_d = query(
        """SELECT strftime('%w', p.page_view_date) AS dow, COUNT(c.donation_id) AS gifts
                    FROM conversions c LEFT JOIN page_views p ON c.page_view_id=p.page_view_id
                    GROUP BY dow ORDER BY dow"""
    )
    dmap = {
        "0": "Sun",
        "1": "Mon",
        "2": "Tue",
        "3": "Wed",
        "4": "Thu",
        "5": "Fri",
        "6": "Sat",
    }
    df_v["day"] = df_v["dow"].map(dmap)
    df_d["day"] = df_d["dow"].map(dmap)
    order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    st.markdown(
        '<div class="how-to-read"><strong>How to read these charts:</strong> Color intensity reflects relative activity — darker bars are higher-traffic days. The left chart shows browsing behavior; the right shows giving behavior. When peaks align, that day is your highest-leverage moment for any campaign action.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Page views by day**")
        fig = px.bar(
            df_v,
            x="day",
            y="views",
            color="views",
            color_continuous_scale=["#dbeafe", "#2563eb"],
            category_orders={"day": order},
            labels={"day": "", "views": "Page Views"},
        )
        fig.update_layout(**PT, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Donations by day**")
        fig2 = px.bar(
            df_d,
            x="day",
            y="gifts",
            color="gifts",
            color_continuous_scale=["#d1fae5", "#16a34a"],
            category_orders={"day": order},
            labels={"day": "", "gifts": "Gifts"},
        )
        fig2.update_layout(**PT, coloraxis_showscale=False, height=300)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        """
    <div class="insight">
      <div class="insight-title">Interpretation & Next Steps</div>
      <span class="tag tag-green">Friday</span> is the single highest-traffic and highest-donation day — both browsing and 
      giving behavior peak as users wind down their work week with more leisure browsing time.<br><br>
      <span class="tag">Tactic</span> Schedule email campaigns and social posts to land <strong>Thursday evening</strong> 
      so they surface in inboxes Friday morning. Any time-limited donation matches or appeals should go live Thursday–Friday.<br><br>
      <span class="tag tag-amber">Weekend</span> traffic is moderate but not negligible. A Sunday re-engagement 
      touchpoint (e.g. a "week ahead" newsletter) could capture users planning their week and convert 
      passive interest into action before Monday fatigue sets in.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# QUERY EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Query Explorer":
    st.markdown(
        '<div class="section-title">Query Explorer</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-desc">Run any SQL query directly against the live in-memory database. Use the presets to get started or write your own from scratch.</div>',
        unsafe_allow_html=True,
    )

    presets = {
        "— Choose a preset —": "",
        "All page views (first 20)": "SELECT * FROM page_views LIMIT 20;",
        "Revenue by device": "SELECT device, SUM(conversion_amount) AS revenue, ROUND(AVG(conversion_amount),2) AS avg_gift, COUNT(*) AS gifts FROM conversions GROUP BY device ORDER BY revenue DESC;",
        "Referral counts": "SELECT referrer, COUNT(*) AS referrals FROM page_views GROUP BY referrer ORDER BY referrals DESC;",
        "Top 10 donors": "SELECT p.user_id, SUM(c.conversion_amount) AS ltv, COUNT(*) AS gifts FROM conversions c LEFT JOIN page_views p ON c.page_view_id=p.page_view_id GROUP BY p.user_id ORDER BY ltv DESC LIMIT 10;",
        "Monthly 2021 views": "SELECT strftime('%m', page_view_date) AS month, page, COUNT(*) AS views FROM page_views WHERE strftime('%Y', page_view_date)='2021' GROUP BY month, page ORDER BY month;",
        "Q1 2021 homepage uniques": "SELECT COUNT(DISTINCT user_id) AS uniq_users FROM page_views WHERE page='homepage' AND page_view_date BETWEEN '2021-01-01' AND '2021-03-31';",
        "Conversion rate by page": "SELECT p.page, COUNT(DISTINCT p.user_id) AS visitors, COUNT(c.donation_id) AS gifts, ROUND(COUNT(c.donation_id)*100.0/COUNT(DISTINCT p.user_id),1) AS conv_pct FROM page_views p LEFT JOIN conversions c ON p.page_view_id=c.page_view_id GROUP BY p.page ORDER BY conv_pct DESC;",
    }

    selected = st.selectbox("Preset queries", list(presets.keys()))
    sql_input = st.text_area(
        "SQL",
        value=presets[selected],
        height=120,
        placeholder="SELECT * FROM page_views LIMIT 10;",
    )

    if st.button("▶  Run", type="primary"):
        if sql_input.strip():
            try:
                result = query(sql_input)
                st.success(f"{len(result)} row(s) returned")
                st.dataframe(result, use_container_width=True)
                if len(result) > 1 and len(result.columns) == 2:
                    cx, cy = result.columns[0], result.columns[1]
                    if pd.api.types.is_numeric_dtype(result[cy]):
                        fig = px.bar(
                            result, x=cx, y=cy, color_discrete_sequence=["#2563eb"]
                        )
                        fig.update_layout(**PT, height=280)
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"SQL error: {e}")
        else:
            st.warning("Enter a query to run.")

    with st.expander("Schema reference"):
        st.markdown(
            """<div class="sql-block">-- page_views
page_view_id   BIGINT    -- primary key
user_id        BIGINT    -- visitor identifier
page_view_date DATE      -- YYYY-MM-DD (2020-03-30 → 2022-03-21)
page           TEXT      -- homepage | blog | issues | news
referrer       TEXT      -- google | twitter | facebook | instagram | yahoo | bing

-- conversions
donation_id        BIGINT
page_view_id       BIGINT    -- FK → page_views
conversion_amount  NUMERIC   -- gift amount in USD
device             TEXT      -- ios | android | windows</div>""",
            unsafe_allow_html=True,
        )


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="footer">
  Web Analytics Dashboard &nbsp;·&nbsp; SQL Portfolio &nbsp;·&nbsp; Mar 2020 – Mar 2022 &nbsp;·&nbsp; Streamlit · Plotly · SQLite
</div>
""",
    unsafe_allow_html=True,
)
