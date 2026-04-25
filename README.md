# 🎬 Cinelexis

**Cinelexis** is an AI-powered movie information extractor that converts unstructured movie descriptions into structured JSON data using LLMs.

Paste any paragraph about a movie, and Cinelexis will extract key details like title, cast, genre, director, and more — instantly.

---

## 🚀 Features

* 🧠 Extract structured movie data from raw text
* 🎬 Supports title, year, genre, cast, director, rating, summary
* ⚡ Powered by LLM (Mistral via LangChain)
* 🧾 JSON output using Pydantic schema validation
* 💻 Interactive UI built with Streamlit
* 🎯 Clean, minimal, and fast interface

---

## 🛠 Tech Stack

* Python
* LangChain
* Mistral AI
* Pydantic
* Streamlit

---

## 📦 Installation

```bash
git clone https://github.com/your-username/cinelexis-movie-extractor.git
cd cinelexis-movie-extractor

pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
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

## 📁 Project Structure

```
cinelexis/
│── app.py              # Streamlit UI
│── extractor.py        # Core extraction logic
│── .env                # API key (not committed)
│── requirements.txt
│── README.md
```

---

## ⚠️ Limitations

* LLM output may occasionally fail strict JSON formatting
* Accuracy depends on input paragraph quality
* Requires internet connection (API-based model)

---

## 🔮 Future Improvements

* Retry mechanism for invalid JSON
* Batch processing support
* Export to CSV/JSON
* Multi-language support

---

## 📌 Author

Developed by Yug

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
