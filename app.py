"""WalletMind - Next-Gen Financial Intelligence Portal (Indian Executive Edition)
Color Palette & Visuals strictly matching the user screenshot:
- Exact Centered White Card with subtle curved shadow
- Attached Circular W+M Wallet Rupee Monogram Logo
- Deep Charcoal / Navy input field boxes
- Golden / Navy Sign In Button
- Indian English Financial Terminology (Khata, Bachat, Kharch, Salahkar)
- Multi-Year & Monthly Budget Khata Planner (2023 - 2026)
- Dedicated AI Budget Advisory Corner (Salahkar)
- Real Gmail OTP Verification
"""
import sqlite3
import uuid
import hashlib
import re
import random
import time
import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from pathlib import Path
import pandas as pd
import altair as alt
import streamlit as st

BASE = Path(__file__).resolve().parent
DB = BASE / 'walletmind_demo.sqlite'
LOGO_PATH = BASE / 'walletmind_logo.jpg'

# ----------------- Streamlit Page Configuration -----------------
st.set_page_config(
    page_title='WalletMind | Executive Financial & Budget Manager',
    page_icon='🪙',
    layout='wide',
    initial_sidebar_state='auto'
)

# Helper to encode logo image to base64
def get_base64_logo():
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{data}"
    return ""

LOGO_BASE64 = get_base64_logo()

# ----------------- CSS Styling Exactly Matching Screenshot -----------------
CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root {{
    --navy-dark: #0A192F;
    --navy-blue: #1E3A5F;
    --gold: #C59B27;
    --gold-bright: #D4AF37;
    --beige-bg: #F7F5EE;
}}

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp {{
    background-color: var(--beige-bg) !important;
}}

/* Main Page Container: Warm Beige Background */
.stApp {{
    background-color: var(--beige-bg) !important;
}}

/* Unrestricted full-width layout for desktop dashboard */
.block-container {{
    max-width: 1200px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    margin: 0 auto !important;
}}

/* Exact Authentication Card in Center of PC Screen */
.auth-main-card {{
    background: #FFFFFF;
    border-radius: 36px;
    padding: 42px 38px 38px 38px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.03);
    border: 1px solid #ECE7DC;
    width: 100%;
    max-width: 440px;
    margin: 0 auto;
}}

/* Enhanced Executive KPI Metric Cards with Gold Border & Gradient */
div[data-testid="stMetric"] {{
    background: linear-gradient(135deg, #FFFFFF 0%, #FAF8F2 100%) !important;
    border: 1px solid #E8E2D2 !important;
    border-left: 4px solid #C59B27 !important;
    border-radius: 14px !important;
    padding: 16px 18px !important;
    box-shadow: 0 4px 15px rgba(10, 25, 47, 0.04) !important;
}}
div[data-testid="stMetric"] label {{
    font-size: 11.5px !important;
    font-weight: 700 !important;
    color: #5C6B73 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #0A192F !important;
}}

/* Category Pill Badges */
.pill-badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
}}
.pill-income {{
    background: #E6F4EA;
    color: #137333;
    border: 1px solid #CEEAD6;
}}
.pill-expense {{
    background: #FEEFC3;
    color: #B06000;
    border: 1px solid #FDD663;
}}
.pill-dining {{
    background: #FEF7E0;
    color: #C59B27;
    border: 1px solid #FEEFC3;
}}
.pill-transport {{
    background: #E8F0FE;
    color: #1967D2;
    border: 1px solid #D2E3FC;
}}
.pill-bills {{
    background: #F3E8FD;
    color: #8430CE;
    border: 1px solid #E9D2FD;
}}

/* Header inside card */
.auth-center-header {{
    text-align: center;
    margin-bottom: 24px;
}}

.logo-img-wrapper {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 14px;
}}

.logo-img {{
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: contain;
    background: #FFFFFF;
    box-shadow: 0 6px 20px rgba(10, 25, 47, 0.08), 0 0 0 2.5px #C59B27;
    padding: 4px;
}}

