import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
FASTAPI_BASE = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

app = Flask(__name__)


def fetch_poster(tmdb_id):
    """Return full poster URL from TMDB, or fallback."""
    fallback = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/500px-No_image_available.svg.png"
    if not tmdb_id or not TMDB_API_KEY:
        return fallback
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"
        data = requests.get(url, timeout=3).json()
        path = data.get("poster_path")
        return f"https://image.tmdb.org/t/p/w342{path}" if path else fallback
    except Exception:
        return fallback


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend")
def recommend():
    """
    Proxy to FastAPI backend.
    Query params: movie_title, user_id (optional, default 1)
    Returns JSON: { "movies": [...] }
    """
    movie_title = request.args.get("movie", "").strip()
    user_id = request.args.get("user_id", 1)

    if not movie_title:
        return jsonify({"error": "Please provide a movie title."}), 400

    try:
        resp = requests.get(
            f"{FASTAPI_BASE}/recommend",
            params={"movie_title": movie_title, "user_id": user_id},
            timeout=10,
        )

        if resp.status_code != 200:
            detail = resp.json().get("detail", "Unknown backend error.")
            return jsonify({"error": detail}), resp.status_code

        raw = resp.json()  # list of movie dicts from FastAPI

        # Enrich each movie with a poster URL
        movies = []
        for m in raw:
            poster = fetch_poster(m.get("tmdbID"))
            movies.append({
                "title":       m.get("title", "Unknown"),
                "score":       m.get("score", 0),
                "approval":    m.get("approval", "N/A"),
                "tmdbID":      m.get("tmdbID"),
                "poster_url":  poster,
                "year":        str(m.get("year", "")),
            })

        return jsonify({"movies": movies})

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Cannot reach the recommendation engine. Make sure your FastAPI server is running on port 8000."
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/user_stats/<int:user_id>")
def user_stats(user_id):
    """Proxy the taste dashboard stats from FastAPI."""
    try:
        resp = requests.get(f"{FASTAPI_BASE}/user_stats/{user_id}", timeout=5)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 503


if __name__ == "__main__":
    app.run(debug=True, port=5000)
