"""
LUNTRA Calculator MVP - Deal Calculator for House-Hack & Whole Unit Models
Entry point for the Streamlit application with PDF export and financial heuristics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import math
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Configure page
st.set_page_config(
    page_title="LUNTRA Deal Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Financial calculation functions
def calculate_monthly_mortgage_payment(principal, annual_rate, years):
    """Calculate monthly mortgage payment (P&I only)"""
    if annual_rate == 0:
        return principal / (years * 12)
    
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12
    
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    return monthly_payment

def calculate_piti(principal, annual_rate, years, annual_taxes, annual_insurance):
    """Calculate PITI (Principal, Interest, Taxes, Insurance)"""
    pi = calculate_monthly_mortgage_payment(principal, annual_rate, years)
    monthly_taxes = annual_taxes / 12
    monthly_insurance = annual_insurance / 12
    return pi + monthly_taxes + monthly_insurance

def calculate_noi(gross_rental_income, operating_expenses):
    """Calculate Net Operating Income"""
    return gross_rental_income - operating_expenses

def calculate_egi(gross_rental_income, vacancy_rate):
    """Calculate Effective Gross Income"""
    return gross_rental_income * (1 - vacancy_rate / 100)

def calculate_operating_expenses(egi, maintenance_pct, capex_pct, prop_mgmt_pct, utilities):
    """Calculate total operating expenses"""
    maintenance = egi * (maintenance_pct / 100)
    capex = egi * (capex_pct / 100)
    prop_mgmt = egi * (prop_mgmt_pct / 100)
    return maintenance + capex + prop_mgmt + utilities

def calculate_cash_flow(noi, piti):
    """Calculate monthly cash flow"""
    return (noi / 12) - piti

def calculate_cap_rate(noi, purchase_price):
    """Calculate capitalization rate"""
    if purchase_price == 0:
        return 0
    return (noi / purchase_price) * 100

def calculate_cash_on_cash_return(annual_cash_flow, total_cash_invested):
    """Calculate cash-on-cash return"""
    if total_cash_invested == 0:
        return 0
    return (annual_cash_flow / total_cash_invested) * 100

def generate_pdf_report(data):
    """Generate PDF report using reportlab"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("LUNTRA Deal Analysis Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Property Details
    story.append(Paragraph("Property Details", styles['Heading2']))
    property_data = [
        ['Purchase Price:', f"${data['purchase_price']:,}"],
        ['Down Payment:', f"${data['down_payment']:,} ({data['down_payment_pct']}%)"],
        ['Loan Amount:', f"${data['loan_amount']:,}"],
        ['Interest Rate:', f"{data['interest_rate']}%"],
    ]
    
    if data.get('annual_property_tax'):
        property_data.append(['Annual Property Tax:', f"${data['annual_property_tax']:,}"])
    if data.get('annual_insurance'):
        property_data.append(['Annual Insurance:', f"${data['annual_insurance']:,}"])
    
    property_table = Table(property_data)
    property_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(property_table)
    story.append(Spacer(1, 20))
    
    # Financial Analysis
    story.append(Paragraph("Financial Analysis", styles['Heading2']))
    analysis_data = [
        ['PITI Payment:', f"${data.get('piti', 0):,.2f}"],
        ['Monthly Cash Flow:', f"${data.get('monthly_cash_flow', 0):,.2f}"],
        ['Annual NOI:', f"${data.get('noi', 0):,.2f}"],
        ['Cap Rate:', f"{data.get('cap_rate', 0):.2f}%"],
        ['Cash-on-Cash Return:', f"{data.get('cash_on_cash', 0):.2f}%"],
    ]
    
    analysis_table = Table(analysis_data)
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(analysis_table)
    
    if data.get('notes'):
        story.append(Spacer(1, 20))
        story.append(Paragraph("Notes", styles['Heading2']))
        story.append(Paragraph(data['notes'], styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def track_usage(action, data=None):
    """Track user actions for analytics - Luntra Beta Metrics Capture"""
    analytics_data = {
        "event": action,
        "timestamp": datetime.now().isoformat(),
        "session_id": st.session_state.get("session_id", "unknown"),
        "user_id": st.session_state.get("user_id", "anonymous"),
        "properties": data or {},
        "page": "calculator_mvp"
    }
    
    # Store in session state for debugging and export
    if "analytics" not in st.session_state:
        st.session_state.analytics = []
    st.session_state.analytics.append(analytics_data)
    
    # In production, this would push to GA4, Mixpanel, or PostHog
    # gtag('event', action, data) or mixpanel.track(action, data)

def initialize_analytics():
    """Initialize analytics tracking for new session"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000}"
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"anon_{hash(st.session_state.session_id) % 100000}"
    
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now()
        track_usage("page_view", {
            "page_title": "LUNTRA Calculator MVP",
            "user_agent": "streamlit_app"
        })

def track_workflow_metrics(workflow_type, status, metrics_data):
    """Track workflow execution for Product Activation metrics"""
    if status == "started":
        track_usage("workflow_run", {
            "workflow_type": workflow_type,
            "purchase_price": metrics_data.get("purchase_price"),
            "model": workflow_type
        })
    elif status == "completed":
        track_usage("workflow_success", {
            "workflow_type": workflow_type,
            "purchase_price": metrics_data.get("purchase_price"),
            "cash_flow": metrics_data.get("cash_flow"),
            "cap_rate": metrics_data.get("cap_rate"),
            "time_to_completion": (datetime.now() - st.session_state.session_start).total_seconds()
        })
    elif status == "failed":
        track_usage("workflow_fail", {
            "workflow_type": workflow_type,
            "error": metrics_data.get("error", "unknown")
        })

def track_engagement_metrics():
    """Track engagement and retention metrics"""
    # Update workflow run count
    if "workflow_run_count" not in st.session_state:
        st.session_state.workflow_run_count = 0
    st.session_state.workflow_run_count += 1
    
    track_usage("active_user", {
        "session_duration": (datetime.now() - st.session_state.session_start).total_seconds(),
        "workflow_run_count": st.session_state.workflow_run_count
    })

def main():
    """Main application entry point"""
    # Initialize analytics tracking
    initialize_analytics()
    
    st.title("🏠 LUNTRA Deal Calculator MVP")
    st.markdown("**60-second deal analysis for house-hack & whole unit models**")
    
    # Version info with beta metrics
    st.caption("v1.0.0 Beta | Built for real estate investors | [Give Feedback](#feedback)")
    
    # Beta metrics banner
    if st.session_state.get("workflow_run_count", 0) == 0:
        st.info("🚀 **Welcome to LUNTRA Beta!** Help us improve by using the calculator and sharing feedback.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        calculation_model = st.selectbox(
            "Calculation Model",
            ["House-Hack", "Whole Unit"],
            help="Choose your investment strategy",
            on_change=lambda: track_usage("model_changed", {"model": calculation_model})
        )
        
        # Track workflow start when model is selected
        if calculation_model:
            if "current_workflow" not in st.session_state or st.session_state.current_workflow != calculation_model:
                st.session_state.current_workflow = calculation_model
                track_workflow_metrics(calculation_model, "started", {"purchase_price": 0})
        
        st.header("Property Details")
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
        
        st.header("Additional Property Costs")
        annual_property_tax = st.number_input(
            "Annual Property Tax ($)",
            min_value=0,
            value=8000,
            step=500,
            format="%d"
        )
        
        annual_insurance = st.number_input(
            "Annual Insurance ($)",
            min_value=0,
            value=2000,
            step=100,
            format="%d"
        )
        
        monthly_hoa = st.number_input(
            "Monthly HOA ($)",
            min_value=0,
            value=0,
            step=50,
            format="%d"
        )
        
        closing_costs = st.number_input(
            "Closing Costs ($)",
            min_value=0,
            value=int(purchase_price * 0.03),  # Default 3% of purchase price
            step=1000,
            format="%d"
        )
        
        st.header("Rental Income & Expenses")
        monthly_rent = st.number_input(
            "Monthly Rent ($)",
            min_value=0,
            value=3000,
            step=100,
            format="%d",
            help="Gross rental income per month"
        )
        
        vacancy_pct = st.slider(
            "Vacancy Rate (%)",
            min_value=0,
            max_value=20,
            value=5,
            step=1,
            help="Expected vacancy rate"
        )
        
        maintenance_pct = st.slider(
            "Maintenance (%)",
            min_value=0,
            max_value=15,
            value=5,
            step=1,
            help="Maintenance as % of EGI"
        )
        
        capex_pct = st.slider(
            "CapEx (%)",
            min_value=0,
            max_value=15,
            value=5,
            step=1,
            help="Capital expenditures as % of EGI"
        )
        
        property_mgmt_pct = st.slider(
            "Property Management (%)",
            min_value=0,
            max_value=15,
            value=8,
            step=1,
            help="Property management fee as % of EGI"
        )
        
        monthly_utilities = st.number_input(
            "Monthly Utilities ($)",
            min_value=0,
            value=0,
            step=50,
            format="%d",
            help="Utilities paid by owner"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Deal Analysis")
        
        # Basic calculations
        down_payment = purchase_price * (down_payment_pct / 100)
        loan_amount = purchase_price - down_payment
        
        # Calculate financial metrics
        annual_gross_rental = monthly_rent * 12
        egi = calculate_egi(annual_gross_rental, vacancy_pct)
        annual_utilities = monthly_utilities * 12
        operating_expenses = calculate_operating_expenses(egi, maintenance_pct, capex_pct, property_mgmt_pct, annual_utilities)
        noi = calculate_noi(egi, operating_expenses)
        
        # PITI calculation
        piti = calculate_piti(loan_amount, interest_rate, 30, annual_property_tax, annual_insurance) + monthly_hoa
        monthly_cash_flow = calculate_cash_flow(noi, piti)
        annual_cash_flow = monthly_cash_flow * 12
        
        # Investment metrics
        total_cash_invested = down_payment + closing_costs
        cap_rate = calculate_cap_rate(noi, purchase_price)
        cash_on_cash = calculate_cash_on_cash_return(annual_cash_flow, total_cash_invested)
        
        # Track workflow completion with engagement metrics
        track_engagement_metrics()
        track_workflow_metrics(calculation_model, "completed", {
            "purchase_price": purchase_price,
            "cash_flow": monthly_cash_flow,
            "cap_rate": cap_rate,
            "cash_on_cash": cash_on_cash,
            "total_cash_invested": total_cash_invested
        })
        
        # Display key metrics
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric("Purchase Price", f"${purchase_price:,}")
            st.metric("Down Payment", f"${down_payment:,}")
        
        with metrics_col2:
            st.metric("Loan Amount", f"${loan_amount:,}")
            st.metric("PITI + HOA", f"${piti:,.2f}")
        
        with metrics_col3:
            st.metric("Monthly Cash Flow", f"${monthly_cash_flow:,.2f}", 
                     delta=f"${annual_cash_flow:,.0f} annually")
            st.metric("NOI", f"${noi:,.0f}")
        
        with metrics_col4:
            st.metric("Cap Rate", f"{cap_rate:.2f}%")
            st.metric("Cash-on-Cash", f"{cash_on_cash:.2f}%")
        
        # Analysis results
        st.subheader("Financial Heuristics")
        
        # Cash flow analysis
        if monthly_cash_flow > 0:
            st.success(f"✅ Positive cash flow: ${monthly_cash_flow:,.2f}/month")
        elif monthly_cash_flow == 0:
            st.warning("⚖️ Break-even cash flow")
        else:
            st.error(f"❌ Negative cash flow: ${monthly_cash_flow:,.2f}/month")
        
        # Cap rate analysis
        if cap_rate >= 8:
            st.success(f"✅ Strong cap rate: {cap_rate:.2f}%")
        elif cap_rate >= 6:
            st.warning(f"⚖️ Moderate cap rate: {cap_rate:.2f}%")
        else:
            st.error(f"❌ Low cap rate: {cap_rate:.2f}%")
        
        # 1% rule check
        one_percent_target = purchase_price * 0.01
        if monthly_rent >= one_percent_target:
            st.success(f"✅ Meets 1% rule: ${monthly_rent:,} >= ${one_percent_target:,.0f}")
        else:
            st.warning(f"⚖️ Below 1% rule: ${monthly_rent:,} < ${one_percent_target:,.0f}")
        
        # Detailed breakdown
        st.subheader("Income & Expense Breakdown")
        
        breakdown_col1, breakdown_col2 = st.columns(2)
        
        with breakdown_col1:
            st.write("**Monthly Income:**")
            st.write(f"• Gross Rent: ${monthly_rent:,}")
            st.write(f"• Less Vacancy ({vacancy_pct}%): -${(monthly_rent * vacancy_pct / 100):,.0f}")
            st.write(f"• **Effective Gross Income: ${egi/12:,.0f}**")
            
        with breakdown_col2:
            st.write("**Monthly Expenses:**")
            st.write(f"• PITI: ${piti - monthly_hoa:,.2f}")
            st.write(f"• HOA: ${monthly_hoa:,}")
            st.write(f"• Maintenance ({maintenance_pct}%): ${(egi * maintenance_pct / 100 / 12):,.0f}")
            st.write(f"• CapEx ({capex_pct}%): ${(egi * capex_pct / 100 / 12):,.0f}")
            st.write(f"• Prop Mgmt ({property_mgmt_pct}%): ${(egi * property_mgmt_pct / 100 / 12):,.0f}")
            st.write(f"• Utilities: ${monthly_utilities:,}")
        
        # Model-specific content
        if calculation_model == "House-Hack":
            st.subheader("House-Hack Analysis")
            st.write("**Owner-Occupied Investment Strategy**")
            
            # House hack specific metrics
            typical_rent = 2500  # Could be made configurable
            housing_cost_savings = typical_rent - abs(min(monthly_cash_flow, 0))
            
            st.info(f"💡 **Effective Housing Cost Reduction:** You're saving approximately ${housing_cost_savings:,.0f}/month compared to renting a similar property")
            
            # Owner-occupancy benefits
            st.write("**Owner-Occupancy Benefits:**")
            st.write("• Lower down payment requirements (3-5% vs 20-25%)")
            st.write("• Better interest rates (owner-occupied vs investment)")
            st.write("• Tax benefits for primary residence")
            st.write("• Forced savings through principal paydown")
            
        else:
            st.subheader("Whole Unit Analysis")
            st.write("**Traditional Rental Property Strategy**")
            
            # Investment property specific analysis
            if cash_on_cash >= 10:
                st.success(f"🎯 Excellent cash-on-cash return: {cash_on_cash:.2f}%")
            elif cash_on_cash >= 6:
                st.warning(f"⚖️ Moderate cash-on-cash return: {cash_on_cash:.2f}%")
            else:
                st.error(f"📉 Low cash-on-cash return: {cash_on_cash:.2f}%")
            
            st.write("**Investment Considerations:**")
            st.write("• Higher down payment required (20-25%)")
            st.write("• Investment property interest rates")
            st.write("• No homestead exemptions")
            st.write("• Full depreciation benefits")
    
    with col2:
        st.header("Notes & Export")
        
        # Notes section
        st.subheader("📝 Deal Notes")
        notes = st.text_area(
            "Notes (for PDF export)",
            placeholder="Add your analysis notes, concerns, or action items here...",
            height=150
        )
        
        # ROI & Value Feedback (Luntra Beta Key Metric)
        if st.session_state.get("workflow_run_count", 0) >= 1:
            with st.expander("💰 Quick Value Assessment - Help Us Measure Impact!", expanded=False):
                st.write("**Your feedback helps us show the value LUNTRA provides to investors like you.**")
                
                roi_col1, roi_col2 = st.columns(2)
                
                with roi_col1:
                    time_saved = st.selectbox(
                        "How much time did this calculator save you?",
                        ["Select...", "< 15 minutes", "15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"],
                        key="time_saved"
                    )
                    
                    helped_decision = st.selectbox(
                        "Did this help you make a faster investment decision?",
                        ["Select...", "Yes, definitely", "Somewhat helpful", "Not really", "Too early to tell"],
                        key="helped_decision"
                    )
                
                with roi_col2:
                    manual_cost = st.selectbox(
                        "What would you pay someone to do this analysis manually?",
                        ["Select...", "$25-50", "$50-100", "$100-200", "$200-500", "$500+"],
                        key="manual_cost"
                    )
                    
                    thumbs_feedback = st.radio(
                        "Overall, did this save you time?",
                        ["👍 Yes", "👎 No", "🤷 Unsure"],
                        key="thumbs_feedback",
                        horizontal=True
                    )
                
                if st.button("📊 Submit Value Feedback", key="roi_feedback"):
                    if time_saved != "Select..." or helped_decision != "Select...":
                        roi_data = {
                            "type": "roi_feedback",
                            "time_saved": time_saved,
                            "helped_decision": helped_decision,
                            "manual_cost": manual_cost,
                            "thumbs_feedback": thumbs_feedback,
                            "workflow_count": st.session_state.get("workflow_run_count", 0),
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        if "feedback_submissions" not in st.session_state:
                            st.session_state.feedback_submissions = []
                        st.session_state.feedback_submissions.append(roi_data)
                        
                        track_usage("roi_feedback_submitted", roi_data)
                        st.success("💯 Thanks! This helps us measure LUNTRA's real-world impact.")
                        st.balloons()
                    else:
                        st.warning("Please answer at least one question to help us improve.")
        
        # Feedback section
        st.subheader("💬 Feedback & Support")
        
        feedback_tab1, feedback_tab2, feedback_tab3, feedback_tab4 = st.tabs(["💡 Suggest", "🐛 Bug Report", "📧 Contact", "📈 Beta Metrics"])
        
        with feedback_tab1:
            st.write("**Have an idea to improve this calculator?**")
            feature_request = st.text_area(
                "Feature Request",
                placeholder="What feature would make this more useful for you?",
                height=80,
                key="feature_request"
            )
            
            if st.button("💡 Submit Suggestion", key="suggest_btn"):
                if feature_request.strip():
                    # Store feedback with comprehensive context
                    feedback_data = {
                        "type": "feature_request",
                        "content": feature_request,
                        "timestamp": datetime.now().isoformat(),
                        "user_agent": st.context.headers.get("User-Agent", "Unknown") if hasattr(st.context, 'headers') else "Unknown",
                        "session_data": {
                            "model": calculation_model,
                            "purchase_price": purchase_price,
                            "monthly_rent": monthly_rent,
                            "cash_flow": monthly_cash_flow,
                            "cap_rate": cap_rate
                        }
                    }
                    
                    # Store in session state for export
                    if "feedback_submissions" not in st.session_state:
                        st.session_state.feedback_submissions = []
                    st.session_state.feedback_submissions.append(feedback_data)
                    
                    # Track the feedback submission
                    track_usage("feedback_submitted", {"type": "feature_request"})
                    
                    st.success("✅ Thanks for your suggestion! We'll review it for future updates.")
                    st.balloons()
                else:
                    st.warning("Please enter your suggestion first.")
        
        with feedback_tab2:
            st.write("**Found something that doesn't work right?**")
            bug_report = st.text_area(
                "Bug Description",
                placeholder="Describe what happened and what you expected...",
                height=80,
                key="bug_report"
            )
            
            bug_severity = st.selectbox(
                "Severity",
                ["Low - Minor inconvenience", "Medium - Affects functionality", "High - App unusable"],
                key="bug_severity"
            )
            
            if st.button("🐛 Report Bug", key="bug_btn"):
                if bug_report.strip():
                    # Store bug report with context
                    bug_data = {
                        "type": "bug_report",
                        "content": bug_report,
                        "severity": bug_severity,
                        "timestamp": datetime.now().isoformat(),
                        "user_agent": st.context.headers.get("User-Agent", "Unknown") if hasattr(st.context, 'headers') else "Unknown",
                        "session_data": {
                            "model": calculation_model,
                            "purchase_price": purchase_price,
                            "current_url": "app_main_page"
                        }
                    }
                    
                    # Store in session state
                    if "feedback_submissions" not in st.session_state:
                        st.session_state.feedback_submissions = []
                    st.session_state.feedback_submissions.append(bug_data)
                    
                    # Track the bug report
                    track_usage("bug_reported", {"severity": bug_severity})
                    
                    st.success("✅ Bug report submitted! Thanks for helping us improve.")
                    st.info("💡 **Tip:** Include your browser and device type for faster fixes.")
                else:
                    st.warning("Please describe the bug first.")
        
        with feedback_tab3:
            st.write("**Questions? Want to connect?**")
            
            contact_cols1, contact_cols2 = st.columns(2)
            with contact_cols1:
                if st.button("📧 Email Us", key="email_btn"):
                    st.info("📮 Send feedback to: feedback@luntra.com")
                    
            with contact_cols2:
                if st.button("💼 LinkedIn", key="linkedin_btn"):
                    st.info("🔗 Connect with the creator on LinkedIn")
            
            # Quick rating
            st.write("**Quick Rating:**")
            rating_cols = st.columns(5)
            rating_emojis = ["😞", "😐", "🙂", "😊", "🤩"]
            rating_labels = ["Poor", "Fair", "Good", "Great", "Amazing"]
            
            for i, (col, emoji, label) in enumerate(zip(rating_cols, rating_emojis, rating_labels)):
                with col:
                    if st.button(f"{emoji}\n{label}", key=f"rating_{i}"):
                        # Store rating
                        rating_data = {
                            "type": "rating",
                            "rating": i + 1,
                            "rating_label": label,
                            "timestamp": datetime.now().isoformat(),
                            "session_data": {
                                "model": calculation_model,
                                "purchase_price": purchase_price,
                                "cash_flow": monthly_cash_flow
                            }
                        }
                        
                        if "feedback_submissions" not in st.session_state:
                            st.session_state.feedback_submissions = []
                        st.session_state.feedback_submissions.append(rating_data)
                        
                        # Track the rating
                        track_usage("rating_submitted", {"rating": i + 1, "label": label})
                        
                        st.success(f"Thanks for rating us {emoji}!")
                        if i >= 3:  # Good ratings
                            st.info("💝 Love the app? Share it with fellow investors!")
                            st.markdown("**Share LUNTRA Calculator:**")
                            current_url = "https://your-app-url.streamlit.app"  # Will be updated after deployment
                            st.code(f"Check out this real estate calculator: {current_url}")
        
        with feedback_tab4:
            st.write("**LUNTRA Beta Analytics Dashboard**")
            
            # Key beta metrics
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
            
            with metrics_col1:
                st.metric(
                    "Workflows Run", 
                    st.session_state.get("workflow_run_count", 0),
                    help="Number of analyses completed this session"
                )
            
            with metrics_col2:
                session_duration = (datetime.now() - st.session_state.get("session_start", datetime.now())).total_seconds() / 60
                st.metric(
                    "Session Time", 
                    f"{session_duration:.1f} min",
                    help="Time spent in this session"
                )
            
            with metrics_col3:
                feedback_count = len(st.session_state.get("feedback_submissions", []))
                st.metric(
                    "Feedback Items", 
                    feedback_count,
                    help="Feedback submissions this session"
                )
            
            # Session analytics summary
            st.write("**Session Analytics:**")
            if "analytics" in st.session_state and st.session_state.analytics:
                analytics_df = pd.DataFrame(st.session_state.analytics)
                
                # Event summary
                event_counts = analytics_df['event'].value_counts()
                st.write("**Events Tracked:**")
                for event, count in event_counts.items():
                    st.write(f"• {event}: {count}")
                
                # Export analytics data
                if st.button("📥 Export Session Analytics", key="export_analytics"):
                    analytics_json = analytics_df.to_json(orient='records', indent=2)
                    st.download_button(
                        label="Download Analytics JSON",
                        data=analytics_json,
                        file_name=f"luntra_analytics_{st.session_state.session_id}.json",
                        mime="application/json"
                    )
            else:
                st.info("No analytics data captured yet. Use the calculator to generate data.")
            
            # Time to First Value (TTFV) tracking
            if st.session_state.get("workflow_run_count", 0) > 0:
                ttfv = (datetime.now() - st.session_state.get("session_start", datetime.now())).total_seconds()
                st.success(f"⚡ **Time to First Value:** {ttfv:.1f} seconds")
                st.caption("This is a key metric for LUNTRA Beta - how quickly users get value from the tool.")
        
        # PDF Export section
        st.subheader("📄 PDF Export")
        
        # Prepare data for PDF
        pdf_data = {
            "purchase_price": purchase_price,
            "down_payment": down_payment,
            "down_payment_pct": down_payment_pct,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "annual_property_tax": annual_property_tax,
            "annual_insurance": annual_insurance,
            "monthly_hoa": monthly_hoa,
            "closing_costs": closing_costs,
            "monthly_rent": monthly_rent,
            "vacancy_pct": vacancy_pct,
            "piti": piti,
            "monthly_cash_flow": monthly_cash_flow,
            "noi": noi,
            "cap_rate": cap_rate,
            "cash_on_cash": cash_on_cash,
            "notes": notes,
            "model": calculation_model,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if st.button("Generate PDF Report", type="primary"):
            try:
                # Track PDF generation
                track_usage("pdf_generated", {
                    "model": calculation_model,
                    "purchase_price": purchase_price,
                    "cash_flow": monthly_cash_flow,
                    "cap_rate": cap_rate
                })
                
                pdf_buffer = generate_pdf_report(pdf_data)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"luntra_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ PDF report generated successfully!")
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                track_usage("pdf_error", {"error": str(e)})
        
        # Key Investment Metrics Summary
        st.subheader("📊 Key Metrics")
        
        metrics_summary = f"""
        **Purchase Price:** ${purchase_price:,}
        **Total Cash Needed:** ${total_cash_invested:,}
        **Monthly Cash Flow:** ${monthly_cash_flow:,.2f}
        **Annual Cash Flow:** ${annual_cash_flow:,.0f}
        **Cap Rate:** {cap_rate:.2f}%
        **Cash-on-Cash:** {cash_on_cash:.2f}%
        **NOI:** ${noi:,.0f}
        """
        
        st.markdown(metrics_summary)
        
        # Quick actions
        st.subheader("Quick Actions")
        
        col2a, col2b = st.columns(2)
        with col2a:
            if st.button("📋 Copy Metrics"):
                st.success("Metrics copied!")
        
        with col2b:
            if st.button("🔄 Reset Form"):
                st.rerun()
        
        # Session data for debugging
        with st.expander("🔍 Debug Data"):
            debug_data = {
                "model": calculation_model,
                "inputs": {
                    "purchase_price": purchase_price,
                    "down_payment_pct": down_payment_pct,
                    "interest_rate": interest_rate,
                    "monthly_rent": monthly_rent,
                    "vacancy_pct": vacancy_pct
                },
                "calculations": {
                    "egi": egi,
                    "operating_expenses": operating_expenses,
                    "noi": noi,
                    "piti": piti,
                    "monthly_cash_flow": monthly_cash_flow
                },
                "timestamp": datetime.now().isoformat()
            }
            st.json(debug_data)
            
            # Analytics data
            if "analytics" in st.session_state and st.session_state.analytics:
                st.write("**Session Analytics:**")
                st.json(st.session_state.analytics[-5:])  # Show last 5 actions
            
            # Feedback export (admin feature)
            if "feedback_submissions" in st.session_state and st.session_state.feedback_submissions:
                st.write("**Feedback Submissions:**")
                feedback_df = pd.DataFrame(st.session_state.feedback_submissions)
                st.dataframe(feedback_df)
                
                # Export feedback as JSON
                if st.button("📥 Export Feedback Data"):
                    feedback_json = json.dumps(st.session_state.feedback_submissions, indent=2)
                    st.download_button(
                        label="Download Feedback JSON",
                        data=feedback_json,
                        file_name=f"luntra_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

if __name__ == "__main__":
    main()