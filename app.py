"""
LUNTRA Calculator MVP - Deal Calculator for House-Hack & Whole Unit Models
Entry point for the Streamlit application with PDF export and financial heuristics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Configure page
st.set_page_config(
    page_title="LUNTRA Deal Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    st.title("🏠 LUNTRA Deal Calculator MVP")
    st.markdown("**60-second deal analysis for house-hack & whole unit models**")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        calculation_model = st.selectbox(
            "Calculation Model",
            ["House-Hack", "Whole Unit"],
            help="Choose your investment strategy"
        )
        
        st.header("Quick Input")
        purchase_price = st.number_input(
            "Purchase Price ($)",
            min_value=0,
            value=500000,
            step=10000,
            format="%d"
        )
        
        down_payment_pct = st.slider(
            "Down Payment (%)",
            min_value=0,
            max_value=50,
            value=20,
            step=5
        )
        
        interest_rate = st.slider(
            "Interest Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=6.5,
            step=0.25,
            format="%.2f"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Deal Analysis")
        
        # Basic calculations
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Display key metrics
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric("Purchase Price", f"${purchase_price:,}")
            st.metric("Down Payment", f"${down_payment:,}")
        
        with metrics_col2:
            st.metric("Loan Amount", f"${loan_amount:,}")
            st.metric("Interest Rate", f"{interest_rate}%")
        
        with metrics_col3:
            # Placeholder for calculated metrics
            st.metric("Monthly Payment", "$TBD")
            st.metric("Cash Flow", "$TBD")
        
        # Analysis results placeholder
        st.subheader("Financial Heuristics")
        st.info("📊 Detailed analysis will be displayed here")
        
        # Model-specific content
        if calculation_model == "House-Hack":
            st.subheader("House-Hack Model")
            st.write("Analysis for owner-occupied investment property")
            # TODO: Add house-hack specific calculations
        else:
            st.subheader("Whole Unit Model")
            st.write("Analysis for traditional rental property")
            # TODO: Add whole unit specific calculations
    
    with col2:
        st.header("Export & Actions")
        
        # PDF Export section
        st.subheader("📄 PDF Export")
        if st.button("Generate PDF Report", type="primary"):
            st.success("PDF generation coming soon!")
            # TODO: Implement PDF export functionality
        
        # Telemetry section
        st.subheader("📊 Session Data")
        session_data = {
            "model": calculation_model,
            "purchase_price": purchase_price,
            "down_payment_pct": down_payment_pct,
            "interest_rate": interest_rate,
            "timestamp": datetime.now().isoformat()
        }
        
        with st.expander("View Session JSON"):
            st.json(session_data)
        
        # Quick actions
        st.subheader("Quick Actions")
        if st.button("Save Configuration"):
            st.success("Configuration saved!")
            # TODO: Implement save functionality
        
        if st.button("Load Sample Data"):
            st.info("Loading sample data...")
            # TODO: Load from sample_data directory

if __name__ == "__main__":
    main()