import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib.parse import quote_plus

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #e50914;
        margin-bottom: 2rem;
    }
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .review-positive {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .review-negative {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .review-neutral {
        background-color: #e2e3e5;
        border-left: 4px solid #6c757d;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
    }
    .cast-card {
        text-align: center;
        padding: 10px;
        margin: 5px;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendations_data' not in st.session_state:
    st.session_state.recommendations_data = None
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'tmdb_api_key' not in st.session_state:
    st.session_state.tmdb_api_key = ""

@st.cache_data
def load_models():
    try:
        data = pd.read_csv('main_data.csv')
        
        try:
            nlp_model = pickle.load(open('nlp_model.pkl', 'rb'))
            vectorizer = pickle.load(open('tranform.pkl', 'rb'))
            return nlp_model, vectorizer, data
        except Exception as model_error:
            st.warning(f"Could not load sentiment analysis models: {str(model_error)}")
            st.info("The app will work without sentiment analysis. Only movie recommendations will be available.")
            return None, None, data
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error("Please make sure you have run 'python setup_files.py' first to copy the required files.")
        return None, None, None

@st.cache_data
def create_similarity_matrix(data):
    """Create cosine similarity matrix for movie recommendations"""
    try:
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(data['comb'])
        similarity = cosine_similarity(count_matrix)
        return similarity
    except Exception as e:
        st.error(f"Error creating similarity matrix: {str(e)}")
        return None

def get_movie_recommendations(movie_title, data, similarity):
    """Get movie recommendations based on similarity"""
    movie_title = movie_title.lower()
    
    if movie_title not in data['movie_title'].str.lower().values:
        return "Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"
    
    # Find the index of the movie
    idx = data[data['movie_title'].str.lower() == movie_title].index[0]
    
    # Get similarity scores
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get top 10 similar movies (excluding the movie itself)
    sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = data['movie_title'].iloc[movie_indices].tolist()
    
    return recommended_movies

def validate_api_key(api_key):
    if not api_key:
        return False, "API key is empty"
    if len(api_key) < 20:
        return False, "API key seems too short"
    if " " in api_key:
        return False, "API key contains spaces"
    return True, "Valid format"

def get_movie_details_from_tmdb(movie_title, api_key):
    is_valid, message = validate_api_key(api_key)
    if not is_valid:
        st.error(f"Invalid API key: {message}")
        return None, None
    
    try:
        encoded_title = quote_plus(movie_title)
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_title}"
        
        response = requests.get(search_url, timeout=10)
        
        if response.status_code == 401:
            st.error("Invalid API key. Please check your TMDb API key.")
            return None, None
        elif response.status_code == 429:
            st.error("API rate limit exceeded. Please wait a moment and try again.")
            return None, None
        elif response.status_code != 200:
            st.error(f"API error: HTTP {response.status_code}")
            return None, None
        
        search_results = response.json()
        if search_results['results']:
            movie_id = search_results['results'][0]['id']
            
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
            details_response = requests.get(details_url, timeout=10)
            
            if details_response.status_code == 200:
                movie_details = details_response.json()
                
                cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
                cast_response = requests.get(cast_url, timeout=10)
                cast_data = cast_response.json() if cast_response.status_code == 200 else {}
                
                return movie_details, cast_data
        
        st.warning(f"No movie found with title: {movie_title}")
        return None, None
        
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please check your internet connection and try again.")
        return None, None
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Please check your internet connection.")
        return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        st.info("Please check your internet connection and try again.")
        return None, None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None, None

def simple_sentiment_analysis(text):
    """Simple sentiment analysis using keyword matching"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'awesome', 'fantastic', 'wonderful', 'brilliant', 'perfect', 'outstanding', 'superb', 'magnificent', 'incredible', 'spectacular', 'marvelous', 'love', 'loved', 'like', 'enjoy', 'enjoyed', 'best', 'better', 'beautiful', 'stunning', 'impressive', 'remarkable', 'extraordinary']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'hated', 'boring', 'disappointing', 'poor', 'weak', 'stupid', 'ridiculous', 'pathetic', 'waste', 'sucks', 'sucked', 'disgusting', 'annoying', 'irritating', 'frustrating', 'mediocre', 'bland', 'dull', 'confusing']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'Positive'
    elif negative_count > positive_count:
        return 'Negative'
    else:
        return 'Neutral'

def get_movie_reviews(imdb_id, nlp_model, vectorizer):
    """Scrape and analyze movie reviews from IMDb"""
    try:
        url = f'https://www.imdb.com/title/{imdb_id}/reviews/?ref_=tt_ov_rt'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            review_elements = soup.find_all("div", {"class": "ipc-html-content-inner-div"})
            
            reviews_data = []
            for review_elem in review_elements[:10]:
                if review_elem.string:
                    review_text = review_elem.string
                    
                    try:
                        if nlp_model is not None and vectorizer is not None:
                            review_vector = vectorizer.transform([review_text])
                            sentiment_pred = nlp_model.predict(review_vector)[0]
                            sentiment = 'Positive' if sentiment_pred else 'Negative'
                        else:
                            sentiment = simple_sentiment_analysis(review_text)
                    except Exception:
                        sentiment = simple_sentiment_analysis(review_text)
                    
                    reviews_data.append({
                        'text': review_text,
                        'sentiment': sentiment
                    })
            
            return reviews_data
        
        return []
    except Exception as e:
        st.error(f"Error fetching reviews: {str(e)}")
        return []

def main():
    nlp_model, vectorizer, data = load_models()
    
    if data is None:
        st.error("Failed to load movie data. Please check if all files are present.")
        st.info("Make sure to run: `python setup_files.py` first to copy the required files.")
        return
    
    similarity = create_similarity_matrix(data)
    if similarity is None:
        return
    
    st.markdown('<h1 class="main-header">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
    
    sentiment_available = nlp_model is not None and vectorizer is not None
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "TMDb API Key", 
            value=st.session_state.tmdb_api_key,
            help="Get your API key from https://www.themoviedb.org/",
            key="api_key_input",
            type="password"
        )
        
        if api_key != st.session_state.tmdb_api_key:
            st.session_state.tmdb_api_key = api_key
        
        if st.session_state.tmdb_api_key:
            is_valid, message = validate_api_key(st.session_state.tmdb_api_key)
            if is_valid:
                st.success("✅ API Key saved!")
                
                if st.button("🔍 Test API Key"):
                    with st.spinner("Testing API key..."):
                        test_details, _ = get_movie_details_from_tmdb("Batman", st.session_state.tmdb_api_key)
                        if test_details:
                            st.success("🎉 API key works perfectly!")
                        else:
                            st.error("❌ API key test failed")
            else:
                st.warning(f"⚠️ {message}")
        else:
            st.warning("⚠️ Please enter your TMDb API Key")
        
        st.markdown("---")
        st.header("📋 Instructions")
        st.markdown("""
        1. Get a free API key from [TMDb](https://www.themoviedb.org/settings/api)
        2. Enter your TMDb API key above
        3. Search for a movie name from the dropdown
        4. Get recommendations and detailed information
        5. View cast information and sentiment analysis of reviews
        """)
        
        if not sentiment_available:
            st.warning("⚠️ Sentiment analysis unavailable due to model compatibility")
        
        st.markdown("---")
        st.header("📊 Dataset Info")
        if data is not None:
            st.metric("Total Movies", len(data))
            st.write("**Sample Movies:**")
            for movie in data['movie_title'].head(5):
                st.write(f"• {movie.title()}")
    
    st.header("🔍 Search Movies")
    
    movie_suggestions = sorted(data['movie_title'].str.title().tolist())
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_movie = st.selectbox(
            "Select or type a movie name:",
            options=[""] + movie_suggestions,
            format_func=lambda x: x if x else "Type to search...",
            key="movie_search"
        )
    
    with col2:
        search_button = st.button("🔍 Get Recommendations", type="primary")
    
    if search_button and selected_movie:
        if not st.session_state.tmdb_api_key:
            st.warning("Please enter your TMDb API key in the sidebar.")
            return
        
        with st.spinner("Finding similar movies..."):
            recommendations = get_movie_recommendations(selected_movie, data, similarity)
            
            if isinstance(recommendations, str):
                st.error(recommendations)
                return
            
            movie_details, cast_data = get_movie_details_from_tmdb(selected_movie, st.session_state.tmdb_api_key)
            
            if movie_details:
                st.session_state.recommendations_data = {
                    'movie_details': movie_details,
                    'cast_data': cast_data,
                    'recommendations': recommendations,
                    'selected_movie': selected_movie
                }
                st.success(f"Found {len(recommendations)} similar movies!")
            else:
                st.error("Could not fetch movie details from TMDb. Please check your API key and movie name.")
    
    if st.session_state.recommendations_data:
        display_movie_details(st.session_state.recommendations_data, nlp_model, vectorizer, st.session_state.tmdb_api_key, data, similarity)

def display_movie_details(data_dict, nlp_model, vectorizer, api_key, movie_data, similarity):
    """Display detailed movie information"""
    movie_details = data_dict['movie_details']
    cast_data = data_dict['cast_data']
    recommendations = data_dict['recommendations']
    
    st.markdown("---")
    st.header(f"🎬 {movie_details['title']}")
    
    # Movie overview section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if movie_details.get('poster_path'):
            poster_url = f"https://image.tmdb.org/t/p/w500{movie_details['poster_path']}"
            st.image(poster_url, width=300)
        else:
            st.info("No poster available")
    
    with col2:
        st.subheader("Movie Information")
        
        # Movie details
        if movie_details.get('overview'):
            st.write(f"**Overview:** {movie_details['overview']}")
        
        if movie_details.get('release_date'):
            st.write(f"**Release Date:** {movie_details['release_date']}")
        
        if movie_details.get('runtime'):
            hours = movie_details['runtime'] // 60
            minutes = movie_details['runtime'] % 60
            st.write(f"**Runtime:** {hours}h {minutes}m")
        
        if movie_details.get('vote_average'):
            st.write(f"**Rating:** ⭐ {movie_details['vote_average']}/10")
        
        if movie_details.get('vote_count'):
            st.write(f"**Vote Count:** {movie_details['vote_count']:,}")
        
        if movie_details.get('genres'):
            genres = [genre['name'] for genre in movie_details['genres']]
            st.write(f"**Genres:** {', '.join(genres)}")
    
    # Cast section
    if cast_data.get('cast'):
        st.subheader("🎭 Main Cast")
        
        cast_cols = st.columns(5)
        for i, actor in enumerate(cast_data['cast'][:5]):
            with cast_cols[i]:
                if actor.get('profile_path'):
                    profile_url = f"https://image.tmdb.org/t/p/w200{actor['profile_path']}"
                    st.image(profile_url, width=120)
                else:
                    st.write("No photo")
                
                st.write(f"**{actor['name']}**")
                st.write(f"*{actor['character']}*")
    
    # Reviews section
    if movie_details.get('imdb_id'):
        if nlp_model is not None and vectorizer is not None:
            st.subheader("📝 Movie Reviews & Sentiment Analysis")
            analysis_method = "Advanced ML Model"
        else:
            st.subheader("📝 Movie Reviews & Sentiment Analysis")
            analysis_method = "Keyword-Based Analysis"
            st.info("ℹ️ Using fallback sentiment analysis (keyword-based) as ML models are unavailable.")
        
        with st.spinner("Analyzing movie reviews..."):
            reviews = get_movie_reviews(movie_details['imdb_id'], nlp_model, vectorizer)
        
        if reviews:
            positive_reviews = sum(1 for r in reviews if r['sentiment'] == 'Positive')
            negative_reviews = sum(1 for r in reviews if r['sentiment'] == 'Negative')
            neutral_reviews = sum(1 for r in reviews if r['sentiment'] == 'Neutral')
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Reviews", len(reviews))
            if positive_reviews > 0:
                col2.metric("Positive", positive_reviews, delta=f"{positive_reviews/len(reviews)*100:.1f}%")
            if negative_reviews > 0:
                col3.metric("Negative", negative_reviews, delta=f"{negative_reviews/len(reviews)*100:.1f}%")
            if neutral_reviews > 0:
                col4.metric("Neutral", neutral_reviews)
            
            for i, review in enumerate(reviews, 1):
                if review['sentiment'] == 'Positive':
                    sentiment_class = "review-positive"
                    sentiment_emoji = "👤"
                elif review['sentiment'] == 'Negative':
                    sentiment_class = "review-negative"
                    sentiment_emoji = "👤"
                else:
                    sentiment_class = "review-neutral"
                    sentiment_emoji = "👤"
                
                st.markdown(f"""
                <div class="{sentiment_class}">
                    <strong>{sentiment_emoji} Person {i} - {review['sentiment']} Review</strong><br>
                    {review['text'][:300]}{'...' if len(review['text']) > 300 else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No reviews found for this movie.")
    
    # Recommendations section
    st.subheader("🎯 Similar Movies You Might Like")
    
    rec_cols = st.columns(5)
    for i, movie in enumerate(recommendations[:5]):
        with rec_cols[i]:
            # Try to get poster for recommended movie
            rec_details, _ = get_movie_details_from_tmdb(movie, api_key)
            
            if rec_details and rec_details.get('poster_path'):
                poster_url = f"https://image.tmdb.org/t/p/w200{rec_details['poster_path']}"
                st.image(poster_url, width=150)
            else:
                st.write("🎬")
            
            st.write(f"**{movie.title()}**")
            
            if st.button(f"View Details", key=f"rec_{i}"):
                # Update session state to show this movie's details
                with st.spinner("Loading movie details..."):
                    new_recommendations = get_movie_recommendations(movie, movie_data, similarity)
                    new_movie_details, new_cast_data = get_movie_details_from_tmdb(movie, api_key)
                    
                    if new_movie_details:
                        st.session_state.recommendations_data = {
                            'movie_details': new_movie_details,
                            'cast_data': new_cast_data,
                            'recommendations': new_recommendations,
                            'selected_movie': movie
                        }
                        st.rerun()
    
    # Show remaining recommendations in a list
    if len(recommendations) > 5:
        with st.expander("View More Recommendations"):
            for movie in recommendations[5:]:
                st.write(f"• {movie.title()}")

if __name__ == "__main__":
    main() 