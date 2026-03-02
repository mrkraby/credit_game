import streamlit as st
import random
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime


st.set_page_config(
    page_title="Credit Risk Analyzer - Wholesale Banking",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>

    .main-header {
        background: linear-gradient(90deg, #1a237e 0%, #0d47a1 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 300 !important;
        letter-spacing: 1px !important;
        margin: 0 !important;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1rem !important;
        margin: 0.5rem 0 0 0 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        border-bottom: 3px solid #1a237e;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    .metric-label {
        color: #546e7a;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: #1a237e;
        font-size: 1.8rem;
        font-weight: 600;
        line-height: 1.2;
    }
    
    .metric-change {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Company Card */
    .company-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }
    
    .company-header {
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .sector-badge {
        background: #e3f2fd;
        color: #1565c0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
    }
    
    /* Info Grid */
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .info-item {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #1a237e;
    }
    
    .info-label {
        color: #546e7a;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        color: #1a237e;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* PD Gauge */
    .pd-gauge {
        background: linear-gradient(90deg, #4caf50, #ffc107, #f44336);
        height: 20px;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton button {
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        border-radius: 25px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }
    
    .stButton button[type="primary"] {
        background: linear-gradient(90deg, #1a237e, #0d47a1) !important;
        border: none !important;
    }
    
    .stButton button[type="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(26,35,126,0.3) !important;
    }
    
    /* Risk Indicators */
    .risk-low {
        color: #4caf50;
        font-weight: 500;
    }
    
    .risk-medium {
        color: #ff9800;
        font-weight: 500;
    }
    
    .risk-high {
        color: #f44336;
        font-weight: 500;
    }
    
    /* Progress Bar Customization */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4caf50, #ffc107, #f44336) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #90a4ae;
        font-size: 0.9rem;
        border-top: 1px solid #eceff1;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


INITIAL_CAPITAL = 10_000_000  # 10 Milyon USD
MAX_ROUNDS = 8
RISK_FREE_RATE = 0.05  # %5 risksiz faiz oranı


SECTORS = {
    'Technology': {
        'base_pd': 0.03,  # Baz PD
        'sector_risk': 0.3,
        'beta': 1.3,  # Piyasa betası
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
    """
    Probability of Default hesaplama - Gelişmiş model
    PD = f(sektör riski, kaldıraç, nakit akışı, karlılık, büyüklük)
    """
    # Baz PD (sektör bazlı)
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
    """Profesyonel firma profili üret"""
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
    
    maturity = random.choice([12, 24, 36, 48, 60])  # ay
    

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
    

    risk_premium = pd_value * 2  # Basit risk primi
    company_data['interest_rate'] = round(RISK_FREE_RATE + risk_premium, 4)
    
    return company_data


def init_session_state():
    """Tüm session state değişkenlerini güvenli bir şekilde başlat"""
    

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
        st.session_state.portfolio = []  # Boş liste olarak başlat
    

    if 'expected_loss' not in st.session_state:
        st.session_state.expected_loss = 0
    
    if 'risk_weighted_assets' not in st.session_state:
        st.session_state.risk_weighted_assets = 0


init_session_state()


st.markdown(f"""
<div class='main-header'>
    <h1>📊 Wholesale Credit Risk Analyzer</h1>
    <p>Advanced Probability of Default (PD) Modeling | Round {st.session_state.round}/{MAX_ROUNDS}</p>
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
    if st.session_state.loans_given > 0:
        # Portfolio'nun var olduğundan emin ol
        if 'portfolio' in st.session_state and st.session_state.portfolio:
            expected_loss = sum([loan.get('pd', 0) * loan.get('amount', 0) for loan in st.session_state.portfolio])
        else:
            expected_loss = 0
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
    

    pd_value = company.get('pd', 0.05)  # Varsayılan %5
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
            <span style='float: right; color: {sector_color}; font-weight: 500;'>{size} Cap</span>
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
            <div class='info-value' style='color: #1a237e;'>%{interest_rate*100:.2f}</div>
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
        
        # Financial Ratios
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
        
        # PD Progress Bar
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
            <span>0%</span>
            <span style='color: {pd_color}; font-weight: 600;'>{pd_class}</span>
            <span>40%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Risk Metrics")
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 1rem; border-radius: 8px;'>
            <p style='margin: 0;'><strong>PD:</strong> %{pd_value*100:.2f}</p>
            <p style='margin: 0;'><strong>Risk Grade:</strong> {chr(65 + int(pd_value*10)) if pd_value*10 < 26 else 'NR'}</p>
            <p style='margin: 0;'><strong>Expected Loss:</strong> ${loan_amount * pd_value:,.0f}</p>
            <p style='margin: 0;'><strong>RWA:</strong> ${loan_amount * (pd_value * 12.5):,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    

    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    
    with col2:
        if st.button("✅ APPROVE LOAN", key=f"approve_{st.session_state.round}", 
                    type="primary", use_container_width=True):
            
            
            if 'portfolio' not in st.session_state:
                st.session_state.portfolio = []
            

            default = random.random() < pd_value
            
            if default:
                # Default
                loss = loan_amount
                st.session_state.capital -= loss
                st.session_state.loans_defaulted += 1
                st.session_state.result_message = f"""
                ❌ **LOAN DEFAULT**
                - Loss: ${loss:,.0f}
                - PD Realized: %{pd_value*100:.2f}
                - Recovery Rate: 0%
                """
                st.session_state.result_color = "error"
            else:

                profit = loan_amount * interest_rate
                st.session_state.capital += profit
                st.session_state.loans_repaid += 1
                st.session_state.result_message = f"""
                ✅ **LOAN REPAID**
                - Interest Income: ${profit:,.0f}
                - PD Realized: 0%
                - Return: %{interest_rate*100:.2f}
                """
                st.session_state.result_color = "success"
            

            st.session_state.portfolio.append({
                'amount': loan_amount,
                'pd': pd_value,
                'interest': interest_rate,
                'sector': sector,
                'default': default
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
    
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1a237e, #0d47a1); padding: 3rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>📊 Portfolio Review</h1>
        <p style='color: rgba(255,255,255,0.9); font-size: 1.2rem;'>Final Risk Assessment Report</p>
    </div>
    """, unsafe_allow_html=True)
    

    total_return = st.session_state.capital - INITIAL_CAPITAL
    return_percent = (total_return / INITIAL_CAPITAL) * 100
    return_class = "risk-high" if total_return < 0 else "risk-low"
    
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
            if 'portfolio' in st.session_state and st.session_state.portfolio:
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
    

    if st.session_state.portfolio:
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
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12)
            )
            st.plotly_chart(fig_sector, use_container_width=True)
        
        with col2:

            fig_pd = px.histogram(
                df, 
                x='pd',
                nbins=10,
                title="PD Distribution",
                labels={'pd': 'Probability of Default'},
                color_discrete_sequence=['#1a237e']
            )
            fig_pd.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12)
            )
            st.plotly_chart(fig_pd, use_container_width=True)
    

    st.subheader("📋 Detailed Risk Report")
    
    if st.session_state.portfolio:
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
        st.success("🏆 **Excellent Performance!** Your risk management strategy delivered superior returns.")
    elif return_percent > 0:
        st.info("📊 **Good Performance!** Positive returns with controlled risk exposure.")
    elif return_percent > -10:
        st.warning("⚠️ **Moderate Performance** Portfolio underperformed. Review risk assessment criteria.")
    else:
        st.error("📉 **Needs Improvement** Significant losses. Strengthen credit analysis process.")
    

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Analysis", key="new_game", use_container_width=True):
        # Tüm session state'i temizle
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


st.markdown("""
<div class='footer'>
    <p>Wholesale Credit Risk Modeling Team | Probability of Default (PD) Model v2.0</p>
    <p style='font-size: 0.8rem;'>© 2024 - Advanced Risk Analytics for Institutional Banking</p>
</div>
""", unsafe_allow_html=True)

