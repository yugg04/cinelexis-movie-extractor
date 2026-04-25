import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cinelexis",
    page_icon="🎬",
    layout="centered",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0C0C0F;
    color: #E8E4DC;
}

/* ── hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; padding-bottom: 3rem; max-width: 760px; }

/* ── hero title ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3.6rem;
    letter-spacing: -0.5px;
    color: #F5F0E8;
    margin: 0;
    line-height: 1.1;
}
.hero h1 em {
    color: #E8A020;
    font-style: italic;
}
.hero p {
    color: #8A857C;
    font-size: 1rem;
    font-weight: 300;
    margin-top: 0.6rem;
    letter-spacing: 0.04em;
}

/* ── textarea label ── */
.input-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8A857C;
    margin-bottom: 0.5rem;
}

/* ── streamlit textarea overrides ── */
textarea {
    background: #141418 !important;
    border: 1px solid #2A2A32 !important;
    border-radius: 10px !important;
    color: #E8E4DC !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s !important;
}
textarea:focus {
    border-color: #E8A020 !important;
    box-shadow: 0 0 0 3px rgba(232,160,32,0.12) !important;
}

/* ── button ── */
div.stButton > button {
    width: 100%;
    background: #E8A020;
    color: #0C0C0F;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.06em;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    margin-top: 0.5rem;
}
div.stButton > button:hover {
    background: #F5B840;
    transform: translateY(-1px);
}
div.stButton > button:active { transform: translateY(0); }

/* ── result card ── */
.result-card {
    background: #141418;
    border: 1px solid #2A2A32;
    border-radius: 14px;
    padding: 2rem 2rem 1.5rem;
    margin-top: 2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #E8A020, #F5B840, #E8A020);
}

/* ── movie title in result ── */
.movie-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #F5F0E8;
    margin: 0 0 0.25rem;
}
.movie-meta {
    color: #8A857C;
    font-size: 0.85rem;
    font-weight: 300;
    margin-bottom: 1.4rem;
}

/* ── field rows ── */
.field-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.field-block {
    background: #0C0C0F;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    flex: 1;
    min-width: 120px;
}
.field-block .flabel {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #E8A020;
    margin-bottom: 0.25rem;
}
.field-block .fvalue {
    font-size: 0.9rem;
    color: #E8E4DC;
    font-weight: 400;
}

/* ── tags ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1rem; }
.tag {
    background: rgba(232,160,32,0.12);
    color: #E8A020;
    border: 1px solid rgba(232,160,32,0.25);
    border-radius: 100px;
    padding: 0.22rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 500;
}

/* ── summary ── */
.summary-block {
    border-top: 1px solid #2A2A32;
    padding-top: 1.2rem;
    margin-top: 0.5rem;
    color: #A09A90;
    font-size: 0.9rem;
    line-height: 1.7;
    font-weight: 300;
}

/* ── error box ── */
.error-box {
    background: #1A0F0F;
    border: 1px solid #5C2020;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-top: 1.5rem;
    color: #E07070;
    font-size: 0.85rem;
    font-family: monospace;
}

