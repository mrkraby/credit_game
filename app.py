import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import time

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Corporate Model Chef - Wholesale Edition",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Profesyonel CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1a237e, #0d47a1);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 300 !important;
        letter-spacing: 1px !important;
    }
    
    .corporate-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        border-left: 5px solid #1a237e;
    }
    
    .corporate-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-good {
        color: #4caf50;
        font-weight: 600;
    }
    
    .metric-bad {
        color: #f44336;
        font-weight: 600;
    }
    
    .metric-neutral {
        color: #ff9800;
        font-weight: 600;
    }
    
    .industry-badge {
        background: #e8eaf6;
        color: #1a237e;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.2rem;
        font-weight: 500;
    }
    
    .cooking-pot {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #1a237e;
        text-align: center;
        margin: 2rem 0;
    }
    
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

# --- Wholesale Oyun Konfigürasyonu ---
CORPORATE_INDUSTRIES = [
    'Manufacturing', 'Technology', 'Healthcare', 'Energy', 
    'Retail', 'Construction', 'Transportation', 'Financial Services'
]

# Kurumsal finansal göstergeler
FINANCIAL_METRICS = {
    'Liquidity': {
        'current_ratio': {'icon': '💧', 'weight': 0.8, 'description': 'Current Assets / Current Liabilities'},
        'quick_ratio': {'icon': '⚡', 'weight': 0.7, 'description': '(Current Assets - Inventory) / Current Liabilities'},
        'cash_ratio': {'icon': '💰', 'weight': 0.6, 'description': 'Cash / Current Liabilities'}
    },
    'Leverage': {
        'debt_to_equity': {'icon': '⚖️', 'weight': 0.9, 'description': 'Total Debt / Shareholders Equity'},
        'interest_coverage': {'icon': '📊', 'weight': 0.8, 'description': 'EBIT / Interest Expense'},
        'debt_to_assets': {'icon': '📉', 'weight': 0.7, 'description': 'Total Debt / Total Assets'}
    },
    'Profitability': {
        'roa': {'icon': '📈', 'weight': 0.7, 'description': 'Return on Assets'},
        'roe': {'icon': '🎯', 'weight': 0.8, 'description': 'Return on Equity'},
        'net_margin': {'icon': '💵', 'weight': 0.6, 'description': 'Net Profit Margin'},
        'operating_margin': {'icon': '🏭', 'weight': 0.7, 'description': 'Operating Profit Margin'}
    },
    'Size_Scale': {
        'revenue': {'icon': '💰', 'weight': 0.6, 'description': 'Annual Revenue (log scale)'},
        'total_assets': {'icon': '🏢', 'weight': 0.5, 'description': 'Total Assets (log scale)'},
        'market_share': {'icon': '🌍', 'weight': 0.7, 'description': 'Market Share %'}
    },
    'Growth': {
        'revenue_growth': {'icon': '📈', 'weight': 0.7, 'description': 'YoY Revenue Growth'},
        'profit_growth': {'icon': '📊', 'weight': 0.8, 'description': 'YoY Profit Growth'},
        'market_expansion': {'icon': '🌐', 'weight': 0.5, 'description': 'New Markets Entered'}
    }
}

# Kurumsal kredi modelleri
CORPORATE_MODELS = {
    'Altman Z-Score': {
        'icon': '📐',
        'description': 'Classic bankruptcy predictor for manufacturing firms',
        'difficulty': 'Medium',
        'base_accuracy': 0.75,
        'formula': '1.2A + 1.4B + 3.3C + 0.6D + 1.0E'
    },
    'Credit Rating Model': {
        'icon': '🏆',
        'description': 'Mimics rating agency methodologies (S&P, Moody\'s)',
        'difficulty': 'Hard',
        'base_accuracy': 0.80,
        'formula': 'Weighted score based on financial ratios'
    },
    'Corporate Scorecard': {
        'icon': '📋',
        'description': 'Balanced scorecard with financial & qualitative factors',
        'difficulty': 'Medium',
        'base_accuracy': 0.73,
        'formula': 'Multi-factor weighted average'
    },
    'Cash Flow Model': {
        'icon': '💸',
        'description': 'Focus on debt service capacity and cash flow adequacy',
        'difficulty': 'Easy',
        'base_accuracy': 0.70,
        'formula': 'DSCR + FFO/Total Debt'
    },
    'Ensemble Corporate': {
        'icon': '🔄',
        'description': 'Combines multiple models for robust prediction',
        'difficulty': 'Expert',
        'base_accuracy': 0.85,
        'formula': 'Voting ensemble of 3 models'
    }
}

