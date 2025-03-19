import os
import re
import json
import requests
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from langdetect import detect
from googletrans import Translator
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import nltk
nltk.download('punkt')


# Download NLTK resources
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class NewsExtractor:
    """Class for extracting news articles about a company."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def search_news(self, company_name, num_articles=10):
        """
        Search for news articles about the given company.
        
        Args:
            company_name (str): The name of the company
            num_articles (int): Number of articles to return
            
        Returns:
            list: List of article URLs
        """
        # Using a search engine API or creating a custom Google search
        # For this example, we'll use a dummy search URL
        search_urls = [
            f"https://news.google.com/search?q={company_name}",
            f"https://www.reuters.com/search/news?blob={company_name}",
            f"https://www.bbc.co.uk/search?q={company_name}&filter=news"
        ]
        
        article_urls = []
        
        for search_url in search_urls:
            try:
                response = requests.get(search_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract article URLs (this would need to be adapted based on the actual website structure)
                    links = soup.find_all('a', href=True)
                    for link in links:
                        # Filter for news article links
                        href = link['href']
                        if any(term in href.lower() for term in ['article', 'news', 'story']):
                            # Ensure it's a complete URL
                            if not href.startswith('http'):
                                base_url = '/'.join(search_url.split('/')[:3])
                                href = f"{base_url}{href if href.startswith('/') else '/' + href}"
                            
                            if href not in article_urls:
                                article_urls.append(href)
                                if len(article_urls) >= num_articles:
                                    break
            except Exception as e:
                print(f"Error fetching search results from {search_url}: {e}")
        
        # For demonstration, if we couldn't find enough real articles, we'll add some dummy URLs
        if len(article_urls) < num_articles:
            for i in range(len(article_urls), num_articles):
                article_urls.append(f"https://example.com/news/{company_name.lower()}-article-{i}")
        
        return article_urls[:num_articles]
    
    def extract_article_content(self, url):
        """
        Extract content from a news article URL.
        
        Args:
            url (str): URL of the news article
            
        Returns:
            dict: Dictionary containing title, content, and other metadata
        """
        try:
            # For real implementation, fetch the actual article content
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract title
                title = soup.find('title')
                title = title.text if title else "No title found"
                
                # Extract content (adapt this based on the website structure)
                content_elements = soup.find_all(['p', 'article', 'div.content', 'div.article-body'])
                content = ' '.join([element.text for element in content_elements])
                
                # Clean up content
                content = re.sub(r'\s+', ' ', content).strip()
                
                # Metadata
                published_date = self._extract_date(soup)
                author = self._extract_author(soup)
                
                return {
                    'title': title,
                    'content': content,
                    'url': url,
                    'published_date': published_date,
                    'author': author
                }
            else:
                print(f"Failed to fetch article content from {url}. Status code: {response.status_code}")
                # Return dummy data for demonstration
                return self._generate_dummy_article(url)
                
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            # Return dummy data for demonstration
            return self._generate_dummy_article(url)
    
    def _extract_date(self, soup):
        """Extract the publication date from the article."""
        date_elements = soup.find_all(['time', 'meta[property="article:published_time"]', 'span.date'])
        for element in date_elements:
            if element.get('datetime'):
                return element.get('datetime')
            elif element.get('content'):
                return element.get('content')
            elif element.text:
                return element.text.strip()
        return "Date not found"
    
    def _extract_author(self, soup):
        """Extract the author from the article."""
        author_elements = soup.find_all(['meta[name="author"]', 'a.author', 'span.author'])
        for element in author_elements:
            if element.get('content'):
                return element.get('content')
            elif element.text:
                return element.text.strip()
        return "Author not found"
    
    def _generate_dummy_article(self, url):
        """Generate dummy article data for demonstration purposes."""
        company_name = url.split('/')[-1].split('-')[0]
        article_num = url.split('-')[-1]
        
        dummy_contents = [
            {
                'title': f"{company_name.capitalize()} Reports Strong Q3 Earnings",
                'content': f"{company_name.capitalize()} announced impressive third-quarter results, surpassing analyst expectations. The company reported a 15% increase in revenue and a 22% boost in net profit compared to the same period last year. CEO Jane Smith attributed the success to expansion in Asian markets and the launch of new product lines. Analysts remain optimistic about the company's future performance.",
                'sentiment': 'positive'
            },
            {
                'title': f"Regulatory Challenges Facing {company_name.capitalize()}",
                'content': f"{company_name.capitalize()} is facing increasing scrutiny from regulators regarding its data privacy practices. The company has been given 30 days to respond to concerns raised by the Federal Trade Commission. This comes after multiple consumer complaints about data handling. The company's stock dropped 3% following the news.",
                'sentiment': 'negative'
            },
            {
                'title': f"{company_name.capitalize()} Announces New Partnership",
                'content': f"{company_name.capitalize()} has entered into a strategic partnership with XYZ Corp to develop next-generation technologies. The collaboration aims to combine {company_name}'s expertise in AI with XYZ's hardware capabilities. Industry experts view this as a neutral development that could potentially lead to new product offerings in the coming years.",
                'sentiment': 'neutral'
            },
            {
                'title': f"{company_name.capitalize()} Expands Global Footprint",
                'content': f"{company_name.capitalize()} has announced the opening of new offices in Singapore and Berlin as part of its global expansion strategy. The company plans to hire over 500 employees across these locations by the end of the year. This move is expected to strengthen the company's presence in European and Asian markets.",
                'sentiment': 'positive'
            },
            {
                'title': f"Investors Concerned About {company_name.capitalize()}'s Growth Strategy",
                'content': f"Following the annual shareholder meeting, investors have expressed concerns about {company_name.capitalize()}'s long-term growth strategy. Critics point to the company's slowing innovation pipeline and increasing competition in the market. The board has promised to address these concerns in the upcoming strategic review.",
                'sentiment': 'negative'
            }
        ]
        
        # Select a dummy content based on the article number
        dummy_idx = int(article_num) % len(dummy_contents)
        dummy = dummy_contents[dummy_idx]
        
        return {
            'title': dummy['title'],
            'content': dummy['content'],
            'url': url,
            'published_date': '2023-11-15',
            'author': 'John Doe'
        }


class SentimentAnalyzer:
    """Class for performing sentiment analysis on news articles."""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.translator = Translator()
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=100)
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of the given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment scores and category
        """
        # Detect language and translate if not English
        try:
            lang = detect(text[:100])
            if lang != 'en':
                text = self.translator.translate(text, dest='en').text
        except Exception as e:
            print(f"Error in language detection/translation: {e}")
        
        # Perform sentiment analysis
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Determine sentiment category
        if sentiment_scores['compound'] >= 0.05:
            category = 'Positive'
        elif sentiment_scores['compound'] <= -0.05:
            category = 'Negative'
        else:
            category = 'Neutral'
        
        return {
            'scores': sentiment_scores,
            'category': category
        }
    
    def summarize_text(self, text, max_length=150):
        """
        Generate a summary of the given text.
        
        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of the summary
            
        Returns:
            str: Summarized text
        """
        # Limit input text to prevent errors with large inputs
        text = text[:1024]
        
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Error in summarization: {e}")
            # Fallback to a simple summary if model fails
            sentences = nltk.sent_tokenize(text)
            return ' '.join(sentences[:3])
    
    def extract_topics(self, text):
        """
        Extract key topics from the given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: List of key topics
        """
        try:
            # Tokenize and remove stopwords
            tokens = nltk.word_tokenize(text.lower())
            stopwords = set(nltk.corpus.stopwords.words('english'))
            tokens = [token for token in tokens if token.isalpha() and token not in stopwords]
            
            # Get word frequencies
            word_freq = Counter(tokens)
            
            # Get the top 5 words
            top_words = word_freq.most_common(5)
            
            # Map these to general topics
            topics = self._map_to_topics([word for word, _ in top_words])
            
            return topics
        except Exception as e:
            print(f"Error extracting topics: {e}")
            return ["General News"]
    
    def _map_to_topics(self, words):
        """Map words to general topics."""
        topic_mapping = {
            'finance': ['revenue', 'profit', 'earnings', 'market', 'stock', 'investment', 'financial'],
            'technology': ['tech', 'innovation', 'software', 'hardware', 'digital', 'ai', 'data'],
            'regulation': ['law', 'regulation', 'compliance', 'legal', 'policy', 'government'],
            'expansion': ['growth', 'expansion', 'global', 'international', 'market'],
            'product': ['product', 'launch', 'release', 'feature', 'development'],
            'leadership': ['ceo', 'executive', 'leadership', 'management', 'board'],
            'sustainability': ['environment', 'sustainable', 'green', 'renewable', 'climate']
        }
        
        detected_topics = set()
        for word in words:
            for topic, related_words in topic_mapping.items():
                if word in related_words or any(word in related_word for related_word in related_words):
                    detected_topics.add(topic.capitalize())
        
        # If no specific topics found, add a general one
        if not detected_topics:
            detected_topics.add("General News")
            
        return list(detected_topics)


