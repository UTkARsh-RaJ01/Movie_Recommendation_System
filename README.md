# 🎬 Movie Recommendation System

A modern, interactive movie recommendation system built with **Streamlit** that provides personalized movie suggestions based on content similarity and performs sentiment analysis on movie reviews.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🔍 **Movie Search**: Search from 4,000+ movies with auto-complete functionality
- 🎯 **Content-Based Recommendations**: Get similar movies based on plot, cast, director, and genres
- 🎬 **Movie Details**: Comprehensive information including posters, cast, ratings, and overview
- 📝 **Sentiment Analysis**: Analyze IMDb reviews and classify them as positive or negative
- 🎨 **Interactive UI**: Clean, modern interface with responsive design
- 🌐 **TMDb Integration**: Real-time movie data and posters from The Movie Database

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- TMDb API key ([Get it free here](https://www.themoviedb.org/settings/api))

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/YOUR_USERNAME/movie-recommendation-system.git
cd movie-recommendation-system
python install_and_run.py
```

#### Option 2: Manual Setup
```bash
git clone https://github.com/YOUR_USERNAME/movie-recommendation-system.git
cd movie-recommendation-system
pip install -r requirements_streamlit.txt
python setup_files.py
streamlit run streamlit_app.py
```

### Usage

1. **Get TMDb API Key**: Register at [TMDb](https://www.themoviedb.org/) and get your free API key
2. **Run the app**: The application will open in your browser at `http://localhost:8501`
3. **Enter API Key**: Add your TMDb API key in the sidebar
4. **Search Movies**: Select a movie from the dropdown or type to search
5. **Get Recommendations**: Click "Get Recommendations" to find similar movies
6. **Explore**: View detailed movie information, cast, and sentiment analysis of reviews

## 🛠️ Technology Stack

- **Backend**: Python, Streamlit
- **Machine Learning**: scikit-learn, pandas, numpy
- **Web Scraping**: BeautifulSoup, requests
- **APIs**: TMDb API for movie data
- **NLP**: Custom sentiment analysis model

## 📊 Dataset

- **Movies**: 4,000+ movies with comprehensive metadata
- **Features**: Plot, cast, director, genres, keywords
- **Models**: Pre-trained sentiment analysis model included

## 🎯 How It Works

1. **Content-Based Filtering**: Uses cosine similarity on combined movie features
2. **Feature Engineering**: Combines plot, cast, director, and genres into unified features
3. **Sentiment Analysis**: Custom NLP model trained on movie reviews
4. **Real-time Data**: Fetches current movie information from TMDb API

## 📁 Project Structure

```
movie-recommendation-system/
├── streamlit_app.py              # Main Streamlit application
├── requirements_streamlit.txt     # Python dependencies
├── setup_files.py               # Setup script for model files
├── install_and_run.py           # Automated installation script
├── main_data.csv                # Movie dataset
├── nlp_model.pkl                # Sentiment analysis model
├── tranform.pkl                 # Text vectorizer
└── README.md                    # Project documentation
```

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy with one click!

### Local Development
```bash
streamlit run streamlit_app.py --server.port 8501
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing the movie API
- [IMDb](https://www.imdb.com/) for movie reviews
- [Streamlit](https://streamlit.io/) for the amazing web framework
- scikit-learn community for machine learning tools

## 📞 Support

If you have any questions or run into issues:

1. Check the [Issues](https://github.com/YOUR_USERNAME/movie-recommendation-system/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your setup and the error you're encountering

## 🎬 Demo

[Add screenshots or GIF demos of your application here]

---

**Happy Movie Watching! 🍿** 