/* Brand typography matching screenshot */
.auth-brand-title {{
    margin: 0;
    font-size: 28px;
    font-weight: 800;
    color: #112240;
    letter-spacing: -0.02em;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.auth-brand-title span {{
    color: #C59B27;
}}
.auth-brand-sub {{
    margin: 6px 0 0 0;
    font-size: 13px;
    color: #5C6B73;
    font-weight: 600;
}}

/* Labels matching screenshot: uppercase bold font */
div[data-testid="stForm"] label p, div[data-testid="stWidgetLabel"] p {{
    font-size: 11px !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: #1E293B !important;
    margin-bottom: 6px !important;
}}

/* Input Fields: Light background (#F8FAFC) with light-blue/gray border (#CBD5E1) matching screenshot */
div[data-testid="stForm"] div[data-baseweb="input"], div[data-baseweb="input"] {{
    background-color: #F8FAFC !important;
    border-radius: 10px !important;
    border: 1.5px solid #CBD5E1 !important;
    height: 48px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}}
div[data-testid="stForm"] div[data-baseweb="input"] input, div[data-baseweb="input"] input {{
    color: #0F172A !important;
    font-size: 14.5px !important;
    font-weight: 500 !important;
    padding-left: 14px !important;
    background-color: transparent !important;
}}
div[data-testid="stForm"] div[data-baseweb="input"] input::placeholder, div[data-baseweb="input"] input::placeholder {{
    color: #94A3B8 !important;
}}
div[data-testid="stForm"] div[data-baseweb="input"]:focus-within, div[data-baseweb="input"]:focus-within {{
    border-color: #C59B27 !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(197, 155, 39, 0.20) !important;
}}

/* Sign In to Portal Button: Navy Blue with Gold Accent border matching screenshot */
div[data-testid="stForm"] div.stButton > button, div.stButton > button, button[kind="primary"], button[kind="secondary"] {{
    background: linear-gradient(180deg, #162C4E 0%, #0D1C33 100%) !important;
    background-color: #0D1C33 !important;
    border: 1.5px solid #C59B27 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border-radius: 10px !important;
    height: 48px !important;
    box-shadow: 0 4px 14px rgba(13, 28, 51, 0.25) !important;
    margin-top: 10px !important;
}}
div[data-testid="stForm"] div.stButton > button:hover, div.stButton > button:hover, button[kind="primary"]:hover {{
    background: linear-gradient(180deg, #1E3A5F 0%, #162C4E 100%) !important;
    border-color: var(--gold-bright) !important;
    box-shadow: 0 6px 18px rgba(197, 155, 39, 0.35) !important;
    color: #FFFFFF !important;
}}

/* Tab Styling matching screenshot: Gold underline on active tab */
.stTabs [data-baseweb="tab-list"] {{
    border-bottom: 1.5px solid #E2E8F0 !important;
    gap: 20px !important;
    justify-content: center !important;
    margin-bottom: 22px !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-size: 14.5px !important;
    font-weight: 600 !important;
    color: #64748B !important;
    padding: 8px 18px !important;
    border: none !important;
    background: transparent !important;
}}
.stTabs [aria-selected="true"] {{
    color: #0F172A !important;
    font-weight: 800 !important;
    border-bottom: 2.5px solid #C59B27 !important;
}}

/* Demo Box matching screenshot: Cream/Beige (#FBF7EE) with subtle rounded border */
.verified-demo-card {{
    background: #FBF7EE;
    border: 1px solid #EADBBE;
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 18px;
    font-size: 12.5px;
    color: #1E3A5F;
    line-height: 1.6;
}}
.verified-demo-card strong.title {{
    color: #C59B27;
    font-weight: 700;
    font-size: 12.5px;
}}
.verified-demo-card code {{
    background: #FFFFFF;
    border: 1px solid #E5DFCF;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    color: #0A192F;
}}

/* Password criteria bullet tags */
.pw-badge {{
    font-size: 11px;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 600;
    margin: 2px 3px 2px 0;
    display: inline-block;
}}
.pw-pass {{
    background: #DCFCE7;
    color: #166534;
    border: 1px solid #86EFAC;
}}
.pw-fail {{
    background: #FEE2E2;
    color: #991B1B;
    border: 1px solid #FCA5A5;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- Database Helpers -----------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.execute('PRAGMA foreign_keys=ON')
    return conn

def query(sql, args=()):
    with get_db() as conn:
        return pd.read_sql_query(sql, conn, params=args)

def write(sql, args):
    with get_db() as conn:
        conn.execute(sql, args)
        conn.commit()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------- Real Gmail SMTP Dispatcher -----------------
def send_otp_to_gmail(recipient_email: str, recipient_name: str, otp_code: str) -> tuple[bool, str]:
    smtp_user = None
    smtp_pass = None

    try:
        if hasattr(st, "secrets"):
            smtp_user = st.secrets.get("EMAIL_HOST_USER", None)
            smtp_pass = st.secrets.get("EMAIL_HOST_PASSWORD", None)
    except Exception:
        pass

    if not smtp_user:
        smtp_user = os.environ.get("EMAIL_HOST_USER", None)
    if not smtp_pass:
        smtp_pass = os.environ.get("EMAIL_HOST_PASSWORD", None)

    if not smtp_user or not smtp_pass or "your_sender_email" in smtp_user:
        return False, "SENDER_NOT_CONFIGURED"

    try:
        msg = MIMEMultipart()
        msg['From'] = f"WalletMind Security <{smtp_user}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"{otp_code} is your WalletMind verification code"

        body = f"""Dear {recipient_name},

Thank you for choosing WalletMind!

Your 6-digit one-time verification OTP for your account is:

    {otp_code}

Please enter this verification code on the registration page to activate your account.
This OTP will expire in 10 minutes.

If you did not initiate this request, please disregard this email.

Warm regards,
WalletMind Security Team
"""
        msg.attach(MIMEText(body, 'plain'))

        import certifi
        import ssl
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=12)
        server.starttls(context=ssl_ctx)
        server.login(smtp_user.strip(), smtp_pass.strip().replace(" ", ""))
        server.send_message(msg)
        server.quit()
        return True, f"Verification OTP successfully sent to {recipient_email}!"
    except smtplib.SMTPAuthenticationError:
        return False, "AUTH_ERROR: Google rejected App Password. Check 2-Step Verification."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

# ----------------- Executive PDF Statement Generator -----------------
def generate_pdf_report(user_name: str, user_email: str, income_amt: float, expense_amt: float, net_amt: float, savings_rate: float, df_budgets: pd.DataFrame, ai_headline: str, ai_body: str) -> bytes:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from datetime import date
    import io
    import re

    fig = plt.figure(figsize=(8.5, 11), facecolor='#FFFFFF')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Header Banner
    ax.fill_between([0, 1], [0.89, 0.89], [1, 1], color='#0A192F', transform=ax.transAxes)
    ax.fill_between([0, 1], [0.88, 0.88], [0.89, 0.89], color='#C59B27', transform=ax.transAxes)

    ax.text(0.08, 0.94, 'WalletMind Executive Statement', fontsize=20, fontweight='bold', color='#FFFFFF', transform=ax.transAxes)
    ax.text(0.08, 0.905, 'Monthly Financial Intelligence & AI Audit Report', fontsize=11, color='#C59B27', transform=ax.transAxes)

    # Client & Metadata
    today_str = date.today().strftime("%B %d, %Y")
    ax.text(0.08, 0.84, f"Account Holder: {user_name} ({user_email})", fontsize=11, fontweight='bold', color='#0A192F', transform=ax.transAxes)
    ax.text(0.08, 0.815, f"Statement Date: {today_str} | Base Currency: Indian Rupee (₹)", fontsize=10, color='#5C6B73', transform=ax.transAxes)

    # Financial Health KPI Cards
    # Inflow
    ax.fill_between([0.08, 0.35], [0.72, 0.72], [0.79, 0.79], color='#F8FAFC', transform=ax.transAxes)
    ax.text(0.10, 0.765, "TOTAL INFLOW (INCOME)", fontsize=9, fontweight='bold', color='#5C6B73', transform=ax.transAxes)
    ax.text(0.10, 0.735, f"₹{income_amt:,.2f}", fontsize=13, fontweight='bold', color='#166534', transform=ax.transAxes)

    # Outflow
    ax.fill_between([0.38, 0.65], [0.72, 0.72], [0.79, 0.79], color='#F8FAFC', transform=ax.transAxes)
    ax.text(0.40, 0.765, "TOTAL OUTFLOW (EXPENSES)", fontsize=9, fontweight='bold', color='#5C6B73', transform=ax.transAxes)
    ax.text(0.40, 0.735, f"₹{expense_amt:,.2f}", fontsize=13, fontweight='bold', color='#991B1B', transform=ax.transAxes)

    # Net Savings
    ax.fill_between([0.68, 0.92], [0.72, 0.72], [0.79, 0.79], color='#F8FAFC', transform=ax.transAxes)
    ax.text(0.70, 0.765, "NET SAVINGS (SURPLUS)", fontsize=9, fontweight='bold', color='#5C6B73', transform=ax.transAxes)
    ax.text(0.70, 0.735, f"₹{net_amt:,.2f} ({savings_rate:.1f}%)", fontsize=13, fontweight='bold', color='#0A192F', transform=ax.transAxes)

    # Section 1: AI Advisory Key Takeaways
    ax.text(0.08, 0.67, "1. Executive AI Advisor Summary", fontsize=13, fontweight='bold', color='#0A192F', transform=ax.transAxes)
    ax.text(0.08, 0.64, f"Status: {ai_headline}", fontsize=10.5, fontweight='bold', color='#C59B27', transform=ax.transAxes)

    clean_body = re.sub(r'[*_#]', '', ai_body).strip()
    lines = clean_body.split('\n')
    y_pos = 0.61
    for line in lines[:6]:
        if line.strip():
            ax.text(0.08, y_pos, line.strip()[:95], fontsize=9.5, color='#1E293B', transform=ax.transAxes)
            y_pos -= 0.026

    # Section 2: Category Budget Compliance Matrix
    y_pos -= 0.02
    ax.text(0.08, y_pos, "2. Category Budget Compliance Matrix", fontsize=13, fontweight='bold', color='#0A192F', transform=ax.transAxes)
    y_pos -= 0.03

    # Table Header
    ax.fill_between([0.08, 0.92], [y_pos-0.005, y_pos-0.005], [y_pos+0.02, y_pos+0.02], color='#0A192F', transform=ax.transAxes)
    ax.text(0.10, y_pos+0.003, "CATEGORY", fontsize=9, fontweight='bold', color='#FFFFFF', transform=ax.transAxes)
    ax.text(0.38, y_pos+0.003, "BUDGET (₹)", fontsize=9, fontweight='bold', color='#FFFFFF', transform=ax.transAxes)
    ax.text(0.58, y_pos+0.003, "ACTUAL SPENT (₹)", fontsize=9, fontweight='bold', color='#FFFFFF', transform=ax.transAxes)
    ax.text(0.78, y_pos+0.003, "COMPLIANCE", fontsize=9, fontweight='bold', color='#FFFFFF', transform=ax.transAxes)
    y_pos -= 0.028

    if not df_budgets.empty:
        cat_agg = df_budgets.groupby('category')[['budget_amount', 'spent_amount']].sum().reset_index()
        for i, row in cat_agg.head(8).iterrows():
            bg_c = '#F8FAFC' if i % 2 == 0 else '#FFFFFF'
            ax.fill_between([0.08, 0.92], [y_pos-0.005, y_pos-0.005], [y_pos+0.02, y_pos+0.02], color=bg_c, transform=ax.transAxes)
            c_name = str(row['category'])[:18]
            b_val = float(row['budget_amount'])
            s_val = float(row['spent_amount'])
            status_txt = "Within Limit" if s_val <= b_val else "Over Budget"
            status_col = "#166534" if s_val <= b_val else "#991B1B"

            ax.text(0.10, y_pos+0.003, c_name, fontsize=9, color='#0A192F', transform=ax.transAxes)
            ax.text(0.38, y_pos+0.003, f"₹{b_val:,.2f}", fontsize=9, color='#0A192F', transform=ax.transAxes)
            ax.text(0.58, y_pos+0.003, f"₹{s_val:,.2f}", fontsize=9, color='#0A192F', transform=ax.transAxes)
            ax.text(0.78, y_pos+0.003, status_txt, fontsize=9, fontweight='bold', color=status_col, transform=ax.transAxes)
            y_pos -= 0.025
    else:
        ax.text(0.10, y_pos, "No category budgets recorded.", fontsize=9, color='#64748B', transform=ax.transAxes)

    # Footer
    ax.fill_between([0, 1], [0, 0], [0.04, 0.04], color='#F8FAFC', transform=ax.transAxes)
    ax.text(0.5, 0.015, "WalletMind Security & AI Financial Vault — Confidential Client Report", fontsize=8, color='#5C6B73', ha='center', transform=ax.transAxes)

    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        pdf.savefig(fig)
    plt.close(fig)
    return pdf_buffer.getvalue()

# ----------------- Specific AI Budget Advisor -----------------
def compute_ai_budget_insights(prompt: str, user_id: str, df_tx: pd.DataFrame, df_budgets: pd.DataFrame) -> dict:
    expenses = df_tx[df_tx['type'] == 'EXPENSE'] if not df_tx.empty else pd.DataFrame()
    income = df_tx[df_tx['type'] == 'INCOME'] if not df_tx.empty else pd.DataFrame()

    total_exp = float(expenses['amount'].sum()) if not expenses.empty else 0.0
    total_inc = float(income['amount'].sum()) if not income.empty else 0.0
    net_surplus = total_inc - total_exp
    savings_rate = (net_surplus / total_inc * 100) if total_inc > 0 else 0.0

    top_cat = "General Expenses"
    top_cat_amt = 0.0
    top_cat_pct = 0.0
    if not expenses.empty:
        c_grp = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
        top_cat = c_grp.index[0]
        top_cat_amt = c_grp.iloc[0]
        top_cat_pct = (top_cat_amt / total_exp * 100) if total_exp > 0 else 0.0

    over_budget_cats = []
    if not df_budgets.empty:
        over_rows = df_budgets[df_budgets['remaining'] < 0]
        if not over_rows.empty:
            over_budget_cats = over_rows['category'].unique().tolist()

    p = prompt.lower().strip()

    # Greetings & Casual Conversation
    if any(k == p or p.startswith(k + ' ') for k in ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good afternoon', 'good evening', 'greetings', 'who are you', 'what can you do', 'help']):
        headline = "👋 Hello! I am your WalletMind AI Budget Advisor"
        body = f"""
I'm here to assist you with all aspects of your personal finances:
- **Analyze your current savings**: You're currently saving **₹{net_surplus:,.2f}** ({savings_rate:.1f}% savings rate).
- **Affordability Advice**: Ask me *"Can I afford a laptop for ₹60,000?"* or *"Can I spend ₹15,000 on travel?"*
- **Budget Tracking**: Ask me to audit your category budgets or check overspending.
- **Spending Optimization**: Inquire about optimizing food, dining, transport, or recurring bills.

How can I help you today?
"""
    # Contextual Affordability Calculator Check
    elif re.search(r'(?:afford|buy|purchase|spend|cost)\s*(?:a|an)?\s*([a-zA-Z\s]+)?(?:for|of)?\s*(?:₹|rs\.?|inr)?\s*(\d+[\d,]*)', p):
        afford_match = re.search(r'(?:afford|buy|purchase|spend|cost)\s*(?:a|an)?\s*([a-zA-Z\s]+)?(?:for|of)?\s*(?:₹|rs\.?|inr)?\s*(\d+[\d,]*)', p)
        item_name = afford_match.group(1).strip() if afford_match.group(1) else "this item"
        amount_str = afford_match.group(2).replace(',', '')
        target_amt = float(amount_str)

        projected_surplus = net_surplus - target_amt
        projected_savings_rate = (projected_surplus / total_inc * 100) if total_inc > 0 else 0.0

        headline = f"💳 Affordability Decision: Purchase of {item_name.title()} (₹{target_amt:,.2f})"
        if projected_surplus >= 0:
            if projected_savings_rate >= 15:
                status = "✅ **Green Light (Safe Purchase)**"
                advice = f"You can comfortably afford this! After this purchase, your remaining monthly savings will be **₹{projected_surplus:,.2f}** with a healthy savings rate of **{projected_savings_rate:.1f}%**."
            else:
                status = "⚠️ **Caution (Tight Savings Buffer)**"
                advice = f"You can afford this from your cash surplus, but it will reduce your monthly savings from **{savings_rate:.1f}%** down to **{projected_savings_rate:.1f}%** (₹{projected_surplus:,.2f} left). Consider splitting into 2 months or trimming {top_cat}."
        else:
            status = "🚫 **Deficit Warning (Not Recommended Right Now)**"
            shortfall = abs(projected_surplus)
            advice = f"This purchase will push your monthly finances into a deficit of **₹{shortfall:,.2f}**. Recommended strategy: Save **₹{target_amt/3:,.2f}/month** for 3 months or wait until next month's salary credit."

        body = f"""
- **Affordability Status**: {status}
- **Current Monthly Surplus**: ₹{net_surplus:,.2f}
- **Projected Surplus After Purchase**: ₹{projected_surplus:,.2f} (Savings Rate: {projected_savings_rate:.1f}%)
- **AI Recommendation**: {advice}
"""
    elif any(k in p for k in ['save', 'saving', 'savings', 'invest', 'wealth', 'sip', 'gold', 'goal', 'grow']):
        headline = "🎯 Savings & Wealth Growth Recommendation"
        body = f"""
- **Current Savings Trajectory**: You are saving **₹{net_surplus:,.2f} ({savings_rate:.1f}%)** of your gross earnings.
- **50 / 30 / 20 Target Budget Planning**:
  - **Needs (50%)**: Keep household and essential living expenses within **₹{total_inc*0.5:,.2f}**.
  - **Wants (30%)**: Keep dining, shopping, and entertainment within **₹{total_inc*0.3:,.2f}**.
  - **Savings & Investments (20%)**: Allocate **₹{total_inc*0.2:,.2f}** into recurring savings, emergency funds, or mutual fund SIPs.
- **Actionable Optimization**: Trimming 15% from your largest spending category (**{top_cat}**, ₹{top_cat_amt:,.2f}) will free up an extra **₹{top_cat_amt*0.15:,.2f}** in monthly savings.
"""
    elif any(k in p for k in ['budget', 'limit', 'exceed', 'over', 'spending', 'expense', 'breach', 'audit', 'overspent', 'deficit']):
        headline = "📊 Budget Variance & Spending Control Audit"
        if over_budget_cats:
            cat_str = ", ".join(over_budget_cats)
            body = f"""
- ⚠️ **Budget Limit Exceeded in**: **{cat_str}**.
- **Action Steps to Regain Balance**:
  1. Restrict non-essential payments in **{cat_str}** until the end of the month.
  2. Reallocate unspent funds from low-spending categories (such as Utilities or Bills) to cover the difference.
  3. Under the **'Annual & Monthly Budget Planner'** tab, review historical spending from FY 2023–2026 to set realistic limits.
"""
        else:
            body = f"""
- ✅ **100% Budget Compliance**: All your category budgets are well within assigned limits!
- **Spending Discipline**: With total outflow at **₹{total_exp:,.2f}**, your monthly burn rate is very well managed.
- **Financial Tip**: Maintain a buffer reserve of ₹5,000 to ₹10,000 in your monthly budget for unforeseen expenses.
"""
    elif any(k in p for k in ['food', 'dining', 'restaurant', 'meal', 'cafe', 'swiggy', 'zomato', 'eating']):
        food_spend = expenses[expenses.category.str.contains('Food|Dining|Canteen', case=False, na=False)]['amount'].sum() if not expenses.empty else 0.0
        pct_food = (food_spend / total_exp * 100) if total_exp > 0 else 0.0
        headline = "🍔 Food & Dining Spending Optimization"
        body = f"""
- **Total Recorded Food & Dining Outflow**: **₹{food_spend:,.2f}** ({pct_food:.1f}% of total outflow).
- **Practical Recommendation**: Delivery charges, packaging fees, and restaurant dining taxes add up quickly.
- **Monthly Savings**: Preparing meals at home during weekdays and reserving dining out for weekends can save approximately **₹{food_spend*0.25:,.2f}** per month.
"""
    elif any(k in p for k in ['transport', 'petrol', 'fuel', 'cab', 'travel', 'commute', 'uber', 'ola', 'auto']):
        travel_spend = expenses[expenses.category.str.contains('Transport|Fuel|Travel', case=False, na=False)]['amount'].sum() if not expenses.empty else 0.0
        headline = "🚗 Fuel & Commute Cost Analysis"
        body = f"""
- **Total Transportation Spending**: **₹{travel_spend:,.2f}** recorded across ledger entries.
- **Cost Reduction Tip**: Using public transit smart cards and carpooling for daily commutes can reduce monthly fuel and cab expenditure by up to 20%.
"""
    elif any(k in p for k in ['income', 'salary', 'earn', 'earning', 'revenue']):
        headline = "💼 Income & Revenue Assessment"
        body = f"""
- **Total Recorded Inflow**: **₹{total_inc:,.2f}**.
- **Net Monthly Surplus**: **₹{net_surplus:,.2f}** after deducting **₹{total_exp:,.2f}** in expenses.
- **Target Emergency Fund**: Financial advisors recommend keeping 3 to 6 months of expenses (**₹{total_exp*3:,.2f} – ₹{total_exp*6:,.2f}**) in a liquid fund or fixed deposit.
"""
    elif any(k in p for k in ['thank', 'thanks', 'great', 'awesome', 'good', 'ok', 'okay', 'perfect', 'nice']):
        headline = "🤝 You're Very Welcome!"
        body = f"""
I'm glad to help! Remember that consistency in tracking your khata and sticking to category budgets is the fastest way to compound your wealth.

Feel free to ask any other questions whenever you need guidance!
"""
    else:
        headline = f"💡 WalletMind AI Financial Advisor: '{prompt}'"
        body = f"""
- **Financial Status**: Total Inflow: **₹{total_inc:,.2f}** | Total Outflow: **₹{total_exp:,.2f}** | Net Savings: **₹{net_surplus:,.2f}** ({savings_rate:.1f}%).
- **Highest Spending Category**: **{top_cat}** represents **{top_cat_pct:.1f}%** (₹{top_cat_amt:,.2f}) of total expenses.
- **Personalized Advice**: 
  1. Try keeping **{top_cat}** spending below **₹{top_cat_amt*0.85:,.2f}** next month.
  2. Check the **'Annual & Monthly Budget Planner'** tab to review allocations across 2023–2026.
  3. You can also ask me specific affordability questions (e.g. *"Can I afford ₹20,000 for travel?"*).
"""

    score = max(10, min(100, int(70 + (20 if savings_rate >= 20 else -10 if savings_rate < 0 else 0) - (10 if over_budget_cats else 0))))
    return {
        'headline': headline,
        'body': body,
        'score': score,
        'savings_rate': savings_rate
    }

    score = max(10, min(100, int(70 + (20 if savings_rate >= 20 else -10 if savings_rate < 0 else 0) - (10 if over_budget_cats else 0))))
    return {
        'headline': headline,
        'body': body,
        'score': score,
        'savings_rate': savings_rate
    }

# ----------------- Password Checker -----------------
def check_password_rules(pwd: str):
    return {
        'len': len(pwd) >= 8,
        'upper': bool(re.search(r'[A-Z]', pwd)),
        'lower': bool(re.search(r'[a-z]', pwd)),
        'digit': bool(re.search(r'\d', pwd)),
        'special': bool(re.search(r'[@$!%*?&#^()_+\-=\[\]{}|;:<>.,/`~]', pwd))
    }

# ----------------- Session State -----------------
if 'auth_user' not in st.session_state:
    st.session_state.auth_user = None
if 'signup_stage' not in st.session_state:
    st.session_state.signup_stage = 'FORM'
if 'pending_data' not in st.session_state:
    st.session_state.pending_data = None
if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = []

# ==============================================================================
# EXACT CENTERED WHITE RECTANGULAR AUTHENTICATION CARD
# ==============================================================================
if not st.session_state.auth_user:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    c_left, c_box, c_right = st.columns([1, 1.4, 1])

    with c_box:
        st.markdown(f"""
        <div class="auth-main-card">
            <div class="auth-center-header">
                <div class="logo-img-wrapper">
                    <img src="{LOGO_BASE64}" class="logo-img" alt="WalletMind Logo" />
                </div>
                <h1 class="auth-brand-title">
                    Wallet<span>Mind</span>
                </h1>
                <p class="auth-brand-sub">
                    Executive Financial Intelligence & AI Budget Khata
                </p>
            </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Create Account"])

        # ----------------- TAB 1: SIGN IN -----------------
        with tab_login:
            with st.form("login_form"):
                in_email = st.text_input("REGISTERED EMAIL ID", value="demo001@example.invalid")
                in_pwd = st.text_input("MASTER PASSWORD", type="password", value="password123")
                btn_login = st.form_submit_button("Sign In to Portal →", type="primary", use_container_width=True)

                if btn_login:
                    if not in_email.strip() or not in_pwd:
                        st.error("Please enter both email ID and password.")
                    else:
                        hashed = hash_password(in_pwd)
                        match = query("SELECT id, display_name, email FROM users WHERE LOWER(email)=? AND password_hash=?",
                                      (in_email.strip().lower(), hashed))
                        if not match.empty:
                            st.session_state.auth_user = {
                                'id': str(match.iloc[0]['id']),
                                'name': str(match.iloc[0]['display_name']),
                                'email': str(match.iloc[0]['email'])
                            }
                            st.success(f"Welcome back, {st.session_state.auth_user['name']}! Logging in...")
                            time.sleep(0.3)
                            st.rerun()
                        else:
                            st.error("Incorrect email ID or password. Please try again.")

            st.markdown("""
            <div class="verified-demo-card">
                <div style="margin-bottom:4px;">💡 <strong class="title">Verified Demo Account:</strong></div>
                <div><strong>Email:</strong> <code>demo001@example.invalid</code></div>
                <div style="margin-top:2px;"><strong>Password:</strong> <code>password123</code></div>
            </div>
            """, unsafe_allow_html=True)

        # ----------------- TAB 2: CREATE ACCOUNT WITH GMAIL OTP -----------------
        with tab_signup:
            if st.session_state.signup_stage == 'FORM':
                with st.form("signup_form"):
                    reg_name = st.text_input("FULL NAME", placeholder="Rahul Sharma")
                    reg_email = st.text_input("REGISTERED GMAIL ID (FOR OTP)", placeholder="yourname@gmail.com")
                    reg_pwd = st.text_input("MASTER PASSWORD", type="password")
                    reg_pwd2 = st.text_input("CONFIRM PASSWORD", type="password")
                    btn_send_otp = st.form_submit_button("Send OTP to My Gmail →", type="primary", use_container_width=True)

                    if btn_send_otp:
                        rules = check_password_rules(reg_pwd)
                        if not reg_name.strip() or not reg_email.strip() or not reg_pwd:
                            st.error("Please fill in all mandatory fields.")
                        elif "@" not in reg_email or "." not in reg_email:
                            st.error("Please enter a valid Gmail address.")
                        elif not all(rules.values()):
                            st.error("Password must contain at least 8 characters with uppercase, lowercase, number, and symbol.")
                        elif reg_pwd != reg_pwd2:
                            st.error("Passwords do not match. Please re-check.")
                        else:
                            existing = query("SELECT id FROM users WHERE LOWER(email)=?", (reg_email.strip().lower(),))
                            if not existing.empty:
                                st.error("An account with this email ID already exists. Please Sign In.")
                            else:
                                otp_code = f"{random.randint(100000, 999999)}"
                                st.session_state.pending_data = {
                                    'name': reg_name.strip(),
                                    'email': reg_email.strip().lower(),
                                    'password': reg_pwd,
                                    'otp': otp_code,
                                    'time': time.time()
                                }

                                with st.spinner("Connecting to Gmail and sending OTP..."):
                                    sent, note = send_otp_to_gmail(reg_email.strip(), reg_name.strip(), otp_code)
                                    if sent:
                                        st.session_state.signup_stage = 'VERIFY'
                                        st.success(note)
                                        time.sleep(0.5)
                                        st.rerun()
                                    elif note == "SENDER_NOT_CONFIGURED":
                                        st.error("⚠️ SENDER GMAIL NOT CONFIGURED in .streamlit/secrets.toml")
                                    else:
                                        st.error(f"⚠️ Email dispatch error: {note}")

            elif st.session_state.signup_stage == 'VERIFY':
                pending = st.session_state.get('pending_data')
                if not pending:
                    st.session_state.signup_stage = 'FORM'
                    st.rerun()

                st.markdown(f"""
                <div style="background:#FBF6E9; border:1px solid #C59B27; border-radius:10px; padding:14px; margin-bottom:16px;">
                    <div style="font-size:14px; font-weight:700; color:#0A192F;">📧 OTP Dispatched to Gmail</div>
                    <div style="font-size:12.5px; color:#5C6B73; margin-top:2px;">A 6-digit verification code has been sent directly to <strong>{pending['email']}</strong>.</div>
                </div>
                """, unsafe_allow_html=True)

                with st.form("verify_form"):
                    entered_code = st.text_input("ENTER 6-DIGIT OTP FROM GMAIL", max_chars=6, placeholder="• • • • • •")
                    btn_activate = st.form_submit_button("Verify OTP & Activate", type="primary", use_container_width=True)

                    if btn_activate:
                        if not entered_code.strip():
                            st.error("Please enter the 6-digit OTP code sent to your Gmail.")
                        elif entered_code.strip() != pending['otp']:
                            st.error("Incorrect verification code. Please check your Gmail inbox.")
                        else:
                            new_uid = str(uuid.uuid4())
                            hashed_pw = hash_password(pending['password'])
                            write("INSERT INTO users (id, display_name, email, created_at, password_hash) VALUES (?, ?, ?, ?, ?)",
                                  (new_uid, pending['name'], pending['email'], date.today().isoformat(), hashed_pw))

                            default_categories = [
                                ('Salary', 'INCOME'),
                                ('Freelance & Consulting', 'INCOME'),
                                ('Food & Dining', 'EXPENSE'),
                                ('Groceries', 'EXPENSE'),
                                ('Transport & Petrol', 'EXPENSE'),
                                ('Utilities & Bills', 'EXPENSE'),
                                ('Entertainment', 'EXPENSE'),
                                ('House Rent', 'EXPENSE'),
                                ('Travel', 'EXPENSE'),
                                ('Medical & Health', 'EXPENSE')
                            ]
                            for c_name, c_type in default_categories:
                                write("INSERT INTO categories (id, user_id, name, type) VALUES (?, ?, ?, ?)",
                                      (str(uuid.uuid4()), new_uid, c_name, c_type))

                            st.session_state.auth_user = {
                                'id': new_uid,
                                'name': pending['name'],
                                'email': pending['email']
                            }
                            st.session_state.signup_stage = 'FORM'
                            st.session_state.pending_data = None
                            st.success("Account activated successfully! Loading your dashboard...")
                            time.sleep(0.4)
                            st.rerun()

                if st.button("← Back / Re-send OTP"):
                    st.session_state.signup_stage = 'FORM'
                    st.rerun()

        # Close the auth-main-card container
        st.markdown("</div>", unsafe_allow_html=True)

    # STRICT GATE: Stop execution here so no dashboard components render
    st.stop()

# ==============================================================================
# LOGGED-IN APPLICATION DASHBOARD (SHOWN ONLY AFTER SUCCESSFUL AUTHENTICATION)
# ==============================================================================
user = st.session_state.get('auth_user')
if not user:
    st.stop()

uid = user['id']
name = user.get('name', 'User')

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
        <img src="{LOGO_BASE64}" style="width:42px; height:42px; border-radius:50%; border:1.5px solid #C59B27;" />
        <div>
            <div style="font-weight:800; font-size:16px; color:#0A192F;">Wallet<span style="color:#C59B27;">Mind</span></div>
            <div style="font-size:10.5px; color:#1E3A5F; font-weight:700; letter-spacing:0.5px;">EXECUTIVE VAULT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#FFFFFF; border-radius:10px; padding:12px; border:1px solid #E8E2D2; margin-bottom:14px;">
        <div style="font-size:10.5px; color:#5C6B73; font-weight:600; text-transform:uppercase;">User Profile</div>
        <div style="font-weight:700; color:#0A192F; font-size:14px; margin-top:2px;">{name}</div>
        <div style="font-size:11.5px; color:#1E3A5F; word-break:break-all;">{user['email']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.auth_user = None
        st.session_state.signup_stage = 'FORM'
        st.rerun()

    st.markdown("---")
    menu = st.radio(
        "Executive Navigation",
        [
            "📊 Dashboard Overview",
            "🤖 AI Budget Advisory Corner",
            "🎯 Annual & Monthly Budget Planner",
            "💳 Smart Transactions Ledger",
            "📈 Forecast & Risk Analytics",
            "📁 Import / Export (50,000 Dataset)"
        ]
    )

# Fetch user data
cats = query("SELECT id, name, type FROM categories WHERE user_id=? ORDER BY name", (uid,))
txs = query("""
    SELECT t.id, t.transaction_date, t.type, t.amount, c.name AS category,
           t.description, t.payment_method, t.notes, t.category_id 
    FROM transactions t 
    JOIN categories c ON c.id=t.category_id AND c.user_id=t.user_id 
    WHERE t.user_id=? 
    ORDER BY t.transaction_date DESC
""", (uid,))

if not txs.empty:
    txs['transaction_date'] = pd.to_datetime(txs['transaction_date'], errors='coerce')
    expenses = txs[txs.type == 'EXPENSE'].copy()
    income = txs[txs.type == 'INCOME'].copy()
else:
    expenses = pd.DataFrame(columns=['id', 'transaction_date', 'type', 'amount', 'category', 'description', 'payment_method', 'notes', 'category_id'])
    income = pd.DataFrame(columns=['id', 'transaction_date', 'type', 'amount', 'category', 'description', 'payment_method', 'notes', 'category_id'])

# Fetch Budgets across years
budgets = query("""
    SELECT b.id, b.year, b.month, c.name AS category, b.amount AS budget_amount 
    FROM budgets b 
    JOIN categories c ON c.id=b.category_id AND c.user_id=b.user_id 
    WHERE b.user_id=? 
    ORDER BY b.year DESC, b.month DESC, c.name
""", (uid,))

if not budgets.empty and not expenses.empty:
    spent = expenses.assign(year=expenses.transaction_date.dt.year, month=expenses.transaction_date.dt.month).groupby(['year', 'month', 'category']).amount.sum().reset_index().rename(columns={'amount': 'spent_amount'})
    budgets = budgets.merge(spent, on=['year', 'month', 'category'], how='left').fillna({'spent_amount': 0})
    budgets['remaining'] = budgets['budget_amount'] - budgets['spent_amount']
    budgets['status'] = budgets['remaining'].apply(lambda x: 'Over Budget' if x < 0 else 'Within Budget')
else:
    budgets['spent_amount'] = 0.0
    budgets['remaining'] = budgets['budget_amount'] if not budgets.empty else 0.0
    budgets['status'] = 'Within Budget'

# Header Banner for App
st.markdown(f"""
<div style="background:#FFFFFF; border:1px solid #E8E2D2; border-radius:12px; padding:16px 20px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(10,25,47,0.04);">
    <div style="display:flex; align-items:center; gap:14px;">
        <img src="{LOGO_BASE64}" style="width:40px; height:40px; border-radius:50%; border:1px solid #C59B27;" />
        <div>
            <h2 style="margin:0; font-size:20px; color:#0A192F; font-weight:800;">{menu}</h2>
            <span style="font-size:12.5px; color:#5C6B73;">User: <strong>{name}</strong> &bull; Currency: Rupee (₹) &bull; Active Portal</span>
        </div>
    </div>
    <div style="background:#FBF6E9; border:1px solid #C59B27; color:#0A192F; padding:6px 14px; border-radius:20px; font-weight:700; font-size:12px;">
        🪙 AI Advisor Active
    </div>
</div>
""", unsafe_allow_html=True)

# Helper banner if account has no transactions yet
if txs.empty:
    st.info("💡 **Welcome to WalletMind.** This account does not have transactions yet. You can import records via CSV under **'Import / Export'**, add new entries under **'Smart Transactions Ledger'**, or load verified sample records below.")
    if st.button("📥 Load Sample Financial Records for My Account", type="primary"):
        sample_rows = [
            (str(uuid.uuid4()), uid, str(cats[cats.name=='Salary'].iloc[0]['id']) if not cats[cats.name=='Salary'].empty else str(cats.iloc[0]['id']), 'INCOME', 75000.0, 'Monthly Corporate Salary', 'Bank Transfer', '2026-11-01', 'Direct credit'),
            (str(uuid.uuid4()), uid, str(cats[cats.name=='Food & Dining'].iloc[0]['id']) if not cats[cats.name=='Food & Dining'].empty else str(cats.iloc[0]['id']), 'EXPENSE', 450.0, 'Dinner with friends', 'UPI', '2026-11-03', 'Casual dining'),
            (str(uuid.uuid4()), uid, str(cats[cats.name=='Groceries'].iloc[0]['id']) if not cats[cats.name=='Groceries'].empty else str(cats.iloc[0]['id']), 'EXPENSE', 2400.0, 'Monthly Grocery Supplies', 'Card', '2026-11-05', 'Supermarket'),
            (str(uuid.uuid4()), uid, str(cats[cats.name=='Transport & Petrol'].iloc[0]['id']) if not cats[cats.name=='Transport & Petrol'].empty else str(cats.iloc[0]['id']), 'EXPENSE', 850.0, 'Fuel refill', 'UPI', '2026-11-08', 'Petrol pump'),
            (str(uuid.uuid4()), uid, str(cats[cats.name=='Utilities & Bills'].iloc[0]['id']) if not cats[cats.name=='Utilities & Bills'].empty else str(cats.iloc[0]['id']), 'EXPENSE', 3200.0, 'Electricity & Wi-Fi', 'Net Banking', '2026-11-10', 'Monthly utility bill')
        ]
        with get_db() as conn:
            conn.executemany("INSERT INTO transactions(id, user_id, category_id, type, amount, description, payment_method, transaction_date, notes) VALUES (?,?,?,?,?,?,?,?,?)", sample_rows)
            conn.commit()
        st.success("Sample records loaded!")
        st.rerun()

# ==============================================================================
# 1. DASHBOARD OVERVIEW
# ==============================================================================
if menu == "📊 Dashboard Overview":
    tot_inc = float(income.amount.sum()) if not income.empty else 0.0
    tot_exp = float(expenses.amount.sum()) if not expenses.empty else 0.0
    net = tot_inc - tot_exp
    savings_pct = (net / tot_inc * 100) if tot_inc > 0 else 0.0

    # Executive Action Bar: PDF Statement Download
    head_col1, head_col2 = st.columns([2.5, 1.5])
    with head_col1:
        st.subheader("Financial Overview & Key Metrics")
    with head_col2:
        try:
            ai_eval = compute_ai_budget_insights("summary", uid, txs, budgets)
            pdf_bytes = generate_pdf_report(
                user_name=name,
                user_email=user['email'],
                income_amt=tot_inc,
                expense_amt=tot_exp,
                net_amt=net,
                savings_rate=savings_pct,
                df_budgets=budgets,
                ai_headline=ai_eval.get('headline', 'Financial Intelligence Overview'),
                ai_body=ai_eval.get('body', 'Consistently monitor category allocations to maintain positive liquidity.')
            )
            st.download_button(
                label="📄 Download Monthly PDF Report",
                data=pdf_bytes,
                file_name=f"walletmind_statement_{date.today().strftime('%Y_%m')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.caption(f"PDF generator ready ({e})")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Income", f"₹{tot_inc:,.2f}", delta=f"↑ ₹{tot_inc:,.0f}" if tot_inc > 0 else None, delta_color="normal")
    m2.metric("Total Expenses", f"₹{tot_exp:,.2f}", delta=f"↓ ₹{tot_exp:,.0f}" if tot_exp > 0 else None, delta_color="inverse")
    m3.metric("Net Savings", f"₹{net:,.2f}", delta=f"{savings_pct:+.1f}% Savings Rate", delta_color="normal" if net >= 0 else "inverse")
    m4.metric("Total Ledger Entries", f"{len(txs):,}", delta="Verified Records")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Monthly Spending Trend")
        if not expenses.empty:
            monthly = expenses.assign(month=expenses.transaction_date.dt.to_period('M').astype(str)).groupby('month')['amount'].sum().reset_index()
            monthly.columns = ['Month', 'Expenses (₹)']
            c_line = alt.Chart(monthly).mark_line(point=True, color='#1E3A5F').encode(
                x=alt.X('Month:N', title='Billing Period'),
                y=alt.Y('Expenses (₹):Q', title='Spending Outflow (₹)'),
                tooltip=['Month', alt.Tooltip('Expenses (₹):Q', format=',.2f')]
            ).properties(height=300)
            st.altair_chart(c_line, use_container_width=True)
        else:
            st.info("No expense data recorded yet.")

    with col_g2:
        st.subheader("Spending by Payment Method (UPI vs Card vs Net Banking)")
        if not expenses.empty:
            pm_sum = expenses.groupby('payment_method')['amount'].sum().reset_index()
            pm_sum.columns = ['Payment Method', 'Amount (₹)']
            c_donut = alt.Chart(pm_sum).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Amount (₹)", type="quantitative"),
                color=alt.Color(field="Payment Method", type="nominal", scale=alt.Scale(scheme='tableau10')),
                tooltip=['Payment Method', alt.Tooltip('Amount (₹):Q', format=',.2f')]
            ).properties(height=300)
            st.altair_chart(c_donut, use_container_width=True)
        else:
            st.info("No expense categories recorded yet.")

    # Recurring Subscriptions & Leak Detector
    st.markdown("---")
    st.subheader("🔍 Automated Recurring Subscriptions & Expense Audit")
    if not expenses.empty:
        rec_candidates = expenses[expenses['description'].str.contains('monthly|netflix|spotify|prime|wifi|electricity|gym|rent|subscription|broadband|bill', case=False, na=False)]
        if not rec_candidates.empty:
            rec_summary = rec_candidates.groupby('category')['amount'].agg(['count', 'sum']).reset_index().rename(columns={'count': 'Recurring Charges', 'sum': 'Total Outflow (₹)'})
            rc1, rc2 = st.columns([1.5, 1])
            with rc1:
                st.dataframe(rec_summary, hide_index=True, use_container_width=True)
            with rc2:
                st.info(f"💡 **Audit Insight**: Detected **{len(rec_candidates)} recurring charges** totaling **₹{rec_candidates['amount'].sum():,.2f}**. Review these recurring expenses periodically to eliminate unused subscriptions.")
        else:
            st.caption("No recurring subscription patterns detected in current transactions.")

    st.subheader("Recent Ledger Transactions")
    if not txs.empty:
        display_txs = txs[['transaction_date', 'type', 'category', 'amount', 'description', 'payment_method']].head(15).copy()
        # Add visual badges to transaction type and amount formatting
        display_txs['type'] = display_txs['type'].apply(lambda t: "🟢 INCOME" if str(t).upper() == 'INCOME' else "🔴 EXPENSE")
        display_txs['category'] = display_txs['category'].apply(lambda c: f"🏷️ {c}")
        display_txs['amount'] = display_txs['amount'].apply(lambda a: f"₹{float(a):,.2f}")
        st.dataframe(
            display_txs,
            column_config={
                "transaction_date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                "type": st.column_config.TextColumn("Type"),
                "category": st.column_config.TextColumn("Category"),
                "amount": st.column_config.TextColumn("Amount (₹)"),
                "description": st.column_config.TextColumn("Description"),
                "payment_method": st.column_config.TextColumn("Payment Mode")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No transactions logged yet.")

# ==============================================================================
# 2. SPECIFIC AI BUDGET ADVISORY CORNER & INTERACTIVE CHATBOT
# ==============================================================================
elif menu == "🤖 AI Budget Advisory Corner":
    st.subheader("🤖 Dedicated AI Budget Advisory & Chatbot")
    st.caption("Chat in real-time with your intelligent financial advisor. Get instant advice, budget breakdowns, and dynamic visual charts.")

    ai_eval = compute_ai_budget_insights("summary", uid, txs, budgets)
    ak1, ak2, ak3, ak4 = st.columns(4)
    ak1.metric("Budget Health Score", f"{ai_eval['score']} / 100")
    ak2.metric("Savings Rate", f"{ai_eval['savings_rate']:.1f}%")
    ak3.metric("Multi-Year Budgets Monitored", f"{len(budgets):,}")
    ak4.metric("Total Transactions Analyzed", f"{len(txs):,}")

    st.markdown("---")

    col_chat, col_viz = st.columns([1.35, 1])

    # Left Column: Interactive Chatbot
    with col_chat:
        st.markdown("### 💬 Client AI Financial Chatbot")
        st.caption("Ask questions about your budget, savings trajectory, discretionary limits, or expense reduction.")

        # Quick Prompt Chips
        st.write("**Quick Topics:**")
        qc1, qc2, qc3 = st.columns(3)
        if qc1.button("💡 How to save ₹15k?", use_container_width=True):
            st.session_state.chatbot_messages.append({'role': 'user', 'content': 'How can I save ₹15,000 next month based on my current spending?'})
            res = compute_ai_budget_insights('How can I save ₹15,000 next month based on my current spending?', uid, txs, budgets)
            bot_reply = f"**{res['headline']}**\n\n{res['body']}"
            st.session_state.chatbot_messages.append({'role': 'assistant', 'content': bot_reply})
            st.rerun()

        if qc2.button("📊 Audit all budgets", use_container_width=True):
            st.session_state.chatbot_messages.append({'role': 'user', 'content': 'Audit all my category budgets and highlight any overspending'})
            res = compute_ai_budget_insights('Audit all my category budgets and highlight any overspending', uid, txs, budgets)
            bot_reply = f"**{res['headline']}**\n\n{res['body']}"
            st.session_state.chatbot_messages.append({'role': 'assistant', 'content': bot_reply})
            st.rerun()

        if qc3.button("🍔 Dining expenses", use_container_width=True):
            st.session_state.chatbot_messages.append({'role': 'user', 'content': 'Analyze my food and dining expenses and recommend savings'})
            res = compute_ai_budget_insights('Analyze my food and dining expenses and recommend savings', uid, txs, budgets)
            bot_reply = f"**{res['headline']}**\n\n{res['body']}"
            st.session_state.chatbot_messages.append({'role': 'assistant', 'content': bot_reply})
            st.rerun()

        # Initialize chatbot messages in session state
        if 'chatbot_messages' not in st.session_state:
            st.session_state.chatbot_messages = [
                {
                    'role': 'assistant',
                    'content': f"Hello **{name}**! I am your WalletMind AI Budget Advisor. I have reviewed your recorded transactions and category budgets. You currently have a **{ai_eval['savings_rate']:.1f}% savings rate** with a **Financial Health Score of {ai_eval['score']}/100**.\n\nAsk me anything about your finances, budget targets, or whether you can afford an upcoming purchase!"
                }
            ]

        # Display conversational chat history using native Streamlit chat UI
        for msg in st.session_state.chatbot_messages:
            with st.chat_message(msg['role'], avatar="🪙" if msg['role'] == "assistant" else None):
                st.markdown(msg['content'])

        # Native Streamlit Chat Input for fluent, natural conversation
        user_prompt = st.chat_input("Ask your AI Budget Advisor a question (e.g., 'Can I afford ₹20,000 for travel?')...")
        if user_prompt:
            st.session_state.chatbot_messages.append({'role': 'user', 'content': user_prompt})
            with st.chat_message("user"):
                st.markdown(user_prompt)

            with st.chat_message("assistant", avatar="🪙"):
                with st.spinner("AI Advisor is analyzing your financial records..."):
                    res = compute_ai_budget_insights(user_prompt, uid, txs, budgets)
                    reply_text = f"**{res['headline']}**\n\n{res['body']}"
                    st.markdown(reply_text)
                    st.session_state.chatbot_messages.append({'role': 'assistant', 'content': reply_text})

        if len(st.session_state.chatbot_messages) > 1:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat History"):
                st.session_state.chatbot_messages = [st.session_state.chatbot_messages[0]]
                st.rerun()

    # Right Column: Visuals & Live Budget Charts
    with col_viz:
        st.markdown("### 📊 Live Budget Visuals & Insights")
        
        # 1. 50/30/20 Rule Breakdown
        st.markdown("#### 🎯 50 / 30 / 20 Budget Target Breakdown")
        tot_inc = float(income.amount.sum()) if not income.empty else 0.0
        if tot_inc > 0:
            needs = tot_inc * 0.50
            wants = tot_inc * 0.30
            savings = tot_inc * 0.20
            chart_df = pd.DataFrame({
                'Allocation': ['Needs (50%)', 'Wants (30%)', 'Savings & Investments (20%)'],
                'Amount (₹)': [needs, wants, savings]
            })
            st.bar_chart(chart_df.set_index('Allocation'))
        else:
            st.caption("Record regular income to generate dynamic 50/30/20 savings charts.")

        # 2. Category Spending Distribution Chart
        if not expenses.empty:
            st.markdown("#### 💳 Top Spending Categories")
            cat_totals = expenses.groupby('category')['amount'].sum().sort_values(ascending=False).head(6)
            st.bar_chart(cat_totals)

        # 3. Budget Status & Overspending Warnings
        st.markdown("#### 🛡️ Category Budget Compliance Status")
        if not budgets.empty:
            breaches = budgets[budgets['remaining'] < 0]
            if not breaches.empty:
                st.warning(f"⚠️ Note: {len(breaches)} historical category allocation(s) exceeded their target bounds.")
                for _, br in breaches.head(3).iterrows():
                    st.info(f"📌 **{br['category']} (FY{br['year']}-M{br['month']})**: Over allocation by ₹{abs(br['remaining']):,.2f} (Target: ₹{br['budget_amount']:,.2f})")
            else:
                st.success("✅ **100% Budget Compliant**: All categories are within planned budget limits with zero overspending breaches.")
        else:
            st.caption("No monthly budgets recorded.")

# ==============================================================================
# 3. ANNUAL & MONTHLY BUDGET PLANNER
# ==============================================================================
elif menu == "🎯 Annual & Monthly Budget Planner":
    st.subheader("🎯 Annual & Monthly Category Budget Planner")
    st.caption("Compare planned budget allocations versus actual spending across categories.")

    # Multi-Year Filter Controls
    b_col_y, b_col_m = st.columns(2)
    available_years = sorted(budgets['year'].unique().tolist(), reverse=True) if not budgets.empty else [2026, 2025, 2024, 2023]
    sel_year = b_col_y.selectbox("Financial Year", available_years)
    month_names = ["All Months (Full Year Overview)", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    sel_month_name = b_col_m.selectbox("Select Month", month_names)
    
    if sel_month_name == "All Months (Full Year Overview)":
        b_view = budgets[budgets['year'] == sel_year]
    else:
        m_num = month_names.index(sel_month_name)
        b_view = budgets[(budgets['year'] == sel_year) & (budgets['month'] == m_num)]

    if not b_view.empty:
        tot_b = b_view['budget_amount'].sum()
        tot_s = b_view['spent_amount'].sum()
        tot_r = tot_b - tot_s
        
        bk1, bk2, bk3, bk4 = st.columns(4)
        bk1.metric("Total Budget Allocated", f"₹{tot_b:,.2f}")
        bk2.metric("Total Spending", f"₹{tot_s:,.2f}")
        bk3.metric("Net Variance / Remaining", f"₹{tot_r:,.2f}", delta="Surplus" if tot_r >= 0 else "Over Budget")
        bk4.metric("Tracked Categories", f"{len(b_view):,}")

        # Enhanced Category Budget Graph
        st.subheader(f"📊 Category Budget vs Actual Spending Comparison ({sel_year} - {sel_month_name})")
        chart_data = b_view.groupby('category')[['budget_amount', 'spent_amount']].sum().rename(columns={
            'budget_amount': 'Planned Budget (₹)',
            'spent_amount': 'Actual Spending (₹)'
        })
        st.bar_chart(chart_data)

        # Category Budget Data Table
        st.subheader("📋 Category Budget Breakdown")
        st.dataframe(
            b_view[['year', 'month', 'category', 'budget_amount', 'spent_amount', 'remaining', 'status']].rename(columns={
                'year': 'Year',
                'month': 'Month',
                'category': 'Category',
                'budget_amount': 'Budget Target (₹)',
                'spent_amount': 'Spent Amount (₹)',
                'remaining': 'Remaining Balance (₹)',
                'status': 'Status'
            }),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info(f"No budget records found for FY {sel_year}. You can define category budgets below.")

    st.markdown("---")
    with st.expander("➕ Define / Update Category Budget"):
        with st.form("set_budget_form"):
            col_by1, col_by2, col_by3 = st.columns(3)
            new_byear = col_by1.number_input("Financial Year", min_value=2020, max_value=2030, value=date.today().year)
            new_bmonth = col_by2.selectbox("Month", list(range(1, 13)), index=date.today().month-1)
            expense_cats = cats[cats.type == 'EXPENSE']
            if not expense_cats.empty:
                new_bcat = col_by3.selectbox("Category", list(expense_cats.index), format_func=lambda i: expense_cats.loc[i, 'name'])
                new_bamt = st.number_input("Budget Amount (₹)", min_value=100.0, value=5000.0, step=500.0)
                if st.form_submit_button("Save Budget Target", type="primary"):
                    chosen_cid = str(expense_cats.loc[new_bcat, 'id'])
                    existing = query("SELECT id FROM budgets WHERE user_id=? AND category_id=? AND year=? AND month=?", (uid, chosen_cid, new_byear, new_bmonth))
                    if not existing.empty:
                        write("UPDATE budgets SET amount=? WHERE id=?", (new_bamt, str(existing.iloc[0]['id'])))
                        st.success("Budget updated!")
                    else:
                        write("INSERT INTO budgets(id, user_id, category_id, year, month, amount) VALUES (?,?,?,?,?,?)",
                              (str(uuid.uuid4()), uid, chosen_cid, new_byear, new_bmonth, new_bamt))
                        st.success("Budget established successfully!")
                    st.rerun()

# ==============================================================================
# 4. SMART TRANSACTIONS LEDGER
# ==============================================================================
elif menu == "💳 Smart Transactions Ledger":
    st.subheader("➕ Record New Transaction (Entry)")
    if cats.empty:
        st.warning("Please create at least one category first.")
    else:
        with st.form("add_tx_form", clear_on_submit=True):
            col_a1, col_a2, col_a3 = st.columns(3)
            t_type = col_a1.selectbox("Transaction Type", ["EXPENSE", "INCOME"])
            t_amt = col_a2.number_input("Amount (₹)", min_value=1.0, value=250.0, step=50.0)
            t_date = col_a3.date_input("Date", value=date.today())

            matching_cats = cats[cats.type == t_type]
            cat_list = matching_cats if not matching_cats.empty else cats
            chosen_cat = st.selectbox("Category", list(cat_list.index), format_func=lambda i: cat_list.loc[i, 'name'])

            t_desc = st.text_input("Description", placeholder="e.g. Grocery shopping at DMart")
            t_method = st.selectbox("Payment Method", ["UPI", "Cash", "Credit Card", "Debit Card", "Net Banking", "Wallet"])
            t_notes = st.text_input("Notes (Optional)")

            if st.form_submit_button("Save Entry in Ledger 💾", type="primary"):
                cat_id = str(cat_list.loc[chosen_cat, 'id'])
                write("INSERT INTO transactions (id, user_id, category_id, type, amount, description, payment_method, transaction_date, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (str(uuid.uuid4()), uid, cat_id, t_type, t_amt, t_desc, t_method, t_date.isoformat(), t_notes))
                st.success("Transaction saved successfully!")
                st.rerun()

    st.markdown("---")
    st.subheader("📋 Account Ledger History")
    if not txs.empty:
        st.dataframe(txs[['transaction_date', 'type', 'category', 'amount', 'description', 'payment_method']].head(40),
                     hide_index=True, use_container_width=True)
    else:
        st.info("No transactions found.")

# ==============================================================================
# 5. FORECAST & RISK ANALYTICS
# ==============================================================================
elif menu == "📈 Forecast & Risk Analytics":
    st.subheader("📈 Predictive Spending Forecast & Outlier Detection")
    if expenses.empty:
        st.info("No expenses recorded to forecast.")
    else:
        monthly = expenses.assign(month=expenses.transaction_date.dt.to_period('M')).groupby('month').amount.sum()
        st.line_chart(monthly.rename_axis('Month').rename('Spending (₹)'))
        avg_spend = monthly.mean()
        st.metric("Projected Next Month Outflow", f"₹{avg_spend:,.2f}")

        st.subheader("⚡ Statistical Outlier Transactions (>95th Percentile)")
        threshold = float(expenses['amount'].quantile(0.95))
        st.caption(f"Flagging expenses above ₹{threshold:,.2f}:")
        st.dataframe(expenses[expenses['amount'] > threshold][['transaction_date', 'category', 'amount', 'description']], hide_index=True, use_container_width=True)

# ==============================================================================
# 6. IMPORT / EXPORT (WITH 50,000 DATASET READY FOR TESTING)
# ==============================================================================
elif menu == "📁 Import / Export (50,000 Dataset)":
    st.subheader("📁 Complete 50,000 Transaction Dataset & Export")
    
    DATASET_CSV = BASE / 'walletmind_full_50000_transactions.csv'
    if DATASET_CSV.exists():
        st.markdown("""
        <div style="background:#FBF6E9; border:1px solid #C59B27; border-radius:12px; padding:16px 20px; margin-bottom:20px;">
            <h4 style="margin:0 0 6px 0; color:#0A192F;">📦 Master 50,000 Transaction Dataset Ready</h4>
            <p style="font-size:13px; color:#5C6B73; margin:0 0 12px 0;">
                A comprehensive dataset containing 50,000+ real records across 2024–2026 with categorized expenses, incomes, payment methods, and timestamps matching your import format.
            </p>
        </div>
        """, unsafe_allow_html=True)
        with open(DATASET_CSV, "rb") as f_data:
            st.download_button(
                "📥 Download Complete 50,000 Transactions Dataset (CSV)",
                f_data.read(),
                "walletmind_master_50000_transactions.csv",
                "text/csv",
                type="primary"
            )

    st.markdown("---")
    st.subheader("📤 Export Your Account Ledger")
    if not txs.empty:
        csv_data = txs.drop(columns=['category_id']).to_csv(index=False).encode('utf-8')
        st.download_button("Download My Transactions (CSV)", csv_data, f"walletmind_{name.lower().replace(' ','_')}.csv", "text/csv")

    st.markdown("---")
    st.subheader("📥 Import CSV Transactions into Account")
    st.caption("Upload any CSV with columns: `transaction_date`, `type`, `amount`, `category`, `description`.")

    uploaded = st.file_uploader("Select CSV File", type=['csv'])
    if uploaded is not None:
        try:
            df_in = pd.read_csv(uploaded)
            req = {'transaction_date', 'type', 'amount', 'category', 'description'}
            if not req.issubset(df_in.columns):
                st.error(f"Missing required columns in CSV: {sorted(req - set(df_in.columns))}")
            else:
                st.dataframe(df_in.head(10), hide_index=True)
                if st.button("Validate and Commit Import", type="primary"):
                    cat_map = {(str(r['name']).strip().lower(), str(r['type']).upper()): str(r['id']) for _, r in cats.iterrows()}
                    records = []
                    for _, row in df_in.iterrows():
                        r_type = str(row['type']).strip().upper()
                        r_cat_name = str(row['category']).strip()
                        key = (r_cat_name.lower(), r_type)

                        if key not in cat_map:
                            new_cat_id = str(uuid.uuid4())
                            write("INSERT INTO categories (id, user_id, name, type) VALUES (?, ?, ?, ?)",
                                  (new_cat_id, uid, r_cat_name, r_type))
                            cat_map[key] = new_cat_id

                        r_amt = float(row['amount'])
                        r_dt = pd.to_datetime(row['transaction_date']).date().isoformat()
                        records.append((
                            str(uuid.uuid4()), uid, cat_map[key], r_type, r_amt,
                            str(row['description']), str(row.get('payment_method', 'UPI')),
                            r_dt, str(row.get('notes', ''))
                        ))

                    with get_db() as conn:
                        conn.executemany("INSERT INTO transactions(id, user_id, category_id, type, amount, description, payment_method, transaction_date, notes) VALUES (?,?,?,?,?,?,?,?,?)", records)
                        conn.commit()
                    st.success(f"Successfully imported {len(records)} transactions!")
                    time.sleep(0.4)
                    st.rerun()
        except Exception as e:
            st.error(f"Import failed: {str(e)}")
