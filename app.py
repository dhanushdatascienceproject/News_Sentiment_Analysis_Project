import streamlit as st
import requests
import json
import pandas as pd
import os
from streamlit.components.v1 import html

# Set page configuration
st.set_page_config(
    page_title="News Sentiment TTS",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_URL = "http://127.0.0.1:8000"

def get_companies():
    """Get list of sample companies from the API"""
    try:
        response = requests.get(f"{API_URL}/companies")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching companies: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return []

def analyze_company(company_name, num_articles=10):
    """Send request to the API to analyze a company"""
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"company_name": company_name, "num_articles": num_articles}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error analyzing company: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to the API: {e}")
        return None

def display_sentiment_distribution(sentiment_distribution):
    """Display sentiment distribution as a bar chart"""
    df = pd.DataFrame({
        'Sentiment': list(sentiment_distribution.keys()),
        'Count': list(sentiment_distribution.values())
    })
    
    # Set color based on sentiment
    colors = {
        'Positive': '#4CAF50',  # Green
        'Negative': '#F44336',  # Red
        'Neutral': '#2196F3'    # Blue
    }
    
    bar_colors = [colors[sentiment] for sentiment in df['Sentiment']]
    
    st.bar_chart(df.set_index('Sentiment'), color=['#4CAF50'])  # Use any default color


def display_results(results):
    """Display analysis results"""
    if not results:
        return
    
    st.title(f"News Analysis for {results['company']}")
    
    # Display final sentiment analysis
    st.subheader("Overall Sentiment")
    st.write(results['final_sentiment_analysis'])
    
    # Display sentiment distribution
    st.subheader("Sentiment Distribution")
    display_sentiment_distribution(results['comparative_sentiment_score']['sentiment_distribution'])
    
    # Display audio player
    st.subheader("Audio Summary (Hindi)")
    if results['audio_path']:
        try:
            # For local development, use the local file path
            audio_file = results['audio_path'].lstrip('/')  # Remove leading slash
            
            # Check if file exists
            if os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")
            else:
                # Try with API URL
                audio_url = f"{API_URL}{results['audio_path']}"
                st.warning(f"Audio file not found locally. Trying to fetch from API: {audio_url}")
                st.audio(audio_url, format="audio/mp3")
        except Exception as e:
            st.error(f"Error playing audio: {e}")
            st.write("You can find the audio file at: `{audio_file}`")
    else:
        st.warning("Audio summary not available")
    
    # Rest of the function remains the same...
    
    # Display comparative analysis
    st.subheader("Comparative Analysis")
    for comparison in results['comparative_sentiment_score']['coverage_differences']:
        st.write(f"**Comparison:** {comparison['comparison']}")
        st.write(f"**Impact:** {comparison['impact']}")
        st.write("---")
    
    # Display topic overlap
    st.subheader("Topic Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Common Topics:**")
        for topic in results['comparative_sentiment_score']['topic_overlap']['common_topics']:
            st.write(f"- {topic}")
    
    with col2:
        st.write("**Unique Topics:**")
        for topic in results['comparative_sentiment_score']['topic_overlap']['unique_topics']:
            st.write(f"- {topic}")
    
    # Display article details
    st.subheader("Article Details")
    for i, article in enumerate(results['articles']):
        with st.expander(f"Article {i+1}: {article['title']}"):
            st.write(f"**Summary:** {article['summary']}")
            st.write(f"**Sentiment:** {article['sentiment']}")
            st.write(f"**Topics:** {', '.join(article['topics'])}")
            st.write(f"**URL:** {article['url']}")

def main():
    """Main function to run the Streamlit app"""
    st.sidebar.title("News Sentiment Analysis")
    st.sidebar.write("This app extracts news articles about a company, performs sentiment analysis, and generates a summary in Hindi.")
    
    # Get company input
    company_options = get_companies()
    company_options.append("Other")
    
    selected_company = st.sidebar.selectbox("Select a company", company_options)
    
    if selected_company == "Other":
        custom_company = st.sidebar.text_input("Enter company name")
        if custom_company:
            company_name = custom_company
        else:
            company_name = None
    else:
        company_name = selected_company
    
    # Number of articles
   # Number of articles
    num_articles = st.sidebar.slider("Number of articles to analyze", min_value=5, max_value=20, value=10)
    
    # Run analysis button
    analyze_button = st.sidebar.button("Analyze News")
    
    # Add loading spinner
    if analyze_button and company_name:
        with st.spinner(f"Analyzing news for {company_name}..."):
            # Call API
            results = analyze_company(company_name, num_articles)
            
            # Display results
            if results:
                display_results(results)
                
                # Add option to download results as JSON
                st.sidebar.download_button(
                    label="Download Results (JSON)",
                    data=json.dumps(results, indent=2),
                    file_name=f"{company_name.lower().replace(' ', '_')}_analysis.json",
                    mime="application/json"
                )
    elif analyze_button:
        st.warning("Please select or enter a company name")
    else:
        # Display instructions
        st.title("News Sentiment Analysis")
        st.write("""
        ## Instructions
        
        1. Select a company from the dropdown or enter a custom company name
        2. Choose the number of articles to analyze
        3. Click "Analyze News" to start the analysis
        4. View the sentiment analysis results and listen to the Hindi summary
        
        This application extracts news articles related to the company, performs sentiment analysis, 
        and generates a text-to-speech summary in Hindi.
        """)
        
        st.image("https://raw.githubusercontent.com/streamlit/demo-self-driving/master/streamlit-logo-secondary-colormark-darktext.png", width=250)

if __name__ == "__main__":
    main()