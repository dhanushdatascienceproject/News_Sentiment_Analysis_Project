WEBSITE LINK: https://huggingface.co/spaces/Dhanu9945/frontend_news_sentiment

HUGGING FACE STREAMLIT LINK:https://huggingface.co/spaces/Dhanu9945/frontend_news_sentiment

HUGGINGFACE FACE FASTAPI LINK:https://huggingface.co/spaces/Dhanu9945/fastapi-backend

# News Summarization and Text-to-Speech Application

This web application extracts news articles about a specified company, performs sentiment analysis, conducts comparative analysis, and generates a text-to-speech output in Hindi. The tool allows users to input a company name and receive a structured sentiment report along with an audio output.

## Features

- **News Extraction**: Extracts title, summary, and metadata from news articles related to the given company using BeautifulSoup
- **Sentiment Analysis**: Performs sentiment analysis on article content (positive, negative, neutral)
- **Comparative Analysis**: Conducts comparative sentiment analysis across articles to derive insights
- **Text-to-Speech**: Converts summarized content into Hindi speech
- **User Interface**: Simple web-based interface using Streamlit
- **API Development**: Communication between frontend and backend via FastAPI

## Project Structure

```
news_sentiment_tts/
│
├── app.py                  # Main Streamlit application
├── api.py                  # API endpoints
├── utils.py                # Utility functions
├── requirements.txt        # Project dependencies
├── README.md               # Documentation
├── models/                 # Directory for saved models
│   └── __init__.py
├── .gitignore              # Git ignore file
└── tests/                  # Test files
    └── __init__.py
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-sentiment-tts.git
   cd news-sentiment-tts
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required NLTK data:
   ```bash
   python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Running the Application

### Starting the API server

1. Start the FastAPI server:
   ```bash
   python api.py
   ```
   This will start the API server at http://127.0.0.1:8000

2. You can access the API documentation at http://127.0.0.1:8000/docs

### Starting the Streamlit Application

1. In a new terminal window, start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   This will start the Streamlit app and automatically open it in your default web browser.

## API Endpoints

- `GET /` - Welcome message
- `GET /companies` - List of sample companies for testing
- `POST /analyze` - Analyze news articles for a company and generate sentiment analysis with TTS
  - Request body: `{"company_name": "Tesla", "num_articles": 10}`

## Models Used

- **Sentiment Analysis**: NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Summarization**: Hugging Face's BART model (facebook/bart-large-cnn)
- **Topic Extraction**: TF-IDF and frequency-based extraction
- **Translation**: Google Translate API via googletrans
- **Text-to-Speech**: indic-tts library for Hindi TTS conversion

## API Usage

### Using the API with Postman:

1. Open Postman and create a new POST request to `http://127.0.0.1:8000/analyze`
2. Set the request body to JSON and input:
   ```json
   {
     "company_name": "Tesla",
     "num_articles": 10
   }
   ```
3. Send the request and view the response

### API Response Format:

```json
{
  "company": "Tesla",
  "articles": [
    {
      "title": "Tesla's New Model Breaks Sales Records",
      "summary": "Tesla's latest EV sees record sales in Q3...",
      "content": "Full article content...",
      "url": "https://example.com/article1",
      "sentiment": "Positive",
      "topics": ["Electric Vehicles", "Stock Market", "Innovation"]
    },
    ...
  ],
  "comparative_sentiment_score": {
    "sentiment_distribution": {
      "Positive": 5,
      "Negative": 3,
      "Neutral": 2
    },
    "coverage_differences": [
      {
        "comparison": "Positive articles focus on Electric Vehicles, Innovation, while negative articles discuss Regulations, Autonomous Vehicles.",
        "impact": "The contrast in coverage highlights the company's areas of strength and challenges."
      }
    ],
    "topic_overlap": {
      "common_topics": ["Electric Vehicles"],
      "unique_topics": ["Stock Market", "Innovation", "Regulations", "Autonomous Vehicles"]
    }
  },
  "final_sentiment_analysis": "Overall sentiment is positive (50.0% of articles), suggesting favorable news coverage.",
  "audio_path": "/static/audio/tesla_summary.mp3"
}
```

## Assumptions & Limitations

- **News Extraction**: The application assumes availability of non-JS weblinks that can be scraped using BeautifulSoup. In some cases, dynamic websites with heavy JavaScript may not be properly scraped.
- **Sentiment Analysis**: VADER is used for sentiment analysis, which works well for general news content but may miss nuances in financial reporting.
- **TTS Quality**: The quality of Hindi TTS depends on the indic-tts library, which may have some pronunciation limitations.
- **News Sources**: The application uses direct scraping of public news sources, which might be rate-limited or blocked by some sites.
- **Article Limit**: For performance reasons, analysis is limited to a maximum of 20 articles.

## Deployment

The application can be deployed on Hugging Face Spaces:

1. Create a new Hugging Face Space with Streamlit SDK
2. Upload the code to the GitHub repository linked to the Space
3. Add the requirements.txt file for dependencies
4. Configure the build to run both the API and Streamlit app

## Future Improvements

- Implement more sophisticated NLP techniques for better summarization
- Add support for more languages in text-to-speech
- Enhance the UI with interactive visualizations
- Add caching mechanisms for faster analysis of frequently searched companies
- Implement more comprehensive error handling and recovery

## License

This project is licensed under the MIT License - see the LICENSE file for details.
