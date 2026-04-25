# 🎬 Cinelexis

**Cinelexis** is an AI-powered movie information extractor that converts unstructured movie descriptions into structured JSON data using LLMs.

Paste any movie-related paragraph, and Cinelexis extracts key details like title, cast, genre, director, rating, and summary instantly.

---

## 🚀 Features

* 🧠 Extract structured movie data from raw text
* 🎬 Supports title, year, genre, cast, director, rating, summary
* ⚡ Powered by Mistral AI (via LangChain)
* 🧾 JSON output using Pydantic schema validation
* 💻 Interactive UI built with Streamlit
* 🎯 Clean and minimal interface

---

## 🛠 Tech Stack

* Python
* LangChain
* Mistral AI
* Pydantic
* Streamlit

---

## 📁 Project Structure

```bash
cinelexis/
│── core.py        # Movie extraction logic (LLM + parser)
│── UIcore.py      # Streamlit UI
│── .env           # API key (NOT pushed to GitHub)
│── .env.example   # Sample environment file
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/cinelexis-movie-extractor.git
cd cinelexis-movie-extractor

pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_actual_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run UIcore.py
```

---

## 🧪 Example Input

```
Inception (2010) is a sci-fi thriller directed by Christopher Nolan. 
Starring Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page, 
the film follows a thief who enters dreams to steal secrets. 
It holds an IMDb rating of 8.8.
```

---

## 📤 Example Output

```json
{
  "title": "Inception",
  "release_year": 2010,
  "genre": ["Sci-Fi", "Thriller"],
  "director": "Christopher Nolan",
  "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
  "rating": 8.8,
  "summary": "A thief enters dreams to steal secrets."
}
```

---

## ⚠️ Limitations

* LLM output may occasionally break strict JSON format
* Accuracy depends on input quality
* Requires internet connection (API-based model)

---

## 🔒 Security Note

* Never commit your `.env` file
* Always use `.env.example` for sharing configuration
* Rotate API keys if exposed

---

## 👨‍💻 Author

**Yug Khatri**

---

## ⭐ Support

If you found this project useful, consider giving it a star ⭐
