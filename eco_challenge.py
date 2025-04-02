"""
Eco-Challenge module for the Carbon Footprint Calculator
Allows users to commit to specific carbon reduction challenges and share their commitments
on social media platforms.
"""

import streamlit as st
import base64
from urllib.parse import quote

def generate_share_url(platform, message, url=None):
    """
    Generate sharing URLs for different social media platforms
    
    Parameters:
    - platform: Social media platform (twitter, linkedin, facebook, email)
    - message: Message to share
    - url: URL to include in the share (optional)
    
    Returns:
    - URL for sharing on the specified platform
    """
    encoded_message = quote(message)
    
    if platform == "twitter":
        return f"https://twitter.com/intent/tweet?text={encoded_message}"
    elif platform == "linkedin":
        return f"https://www.linkedin.com/sharing/share-offsite/?url={quote(url) if url else ''}&summary={encoded_message}"
    elif platform == "facebook":
        return f"https://www.facebook.com/sharer/sharer.php?u={quote(url) if url else ''}&quote={encoded_message}"
    elif platform == "email":
        subject = quote("My Carbon Reduction Commitment")
        return f"mailto:?subject={subject}&body={encoded_message}"
    return "#"

def get_challenge_icon(challenge_type):
    """
    Return an appropriate emoji icon for each challenge type
    
    Parameters:
    - challenge_type: Type of challenge
    
    Returns:
    - Emoji icon for the challenge type
    """
    icons = {
        "Energy": "⚡",
        "Transportation": "🚗",
        "Waste": "♻️",
        "Food": "🥗",
        "Purchasing": "🛍️",
        "Water": "💧",
        "Community": "👪"
    }
    return icons.get(challenge_type, "🌱")

def generate_challenge_message(name, organization, challenge_type, challenge_description, 
                               emissions_reduced, timeframe):
    """
    Generate a message for sharing on social media
    
    Parameters:
    - name: User's name
    - organization: Organization name
    - challenge_type: Type of challenge
    - challenge_description: Description of the challenge
    - emissions_reduced: Estimated emissions to be reduced
    - timeframe: Timeframe for the challenge
    
    Returns:
    - Formatted message for social media sharing
    """
    icon = get_challenge_icon(challenge_type)
    
    # Format the message
    message = f"I just committed to the {icon} {challenge_type} Eco-Challenge!\n\n"
    
    if organization:
        message += f"At {organization}, "
    else:
        message += "I "
        
    message += f"commit to: {challenge_description}\n\n"
    
    if emissions_reduced:
        message += f"This will help reduce approximately {emissions_reduced:.2f} tonnes CO₂e "
        if timeframe:
            message += f"over {timeframe}.\n\n"
        else:
            message += "annually.\n\n"
    
    message += "Join me in taking climate action! Calculate your carbon footprint and make your own commitment."
    
    return message

def generate_challenge_image(name, challenge_type, challenge_description):
    """
    This function would generate a shareable image with the challenge details
    For this implementation, we'll return a placeholder function that could be expanded later
    """
    # In a full implementation, this would use Pillow or another library to generate an image
    return None