# --- Session State Başlatma ---
def init_session_state():
    """Session state değişkenlerini başlat"""
    
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    if 'best_score' not in st.session_state:
        st.session_state.best_score = 0
    
    if 'best_model' not in st.session_state:
        st.session_state.best_model = None
    
    if 'models_tried' not in st.session_state:
        st.session_state.models_tried = 0

# --- Kurumsal Veri Üretme Fonksiyonu ---
def generate_corporate_data(n_companies=100):
    """Kurumsal firma verisi üret"""
    data = []
    
    for i in range(n_companies):
        industry = random.choice(CORPORATE_INDUSTRIES)
        
        # Sektöre göre baz risk farklılıkları
        industry_risk = {
            'Manufacturing': 0.5,
            'Technology': 0.4,
            'Healthcare': 0.3,
            'Energy': 0.7,
            'Retail': 0.5,
            'Construction': 0.6,
            'Transportation': 0.5,
            'Financial Services': 0.4
        }
        
        # Finansal metrikler
        company = {
            'company_id': f'CORP_{i+1:04d}',
            'industry': industry,
            'years_in_business': random.randint(5, 100),
            'employee_count': random.randint(50, 50000),
            
            # Liquidity
            'current_ratio': round(random.uniform(0.5, 3.0), 2),
            'quick_ratio': round(random.uniform(0.3, 2.5), 2),
            'cash_ratio': round(random.uniform(0.1, 1.5), 2),
            
            # Leverage
            'debt_to_equity': round(random.uniform(0.1, 3.0), 2),
            'interest_coverage': round(random.uniform(0.5, 10.0), 2),
            'debt_to_assets': round(random.uniform(0.1, 0.8), 2),
            
            # Profitability
            'roa': round(random.uniform(-0.1, 0.25), 3),
            'roe': round(random.uniform(-0.2, 0.4), 3),
            'net_margin': round(random.uniform(-0.05, 0.2), 3),
            'operating_margin': round(random.uniform(-0.05, 0.25), 3),
            
            # Size
            'revenue': random.randint(10_000_000, 10_000_000_000),
            'total_assets': random.randint(20_000_000, 20_000_000_000),
            'market_share': round(random.uniform(0.01, 0.3), 3),
            
            # Growth
            'revenue_growth': round(random.uniform(-0.1, 0.4), 3),
            'profit_growth': round(random.uniform(-0.2, 0.5), 3),
            'market_expansion': random.randint(0, 5),
            
            # Credit specific
            'loan_amount': random.randint(1_000_000, 100_000_000),
            'loan_term': random.choice([12, 24, 36, 48, 60]),
            'previous_defaults': random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]
        }
        
        # Altman Z-Score hesapla
        altman_z = (
            1.2 * (company['current_ratio'] / 10) +
            1.4 * max(company['roe'], 0) +
            3.3 * company['roa'] * 10 +
            0.6 * (1 / (company['debt_to_equity'] + 0.1)) +
            1.0 * (company['revenue'] / company['total_assets'])
        )
        
        # Risk skoru hesapla
        risk_score = (
            industry_risk[industry] * 0.3 +
            (1 - min(company['current_ratio'] / 3, 1)) * 0.15 +
            min(company['debt_to_equity'] / 3, 1) * 0.2 +
            (1 - min(company['interest_coverage'] / 5, 1)) * 0.15 +
            (1 - min(company['roa'] / 0.2, 1)) * 0.1 +
            (company['previous_defaults'] * 0.2) +
            random.uniform(-0.1, 0.1)
        )
        
        company['altman_z'] = round(altman_z, 2)
        company['risk_score'] = round(risk_score, 3)
        company['default'] = 1 if risk_score > 0.5 else 0
        company['rating'] = 'AAA' if risk_score < 0.2 else 'AA' if risk_score < 0.3 else 'A' if risk_score < 0.4 else 'BBB' if risk_score < 0.5 else 'BB' if risk_score < 0.6 else 'B' if risk_score < 0.7 else 'CCC'
        
        data.append(company)
    
    df = pd.DataFrame(data)
    return df

