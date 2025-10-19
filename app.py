import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Page config
st.set_page_config(
    page_title="Elektra - Smart Energy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(to bottom right, #dbeafe, #ccfbf1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 1rem;
        height: 3rem;
        font-weight: bold;
        background: linear-gradient(to right, #22d3ee, #06b6d4);
        color: white;
        border: none;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .user-card {
        background: rgba(255,255,255,0.9);
        padding: 1.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    .ai-message {
        background: #cffafe;
    }
    .user-message {
        background: #f3e8ff;
    }
    h1, h2, h3 {
        color: #0e7490;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = 'splash'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': 'Thomas',
        'address': 'Savanoriu. 48',
        'objectId': '543567012345',
        'contractType': 'Fixed'
    }
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Load data function
@st.cache_data
def load_energy_data():
 
    return None

# Splash Screen
def show_splash():
    st.markdown("""
    <div style='text-align: center; padding: 5rem 0;'>
        <div style='width: 8rem; height: 8rem; margin: 0 auto; border: 0.5rem solid #22d3ee; 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.2);'>
            <span style='font-size: 4rem;'>⚡</span>
        </div>
        <h1 style='font-size: 3.5rem; color: #22d3ee; margin-top: 2rem;'>ELEKTRA</h1>
        <p style='font-size: 1.5rem; color: #06b6d4;'>Power in Your Hands</p>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(2)
    st.session_state.screen = 'login'
    st.rerun()

# Login Screen
def show_login():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>⚡ ELEKTRA</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="••••••••")
        
        if st.button("LOGIN", type="primary"):
            st.session_state.authenticated = True
            st.session_state.screen = 'home'
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 1rem;'>Don't have an account yet?<br><strong>Create an account</strong></p>", unsafe_allow_html=True)

# Home Screen
def show_home(df):
    st.markdown(f"""
    <div class='user-card'>
        <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
            <div style='width: 4rem; height: 4rem; background: linear-gradient(to bottom right, #22d3ee, #3b82f6);
                        border-radius: 50%; display: flex; align-items: center; justify-content: center;'>
                <span style='font-size: 2rem; color: white;'>👤</span>
            </div>
            <h2 style='margin: 0;'>{st.session_state.user_data['name']}</h2>
        </div>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
            <div style='background: white; padding: 0.75rem; border-radius: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                🏠 {st.session_state.user_data['address']}
            </div>
            <div style='background: white; padding: 0.75rem; border-radius: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                ⚡ {st.session_state.user_data['objectId']}
            </div>
        </div>
        <div style='margin-top: 1rem;'>
            <span style='background: #22d3ee; color: white; padding: 0.5rem 1.5rem; border-radius: 1rem; font-weight: bold;'>
                Contract: {st.session_state.user_data['contractType']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if df is not None:
        # Filter for selected object
        selected_obj = st.selectbox("Select Object ID", df['obj_id'].unique(), key='obj_selector')
        user_df = df[df['obj_id'] == selected_obj].copy()
        
        # Calculate metrics
        last_30_days = user_df[user_df['date'] >= (datetime.now().date() - timedelta(days=30))]
        total_30d = last_30_days['v_kwh'].sum()
        avg_daily = last_30_days.groupby('date')['v_kwh'].sum().mean()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("30-Day Usage", f"{total_30d:.1f} kWh", f"+5.27%")
        with col2:
            st.metric("Avg Daily", f"{avg_daily:.2f} kWh")
        with col3:
            st.metric("Est. Cost", f"€{total_30d * 0.25:.2f}")
        
        # Monthly trend chart
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("📊 Energy Consumption Trend")
        
        monthly_data = user_df.groupby(user_df['date_time'].dt.to_period('M'))['v_kwh'].sum().reset_index()
        monthly_data['date_time'] = monthly_data['date_time'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_data['date_time'],
            y=monthly_data['v_kwh'],
            mode='lines',
            fill='tozeroy',
            line=dict(color='#22d3ee', width=3),
            fillcolor='rgba(168, 85, 247, 0.2)'
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Month",
            yaxis_title="kWh",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Daily breakdown
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("📅 Daily Breakdown")
        
        daily_data = last_30_days.groupby('date')['v_kwh'].sum().reset_index()
        daily_data = daily_data.tail(10)
        
        fig2 = px.bar(daily_data, x='date', y='v_kwh', 
                      color_discrete_sequence=['#22d3ee'])
        fig2.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Date",
            yaxis_title="kWh",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Detailed Stats Screen
def show_stats(df):
    if df is None:
        st.warning("No data available")
        return
    
    st.subheader("📊 Detailed Statistics")
    
    selected_obj = st.selectbox("Select Object", df['obj_id'].unique(), key='stats_obj')
    user_df = df[df['obj_id'] == selected_obj].copy()
    
    # Date picker
    selected_date = st.date_input("Select Date", datetime.now())
    
    # Filter for selected date
    daily_data = user_df[user_df['date'] == selected_date]
    
    if len(daily_data) > 0:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        
        # Hourly consumption
        hourly = daily_data.groupby('hour')['v_kwh'].sum().reset_index()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Consumption", f"{daily_data['v_kwh'].sum():.2f} kWh")
        with col2:
            st.metric("Peak Hour", f"{hourly.loc[hourly['v_kwh'].idxmax(), 'hour']}:00")
        
        # Hourly chart
        fig = px.bar(hourly, x='hour', y='v_kwh',
                     color_discrete_sequence=['#22d3ee'],
                     labels={'hour': 'Hour of Day', 'v_kwh': 'kWh'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No data available for selected date")

# AI Cam Screen
def show_ai_cam():
    st.markdown("<div class='metric-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("📷", unsafe_allow_html=True)
    st.title("AI Appliance Detection")
    st.write("Take a photo of your room and let AI identify all your electrical appliances")
    
    uploaded_file = st.file_uploader("Upload a photo", type=['jpg', 'jpeg', 'png'])
    
    if st.button("Analyze Photo", type="primary"):
        with st.spinner("Analyzing image..."):
            time.sleep(2)
            st.success("Analysis complete!")
    
    st.markdown("### Detected Appliances:")
    appliances = [
        ("🧊 Refrigerator", "~150W", "#22d3ee"),
        ("📺 TV", "~100W", "#a855f7"),
        ("❄️ Air Conditioner", "~2000W", "#06b6d4")
    ]
    
    for name, power, color in appliances:
        st.markdown(f"""
        <div style='background: {color}20; padding: 1rem; border-radius: 1rem; 
                    margin: 0.5rem 0; border-left: 4px solid {color};'>
            <div style='display: flex; justify-content: space-between;'>
                <span>{name}</span>
                <strong style='color: {color};'>{power}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Payment Screen
def show_payment():
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.title("💳 Payment Details")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### Total Amount")
    with col2:
        st.markdown("### €112.50")
    
    st.markdown("---")
    st.markdown("**Consumption (450 kWh)** — €112.50")
    
    st.markdown("### Select Payment Method")
    
    payment_method = st.radio(
        "",
        ["💳 Credit Card", "🏦 Bank Transfer", "💰 PayPal"],
        label_visibility="collapsed"
    )
    
    if st.button("Pay Now", type="primary"):
        with st.spinner("Processing payment..."):
            time.sleep(2)
            st.success("Payment successful!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# AI Assistant Screen
def show_ai_assistant():
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.title("💬 AI Energy Assistant")
    
    messages = [
        ("ai", "Based on your usage patterns, I've identified 3 ways to reduce your energy costs by up to 15%"),
        ("suggestion", "💡 Shift to Off-Peak Hours", "Your washing machine and dishwasher usage could save €8/month if run between 22:00-06:00", "#22d3ee"),
        ("suggestion", "🌡️ Optimize Heating", "Your heating spiked on July 14. Consider lowering by 1°C to save €12/month", "#a855f7"),
        ("suggestion", "⚡ Standby Power", "5 devices detected in standby mode. Unplug to save €3/month", "#10b981"),
        ("user", "What happened on July 14?"),
        ("ai", "There was a 2.5 kWh spike at 14:00. What appliances were running?")
    ]
    
    for msg in messages:
        if msg[0] == "ai":
            st.markdown(f"""
            <div class='chat-message ai-message'>
                <strong>AI:</strong> {msg[1]}
            </div>
            """, unsafe_allow_html=True)
        elif msg[0] == "user":
            st.markdown(f"""
            <div class='chat-message user-message'>
                <strong>You:</strong> {msg[1]}
            </div>
            """, unsafe_allow_html=True)
        elif msg[0] == "suggestion":
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 1rem; 
                        margin: 0.5rem 0; border-left: 4px solid {msg[3]}; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='font-weight: bold; margin: 0;'>{msg[1]}</p>
                <p style='margin: 0.5rem 0 0 0; color: #666;'>{msg[2]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    user_input = st.text_input("Type your message...", key="chat_input")
    if st.button("Send", type="primary"):
        st.success("Message sent!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Cost Comparison Screen
def show_cost_comparison():
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.title("💰 Energy Market Prices")
    
    providers = [
        ("Ignitis", 0.25, "current", None),
        ("INTER RAO Lietuva", 0.23, "save", 9),
        ("Enefit", 0.27, "lose", -9),
        ("IMLITEX ENERGY", 0.24, "save", 4.5)
    ]
    
    for name, price, status, savings in providers:
        if status == "current":
            st.markdown(f"""
            <div style='background: linear-gradient(to right, #22d3ee, #06b6d4); 
                        color: white; padding: 1.5rem; border-radius: 1rem; margin: 1rem 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='margin: 0; opacity: 0.9;'>Current Provider</p>
                        <h3 style='margin: 0.5rem 0; color: white;'>{name}</h3>
                    </div>
                    <div style='text-align: right;'>
                        <h2 style='margin: 0; color: white;'>€{price}</h2>
                        <p style='margin: 0; opacity: 0.9;'>/kWh</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            badge_color = "#10b981" if status == "save" else "#ef4444"
            badge_text = f"Save €{savings}/mo" if savings > 0 else f"+€{abs(savings)}/mo"
            
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 1rem; 
                        margin: 1rem 0; border: 2px solid #e5e7eb;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <p style='margin: 0; color: #666;'>{name}</p>
                        <h3 style='margin: 0.5rem 0;'>€{price}/kWh</h3>
                    </div>
                    <div style='background: {badge_color}20; color: {badge_color}; 
                                padding: 0.5rem 1rem; border-radius: 0.75rem; font-weight: bold;'>
                        {badge_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Switching to INTER RAO Lietuva could save you €108 per year based on your current usage of 450 kWh/month.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main app logic
def main():
    if st.session_state.screen == 'splash':
        show_splash()
    elif st.session_state.screen == 'login' and not st.session_state.authenticated:
        show_login()
    else:
        # Navigation
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Home", "📊 Stats", "📷 AI Cam", "💳 Pay", "⭐ Premium", "💰 Cost"
        ])
        
        # Load data once
        df = load_energy_data()
        
        with tab1:
            show_home(df)
        with tab2:
            show_stats(df)
        with tab3:
            show_ai_cam()
        with tab4:
            show_payment()
        with tab5:
            show_ai_assistant()
        with tab6:
            show_cost_comparison()

if __name__ == "__main__":
    main()
