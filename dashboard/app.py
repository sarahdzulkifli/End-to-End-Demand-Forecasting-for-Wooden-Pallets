import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

# API URL (update with your deployed API)
API_URL = "http://localhost:8080"  # Local API endpoint

st.title("🔮 Wooden Pallet Demand Forecasting")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    forecast_periods = st.slider(
        "Forecast Periods (Months)",
        min_value=1,
        max_value=12,
        value=6
    )
    
    st.markdown("---")
    st.header("📊 Input Parameters")
    
    last_quantity = st.number_input(
        "Last Known Quantity",
        min_value=0.0,
        value=1000.0,
        step=10.0
    )
    
    current_month = st.selectbox(
        "Current Month",
        options=list(range(1, 13)),
        index=datetime.now().month - 1
    )
    
    rate = st.number_input(
        "Current Rate",
        min_value=0.0,
        value=100.0,
        step=1.0
    )
    
    freight_cost = st.number_input(
        "Freight Cost",
        min_value=0.0,
        value=50.0,
        step=1.0
    )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📈 Forecast Results")
    
    if st.button("🚀 Generate Forecast", type="primary"):
        with st.spinner("Generating forecast..."):
            try:
                # Call API
                response = requests.post(
                    f"{API_URL}/predict",
                    json={
                        "periods": forecast_periods,
                        "last_quantity": last_quantity,
                        "current_month": current_month,
                        "rate": rate,
                        "freight_cost": freight_cost
                    }
                )
                
                if response.status_code == 200:
                    forecast_data = response.json()
                    df_forecast = pd.DataFrame(forecast_data)
                    
                    # Store in session state
                    st.session_state['forecast'] = df_forecast
                    
                    st.success("✅ Forecast generated successfully!")
                else:
                    st.error(f"❌ Error: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
                st.info("💡 Make sure the API is running and the URL is correct")

# Display forecast if available
if 'forecast' in st.session_state:
    df_forecast = st.session_state['forecast']
    
    # Visualization
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_forecast['date'],
        y=df_forecast['predicted_quantity'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Demand Forecast",
        xaxis_title="Date",
        yaxis_title="Predicted Quantity",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Table
    st.subheader("📋 Forecast Table")
    st.dataframe(
        df_forecast.style.format({
            'predicted_quantity': '{:.2f}'
        }),
        use_container_width=True
    )
    
    # Download button
    csv = df_forecast.to_csv(index=False)
    st.download_button(
        label="📥 Download Forecast",
        data=csv,
        file_name=f"forecast_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    st.header("📊 Summary Statistics")
    
    if 'forecast' in st.session_state:
        df_forecast = st.session_state['forecast']
        
        total_forecast = df_forecast['predicted_quantity'].sum()
        avg_forecast = df_forecast['predicted_quantity'].mean()
        max_forecast = df_forecast['predicted_quantity'].max()
        min_forecast = df_forecast['predicted_quantity'].min()
        
        st.metric("Total Forecasted", f"{total_forecast:,.0f}")
        st.metric("Average", f"{avg_forecast:,.0f}")
        st.metric("Maximum", f"{max_forecast:,.0f}")
        st.metric("Minimum", f"{min_forecast:,.0f}")
    else:
        st.info("Generate a forecast to see statistics")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit & FastAPI</p>
    </div>
    """,
    unsafe_allow_html=True
)