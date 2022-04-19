from fastapi import APIRouter
from dotenv import load_dotenv
import openai
import os

router = APIRouter()
load_dotenv()
openai.api_key = os.environ.get("OPEN_AI")

@router.post('/revision/question')
def query(query:str):
    answers = openai.Answer.create(
        search_model="ada",
        model="curie",
        question=query,
        documents=["Kedaulatan ditakrifkan sebagai kekuasaan tertinggi dan kewibawaan sesebuah negara yang bebas serta mempunyai hak untuk melaksanakan pemerintahan dan pentadbiran negara."],
        examples_context= "In 2017, U.S. life expectancy was 78.6 years.",
        examples=[["What is human life expectancy in the United States?","78 years."]],
        max_tokens = 100,
        stop= ["\n", "<|endoftext|>"]
    )
    return answers["answers"]


