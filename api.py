from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from utils import NewsExtractor, SentimentAnalyzer, ComparativeAnalyzer, TextToSpeechConverter
import os

app = FastAPI(title="News Sentiment TTS API", 
              description="API for extracting, analyzing, and converting news articles to speech",
              version="1.0.0")


# Models for request/response
class CompanyRequest(BaseModel):
    company_name: str
    num_articles: int = 10

class ArticleResponse(BaseModel):
    title: str
    summary: str
    content: str
    url: str
    sentiment: str
    topics: list

class CompanyAnalysisResponse(BaseModel):
    company: str
    articles: list
    comparative_sentiment_score: dict
    final_sentiment_analysis: str
    audio_path: str

# Initialize the components
news_extractor = NewsExtractor()
sentiment_analyzer = SentimentAnalyzer()
comparative_analyzer = ComparativeAnalyzer()
tts_converter = TextToSpeechConverter()

# Create a directory for audio files if it doesn't exist
os.makedirs('static/audio', exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to the News Sentiment TTS API"}

@app.post("/analyze", response_model=dict)
async def analyze_company(request: CompanyRequest):
    """
    Analyze news articles for a company and generate sentiment analysis with TTS.
    
    Args:
        request (CompanyRequest): Company name and number of articles to analyze
    
    Returns:
        dict: Analysis results
    """
    try:
        # Extract news articles
        article_urls = news_extractor.search_news(request.company_name, request.num_articles)
        
        # Process each article
        processed_articles = []
        for url in article_urls:
            article = news_extractor.extract_article_content(url)
            
            # Analyze sentiment
            sentiment_result = sentiment_analyzer.analyze_sentiment(article['content'])
            
            # Generate summary
            summary = sentiment_analyzer.summarize_text(article['content'])
            
            # Extract topics
            topics = sentiment_analyzer.extract_topics(article['content'])
            
            processed_article = {
                'title': article['title'],
                'summary': summary,
                'content': article['content'],
                'url': article['url'],
                'sentiment': sentiment_result['category'],
                'topics': topics
            }
            
            processed_articles.append(processed_article)
        
        # Perform comparative analysis
        comparative_results = comparative_analyzer.perform_comparative_analysis(processed_articles)
        
        # Generate a detailed summary of all articles for TTS
        summary_text = f"Here is a detailed summary of all the news articles about {request.company_name}. "
        
        for i, article in enumerate(processed_articles):
            article_summary = f"Article {i + 1}: {article['summary']} The sentiment of this article is {article['sentiment']}. "
            summary_text += article_summary
        
        summary_text += f"Overall, the news about {request.company_name} is mostly {comparative_results['final_sentiment_analysis']}. "
        
        if comparative_results['topic_overlap']['common_topics']:
            summary_text += f"The main topics discussed across articles include {', '.join(comparative_results['topic_overlap']['common_topics'])}. "
        
        summary_text += "This is the overall summary of the news."
        
        # Generate TTS audio in Hindi
        audio_filename = f"{request.company_name.lower().replace(' ', '_')}_summary.mp3"
        audio_path = os.path.join('static/audio', audio_filename)
        tts_converter.generate_speech(summary_text, audio_path)
        
        # Prepare response
        response = {
            "company": request.company_name,
            "articles": processed_articles,
            "comparative_sentiment_score": comparative_results,
            "final_sentiment_analysis": comparative_results['final_sentiment_analysis'],
            "audio_path": f"/static/audio/{audio_filename}"
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/companies")
async def get_sample_companies():
    """
    Get a list of sample companies for testing.
    
    Returns:
        list: List of company names
    """
    return ["Apple", "Microsoft", "Google", "Amazon", "Tesla", "Facebook", "Netflix", "IBM", "Intel", "Oracle"]

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)