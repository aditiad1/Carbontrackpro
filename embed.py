"""
Embeddable version of the Carbon Footprint Calculator
This script creates an HTML/JavaScript version that can be embedded in third-party websites
"""
import streamlit as st
import json
import base64

def main():
    st.title("Carbon Footprint Calculator - Embed Generator")
    st.write("Use this page to generate embed code for the Carbon Footprint Calculator that can be placed on any website.")
    
    # Configuration Options
    st.subheader("Configuration Options")
    
    with st.expander("Display Options", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input("Width (px)", min_value=400, max_value=1200, value=800)
            theme = st.selectbox("Theme", ["light", "dark"])
        with col2:
            height = st.number_input("Height (px)", min_value=600, max_value=2000, value=1000)
            show_branding = st.checkbox("Show Branding", value=True)
    
    # Generate the embed code
    app_url = st.text_input("Your App URL (REQUIRED - enter your Replit app URL)", 
                           placeholder="https://your-app-name.replit.app")
    if not app_url:
        st.warning("Please enter your Replit app URL. It should look something like 'https://your-app-name.replit.app'")
    
    # The iframe embed code
    iframe_code = f"""<iframe 
    src="{app_url}?embed=true&theme={theme}&showBranding={'true' if show_branding else 'false'}" 
    width="{width}" 
    height="{height}" 
    style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
    allow="camera; microphone; autoplay; encrypted-media; fullscreen; geolocation"
    frameborder="0"
    scrolling="auto"
></iframe>"""
    
    # Alternative JavaScript embed method
    js_code = f"""<div id="carbon-footprint-calculator"></div>
<script>
    (function() {{
        var iframe = document.createElement('iframe');
        iframe.src = "{app_url}?embed=true&theme={theme}&showBranding={'true' if show_branding else 'false'}";
        iframe.width = "{width}";
        iframe.height = "{height}";
        iframe.style = "border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);";
        iframe.allow = "camera; microphone; autoplay; encrypted-media; fullscreen; geolocation";
        iframe.frameBorder = "0";
        iframe.scrolling = "auto";
        
        document.getElementById('carbon-footprint-calculator').appendChild(iframe);
    }})();
</script>"""
    
    # Display the embed codes
    st.subheader("Embed Codes")
    
    with st.expander("HTML iFrame Embed Code", expanded=True):
        st.code(iframe_code, language="html")
    
    with st.expander("JavaScript Embed Code"):
        st.code(js_code, language="javascript")
    
    st.markdown("---")
    
    # Preview
    st.subheader("Preview")
    st.write("This is how your embedded calculator will appear:")
    
    # Display a live preview with an actual iframe
    if st.checkbox("Show live preview (may take a moment to load)", value=False):
        st.components.html(
            f"""
            <iframe 
                src="{app_url}?embed=true&theme={theme}&showBranding={'true' if show_branding else 'false'}" 
                width="{width}" 
                height="{height}" 
                style="border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
                frameborder="0"
                scrolling="auto"
            ></iframe>
            """,
            height=height+50,
            width=width+20,
        )
    else:
        # Display a mock preview
        st.markdown(f"""
        <div style="width: {width}px; height: {height}px; border: 1px solid #ddd; border-radius: 8px; 
        background-color: {'#f9f9f9' if theme == 'light' else '#333'};
        color: {'#333' if theme == 'light' else '#f9f9f9'};
        display: flex; align-items: center; justify-content: center; font-family: sans-serif;">
        <div style="text-align: center;">
            <h3>Carbon Footprint Calculator</h3>
            <p>This is a preview of how the embedded calculator will appear.</p>
            <p>The actual embedded version will be fully functional.</p>
            {('<div style="margin-top: 20px; font-size: 12px;">Powered by Your Company</div>' if show_branding else '')}
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instructions
    with st.expander("Implementation Instructions", expanded=True):
        st.markdown("""
        ### How to embed this calculator on your website
        
        1. **Enter your Replit app URL above** - This is crucial! The URL should be the full address where your app is hosted, like "https://your-app-name.replit.app"
        2. **Choose your preferred embed method** - iFrame (simplest) or JavaScript (more flexible)
        3. **Copy the generated code** from above
        4. **Paste the code** into your website's HTML where you want the calculator to appear
        
        #### Troubleshooting
        
        - **If the embed doesn't work:** Make sure your Replit app is deployed and publicly accessible
        - **For security issues:** Some websites block iframes by default. You may need to adjust your website's Content Security Policy (CSP)
        - **For cross-origin issues:** Ensure your Replit app allows cross-origin requests (this should be automatic)
        
        #### WordPress Instructions
        
        If you're using WordPress:
        1. Go to the page where you want to add the calculator
        2. Switch to the "Text" or "HTML" editor mode (not Visual)
        3. Paste the embed code
        4. Save/Update your page
        
        #### Additional Notes
        
        - Make sure your Replit app is **running** when you want to embed it
        - You may need to adjust the width and height based on your website's layout
        - For responsive designs, you might want to set width to 100% instead of a fixed pixel value
        """)

if __name__ == "__main__":
    main()