# --- Kurumsal Model Pişirme Fonksiyonu ---
def cook_corporate_model(model_name, selected_metrics, params, df):
    """Seçilen corporate model ile tahmin yap"""
    
    train_df = df.sample(frac=0.7, random_state=42)
    test_df = df.drop(train_df.index)
    
    if model_name == 'Altman Z-Score':
        def predict(row):
            z_score = (
                1.2 * (row['current_ratio'] / 10) +
                1.4 * max(row['roe'], 0) +
                3.3 * row['roa'] * 10 +
                0.6 * (1 / (row['debt_to_equity'] + 0.1)) +
                1.0 * (row['revenue'] / row['total_assets'])
            )
            threshold = params.get('z_threshold', 1.8)
            return 1 if z_score < threshold else 0
        
        train_pred = train_df.apply(predict, axis=1)
        test_pred = test_df.apply(predict, axis=1)
        
    elif model_name == 'Credit Rating Model':
        weights = {
            'debt_to_equity': params.get('debt_weight', 0.25),
            'interest_coverage': params.get('coverage_weight', 0.2),
            'roa': params.get('profitability_weight', 0.2),
            'current_ratio': params.get('liquidity_weight', 0.15),
            'revenue_growth': params.get('growth_weight', 0.1),
            'previous_defaults': params.get('history_weight', 0.1)
        }
        
        def predict(row):
            score = 0
            score += min(row['debt_to_equity'] / 5, 1) * weights['debt_to_equity']
            score += (1 - min(row['interest_coverage'] / 10, 1)) * weights['interest_coverage']
            score += (1 - min(row['roa'] / 0.25, 1)) * weights['roa']
            score += (1 - min(row['current_ratio'] / 3, 1)) * weights['current_ratio']
            score += (1 - min((row['revenue_growth'] + 0.1) / 0.5, 1)) * weights['revenue_growth']
            score += row['previous_defaults'] * 0.2 * weights['history_weight']
            return 1 if score > params.get('rating_threshold', 0.5) else 0
        
        train_pred = train_df.apply(predict, axis=1)
        test_pred = test_df.apply(predict, axis=1)
        
    elif model_name == 'Corporate Scorecard':
        category_weights = {
            'Liquidity': params.get('liq_weight', 0.15),
            'Leverage': params.get('lev_weight', 0.25),
            'Profitability': params.get('prof_weight', 0.25),
            'Size_Scale': params.get('size_weight', 0.15),
            'Growth': params.get('growth_weight', 0.2)
        }
        
        def predict(row):
            liq_score = (
                (1 - min(row['current_ratio'] / 3, 1)) * 0.4 +
                (1 - min(row['quick_ratio'] / 2.5, 1)) * 0.3 +
                (1 - min(row['cash_ratio'] / 1.5, 1)) * 0.3
            )
            
            lev_score = (
                min(row['debt_to_equity'] / 3, 1) * 0.4 +
                (1 - min(row['interest_coverage'] / 10, 1)) * 0.4 +
                min(row['debt_to_assets'], 1) * 0.2
            )
            
            prof_score = (
                (1 - min((row['roa'] + 0.1) / 0.35, 1)) * 0.3 +
                (1 - min((row['roe'] + 0.2) / 0.6, 1)) * 0.3 +
                (1 - min((row['net_margin'] + 0.05) / 0.25, 1)) * 0.2 +
                (1 - min((row['operating_margin'] + 0.05) / 0.3, 1)) * 0.2
            )
            
            size_score = 1 - min(row['revenue'] / 10_000_000_000, 1) * 0.5
            
            growth_score = (
                (1 - min((row['revenue_growth'] + 0.1) / 0.5, 1)) * 0.5 +
                (1 - min((row['profit_growth'] + 0.2) / 0.7, 1)) * 0.3 +
                (1 - min(row['market_expansion'] / 5, 1)) * 0.2
            )
            
            total_score = (
                liq_score * category_weights['Liquidity'] +
                lev_score * category_weights['Leverage'] +
                prof_score * category_weights['Profitability'] +
                size_score * category_weights['Size_Scale'] +
                growth_score * category_weights['Growth']
            )
            
            return 1 if total_score > params.get('scorecard_threshold', 0.5) else 0
        
        train_pred = train_df.apply(predict, axis=1)
        test_pred = test_df.apply(predict, axis=1)
        
    elif model_name == 'Cash Flow Model':
        def predict(row):
            dscr = row['operating_margin'] * row['revenue'] / (row['loan_amount'] * 0.1)
            ffo_to_debt = row['roa'] * row['total_assets'] / (row['debt_to_equity'] * row['total_assets'] / (1 + row['debt_to_equity']))
            dscr_score = 1 - min(dscr / 2, 1)
            ffo_score = 1 - min(ffo_to_debt / 0.2, 1)
            total_score = (dscr_score * 0.6 + ffo_score * 0.4)
            return 1 if total_score > params.get('cashflow_threshold', 0.5) else 0
        
        train_pred = train_df.apply(predict, axis=1)
        test_pred = test_df.apply(predict, axis=1)
        
    else:  # Ensemble Corporate
        n_models = params.get('n_models', 3)
        
        def predict(row):
            votes = []
            for _ in range(n_models):
                rand_threshold = random.uniform(0.4, 0.6)
                
                z_score = (
                    1.2 * (row['current_ratio'] / 10) +
                    1.4 * max(row['roe'], 0) +
                    3.3 * row['roa'] * 10 +
                    0.6 * (1 / (row['debt_to_equity'] + 0.1)) +
                    1.0 * (row['revenue'] / row['total_assets'])
                )
                vote1 = 1 if z_score < 1.8 else 0
                
                score = (
                    min(row['debt_to_equity'] / 5, 1) * 0.25 +
                    (1 - min(row['interest_coverage'] / 10, 1)) * 0.2 +
                    (1 - min(row['roa'] / 0.25, 1)) * 0.2 +
                    (1 - min(row['current_ratio'] / 3, 1)) * 0.15 +
                    row['previous_defaults'] * 0.1
                )
                vote2 = 1 if score > rand_threshold else 0
                
                dscr = row['operating_margin'] * row['revenue'] / (row['loan_amount'] * 0.1)
                vote3 = 1 if dscr < 1.2 else 0
                
                votes.extend([vote1, vote2, vote3])
            
            return 1 if sum(votes) > n_models * 1.5 else 0
        
        train_pred = train_df.apply(predict, axis=1)
        test_pred = test_df.apply(predict, axis=1)
    
    # 'default' sütununu kullan
    train_accuracy = (train_pred == train_df['default']).mean()
    test_accuracy = (test_pred == test_df['default']).mean()
    
    tp = ((test_pred == 1) & (test_df['default'] == 1)).sum()
    tn = ((test_pred == 0) & (test_df['default'] == 0)).sum()
    fp = ((test_pred == 1) & (test_df['default'] == 0)).sum()
    fn = ((test_pred == 0) & (test_df['default'] == 1)).sum()
    
    precision = tp / (tp + fp + 1e-10)
    recall = tp / (tp + fn + 1e-10)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-10)
    
    return {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': int(tp), 'tn': int(tn), 'fp': int(fp), 'fn': int(fn)
    }, test_pred

