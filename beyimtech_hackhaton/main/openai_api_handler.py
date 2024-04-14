import os
import json

from pathlib import Path
from openai import OpenAI
from environ import Env

from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
# from langchain.llms.openai import OpenAI
from langchain_openai import ChatOpenAI

from .prompts.prompts import SPEC_PROMPT, CONCLUSION_PROMPT, LEVEL_PROMPT


env = Env()
env_file = Path(__file__).resolve().parent / '.env'
env.read_env(env_file)


class ApiHandler:
    def __init__(self):
        self.api_key = env("OPENAI_API_KEY")
        self.client = OpenAI()
        self.model_name = "gpt-3.5-turbo-instruct"
        self.conversation = ConversationChain(
            prompt=SPEC_PROMPT,
            llm=ChatOpenAI(),
            verbose=True,
            memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
        )

    def get_specialization(self, chat_history):
        specialization_response = self.client.completions.create(
            model=self.model_name,
            prompt=CONCLUSION_PROMPT.format(history=chat_history),
            temperature=0.0,
            max_tokens=64,
        )

        specialization = specialization_response.choices[0].text
        return specialization

    def get_level(self, chat_history, specialization):
        level_response = self.client.completions.create(
            model=self.model_name,
            prompt=LEVEL_PROMPT.format(history=chat_history, spec=specialization),
            temperature=0.0,
            max_tokens=64
        )

        level = level_response.choices[0].text
        return level
    

    def send_message_to_chat(self, query):
        self.conversation.invoke({'input':query})
        answer = self.conversation.memory.chat_memory.messages[-1].content
        return answer


    def get_conclusion(self):
        chat_history = self.conversation.memory.chat_memory
        specialization = self.get_specialization(chat_history)
        level = self.get_level(chat_history, specialization)

        conclusion_response = {
            "level": level,
            "specialization": specialization,
        }

        conclusion_response_json = json.dumps(conclusion_response)
        return conclusion_response_json

    def transcript_text(self, audio_file_name):
        audio_file= open(audio_file_name, "rb")
        transcription = self.client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )
        print(transcription.text)
        transcription_text = transcription.text
        return transcription_text