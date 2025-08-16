import streamlit as st
import datetime
import pytz
from decimal import Decimal, getcontext

# Set precision for high-precision decimal calculations
getcontext().prec = 25

# Configure the Streamlit page
st.set_page_config(
    page_title="Appointment Time Checker",
    page_icon="🕒",
    layout="centered"
)

def get_pakistan_time():
    """Get current Pakistan Standard Time"""
    pakistan_tz = pytz.timezone('Asia/Karachi')
    return datetime.datetime.now(pakistan_tz)

def add_weeks_to_time(base_time, weeks_decimal):
    """Add decimal weeks to a datetime object with high precision"""
    # Convert weeks to seconds (1 week = 604800 seconds)
    weeks_precise = Decimal(str(weeks_decimal))
    seconds_to_add = weeks_precise * Decimal('604800')
    
    # Convert to float for timedelta (maintaining precision as much as possible)
    seconds_float = float(seconds_to_add)
    
    # Add the time delta
    future_time = base_time + datetime.timedelta(seconds=seconds_float)
    return future_time

def main():
    st.title("🕒 Appointment Time Checker")
    st.subheader("German Embassy Waiting List Calculator")
    st.markdown("---")
    
    # Display current Pakistan time
    current_pak_time = get_pakistan_time()
    st.info(f"**Current Pakistan Standard Time:** {current_pak_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Input section
    st.markdown("### Enter Number of Weeks (Floating Point from API Call)")
    
    weeks_input = st.text_input(
        "Weeks to add:",
        placeholder="Enter precise number of weeks (up to 20 decimal places)",
        help="Enter the exact number of weeks returned from the API call"
    )
    
    if weeks_input:
        try:
            # Validate and process input
            weeks_decimal = float(weeks_input)
            
            # Calculate future appointment time
            appointment_time = add_weeks_to_time(current_pak_time, weeks_decimal)
            
            # Display results
            st.markdown("---")
            st.success("**Calculated Appointment Time:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Date",
                    value=appointment_time.strftime('%Y-%m-%d')
                )
                
            with col2:
                st.metric(
                    label="Time (PST)",
                    value=appointment_time.strftime('%H:%M:%S')
                )
            
            # Full datetime display
            st.info(f"**Full Appointment DateTime:** {appointment_time.strftime('%A, %B %d, %Y at %H:%M:%S %Z')}")
            
            # Additional information
            st.markdown("### Calculation Details")
            days_total = weeks_decimal * 7
            st.write(f"• **Weeks added:** {weeks_decimal}")
            st.write(f"• **Days equivalent:** {days_total:.2f} days")
            st.write(f"• **Time difference:** {appointment_time - current_pak_time}")
            
            # Show in different formats
            with st.expander("📅 View in Different Formats"):
                st.write(f"**ISO Format:** {appointment_time.isoformat()}")
                st.write(f"**Unix Timestamp:** {appointment_time.timestamp()}")
                st.write(f"**Day of Week:** {appointment_time.strftime('%A')}")
                st.write(f"**Month:** {appointment_time.strftime('%B')}")
                
        except ValueError:
            st.error("⚠️ Please enter a valid number (floating point format)")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
    
    # Footer information
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    <p>German Embassy Appointment Calculator • Pakistan Standard Time (UTC+5)</p>
    <p>Enter the precise number of weeks from your API response for accurate appointment scheduling</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()