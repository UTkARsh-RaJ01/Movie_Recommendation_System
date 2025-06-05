# 🎬 Movie Recommendation System - Streamlit Version

A modern, interactive movie recommendation system built with Streamlit that provides personalized movie suggestions based on content similarity and performs sentiment analysis on movie reviews.

## ✨ Features

- **Movie Search**: Search from a database of movies with auto-complete functionality
- **Content-Based Recommendations**: Get similar movies based on plot, cast, director, and genres
- **Movie Details**: Comprehensive movie information including poster, cast, ratings, and overview
- **Sentiment Analysis**: Analyze IMDb reviews and classify them as positive or negative
- **Interactive UI**: Clean, modern interface with responsive design
- **TMDb Integration**: Real-time movie data and posters from The Movie Database

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- TMDb API key (free registration required)

### Installation Steps

1. **Clone or Download the Repository**
   ```bash
   # If you have git installed
   git clone <repository-url>
   cd MOVIERECOMMENDER_SYSTEM
   
   # Or download and extract the ZIP file
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

3. **Setup Data Files**
   ```bash
   python setup_files.py
   ```
   This will copy the necessary model files and dataset to the root directory.

4. **Get TMDb API Key**
   - Go to [TMDb website](https://www.themoviedb.org/)
   - Create a free account
   - Navigate to Settings → API
   - Copy your API key

5. **Run the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Access the App**
   - Open your browser and go to `http://localhost:8501`
   - Enter your TMDb API key in the sidebar
   - Start searching for movies!

## 📋 Required Files

After running `setup_files.py`, these files should be in your root directory:

- `main_data.csv` - Movie dataset with features for recommendations
- `nlp_model.pkl` - Pre-trained sentiment analysis model
- `tranform.pkl` - Text vectorizer for sentiment analysis

## 🎯 How to Use

1. **Enter API Key**: Add your TMDb API key in the sidebar
2. **Search Movies**: Select a movie from the dropdown or type to search
3. **Get Recommendations**: Click "Get Recommendations" to find similar movies
4. **Explore Details**: View movie information, cast, and reviews
5. **Navigate**: Click on recommended movies to explore further

## 📊 What's Different from Flask Version

### ✅ Improvements
- **No Server Setup**: Runs directly with `streamlit run`
- **Interactive UI**: Better user experience with real-time updates
- **Auto-complete Search**: Easy movie selection with searchable dropdown
- **Responsive Design**: Works well on different screen sizes
- **Session Management**: Maintains state without complex session handling
- **Error Handling**: Better error messages and user guidance

### 🔄 Changes Made
- **Framework**: Flask → Streamlit
- **Frontend**: HTML/CSS/JS → Streamlit components
- **AJAX Calls**: Replaced with Streamlit's reactive programming
- **File Structure**: Simplified with single main file
- **Dependencies**: Updated to modern package versions

## 📦 Package Requirements

```txt
streamlit==1.28.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
beautifulsoup4>=4.10.0
requests>=2.25.0
lxml>=4.6.0
pickle-mixin>=1.0.2
```

## 🔧 Configuration

### TMDb API Setup
1. Visit [TMDb API Documentation](https://developers.themoviedb.org/3)
2. Register for a free account
3. Request an API key
4. Copy the key and paste it in the sidebar of the app

### Environment Variables (Optional)
You can set your API key as an environment variable:
```bash
export TMDB_API_KEY="your_api_key_here"
```

## 🐛 Troubleshooting

### Common Issues

1. **"Error loading models" message**
   - Run `python setup_files.py` first
   - Check if all .pkl files are in the root directory

2. **"Could not fetch movie details" error**
   - Verify your TMDb API key is correct
   - Check your internet connection
   - Try a different movie name

3. **Package import errors**
   - Install requirements: `pip install -r requirements_streamlit.txt`
   - Try upgrading pip: `pip install --upgrade pip`

4. **Streamlit not found**
   - Install streamlit: `pip install streamlit`
   - Check Python version (3.8+ required)

### Performance Tips

- **First Load**: Initial loading may take time due to model loading and similarity matrix creation
- **Caching**: Streamlit caches models and similarity matrix for faster subsequent requests
- **API Limits**: TMDb has rate limits; avoid rapid consecutive searches

## 🎨 Customization

### Styling
Modify the CSS in the `st.markdown()` section to customize:
- Colors and themes
- Layout and spacing
- Component styling

### Features
Easy to extend with:
- More recommendation algorithms
- Additional movie databases
- Enhanced sentiment analysis
- User ratings and reviews

## 📈 Dataset Information

The movie dataset includes:
- **Movie Titles**: Over 4,000 movies
- **Features**: Director, cast, genres, keywords
- **Combined Features**: Preprocessed text for similarity calculation

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Improving documentation
- Adding new recommendation algorithms

## 📝 License

This project is for educational and non-commercial use.

## 🙏 Acknowledgments

- **Original Flask Version**: AJAX Movie Recommendation System with Sentiment Analysis
- **Movie Data**: The Movie Database (TMDb)
- **ML Libraries**: scikit-learn, pandas, numpy
- **Web Framework**: Streamlit

---

**Happy Movie Watching! 🍿** 