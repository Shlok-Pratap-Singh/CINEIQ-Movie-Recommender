# CINEIQ

An open, explainable movie recommendation engine that combines collaborative filtering, content-based filtering, and sentiment-aware re-ranking to deliver personalized, interpretable suggestions that evolve with user taste.

## Problem Statement
Content discovery on modern streaming platforms is opaque, biased toward promoted titles, and can trap users in recommendation loops. **CINEIQ** aims to provide an open and explainable system that blends multiple ML strategies for better, more transparent recommendations.

## Deliverables
- **Hybrid Recommendation Engine**: Collaborative filtering + content-based filtering (TF‑IDF + cosine similarity) + SVD-based matrix factorization via weighted ensemble
- **Sentiment-Aware Re‑Ranker**: Uses VADER on user reviews to re-rank recommendations
- **User Taste Dashboard**: Streamlit interface with genre radar charts and decade preferences
- **Explainability Layer**: Human-readable recommendation rationale (rule-based in current code)

## Tech Stack
- **ML**: Python, scikit‑learn, Surprise (SVD), Pandas, NumPy
- **NLP**: NLTK VADER
- **Serving**: FastAPI
- **Dashboard**: Streamlit + Plotly
- **Tracking**: MLflow (installed; tracking optional)

## Repository Structure
```
.
├── app.py                 # Flask web application server (Frontend proxy)
├── main.py                # FastAPI backend engine (Recommendation logic & API)
├── filtering_content.py   # Data preparation, preprocessing, and offline model training
├── templates/             # Frontend UI templates
│   └── index.html         # Main web portal layout
├── data/                  # Dataset folder (download required)
├── models/                # Trained serialization model artifacts (download required)
├── .env.example           # Environment configuration template
└── requirements.txt       # Project dependencies
```

## Setup
### 1) Create virtual environment & install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure environment
Create a `.env` file using `.env.example`:
```bash
TMDB_API_KEY=YOUR_TMDB_KEY
```

## Downloading Datasets & Models
Large files are hosted on Google Drive.

### ✅ Datasets
Download from:
- https://drive.google.com/drive/folders/15-w7RubqiwIjvltmjiMaPQ44gQYJ1HAH?usp=sharing

Place the following in `data/`:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`
- `links.csv`
- `ratings.csv`

### ✅ Models
Download from:
- https://drive.google.com/drive/folders/1BsvU_4uSxTSvKv2ysKovJufq0Lyeqqq2?usp=sharing

Place the following in `models/`:
- `movie_list.pkl`
- `similarity.pkl`
- `svd_model.pkl`
- `user_ratings.pkl`

## Running the Project
### 1) (Optional) Train or regenerate models
If you want to rebuild models from raw data:
```bash
python filtering_content.py
```

### 2) Start the FastAPI backend
```bash
uvicorn main:app --reload
```
The API will run at `http://127.0.0.1:8000`.

### 3) Start the Streamlit dashboard
In a separate terminal:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000` to interact with the dashboard.

## API Endpoints
- `GET /recommend?user_id=...&movie_title=...`: Fetches top 5 content-collaborative hybrid recommendations re-ranked with active VADER sentiment analytics.
- `GET /user_stats/{user_id}`:Compiles taste profiling distributions (genre weights and decade metrics) for a given user profile.

---