/* ── spinner override ── */
.stSpinner > div { border-top-color: #E8A020 !important; }

/* ── example pills ── */
.example-bar {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
    align-items: center;
}
.example-pill-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8A857C;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Cine<em>lexis</em></h1>
  <p>Paste any movie description · Get structured data instantly</p>
</div>
""", unsafe_allow_html=True)

# ── Pydantic Schema ───────────────────────────────────────────────────────────
class Movie(BaseModel):
    title: str = Field(description="Movie title")
    release_year: Optional[int] = Field(default=None)
    genre: List[str] = Field(description="List of genres")
    director: Optional[str] = Field(default=None)
    cast: List[str] = Field(description="Main cast members")
    rating: Optional[float] = Field(default=None)
    summary: str = Field(description="Short summary")

# ── Example Paragraphs ────────────────────────────────────────────────────────
EXAMPLES = {
    "Inception": (
        "Inception (2010) is a sci-fi thriller directed by Christopher Nolan. "
        "Starring Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page, the film follows a skilled "
        "thief who enters people's dreams to steal secrets. It holds an IMDb rating of 8.8."
    ),
    "The Godfather": (
        "The Godfather (1972), directed by Francis Ford Coppola, is a landmark crime drama. "
        "Marlon Brando, Al Pacino, and James Caan star in this story of the powerful Corleone mafia "
        "family. The film has an IMDb rating of 9.2 and is widely regarded as one of the greatest "
        "movies ever made."
    ),
    "Parasite": (
        "Parasite (2019) is a South Korean black comedy thriller directed by Bong Joon-ho. "
        "The film stars Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong and Choi Woo-shik. "
        "It became the first non-English language film to win the Academy Award for Best Picture "
        "and holds a rating of 8.5 on IMDb."
    ),
}

# ── Example Buttons ───────────────────────────────────────────────────────────
st.markdown('<div class="input-label">Try an example</div>', unsafe_allow_html=True)

cols = st.columns(len(EXAMPLES))
for col, (name, text) in zip(cols, EXAMPLES.items()):
    if col.button(f"🎬 {name}", key=f"ex_{name}"):
        st.session_state["paragraph"] = text

# ── Text Area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label" style="margin-top:1.2rem">Your paragraph</div>', unsafe_allow_html=True)

paragraph = st.text_area(
    label="paragraph_input",
    label_visibility="collapsed",
    placeholder="Paste a movie description here — a Wikipedia blurb, review snippet, or anything that mentions title, cast, director, genre…",
    height=160,
    key="paragraph",
)

extract_btn = st.button("✦  Extract Movie Data", key="extract")

# ── Extraction Logic ──────────────────────────────────────────────────────────
if extract_btn:
    if not paragraph.strip():
        st.warning("Please enter a paragraph first.")
    else:
        load_dotenv()
        try:
            with st.spinner("Extracting structured data…"):
                model = ChatMistralAI(model="mistral-small-latest", temperature=0)
                parser = PydanticOutputParser(pydantic_object=Movie)

                prompt = ChatPromptTemplate.from_messages([
                    ("system", """
Extract structured movie information from the given paragraph.
Strictly follow this format:
{format_instructions}
Return only JSON. Do not add extra text.
"""),
                    ("human", "{paragraph}")
                ])

                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)
                movie = parser.parse(response.content)

            # ── Render Result ─────────────────────────────────────────────────
            rating_str = f"★ {movie.rating}" if movie.rating else "N/A"
            year_str   = str(movie.release_year) if movie.release_year else "Unknown"
            director_str = movie.director or "Unknown"

            genre_tags = "".join(f'<span class="tag">{g}</span>' for g in movie.genre) if movie.genre else "—"
            cast_tags  = "".join(f'<span class="tag">{c}</span>' for c in movie.cast)  if movie.cast  else "—"

            st.markdown(f"""
<div class="result-card">
  <div class="movie-title">{movie.title}</div>
  <div class="movie-meta">{year_str} &nbsp;·&nbsp; Directed by {director_str} &nbsp;·&nbsp; {rating_str}</div>

  <div class="field-row">
    <div class="field-block">
      <div class="flabel">Year</div>
      <div class="fvalue">{year_str}</div>
    </div>
    <div class="field-block">
      <div class="flabel">Director</div>
      <div class="fvalue">{director_str}</div>
    </div>
    <div class="field-block">
      <div class="flabel">Rating</div>
      <div class="fvalue">{rating_str}</div>
    </div>
  </div>

  <div class="flabel" style="margin-bottom:0.4rem">Genres</div>
  <div class="tag-row">{genre_tags}</div>

  <div class="flabel" style="margin-bottom:0.4rem">Cast</div>
  <div class="tag-row">{cast_tags}</div>

  <div class="summary-block">{movie.summary}</div>
</div>
""", unsafe_allow_html=True)

        except ValidationError as e:
            st.markdown(f"""
<div class="error-box">
  <strong>⚠ Parsing failed</strong><br><br>{str(e)}
</div>
""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
<div class="error-box">
  <strong>⚠ Error</strong><br><br>{str(e)}
</div>
""", unsafe_allow_html=True)