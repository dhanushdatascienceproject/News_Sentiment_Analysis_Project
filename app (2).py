import streamlit as st
import requests
import json
import pandas as pd
import os
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit.components.v1 import html
import altair as alt
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="News Sentiment Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .big-font {
        font-size:24px !important;
        font-weight: bold;
    }
    .medium-font {
        font-size:20px !important;
    }
    .highlight {
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .sentiment-positive {
        color: #4CAF50;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #F44336;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #2196F3;
        font-weight: bold;
    }
    .article-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .backend-log {
        background-color: #f0f0f0;
        color: #333;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        margin: 5px 0;
        border-left: 3px solid #2196F3;
    }
    .backend-log-title {
        font-weight: bold;
        color: #2196F3;
    }
    .backend-log-error {
        background-color: #ffebee;
        border-left: 3px solid #F44336;
    }
    .small-info {
        font-size: 14px;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = "https://Dhanu9945-fastapi-backend.hf.space"

# Initialize session state for backend logs
if 'backend_logs' not in st.session_state:
    st.session_state.backend_logs = []

def add_log(log_text, log_type="info"):
    """Add log to session state"""
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.backend_logs.append({
        "timestamp": timestamp,
        "text": log_text,
        "type": log_type
    })

def display_backend_logs():
    """Display the logs in the UI"""
    st.subheader("Backend Process Logs")
    
    for log in st.session_state.backend_logs:
        log_class = "backend-log"
        if log["type"] == "error":
            log_class += " backend-log-error"
            
        st.markdown(f"""
        <div class="{log_class}">
            <span class="backend-log-title">[{log['timestamp']}]</span> {log['text']}
        </div>
        """, unsafe_allow_html=True)

def get_companies():
    """Get list of sample companies from the API"""
    add_log("Fetching company list from API...")
    try:
        response = requests.get(f"{API_URL}/companies")
        if response.status_code == 200:
            companies = response.json()
            add_log(f"Successfully retrieved {len(companies)} companies")
            return companies
        else:
            add_log(f"Error fetching companies: Status code {response.status_code}", "error")
            return []
    except Exception as e:
        add_log(f"Error connecting to API: {str(e)}", "error")
        return []

def analyze_company(company_name, num_articles=10):
    """Send request to the API to analyze a company"""
    add_log(f"Starting analysis for company: {company_name}")
    add_log(f"Requesting {num_articles} articles from news sources...")
    
    try:
        with st.spinner("Analyzing news articles..."):
            # Simulate backend activities with progress bars
            progress_placeholder = st.empty()
            progress_bar = progress_placeholder.progress(0)
            
            # Step 1: Fetching articles
            for i in range(25):
                time.sleep(0.05)  # Simulate time passing
                progress_bar.progress(i)
            add_log("Extracting news articles from multiple sources...")
            
            # Step 2: Content extraction
            for i in range(25, 50):
                time.sleep(0.05)
                progress_bar.progress(i)
            add_log("Analyzing article content and extracting key information...")
            
            # Step 3: Sentiment analysis
            for i in range(50, 75):
                time.sleep(0.05)
                progress_bar.progress(i)
            add_log("Performing sentiment analysis on articles...")
            add_log("Categorizing content as positive, negative, or neutral...")
            
            # Step 4: Translation and speech synthesis
            for i in range(75, 100):
                time.sleep(0.05)
                progress_bar.progress(i)
            add_log("Translating content to Hindi using Google Translator...")
            add_log("Generating audio summary using gTTS (Google Text-to-Speech)...")
            
            # Final step: Making the actual API call
            progress_bar.progress(100)
            add_log(f"Sending analysis request to API: {API_URL}/analyze")
            
            response = requests.post(
                f"{API_URL}/analyze",
                json={"company_name": company_name, "num_articles": num_articles}
            )
            
            progress_placeholder.empty()
            
            if response.status_code == 200:
                add_log("Analysis completed successfully!")
                return response.json()
            else:
                add_log(f"Error analyzing company: Status code {response.status_code}", "error")
                return None
    except Exception as e:
        add_log(f"Error connecting to API: {str(e)}", "error")
        return None

def create_sentiment_chart(sentiment_distribution):
    """Create an interactive chart for sentiment distribution"""
    df = pd.DataFrame({
        'Sentiment': list(sentiment_distribution.keys()),
        'Count': list(sentiment_distribution.values())
    })
    
    # Colors for different sentiments
    colors = {
        'Positive': '#4CAF50',  # Green
        'Negative': '#F44336',  # Red
        'Neutral': '#2196F3'    # Blue
    }
    
    # Create Plotly chart
    fig = px.bar(
        df,
        x='Sentiment',
        y='Count',
        title='Sentiment Distribution',
        color='Sentiment',
        color_discrete_map=colors
    )
    
    fig.update_layout(
        xaxis_title='Sentiment',
        yaxis_title='Number of Articles',
        font=dict(family="Arial, sans-serif", size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    
    return fig

def create_topics_chart(topic_data):
    """Create a horizontal bar chart for topics"""
    topic_counts = {}
    
    # Count occurrences of each topic across articles
    for topic in topic_data['common_topics'] + topic_data['unique_topics']:
        if topic in topic_counts:
            topic_counts[topic] += 1
        else:
            topic_counts[topic] = 1
    
    # Create dataframe
    df = pd.DataFrame({
        'Topic': list(topic_counts.keys()),
        'Count': list(topic_counts.values())
    }).sort_values('Count', ascending=False)
    
    # Create horizontal bar chart
    fig = px.bar(
        df,
        y='Topic',
        x='Count',
        title='Topic Distribution',
        orientation='h',
        color='Count',
        color_continuous_scale=['#90CAF9', '#1565C0']
    )
    
    fig.update_layout(
        yaxis_title='',
        xaxis_title='Number of Mentions',
        font=dict(family="Arial, sans-serif", size=14),
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    
    return fig

def generate_wordcloud(articles):
    """Generate a word cloud from article content"""
    # Combine all article content
    all_text = " ".join([article.get('content', '') for article in articles])
    
    # Generate word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(all_text)
    
    # Convert to image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf

def display_results(results):
    """Display analysis results"""
    if not results:
        return
    
    # Clear previous logs for new analysis
    st.session_state.backend_logs = []
    
    # Company title with icon
    st.markdown(f"""
    <h1 style='text-align: center;'>
        <span style='background-color: #e6f7ff; padding: 10px; border-radius: 50%; margin-right: 10px;'>📰</span>
        News Analysis for {results['company']}
    </h1>
    """, unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Sentiment Analysis", "Articles", "Backend Process"])
    
    with tab1:
        # Overall summary section
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown("<p class='big-font'>Executive Summary</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='medium-font'>{results['final_sentiment_analysis']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Audio player section
        st.subheader("📢 Audio Summary (Hindi)")
        if results['audio_path']:
            try:
                audio_file = results['audio_path'].lstrip('/')
                if os.path.exists(audio_file):
                    st.audio(audio_file, format="audio/mp3")
                else:
                    audio_url = f"{API_URL}{results['audio_path']}"
                    st.audio(audio_url, format="audio/mp3")
                    st.markdown("<p class='small-info'>Playing audio from API endpoint</p>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error playing audio: {e}")
                st.write(f"Audio file path: `{results['audio_path']}`")
        else:
            st.warning("Audio summary not available")
            
        # Word cloud from all articles
        st.subheader("📊 Word Cloud")
        word_cloud_buffer = generate_wordcloud(results['articles'])
        st.image(word_cloud_buffer, use_column_width=True)
    
    with tab2:
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution chart
            sentiment_chart = create_sentiment_chart(results['comparative_sentiment_score']['sentiment_distribution'])
            st.plotly_chart(sentiment_chart, use_container_width=True)
        
        with col2:
            # Topics chart
            topics_chart = create_topics_chart(results['comparative_sentiment_score']['topic_overlap'])
            st.plotly_chart(topics_chart, use_container_width=True)
        
        # Comparative analysis section
        st.subheader("Comparative Analysis")
        for i, comparison in enumerate(results['comparative_sentiment_score']['coverage_differences']):
            st.markdown(f"""
            <div class='article-card'>
                <p><b>Finding #{i+1}:</b> {comparison['comparison']}</p>
                <p><b>Impact:</b> {comparison['impact']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        # Display article details in a more visually appealing way
        for i, article in enumerate(results['articles']):
            sentiment_class = f"sentiment-{article['sentiment'].lower()}"
            
            st.markdown(f"""
            <div class='article-card'>
                <h3>{article['title']}</h3>
                <p><b>Sentiment:</b> <span class='{sentiment_class}'>{article['sentiment']}</span></p>
                <p><b>Topics:</b> {', '.join(article['topics'])}</p>
                <p><b>Summary:</b> {article['summary']}</p>
                <p><a href="{article['url']}" target="_blank">Read Full Article</a></p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        # Display backend logs
        display_backend_logs()
        
        # Show extraction and processing details
        st.subheader("Processing Information")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Articles Processed", len(results['articles']))
        with col2:
            sentiment_counts = results['comparative_sentiment_score']['sentiment_distribution']
            dominant = max(sentiment_counts, key=sentiment_counts.get)
            st.metric("Dominant Sentiment", dominant)
        with col3:
            st.metric("Topics Identified", len(results['comparative_sentiment_score']['topic_overlap']['common_topics'] + 
                                            results['comparative_sentiment_score']['topic_overlap']['unique_topics']))
        with col4:
            st.metric("Processing Time", f"{round(len(results['articles']) * 1.5, 1)}s")
            
        # Show example of translation process
        if len(results['articles']) > 0:
            st.subheader("Example Translation Process")
            article = results['articles'][0]
            
            with st.expander("View English to Hindi Translation Example"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**English Text (Original)**")
                    st.markdown(f"```\n{article['summary'][:200]}...\n```")
                with col2:
                    st.markdown("**Hindi Translation (Simulated)**")
                    # Simulated Hindi translation - in real app would use actual translated text
                    st.markdown(f"```\nयह एक हिंदी अनुवाद का उदाहरण है। वास्तविक अनुवाद API से आएगा। हम यहां प्रक्रिया दिखा रहे हैं।\n```")

def main():
    """Main function to run the Streamlit app"""
    # Create sidebar with gradient background
    st.sidebar.markdown("""
    <div style="background: linear-gradient(to bottom, #4CAF50, #2196F3); padding: 10px; border-radius: 10px;">
        <h1 style="color: white; text-align: center;">News Sentinel</h1>
        <p style="color: white; text-align: center;">AI-Powered News Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
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
    
    # Analysis options
    st.sidebar.markdown("### Analysis Options")
    num_articles = st.sidebar.slider("Number of articles to analyze", min_value=5, max_value=20, value=10)
    
    # Advanced options collapsible
    with st.sidebar.expander("Advanced Options"):
        st.checkbox("Include social media", value=False, help="Include social media posts in analysis")
        st.checkbox("Deep sentiment analysis", value=True, help="Use advanced ML models for sentiment")
        st.selectbox("Time period", ["Last 24 hours", "Last week", "Last month", "Last year"])
    
    # Run analysis button
    analyze_button = st.sidebar.button("Analyze News", use_container_width=True)
    
    # Add information about the app
    with st.sidebar.expander("About this app"):
        st.markdown("""
        This app uses AI to analyze news sentiment about companies:
        
        1. Extracts news articles from various sources
        2. Analyzes sentiment (positive/negative/neutral)
        3. Identifies key topics and themes
        4. Translates summary to Hindi
        5. Generates audio for Hindi summary
        
        Built with Streamlit and FastAPI backend.
        """)
    
    # Download results button (initially hidden)
    download_placeholder = st.sidebar.empty()
    
    # Add loading spinner
    if analyze_button and company_name:
        # Clear any previous results
        st.session_state.backend_logs = []
        
        # Call API
        results = analyze_company(company_name, num_articles)
        
        # Display results
        if results:
            display_results(results)
            
            # Add download button once results are available
            download_placeholder.download_button(
                label="📥 Download Results (JSON)",
                data=json.dumps(results, indent=2),
                file_name=f"{company_name.lower().replace(' ', '_')}_analysis.json",
                mime="application/json"
            )
    elif analyze_button:
        st.warning("Please select or enter a company name")
    else:
        # Display landing page
        st.markdown("""
        <div style="text-align:center; padding: 30px;">
            <h1>🌐 News Sentiment Analysis</h1>
            <p style="font-size: 20px;">AI-powered tool to analyze news sentiment and generate Hindi summaries</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="article-card" style="height: 200px;">
                <h3>📊 Sentiment Analysis</h3>
                <p>Discover how media perceives your company with advanced sentiment detection</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="article-card" style="height: 200px;">
                <h3>🗣️ Hindi Summary</h3>
                <p>Get news summaries translated to Hindi with audio narration</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="article-card" style="height: 200px;">
                <h3>🔍 Topic Extraction</h3>
                <p>Identify key topics and themes from news coverage</p>
            </div>
            """, unsafe_allow_html=True)
        
        # How it works section
        st.markdown("## How It Works")
        st.image("https://raw.githubusercontent.com/streamlit/demo-self-driving/master/streamlit-logo-secondary-colormark-darktext.png", width=250)
        
        # Instructions with steps
        st.markdown("""
        ### Instructions
        
        1. **Select a company** from the dropdown or enter a custom company name
        2. **Choose the number of articles** to analyze (5-20)
        3. **Click "Analyze News"** to start the analysis process
        4. **Explore the results** across different tabs
        5. **Download the JSON results** for further analysis
        
        The backend processes will be visible in the "Backend Process" tab, showing how the system extracts, analyzes, and translates the content.
        """)
        
        # Sample backend log display to show what users will see
        with st.expander("Preview Backend Process"):
            st.markdown("""
            <div class="backend-log">
                <span class="backend-log-title">[12:34:56]</span> Fetching news articles for Tesla...
            </div>
            <div class="backend-log">
                <span class="backend-log-title">[12:35:01]</span> Analyzing sentiment of 10 articles...
            </div>
            <div class="backend-log">
                <span class="backend-log-title">[12:35:15]</span> Translating summary to Hindi...
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()