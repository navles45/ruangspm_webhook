from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os

router = APIRouter()
load_dotenv()
openai.api_key = os.environ.get("OPEN_AI")

class Question(BaseModel):
    query:str

@router.post('/revision/question')
async def question(query:Question):
    question_request = query.query
    answers = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=question_request,
        documents=["Kedaulatan ditakrifkan sebagai kekuasaan tertinggi dan kewibawaan sesebuah negara yang bebas serta mempunyai hak untuk melaksanakan pemerintahan dan pentadbiran negara."],
        examples_context= "In 2017, U.S. life expectancy was 78.6 years.",
        examples=[["What is human life expectancy in the United States?","78 years."]],
        max_tokens = 100,
        stop= ["\n", "<|endoftext|>"]
    )
    return answers


