from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI

# Load env
load_dotenv()

# Model
model = ChatMistralAI(model="mistral-small-latest", temperature=0)

# Schema
class Movie(BaseModel):
    title: str = Field(description="Movie title")
    release_year: Optional[int] = Field(default=None)
    genre: List[str] = Field(description="List of genres")
    director: Optional[str] = Field(default=None)
    cast: List[str] = Field(description="Main cast members")
    rating: Optional[float] = Field(default=None)
    summary: str = Field(description="Short summary")

# Parser
parser = PydanticOutputParser(pydantic_object=Movie)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
Extract structured movie information from the given paragraph.

Strictly follow this format:
{format_instructions}

Return only JSON. Do not add extra text.
"""),
    ("human", "{paragraph}")
])

# Input
para = input("Give your paragraph: ")

# Build prompt
final_prompt = prompt.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})

# Invoke model
response = model.invoke(final_prompt)

# Parse safely
try:
    movie_data = parser.parse(response.content)
    print("\n Extracted Data:\n")
    print(movie_data.model_dump())
except ValidationError as e:
    print("\n Parsing failed:")
    print(e)
    print("\nRaw response:\n", response.content)