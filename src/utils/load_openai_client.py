import os
import openai

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')


openai.api_key = api_key
client = OpenAI()