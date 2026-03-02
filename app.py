import streamlit as st
import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Beat The Risk - HBTR GRA Team",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Roboto:wght@300;400;500&display=swap');
    
    /* Ana sayfa arka planı - koyu finansal tema */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #1a2639 100%);
    }
    
    /* Tüm ana container */
    .main-container {
        background: rgba(26, 35, 62, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .main-header {
        background: linear-gradient(135deg, #0d1b3a 0%, #1a2c4e 100%);
        padding: 1rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,215,0,0.1);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .hsbc-logo {
        background: #ffffff;
        padding: 8px 20px;
        border-radius: 12px;
        font-family: "Times New Roman", serif;
        font-weight: 800;
        font-size: 28px;
        color: #DB0011;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,215,0,0.3);
    }
    
    .header-text {
        flex: 1;
    }
    
    .main-header h1 {
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        letter-spacing: 2px !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        background: linear-gradient(135deg, #fff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Roboto', sans-serif !important;
        font-size: 1rem !important;
        margin: 0.3rem 0 0 0 !important;
        letter-spacing: 0.5px;
    }
    
    .round-badge {
        background: rgba(255,215,0,0.15);
        backdrop-filter: blur(5px);
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        border: 1px solid rgba(255,215,0,0.3);
        color: #ffd700;
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e2a3a, #0f1a2a);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        text-align: center;
        border-bottom: 4px solid #ffd700;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,215,0,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(255,215,0,0.15);
    }
    
    .metric-label {
        color: #a0b0c0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .metric-value {
        color: #ffd700;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 2px 10px rgba(255,215,0,0.3);
    }
    
    .company-card {
        background: linear-gradient(135deg, #1e2a3a, #0f1a2a);
        border-radius: 25px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,215,0,0.1);
    }
    
    .company-header {
        border-bottom: 2px solid rgba(255,215,0,0.2);
        padding-bottom: 1.2rem;
        margin-bottom: 1.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sector-badge {
        background: linear-gradient(135deg, #2a3a4a, #1a2a3a);
        color: #ffd700;
        padding: 0.6rem 1.5rem;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 10px rgba(255,215,0,0.1);
        border: 1px solid rgba(255,215,0,0.2);
    }
    
    .size-badge {
        background: #ffd700;
        color: #0a0f1e;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .info-item {
        padding: 1.2rem;
        background: rgba(10, 15, 30, 0.6);
        border-radius: 15px;
        border-left: 6px solid #ffd700;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
        backdrop-filter: blur(5px);
    }
    
    .info-item:hover {
        background: rgba(20, 30, 50, 0.8);
        transform: translateX(5px);
    }
    
    .info-label {
        color: #a0b0c0;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    
    .info-value {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .stButton button {
        font-size: 1rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button[type="primary"] {
        background: linear-gradient(135deg, #ffd700, #ffa500) !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3) !important;
        color: #0a0f1e !important;
    }
    
    .stButton button[type="primary"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255,215,0,0.4) !important;
    }
    
    .risk-low {
        color: #4caf50;
        font-weight: 600;
    }
    
    .risk-medium {
        color: #ff9800;
        font-weight: 600;
    }
    
    .risk-high {
        color: #f44336;
        font-weight: 600;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4caf50, #ffc107, #f44336) !important;
        border-radius: 10px !important;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #a0b0c0;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,215,0,0.1);
        margin-top: 3rem;
        font-family: 'Roboto', sans-serif;
    }
    
    .footer .team {
        color: #ffd700;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Metric change renkleri */
    .metric-change {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Tüm yazılar için genel renk */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #ffffff;
    }
    
    /* Streamlit'in default beyaz arkaplanını kapat */
    .stApp > header {
        background-color: transparent !important;
    }
    
    .stApp [data-testid="stToolbar"] {
        right: 2rem;
        background: rgba(10, 15, 30, 0.8);
    }
    
    .stApp [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #0d1b3a, #1a2c4e);
    }
</style>
""", unsafe_allow_html=True)

INITIAL_CAPITAL = 10_000_000
MAX_ROUNDS = 8
RISK_FREE_RATE = 0.05

SECTORS = {
    'Technology': {
        'base_pd': 0.03,
        'sector_risk': 0.3,
        'beta': 1.3,
        'icon': '💻',
        'color': '#2196f3',
        'description': 'High growth, high volatility'
    },
    'Healthcare': {
        'base_pd': 0.02,
        'sector_risk': 0.2,
        'beta': 0.7,
        'icon': '🏥',
        'color': '#4caf50',
        'description': 'Defensive, stable cash flows'
    },
    'Energy': {
        'base_pd': 0.06,
        'sector_risk': 0.6,
        'beta': 1.2,
        'icon': '⚡',
        'color': '#ff9800',
        'description': 'Commodity price sensitive'
    },
    'Real Estate': {
        'base_pd': 0.05,
        'sector_risk': 0.5,
        'beta': 0.9,
        'icon': '🏢',
        'color': '#9c27b0',
        'description': 'Interest rate sensitive'
    },
    'Manufacturing': {
        'base_pd': 0.04,
        'sector_risk': 0.4,
        'beta': 1.0,
        'icon': '🏭',
        'color': '#795548',
        'description': 'Cyclical, asset intensive'
    },
    'Financial Services': {
        'base_pd': 0.035,
        'sector_risk': 0.35,
        'beta': 1.1,
        'icon': '🏦',
        'color': '#607d8b',
        'description': 'Regulatory sensitive'
    }
}

LEVERAGE_RATIOS = ['Very Low (<20%)', 'Low (20-40%)', 'Moderate (40-60%)', 'High (60-80%)', 'Very High (>80%)']
COVERAGE_RATIOS = ['Strong (>3x)', 'Good (2-3x)', 'Adequate (1.5-2x)', 'Weak (1-1.5x)', 'Critical (<1x)']
PROFITABILITY = ['Strong (>15%)', 'Good (10-15%)', 'Average (5-10%)', 'Weak (0-5%)', 'Loss Making']

def calculate_pd(company_data):
    base_pd = SECTORS[company_data['sector']]['base_pd']
    
    leverage_score = {
        'Very Low (<20%)': -0.02,
        'Low (20-40%)': 0,
        'Moderate (40-60%)': 0.02,
        'High (60-80%)': 0.05,
        'Very High (>80%)': 0.10
    }.get(company_data['leverage'], 0)
    
    coverage_score = {
        'Strong (>3x)': -0.03,
        'Good (2-3x)': -0.01,
        'Adequate (1.5-2x)': 0.01,
        'Weak (1-1.5x)': 0.04,
        'Critical (<1x)': 0.08
    }.get(company_data['coverage'], 0)
    
    profitability_score = {
        'Strong (>15%)': -0.02,
        'Good (10-15%)': 0,
        'Average (5-10%)': 0.02,
        'Weak (0-5%)': 0.04,
        'Loss Making': 0.07
    }.get(company_data['profitability'], 0)
    
    size_score = -0.01 if company_data['size'] == 'Large' else 0.01 if company_data['size'] == 'Small' else 0
    
    pd_value = base_pd + leverage_score + coverage_score + profitability_score + size_score
    pd_value = max(0.01, min(0.40, pd_value))
    
    return round(pd_value, 4)

def generate_company():
    sector = random.choice(list(SECTORS.keys()))
    size = random.choice(['Small', 'Medium', 'Large'])
    leverage = random.choice(LEVERAGE_RATIOS)
    coverage = random.choice(COVERAGE_RATIOS)
    profitability = random.choice(PROFITABILITY)
    
    if size == 'Large':
        loan_amount = random.randint(2_000_000, 5_000_000)
    elif size == 'Medium':
        loan_amount = random.randint(1_000_000, 2_000_000)
    else:
        loan_amount = random.randint(500_000, 1_000_000)
    
    maturity = random.choice([12, 24, 36, 48, 60])
    years_in_business = random.randint(3, 50)
    previous_defaults = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]
    
    company_data = {
        'sector': sector,
        'sector_icon': SECTORS[sector]['icon'],
        'sector_color': SECTORS[sector]['color'],
        'size': size,
        'leverage': leverage,
        'coverage': coverage,
        'profitability': profitability,
        'loan_amount': loan_amount,
        'maturity': maturity,
        'years_in_business': years_in_business,
        'previous_defaults': previous_defaults
    }
    
    pd_value = calculate_pd(company_data)
    company_data['pd'] = pd_value
    risk_premium = pd_value * 2
    company_data['interest_rate'] = round(RISK_FREE_RATE + risk_premium, 4)
    
    return company_data

def init_session_state():
    if 'capital' not in st.session_state:
        st.session_state.capital = INITIAL_CAPITAL
    if 'initial_capital' not in st.session_state:
        st.session_state.initial_capital = INITIAL_CAPITAL
    if 'round' not in st.session_state:
        st.session_state.round = 1
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'current_company' not in st.session_state:
        st.session_state.current_company = generate_company()
    if 'result_message' not in st.session_state:
        st.session_state.result_message = ""
    if 'result_color' not in st.session_state:
        st.session_state.result_color = "info"
    if 'loans_given' not in st.session_state:
        st.session_state.loans_given = 0
    if 'loans_defaulted' not in st.session_state:
        st.session_state.loans_defaulted = 0
    if 'loans_repaid' not in st.session_state:
        st.session_state.loans_repaid = 0
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    if 'expected_loss' not in st.session_state:
        st.session_state.expected_loss = 0
    if 'risk_weighted_assets' not in st.session_state:
        st.session_state.risk_weighted_assets = 0

init_session_state()

st.markdown(f"""
<div class='main-header'>
    <div class='header-content'>
        <div class='hsbc-logo'>
            HSBC
        </div>
        <div class='header-text'>
            <h1>🎯 BEAT THE RISK</h1>
            <p><span class='round-badge'>Round {st.session_state.round}/{MAX_ROUNDS}</span></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta = st.session_state.capital - INITIAL_CAPITAL
    delta_percent = (delta / INITIAL_CAPITAL) * 100
    delta_class = "risk-high" if delta < 0 else "risk-low"
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Portfolio Value</div>
        <div class='metric-value'>${st.session_state.capital:,.0f}</div>
        <div class='metric-change {delta_class}'>
            {delta:+,.0f} ({delta_percent:+.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.session_state.loans_given > 0:
        default_rate = (st.session_state.loans_defaulted / st.session_state.loans_given) * 100
    else:
        default_rate = 0
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Default Rate</div>
        <div class='metric-value'>%{default_rate:.1f}</div>
        <div class='metric-change'>{st.session_state.loans_defaulted} defaults</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Loans Given</div>
        <div class='metric-value'>{st.session_state.loans_given}</div>
        <div class='metric-change'>{st.session_state.loans_repaid} repaid</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if st.session_state.loans_given > 0 and len(st.session_state.portfolio) > 0:
        expected_loss = sum([loan.get('pd', 0) * loan.get('amount', 0) for loan in st.session_state.portfolio])
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Expected Loss</div>
            <div class='metric-value'>${expected_loss:,.0f}</div>
            <div class='metric-change'>Risk-Adjusted</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Expected Loss</div>
            <div class='metric-value'>$0</div>
            <div class='metric-change'>No loans yet</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.game_over and st.session_state.round <= MAX_ROUNDS:
    company = st.session_state.current_company
    
    pd_value = company.get('pd', 0.05)
    interest_rate = company.get('interest_rate', RISK_FREE_RATE + pd_value * 2)
    years_in_business = company.get('years_in_business', random.randint(3, 20))
    previous_defaults = company.get('previous_defaults', 0)
    loan_amount = company.get('loan_amount', 1_000_000)
    maturity = company.get('maturity', 24)
    sector = company.get('sector', 'Technology')
    sector_icon = company.get('sector_icon', '💼')
    sector_color = company.get('sector_color', '#1a237e')
    size = company.get('size', 'Medium')
    leverage = company.get('leverage', 'Moderate (40-60%)')
    coverage = company.get('coverage', 'Adequate (1.5-2x)')
    profitability = company.get('profitability', 'Average (5-10%)')
    
    st.markdown(f"""
    <div class='company-card'>
        <div class='company-header'>
            <span class='sector-badge'>{sector_icon} {sector}</span>
            <span class='size-badge'>{size} Cap</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Credit Application")
        
        st.markdown(f"""
        <div class='info-item'>
            <div class='info-label'>Requested Amount</div>
            <div class='info-value'>${loan_amount:,.0f}</div>
        </div>
        
        <div class='info-item'>
            <div class='info-label'>Maturity</div>
            <div class='info-value'>{maturity} months</div>
        </div>
        
        <div class='info-item'>
            <div class='info-label'>Proposed Interest Rate</div>
            <div class='info-value' style='color: #ffd700;'>%{interest_rate*100:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='info-item'>
            <div class='info-label'>Years in Business</div>
            <div class='info-value'>{years_in_business} years</div>
        </div>
        
        <div class='info-item'>
            <div class='info-label'>Previous Defaults</div>
            <div class='info-value'>{previous_defaults}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Financial Analysis")
        
        st.markdown(f"""
        <div class='info-item'>
            <div class='info-label'>Leverage Ratio</div>
            <div class='info-value'>{leverage}</div>
        </div>
        
        <div class='info-item'>
            <div class='info-label'>Interest Coverage</div>
            <div class='info-value'>{coverage}</div>
        </div>
        
        <div class='info-item'>
            <div class='info-label'>Profitability</div>
            <div class='info-value'>{profitability}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📈 Probability of Default (PD)")
        
        if pd_value < 0.05:
            pd_class = "Low Risk"
            pd_color = "#4caf50"
        elif pd_value < 0.10:
            pd_class = "Moderate Risk"
            pd_color = "#ff9800"
        elif pd_value < 0.20:
            pd_class = "High Risk"
            pd_color = "#f44336"
        else:
            pd_class = "Very High Risk"
            pd_color = "#b71c1c"
        
        st.progress(pd_value)
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; margin-top: 5px;'>
            <span style='color: white;'>0%</span>
            <span style='color: {pd_color}; font-weight: 600;'>{pd_class}</span>
            <span style='color: white;'>40%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Risk Metrics")
        st.markdown(f"""
        <div style='background: rgba(10, 15, 30, 0.8); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(255,215,0,0.1);'>
            <p style='margin: 0; color: white;'><strong style='color: #ffd700;'>PD:</strong> %{pd_value*100:.2f}</p>
            <p style='margin: 0; color: white;'><strong style='color: #ffd700;'>Risk Grade:</strong> {chr(65 + int(pd_value*10)) if pd_value*10 < 26 else 'NR'}</p>
            <p style='margin: 0; color: white;'><strong style='color: #ffd700;'>Expected Loss:</strong> ${loan_amount * pd_value:,.0f}</p>
            <p style='margin: 0; color: white;'><strong style='color: #ffd700;'>RWA:</strong> ${loan_amount * (pd_value * 12.5):,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        if st.button("✅ APPROVE LOAN", key=f"approve_{st.session_state.round}", 
                    type="primary", use_container_width=True):
            
            if 'portfolio' not in st.session_state:
                st.session_state.portfolio = []
            
            default_reason = ""
            
            if pd_value < 0.05:
                default_threshold = 0.05
                risk_level = "Low Risk"
            elif pd_value < 0.10:
                default_threshold = 0.25
                risk_level = "Moderate Risk"
            elif pd_value < 0.15:
                default_threshold = 0.45
                risk_level = "High Risk"
            elif pd_value < 0.20:
                default_threshold = 0.65
                risk_level = "Very High Risk"
            else:
                default_threshold = 0.85
                risk_level = "Extreme Risk"
            
            risk_factors = []
            if leverage in ['High (60-80%)', 'Very High (>80%)']:
                default_threshold *= 1.2
                risk_factors.append(f"High Leverage ({leverage})")
            if coverage in ['Weak (1-1.5x)', 'Critical (<1x)']:
                default_threshold *= 1.15
                risk_factors.append(f"Weak Interest Coverage ({coverage})")
            if profitability in ['Weak (0-5%)', 'Loss Making']:
                default_threshold *= 1.1
                risk_factors.append(f"Poor Profitability ({profitability})")
            if previous_defaults > 0:
                default_threshold *= (1 + previous_defaults * 0.15)
                risk_factors.append(f"Previous Defaults ({previous_defaults})")
            
            default = random.random() < min(default_threshold, 0.95)
            
            if default:
                loss = loan_amount
                st.session_state.capital -= loss
                st.session_state.loans_defaulted += 1
                
                if risk_factors:
                    reasons = ", ".join(risk_factors)
                    default_reason = f"**Primary Risk Factors:** {reasons}"
                else:
                    default_reason = f"**Primary Risk Factor:** Base PD of {pd_value*100:.1f}% indicates significant risk"
                
                st.session_state.result_message = f"""
                ❌ **LOAN DEFAULT**
                - Loss: ${loss:,.0f}
                - Risk Grade: {risk_level}
                - PD: %{pd_value*100:.2f}
                
                {default_reason}
                """
                st.session_state.result_color = "error"
            else:
                profit = loan_amount * interest_rate
                st.session_state.capital += profit
                st.session_state.loans_repaid += 1
                st.session_state.result_message = f"""
                ✅ **LOAN REPAID**
                - Interest Income: ${profit:,.0f}
                - Return: %{interest_rate*100:.2f}
                - Risk Grade: {risk_level}
                - PD Realized: 0%
                """
                st.session_state.result_color = "success"
            
            st.session_state.portfolio.append({
                'amount': loan_amount,
                'pd': pd_value,
                'interest': interest_rate,
                'sector': sector,
                'default': default,
                'leverage': leverage,
                'coverage': coverage,
                'profitability': profitability,
                'risk_factors': risk_factors
            })
            
            st.session_state.loans_given += 1
            
            if st.session_state.round < MAX_ROUNDS:
                st.session_state.round += 1
                st.session_state.current_company = generate_company()
            else:
                st.session_state.game_over = True
            
            st.rerun()
    
    with col3:
        if st.button("❌ REJECT", key=f"reject_{st.session_state.round}", 
                    use_container_width=True):
            st.session_state.result_message = """
            ℹ️ **LOAN REJECTED**
            - No impact on portfolio
            - Risk avoided
            """
            st.session_state.result_color = "info"
            
            if st.session_state.round < MAX_ROUNDS:
                st.session_state.round += 1
                st.session_state.current_company = generate_company()
            else:
                st.session_state.game_over = True
            
            st.rerun()
    
    if st.session_state.result_message:
        if st.session_state.result_color == "error":
            st.error(st.session_state.result_message)
        elif st.session_state.result_color == "success":
            st.success(st.session_state.result_message)
        else:
            st.info(st.session_state.result_message)

elif st.session_state.game_over:
    st.balloons()
    st.snow()
    
    total_return = st.session_state.capital - INITIAL_CAPITAL
    return_percent = (total_return / INITIAL_CAPITAL) * 100
    return_class = "risk-high" if total_return < 0 else "risk-low"
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0d1b3a, #1a2c4e); padding: 3rem; border-radius: 25px; text-align: center; margin-bottom: 2rem; border: 1px solid rgba(255,215,0,0.2);'>
        <h1 style='color: #ffd700; font-size: 3rem; margin: 0; font-family: Orbitron; text-shadow: 0 0 20px rgba(255,215,0,0.3);'>GAME OVER</h1>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.3rem;'>Final Portfolio Review</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Total Return</div>
            <div class='metric-value'>${total_return:,.0f}</div>
            <div class='metric-change {return_class}'>(%{return_percent:+.1f})</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.loans_given > 0:
            actual_default_rate = (st.session_state.loans_defaulted / st.session_state.loans_given) * 100
            if 'portfolio' in st.session_state and len(st.session_state.portfolio) > 0:
                avg_pd = sum([loan.get('pd', 0) for loan in st.session_state.portfolio]) / len(st.session_state.portfolio) * 100
            else:
                avg_pd = 0
        else:
            actual_default_rate = 0
            avg_pd = 0
        
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Default Rate</div>
            <div class='metric-value'>%{actual_default_rate:.1f}</div>
            <div class='metric-change'>Avg PD: %{avg_pd:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Portfolio Size</div>
            <div class='metric-value'>{st.session_state.loans_given}</div>
            <div class='metric-change'>{st.session_state.loans_repaid} performing</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.portfolio and len(st.session_state.portfolio) > 0:
        st.subheader("📈 Portfolio Analysis")
        
        df = pd.DataFrame(st.session_state.portfolio)
        
        col1, col2 = st.columns(2)
        
        with col1:
            sector_dist = df['sector'].value_counts()
            fig_sector = px.pie(
                values=sector_dist.values,
                names=sector_dist.index,
                title="Portfolio by Sector",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_sector.update_layout(
                plot_bgcolor='rgba(10,15,30,0.9)',
                paper_bgcolor='rgba(10,15,30,0.9)',
                font=dict(size=12, color='white'),
                title_font_color='#ffd700'
            )
            st.plotly_chart(fig_sector, use_container_width=True)
    
    st.subheader("📋 Detailed Risk Report")
    
    if st.session_state.portfolio and len(st.session_state.portfolio) > 0:
        report_data = []
        for i, loan in enumerate(st.session_state.portfolio, 1):
            report_data.append({
                'Loan #': i,
                'Sector': loan.get('sector', 'Unknown'),
                'Amount': f"${loan.get('amount', 0):,.0f}",
                'PD': f"%{loan.get('pd', 0)*100:.2f}",
                'Status': 'Default' if loan.get('default', False) else 'Performing',
                'Interest': f"%{loan.get('interest', 0)*100:.2f}"
            })
        
        report_df = pd.DataFrame(report_data)
        st.table(report_df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if return_percent > 10:
        st.success("🏆 **Excellent Performance!** You've mastered the risk!")
    elif return_percent > 0:
        st.info("📊 **Good Performance!** Solid risk management.")
    elif return_percent > -10:
        st.warning("⚠️ **Moderate Performance** Review your risk criteria.")
    else:
        st.error("📉 **Needs Improvement** Time to reassess your strategy.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Play Again", key="new_game", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.markdown("""
<div class='footer'>
    <div class='team'>HBTR GRA Team</div>
</div>
""", unsafe_allow_html=True)