# Session state'i başlat
init_session_state()

# Eğer df yoksa yeni veri üret
if st.session_state.df is None:
    with st.spinner("Generating corporate data..."):
        st.session_state.df = generate_corporate_data(200)

# --- Debug: DataFrame sütunlarını göster ---
with st.expander("🔍 Debug - DataFrame Info", expanded=False):
    st.write("DataFrame shape:", st.session_state.df.shape)
    st.write("Columns:", list(st.session_state.df.columns))
    st.write("First 3 rows:")
    st.dataframe(st.session_state.df.head(3))
    st.write("Default distribution:", st.session_state.df['default'].value_counts())

# --- Ana Header ---
st.markdown("""
<div class='main-header'>
    <h1>🏢 Corporate Model Chef - Wholesale Edition</h1>
    <p style='color: rgba(255,255,255,0.9);'>Build credit risk models for large corporations and financial institutions</p>
</div>
""", unsafe_allow_html=True)

# --- Portfolio Overview ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Companies", len(st.session_state.df))
with col2:
    default_rate = st.session_state.df['default'].mean() * 100
    st.metric("Default Rate", f"%{default_rate:.1f}")
with col3:
    avg_loan = st.session_state.df['loan_amount'].mean() / 1_000_000
    st.metric("Avg Loan (M$)", f"${avg_loan:.1f}M")
with col4:
    st.metric("Industries", len(st.session_state.df['industry'].unique()))