class ComparativeAnalyzer:
    """Class for performing comparative analysis across articles."""
    
    def __init__(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
    
    def perform_comparative_analysis(self, articles):
        """
        Perform comparative analysis across multiple articles.
        
        Args:
            articles (list): List of article dictionaries with sentiment analysis
            
        Returns:
            dict: Comparative analysis results
        """
        # Count sentiment distribution
        sentiment_count = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        for article in articles:
            sentiment_count[article['sentiment']] += 1
        
        # Analyze content similarity
        article_texts = [article['content'] for article in articles]
        
        # Create coverage differences comparisons
        coverage_differences = []
        
        # Compare articles with different sentiments
        positive_articles = [a for a in articles if a['sentiment'] == 'Positive']
        negative_articles = [a for a in articles if a['sentiment'] == 'Negative']
        neutral_articles = [a for a in articles if a['sentiment'] == 'Neutral']
        
        # Compare positive vs negative articles
        if positive_articles and negative_articles:
            positive_topics = set(sum([a['topics'] for a in positive_articles], []))
            negative_topics = set(sum([a['topics'] for a in negative_articles], []))
            
            coverage_differences.append({
                'comparison': f"Positive articles focus on {', '.join(positive_topics)}, while negative articles discuss {', '.join(negative_topics)}.",
                'impact': "The contrast in coverage highlights the company's areas of strength and challenges."
            })
        
        # Analyze topic overlap
        all_topics = [topic for article in articles for topic in article['topics']]
        topic_counter = Counter(all_topics)
        common_topics = [topic for topic, count in topic_counter.items() if count > 1]
        unique_topics = [topic for topic, count in topic_counter.items() if count == 1]
        
        # For each article, find unique topics
        article_unique_topics = {}
        for i, article in enumerate(articles):
            article_unique_topics[f"Article {i+1}"] = [
                topic for topic in article['topics'] 
                if sum(1 for a in articles if topic in a['topics']) == 1
            ]
        
        # Overall sentiment analysis
        dominant_sentiment = max(sentiment_count, key=sentiment_count.get)
        total_articles = len(articles)
        sentiment_percentage = (sentiment_count[dominant_sentiment] / total_articles) * 100
        
        if dominant_sentiment == 'Positive':
            final_sentiment = f"Overall sentiment is positive ({sentiment_percentage:.1f}% of articles), suggesting favorable news coverage."
        elif dominant_sentiment == 'Negative':
            final_sentiment = f"Overall sentiment is negative ({sentiment_percentage:.1f}% of articles), indicating potential challenges or issues."
        else:
            final_sentiment = f"Overall sentiment is neutral ({sentiment_percentage:.1f}% of articles), suggesting balanced news coverage."
        
        # Add more comparisons based on topics
        if len(common_topics) > 0:
            coverage_differences.append({
                'comparison': f"Common topics across articles include {', '.join(common_topics)}.",
                'impact': "These represent key areas of focus in the company's news coverage."
            })
        
        if len(unique_topics) > 0:
            coverage_differences.append({
                'comparison': f"Several unique topics appear in only one article each.",
                'impact': "These represent niche or emerging areas of interest for the company."
            })
        
        # Prepare the final results
        result = {
            'sentiment_distribution': sentiment_count,
            'coverage_differences': coverage_differences,
            'topic_overlap': {
                'common_topics': common_topics,
                'unique_topics': unique_topics,
                'article_unique_topics': article_unique_topics
            },
            'final_sentiment_analysis': final_sentiment
        }
        
        return result
import os
from googletrans import Translator
from gtts import gTTS
import nltk

class TextToSpeechConverter:
    """Class for converting text to speech in Hindi and generating summaries."""
    
    def __init__(self):
        self.translator = Translator()
        try:
            from gtts import gTTS
            self.tts_engine = gTTS
            self.tts_available = True
        except ImportError:
            print("Warning: gTTS not available. Install it using 'pip install gtts'.")
            self.tts_available = False
    
    def translate_to_hindi(self, text):
        """
        Translate text to Hindi.
        
        Args:
            text (str): Text to translate
            
        Returns:
            str: Translated text
        """
        try:
            hindi_text = self.translator.translate(text, dest='hi').text
            return hindi_text
        except Exception as e:
            print(f"Error translating to Hindi: {e}")
            return text  # Return original text if translation fails
    
    def generate_speech(self, text, output_file='output.mp3'):
        """
        Generate speech from text in Hindi using gTTS.
        
        Args:
            text (str): Text to convert to speech
            output_file (str): Path to save the audio file
            
        Returns:
            str: Path to the generated audio file
        """
        hindi_text = self.translate_to_hindi(text)
        
        if self.tts_available:
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                # Generate and save the audio file
                tts = self.tts_engine(text=hindi_text, lang='hi')
                tts.save(output_file)
                return output_file
            except Exception as e:
                print(f"Error generating speech: {e}")
                return None
        else:
            print("TTS engine not available. Would generate speech here.")
            return output_file
    
    def create_hindi_summary(self, company_name, articles):
        """
        Create a natural-sounding Hindi summary of all articles.
        
        Args:
            company_name (str): Name of the company
            articles (list): List of article dictionaries with content and sentiment
            
        Returns:
            str: Hindi summary text
        """
        english_summary = self._create_combined_summary(company_name, articles)
        hindi_summary = self.translate_to_hindi(english_summary)
        return hindi_summary
    
    def _create_combined_summary(self, company_name, articles):
        """
        Create a combined summary of all articles in English.
        
        Args:
            company_name (str): Name of the company
            articles (list): List of article dictionaries with content and sentiment
            
        Returns:
            str: Combined summary text
        """
        summary = f"Here is a simple summary of all the news articles about {company_name}. "
        
        for i, article in enumerate(articles):
            article_summary = self._summarize_article(article)
            summary += f"Article {i + 1}: {article_summary} "
        
        summary += "This is the overall summary of the news about {company_name}."
        return summary
    
    def _summarize_article(self, article):
        """
        Summarize a single article in simple terms.
        
        Args:
            article (dict): Article dictionary with content and sentiment
            
        Returns:
            str: Simple summary of the article
        """
        content = article.get('content', '')
        sentiment = article.get('sentiment', 'Neutral')
        
        # Extract the first few sentences as a simple summary
        sentences = nltk.sent_tokenize(content)
        simple_summary = ' '.join(sentences[:3])  # Use the first 3 sentences
        
        # Add sentiment context
        if sentiment == 'Positive':
            sentiment_context = "This article has a positive tone. "
        elif sentiment == 'Negative':
            sentiment_context = "This article has a negative tone. "
        else:
            sentiment_context = "This article has a neutral tone. "
        
        return f"{sentiment_context} {simple_summary}"

# Example usage
if __name__ == "__main__":
    converter = TextToSpeechConverter()
    
    # Example articles
    articles = [
        {
            'content': "TechCorp announced record profits this quarter, driven by strong sales in Asian markets. The company's revenue grew by 15%, exceeding analyst expectations. CEO Jane Smith praised the team for their hard work and innovation.",
            'sentiment': 'Positive'
        },
        {
            'content': "Regulators are investigating TechCorp for potential data privacy violations. The company has been accused of mishandling user data, leading to concerns among consumers. TechCorp's stock price dropped by 5% following the news.",
            'sentiment': 'Negative'
        },
        {
            'content': "TechCorp has partnered with XYZ Corp to develop new AI-powered products. The collaboration aims to combine TechCorp's expertise in software with XYZ's hardware capabilities. Industry experts believe this could lead to groundbreaking innovations.",
            'sentiment': 'Neutral'
        }
    ]
    
    # Generate a Hindi summary
    hindi_summary = converter.create_hindi_summary("TechCorp", articles)
    print("Hindi Summary:", hindi_summary)
    
    # Convert the summary to speech
    output_file = os.path.abspath("summary.mp3")  # Use absolute path
    output_file = converter.generate_speech(hindi_summary, output_file=output_file)
    if output_file:
        print(f"Speech saved to {output_file}")