def display_eco_challenge_tab():
    """
    Display the Eco-Challenge tab content
    """
    st.header("Eco-Challenge: Commit to Climate Action")
    
    st.markdown("""
    Make a public commitment to reduce your carbon footprint! 
    Select a challenge below, customize it, and share it on social media to inspire others.
    """)
    
    # Challenge selection
    st.subheader("1. Select Your Challenge")
    
    challenge_type = st.selectbox(
        "Challenge Category",
        ["Energy", "Transportation", "Waste", "Food", "Purchasing", "Water", "Community"]
    )
    
    # Challenge options based on type
    if challenge_type == "Energy":
        challenge_options = [
            "Switch to 100% renewable energy",
            "Reduce energy consumption by 20%",
            "Install smart thermostats and energy-efficient lighting",
            "Conduct an energy audit and implement recommendations",
            "Other (custom)"
        ]
    elif challenge_type == "Transportation":
        challenge_options = [
            "Commute by public transit, cycling, or walking",
            "Transition to an electric or hybrid vehicle",
            "Implement a car-free day each week",
            "Reduce business air travel by 50%",
            "Other (custom)"
        ]
    elif challenge_type == "Waste":
        challenge_options = [
            "Achieve zero waste to landfill",
            "Implement comprehensive recycling program",
            "Eliminate single-use plastics",
            "Compost all food and organic waste",
            "Other (custom)"
        ]
    elif challenge_type == "Food":
        challenge_options = [
            "Adopt a plant-based diet 3+ days per week",
            "Source food locally to reduce transportation emissions",
            "Reduce food waste by 50%",
            "Choose organic and regenerative food options",
            "Other (custom)"
        ]
    elif challenge_type == "Purchasing":
        challenge_options = [
            "Implement sustainable procurement policies",
            "Choose products with lower carbon footprints",
            "Extend product lifecycles through repair and reuse",
            "Support carbon-neutral companies and products",
            "Other (custom)"
        ]
    elif challenge_type == "Water":
        challenge_options = [
            "Reduce water consumption by 25%",
            "Install water-efficient fixtures and appliances",
            "Harvest rainwater for irrigation",
            "Address water leaks and inefficiencies",
            "Other (custom)"
        ]
    elif challenge_type == "Community":
        challenge_options = [
            "Organize a community climate action event",
            "Volunteer with environmental organizations",
            "Advocate for climate policies with local representatives",
            "Start a sustainability initiative at work or school",
            "Other (custom)"
        ]
    
    selected_challenge = st.selectbox("Select Challenge", challenge_options)
    
    if selected_challenge == "Other (custom)":
        custom_challenge = st.text_area("Describe your custom challenge", height=100)
        challenge_description = custom_challenge
    else:
        challenge_description = selected_challenge
    
    # Challenge details
    st.subheader("2. Customize Your Commitment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name")
        organization = st.text_input("Organization (optional)")
    
    with col2:
        timeframe_options = ["1 month", "3 months", "6 months", "1 year", "Ongoing"]
        timeframe = st.selectbox("Commitment Timeframe", timeframe_options)
        emissions_reduced = st.number_input("Estimated Emissions Reduction (tonnes CO₂e)", 
                                          min_value=0.0, value=1.0, step=0.1)
    
    # Preview commitment
    st.subheader("3. Preview Your Commitment")
    
    if challenge_description:
        preview_message = generate_challenge_message(
            name, organization, challenge_type, challenge_description, 
            emissions_reduced, timeframe
        )
        
        with st.expander("Preview", expanded=True):
            st.markdown(f"**Your Eco-Challenge Commitment:**")
            st.markdown(preview_message)
    
    # Share options
    st.subheader("4. Share Your Commitment")
    
    if not challenge_description or not name:
        st.warning("Please complete your challenge details and name to enable sharing options.")
    else:
        share_message = generate_challenge_message(
            name, organization, challenge_type, challenge_description, 
            emissions_reduced, timeframe
        )
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            twitter_url = generate_share_url("twitter", share_message)
            st.markdown(f"<a href='{twitter_url}' target='_blank' class='share-button twitter-button'>Twitter</a>", unsafe_allow_html=True)
        
        with col2:
            linkedin_url = generate_share_url("linkedin", share_message)
            st.markdown(f"<a href='{linkedin_url}' target='_blank' class='share-button linkedin-button'>LinkedIn</a>", unsafe_allow_html=True)
        
        with col3:
            facebook_url = generate_share_url("facebook", share_message)
            st.markdown(f"<a href='{facebook_url}' target='_blank' class='share-button facebook-button'>Facebook</a>", unsafe_allow_html=True)
        
        with col4:
            email_url = generate_share_url("email", share_message)
            st.markdown(f"<a href='{email_url}' target='_blank' class='share-button email-button'>Email</a>", unsafe_allow_html=True)
        
        # Copy to clipboard option
        st.markdown("### Copy to Clipboard")
        st.text_area("", share_message, height=150)
        
        # Display eco-challenge badge or certificate (placeholder for future enhancement)
        st.markdown("---")
        st.markdown("### Your Eco-Challenge Badge")
        
        # Simple badge display
        badge_html = f"""
        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center; max-width: 400px; margin: 0 auto;">
            <div style="font-size: 48px; margin-bottom: 10px;">{get_challenge_icon(challenge_type)}</div>
            <h3 style="margin: 5px 0;">{challenge_type} Eco-Challenge</h3>
            <p style="font-style: italic; margin: 5px 0;">Committed by: {name}</p>
            <p style="margin: 10px 0;">"{challenge_description}"</p>
            <p style="margin: 5px 0; font-size: 0.9em;">Reducing approximately {emissions_reduced:.2f} tonnes CO₂e</p>
            <p style="margin: 5px 0; font-size: 0.9em;">Timeframe: {timeframe}</p>
            <div style="background-color: #4CAF50; color: white; padding: 5px; margin-top: 15px; border-radius: 5px;">
                Climate Action Champion
            </div>
        </div>
        """
        st.markdown(badge_html, unsafe_allow_html=True)

def add_eco_challenge_css():
    """
    Add CSS for the Eco-Challenge tab
    """
    st.markdown("""
    <style>
    .share-button {
        display: inline-block;
        padding: 8px 16px;
        color: white;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 5px;
        margin: 5px 0;
        width: 100%;
    }
    .twitter-button {
        background-color: #1DA1F2;
    }
    .linkedin-button {
        background-color: #0077B5;
    }
    .facebook-button {
        background-color: #4267B2;
    }
    .email-button {
        background-color: #D44638;
    }
    .share-button:hover {
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)