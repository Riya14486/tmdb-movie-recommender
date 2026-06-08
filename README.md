# TMDB Movie Recommender

A Streamlit movie recommender app using TMDB data.

APP url : https://tmdb-movie-recommender-ljchb9w4b25pskkqnza3zl.streamlit.app/

## Setup

1. Create and activate your virtual environment.
2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Create a local secret file at `.streamlit/secrets.toml`:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

4. Run locally:

```powershell
streamlit run app.py
```

## Deployment

### Streamlit Cloud

1. Push your repo to GitHub.
2. Open Streamlit Cloud and connect your repository.
3. In the app dashboard, go to **Settings** → **Secrets**.
4. Add:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

5. Deploy the app.

### Notes

- The app already reads `TMDB_API_KEY` from `st.secrets` or from the `TMDB_API_KEY` environment variable.
- Do not commit `.streamlit/secrets.toml` to GitHub.
- The `.streamlit/` folder is already ignored by `.gitignore`.