# --- İki Kolonlu Layout ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### 📊 Financial Metrics")
    st.markdown("Select metrics for your model:")
    
    selected_metrics = []
    
    for category, metrics in FINANCIAL_METRICS.items():
        with st.expander(f"{category} Metrics", expanded=True):
            cols = st.columns(2)
            for i, (metric_name, metric_info) in enumerate(metrics.items()):
                with cols[i % 2]:
                    if st.checkbox(f"{metric_info['icon']} {metric_name.replace('_', ' ').title()}", 
                                  key=f"metric_{metric_name}", value=True):
                        selected_metrics.append(metric_name)
                        st.caption(metric_info['description'])
    
    st.markdown(f"**Selected Metrics:** {len(selected_metrics)}")
    
    st.divider()
    
    st.markdown("### 🏭 Industry Focus")
    selected_industries = st.multiselect(
        "Filter by industry (optional)",
        options=CORPORATE_INDUSTRIES,
        default=[]
    )
    
    st.divider()
    
    st.markdown("### 📈 Corporate Model")
    
    model_name = st.selectbox(
        "Choose your model",
        options=list(CORPORATE_MODELS.keys()),
        format_func=lambda x: f"{CORPORATE_MODELS[x]['icon']} {x} ({CORPORATE_MODELS[x]['difficulty']})"
    )
    
    st.caption(CORPORATE_MODELS[model_name]['description'])
    st.code(CORPORATE_MODELS[model_name]['formula'], language="text")
    
    st.markdown("#### ⚙️ Model Parameters")
    
    params = {}
    if model_name == 'Altman Z-Score':
        params['z_threshold'] = st.slider("Z-Score Threshold", 1.0, 3.0, 1.8, 0.1)
        st.caption("Companies with Z-Score below threshold are predicted to default")
        
    elif model_name == 'Credit Rating Model':
        col_a, col_b = st.columns(2)
        with col_a:
            params['debt_weight'] = st.slider("Debt Weight", 0.1, 0.5, 0.25, 0.05)
            params['coverage_weight'] = st.slider("Coverage Weight", 0.1, 0.4, 0.2, 0.05)
            params['profitability_weight'] = st.slider("Profitability Weight", 0.1, 0.4, 0.2, 0.05)
        with col_b:
            params['liquidity_weight'] = st.slider("Liquidity Weight", 0.05, 0.3, 0.15, 0.05)
            params['growth_weight'] = st.slider("Growth Weight", 0.05, 0.25, 0.1, 0.05)
            params['history_weight'] = st.slider("History Weight", 0.05, 0.25, 0.1, 0.05)
        params['rating_threshold'] = st.slider("Risk Threshold", 0.3, 0.7, 0.5, 0.05)
        
    elif model_name == 'Corporate Scorecard':
        col_a, col_b = st.columns(2)
        with col_a:
            params['liq_weight'] = st.slider("Liquidity Weight", 0.05, 0.3, 0.15, 0.05)
            params['lev_weight'] = st.slider("Leverage Weight", 0.1, 0.4, 0.25, 0.05)
            params['prof_weight'] = st.slider("Profitability Weight", 0.1, 0.4, 0.25, 0.05)
        with col_b:
            params['size_weight'] = st.slider("Size Weight", 0.05, 0.3, 0.15, 0.05)
            params['growth_weight'] = st.slider("Growth Weight", 0.05, 0.3, 0.2, 0.05)
        params['scorecard_threshold'] = st.slider("Risk Threshold", 0.3, 0.7, 0.5, 0.05)
        
    elif model_name == 'Cash Flow Model':
        params['cashflow_threshold'] = st.slider("Risk Threshold", 0.3, 0.7, 0.5, 0.05)
        
    else:  # Ensemble Corporate
        params['n_models'] = st.slider("Number of Models in Ensemble", 2, 7, 3)

