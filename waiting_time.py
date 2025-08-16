import streamlit as st
import datetime
import pytz
import json
from decimal import Decimal, getcontext

# Set precision for high-precision decimal calculations (maximum precision)
getcontext().prec = 50

# Configure the Streamlit page
st.set_page_config(
    page_title="German Embassy Visa Application Waiting List",
    page_icon="🇩🇪",
    layout="wide"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }
    
    /* Force light text on all elements */
    .stApp *, .stMarkdown *, div[data-testid="stMarkdownContainer"] *, .stSelectbox *, .stRadio *, .stTextInput *, .stNumberInput *, .stTextArea *, p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #f8fafc !important;
    }
    
    /* Main Header */
    .embassy-header {
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e293b 100%);
        color: #f8fafc;
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #334155;
        position: relative;
        overflow: hidden;
    }
    
    .embassy-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #fbbf24, #ef4444, #1f2937);
    }
    
    .embassy-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.1), transparent 50%);
        pointer-events: none;
    }
    
    .embassy-header h1 {
        color: #f8fafc !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        background: linear-gradient(135deg, #f8fafc, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .embassy-header h3 {
        color: #cbd5e1 !important;
        font-size: 1.3rem !important;
        font-weight: 400 !important;
        margin: 0.5rem 0 0 0 !important;
        opacity: 0.9;
    }
    
    /* Current Time Card */
    .time-display {
        background: linear-gradient(135deg, #1e293b, #334155, #475569);
        color: #f8fafc;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #475569;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    
    .time-display::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 70% 20%, rgba(59, 130, 246, 0.15), transparent 60%);
        pointer-events: none;
    }
    
    .time-display .time-label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .time-display .time-value {
        color: #f8fafc !important;
        font-weight: 500 !important;
        font-size: 1.2rem !important;
        margin-top: 0.5rem;
    }
    
    /* Instructions Card */
    .instructions-card {
        background: linear-gradient(135deg, #1e293b, #334155, #475569);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #64748b;
        position: relative;
        overflow: hidden;
    }
    
    .instructions-card::before {
        content: '📋';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.2;
    }
    
    .instructions-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8, #1e40af);
        border-radius: 20px 20px 0 0;
    }
    
    .instructions-card h4 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .instructions-card ol {
        color: #cbd5e1 !important;
    }
    
    .instructions-card li {
        color: #cbd5e1 !important;
        margin-bottom: 0.8rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
    }
    
    .instructions-card code {
        background: linear-gradient(135deg, #1e40af, #1e3a8a) !important;
        color: #ffffff !important;
        padding: 0.3rem 0.6rem !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #3b82f6 !important;
    }
    
    /* API Response Card */
    .api-response-card {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
        position: relative;
        overflow: hidden;
    }
    
    .api-response-card::after {
        content: '{ }';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        color: #475569;
        opacity: 0.3;
        font-family: 'Monaco', monospace;
    }
    
    .api-response-card h5 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .json-code {
        background: linear-gradient(135deg, #020617, #0f172a) !important;
        color: #a3e635 !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid #1e293b !important;
        box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.5) !important;
        position: relative;
    }
    
    .json-key {
        color: #60a5fa !important;
    }
    
    .json-value {
        color: #a3e635 !important;
    }
    
    .json-number {
        color: #f472b6 !important;
    }
    
    .json-boolean {
        color: #38bdf8 !important;
    }
    
    /* Input Section */
    .input-section {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #475569;
        position: relative;
        overflow: hidden;
    }
    
    .input-section::before {
        content: '🔢';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.1;
    }
    
    .input-section h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Waiting List Status Card */
    .waiting-status {
        background: linear-gradient(135deg, #451a03, #78350f, #92400e);
        border: 2px solid #d97706;
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(217, 119, 6, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .waiting-status::before {
        content: '⏳';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 5rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    .waiting-status::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 80%, rgba(245, 158, 11, 0.2), transparent 60%);
        pointer-events: none;
    }
    
    .waiting-status h3 {
        color: #fbbf24 !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .waiting-status p {
        color: #fde68a !important;
        line-height: 1.7 !important;
        font-weight: 400 !important;
        margin-bottom: 1rem !important;
    }
    
    .waiting-status h4 {
        color: #fbbf24 !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 0.5rem 0 !important;
    }
    
    .waiting-time {
        color: #fde68a !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Result Card */
    .result-notification {
        background: linear-gradient(135deg, #022c22, #064e3b, #047857);
        border: 2px solid #10b981;
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(16, 185, 129, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .result-notification::before {
        content: '📬';
        position: absolute;
        top: -5px;
        right: 15px;
        font-size: 3.5rem;
        opacity: 0.15;
    }
    
    .result-notification::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 80% 30%, rgba(16, 185, 129, 0.2), transparent 60%);
        pointer-events: none;
    }
    
    .result-notification h3 {
        color: #6ee7b7 !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        margin: 0 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #334155, #475569);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #64748b;
        margin: 0.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8, #1e40af);
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1), transparent 70%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
        border-color: #3b82f6;
    }
    
    .metric-card h4 {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        margin: 0.5rem 0 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    .metric-card h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        margin: 1rem 0 !important;
        font-size: 2rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    };
        margin: 0.5rem 0 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .metric-card h3 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 !important;
        font-size: 1.8rem !important;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #1e293b, #334155, #3b82f6);
        color: #f8fafc;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #60a5fa;
        position: relative;
        overflow: hidden;
    }
    
    .success-message::before {
        content: '🎯';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 2rem;
        opacity: 0.3;
    }
    
    .success-message strong {
        color: #f8fafc !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Footer */
    .footer-section {
        background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
        color: #e2e8f0;
        padding: 3rem;
        border-radius: 24px;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border: 1px solid #475569;
        position: relative;
        overflow: hidden;
    }
    
    .footer-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.05), transparent 70%);
        pointer-events: none;
    }
    
    .footer-section p {
        color: #cbd5e1 !important;
        margin: 0.8rem 0 !important;
    }
    
    .footer-section strong {
        color: #f8fafc !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Info Section */
    .info-section {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid #3b82f6;
        position: relative;
        overflow: hidden;
    }
    
    .info-section::before {
        content: '💡';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.2;
    }
    
    .info-section h3 {
        color: #60a5fa !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .info-section li {
        color: #cbd5e1 !important;
        margin-bottom: 0.8rem !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
    }
    
    .info-section strong {
        color: #f8fafc !important;
    }
    
    /* Streamlit Input Styling */
    .stSelectbox > div > div {
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }
    
    .stRadio > div {
        background-color: transparent !important;
    }
    
    .stRadio > div label {
        color: #f8fafc !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }
    
    /* Hide Streamlit elements 
    .stDeployButton {
        display: none;
    } */
    
    footer {
        visibility: hidden;
    }
    
    .stException {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
</style>
""", unsafe_allow_html=True)

def get_pakistan_time():
    """Get current Pakistan Standard Time"""
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.datetime.now(pakistan_tz)

def add_weeks_to_time(base_time, weeks_decimal):
    """Add decimal weeks to a datetime object with high precision"""
    weeks_precise = Decimal(str(weeks_decimal))
    seconds_to_add = weeks_precise * Decimal('604800')
    seconds_float = float(seconds_to_add)
    future_time = base_time + datetime.timedelta(seconds=seconds_float)
    return future_time

def estimate_months_range(weeks):
    """Convert weeks to month range estimation"""
    months = weeks / 4.33  # Average weeks per month
    lower_bound = max(1, int(months - 0.5))
    upper_bound = int(months + 1.5)
    return lower_bound, upper_bound

def main():
    # Header
    st.markdown("""
    <div class="embassy-header">
        <h1>🇩🇪 German Embassy - Visa Application Status</h1>
        <h3>Student Visa Waiting List Calculator</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Current time display
    current_pak_time = get_pakistan_time()
    st.markdown(f"""
    <div class="time-display">
        <div class="time-label">📍 Current Pakistan Standard Time</div>
        <div class="time-value">{current_pak_time.strftime('%A, %B %d, %Y at %I:%M:%S %p PST')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="instructions-card">
            <h4>📋 How to Use This Calculator</h4>
            <ol>
                <li>Open the German embassy visa application website</li>
                <li>Open browser Developer Tools (F12)</li>
                <li>Go to Network tab and refresh the page</li>
                <li>Look for the "limits" API call in the network requests</li>
                <li>Copy the <code>estimatedWaitingTime</code> value and paste it below</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="api-response-card">
            <h5>Expected API Response:</h5>
            <div class="json-code">
{<br>
&nbsp;&nbsp;<span class="json-key">"estimatedWaitingTime"</span>: <span class="json-number">8.232</span>,<br>
&nbsp;&nbsp;<span class="json-key">"waitingListActive"</span>: <span class="json-boolean">true</span>,<br>
&nbsp;&nbsp;<span class="json-key">"waitingListActiveCategories"</span>: []<br>
}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input section
    st.markdown("""
    <div class="input-section">
        <h3>🔢 Enter Waiting Time from API Response</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Two input options
    input_method = st.radio(
        "Choose input method:",
        ["Manual Input (estimatedWaitingTime only)", "Full JSON Response"],
        horizontal=True
    )
    
    weeks_input = None
    
    if input_method == "Manual Input (estimatedWaitingTime only)":
        weeks_input = st.number_input(
            "Enter estimated waiting time (weeks):",
            min_value=0.0,
            step=0.000000000000000001,  # Extremely small step for maximum precision
            format="%.20f",  # Display up to 20 decimal places
            help="Enter the exact 'estimatedWaitingTime' value from the API response (supports up to 20 decimal places)"
        )
        if weeks_input > 0:
            weeks_input = str(weeks_input)
    else:
        json_input = st.text_area(
            "Paste the complete JSON response:",
            placeholder='{\n    "estimatedWaitingTime": 8.232104121475054,\n    "waitingListActive": true,\n    "waitingListActiveCategories": []\n}',
            height=120
        )
        
        if json_input.strip():
            try:
                json_data = json.loads(json_input)
                if "estimatedWaitingTime" in json_data:
                    weeks_input = str(json_data["estimatedWaitingTime"])
                    st.success(f"✅ Extracted waiting time: {weeks_input} weeks")
                    if json_data.get("waitingListActive"):
                        st.info("📋 Waiting list is currently active")
                else:
                    st.error("❌ 'estimatedWaitingTime' not found in JSON")
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON format")
    
    # Process the calculation
    if weeks_input:
        try:
            weeks_decimal = float(weeks_input)
            
            if weeks_decimal > 0:
                # Calculate future appointment time
                appointment_time = add_weeks_to_time(current_pak_time, weeks_decimal)
                
                
                # Results display
                st.markdown("""
                <div class="result-notification">
                    <h3>📬 When You'll Be Notified</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📅 Date</h4>
                        <h3>{appointment_time.strftime('%d %b %Y')}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🕐 Time</h4>
                        <h3>{appointment_time.strftime('%I:%M:%S %p')}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📆 Day</h4>
                        <h3>{appointment_time.strftime('%A')}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    days_remaining = (appointment_time - current_pak_time).days
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>⏰ Days Left</h4>
                        <h3>{days_remaining}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Full datetime display
                st.markdown(f"""
                <div class="success-message">
                    <strong>🎯 Complete Notification Time:</strong> {appointment_time.strftime('%A, %B %d, %Y at %I:%M:%S %p PST')}
                </div>
                """, unsafe_allow_html=True)
                
                # Additional details in expandable section
                with st.expander("🔍 Detailed Calculation Information"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**⏱️ Time Breakdown:**")
                        st.write(f"• Exact weeks: {weeks_decimal:.20f}")
                        st.write(f"• Equivalent days: {weeks_decimal * 7:.15f}")
                        st.write(f"• Equivalent hours: {weeks_decimal * 168:.10f}")
                        st.write(f"• Time difference: {appointment_time - current_pak_time}")
                    
                    with col2:
                        st.write("**📋 Technical Details:**")
                        st.write(f"• ISO Format: {appointment_time.isoformat()}")
                        st.write(f"• Unix Timestamp: {int(appointment_time.timestamp())}")
                        st.write(f"• Week of Year: Week {appointment_time.isocalendar()[1]}")
                        st.write(f"• Quarter: Q{((appointment_time.month-1)//3)+1} {appointment_time.year}")
                
                # Important Information
                st.markdown("""
                <div class="info-section">
                    <h3>💡 Important Information</h3>
                    <ul>
                        <li><strong>Email Notification:</strong> You'll receive an email when it's your turn to submit the application</li>
                        <li><strong>Application Window:</strong> Once notified, you'll have a limited time to complete your submission</li>
                        <li><strong>Document Preparation:</strong> Use this waiting time to prepare all required documents</li>
                        <li><strong>Status Updates:</strong> Check the official embassy website regularly for any updates</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.warning("⚠️ Waiting time must be greater than 0")
                
        except ValueError:
            st.error("⚠️ Please enter a valid number")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
    
    # Footer
    st.markdown("""
    <div class="footer-section">
        <p><strong>🇩🇪 German Embassy Visa Application Calculator</strong></p>
        <p>Pakistan Standard Time (UTC+5) • For Student Visa Applications</p>
        <p><em>This tool helps you track when you'll be able to submit your visa application based on the official waiting list API data.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()