with right_col:
    st.markdown("### 🏢 Corporate Portfolio")
    
    # Filtreleme
    display_df = st.session_state.df
    if selected_industries:
        display_df = display_df[display_df['industry'].isin(selected_industries)]
    
    with st.expander("📋 Company Data", expanded=False):
        st.dataframe(display_df[['company_id', 'industry', 'revenue', 'total_assets', 
                                 'debt_to_equity', 'rating', 'default']].head(10))
    
    st.markdown("<div class='cooking-pot'>", unsafe_allow_html=True)
    st.markdown("### 🍳 Model Development Studio")
    
    if st.button("🔥 DEVELOP MODEL", type="primary", use_container_width=True):
        if len(selected_metrics) < 3:
            st.warning("Please select at least 3 financial metrics!")
        else:
            with st.spinner("Developing corporate credit model... 🏢"):
                time.sleep(2)
                
                # Filtrelenmiş veri ile çalış
                work_df = display_df if len(display_df) > 50 else st.session_state.df
                
                results, predictions = cook_corporate_model(
                    model_name, selected_metrics, params, work_df
                )
                st.session_state.models_tried += 1
                
                st.markdown("### 📊 Model Performance")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    delta = results['test_accuracy'] - results['train_accuracy']
                    st.metric("Test Accuracy", f"%{results['test_accuracy']*100:.1f}", 
                             delta=f"%{delta*100:.1f} vs train")
                with col2:
                    st.metric("Precision", f"%{results['precision']*100:.1f}")
                with col3:
                    st.metric("Recall", f"%{results['recall']*100:.1f}")
                
                # Confusion Matrix
                st.markdown("**Confusion Matrix:**")
                
                tn_val = results['tn']
                fp_val = results['fp']
                fn_val = results['fn']
                tp_val = results['tp']
                
                matrix_text = f"""
                ┌───────────── Predicted ─────────────┐
                │            Non-Default    Default    │
                ┌─────────┼─────────────┼─────────────┤
                │ Non-Default│    {tn_val:4d}     │    {fp_val:4d}     │
                │  Default │    {fn_val:4d}     │    {tp_val:4d}     │
                └─────────┴─────────────┴─────────────┘
                """
                
                st.code(matrix_text, language="text")
                
                # Model karşılaştırma
                current_score = results['test_accuracy'] * 100
                if current_score > st.session_state.best_score:
                    st.session_state.best_score = current_score
                    st.session_state.best_model = {
                        'model': model_name,
                        'metrics': selected_metrics.copy(),
                        'params': params.copy(),
                        'industries': selected_industries.copy()
                    }
                    st.balloons()
                    st.success(f"🏆 New benchmark! {current_score:.1f}% accuracy!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Models Developed", st.session_state.models_tried)
    with col2:
        st.metric("Best Accuracy", f"%{st.session_state.best_score:.1f}")
    
    if st.session_state.best_model:
        with st.expander("🏆 Best Model So Far"):
            st.markdown(f"**Model:** {st.session_state.best_model['model']}")
            st.markdown(f"**Metrics:** {', '.join(st.session_state.best_model['metrics'][:5])}...")
            if st.session_state.best_model['industries']:
                st.markdown(f"**Industries:** {', '.join(st.session_state.best_model['industries'])}")

# --- Industry Analysis ---
st.markdown("---")
st.markdown("### 📈 Industry Risk Analysis")

industry_risk = st.session_state.df.groupby('industry')['default'].mean().sort_values()

fig = px.bar(
    x=industry_risk.values * 100,
    y=industry_risk.index,
    orientation='h',
    title='Default Rate by Industry',
    labels={'x': 'Default Rate %', 'y': 'Industry'},
    color=industry_risk.values,
    color_continuous_scale='RdYlGn_r'
)

st.plotly_chart(fig, use_container_width=True)

# --- Challenge Mode ---
st.markdown("---")
st.markdown("### 🏆 Wholesale Banking Challenges")

chal_col1, chal_col2, chal_col3 = st.columns(3)

with chal_col1:
    st.markdown("""
    <div class='corporate-card'>
        <h4>🎯 Target: 80% Accuracy</h4>
        <p>Build a model that achieves 80% test accuracy on the full portfolio</p>
        <p style='color: #1a237e; font-weight: 500;'>Reward: +50 pts</p>
    </div>
    """, unsafe_allow_html=True)

with chal_col2:
    st.markdown("""
    <div class='corporate-card'>
        <h4>🏭 Industry Specialist</h4>
        <p>Achieve 85% accuracy on a single industry (min. 30 companies)</p>
        <p style='color: #1a237e; font-weight: 500;'>Reward: +75 pts</p>
    </div>
    """, unsafe_allow_html=True)

with chal_col3:
    st.markdown("""
    <div class='corporate-card'>
        <h4>⚡ Model Efficiency</h4>
        <p>Reach 75% accuracy with max 5 financial metrics</p>
        <p style='color: #1a237e; font-weight: 500;'>Reward: +40 pts</p>
    </div>
    """, unsafe_allow_html=True)

# New Challenge button
if st.button("🎲 Generate New Challenges", key="new_challenges"):
    st.rerun()

# --- Footer (SON HALİ - DÜZGÜN KAPATILMIŞ) ---
st.markdown("""
<div class='footer'>
    <p>🏢 Corporate Model Chef - Wholesale Credit Risk Modeling Team</p>
    <p style='font-size: 0.8rem;'>© 2024 - Develop sophisticated models for corporate clients</p>
</div>
""", unsafe_allow_html=True)


