from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
# from langchain.llms.openai import OpenAI
from langchain_openai import ChatOpenAI

from utils.load_openai_client import *
from prompts.prompts import SPEC_PROMPT, CONCLUSION_PROMPT, LEVEL_PROMPT


llm = ChatOpenAI()

conversation = ConversationChain(
    prompt=SPEC_PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)
 

for _ in range(10):
    query = input('Enter query: ')
    # conversation.predict(input=query)
    conversation.invoke({'input':query})
    answer = conversation.memory.chat_memory.messages[-1].content
    print(answer)

chat_history = conversation.memory.chat_memory
    

specialization_response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=CONCLUSION_PROMPT.format(history=chat_history),
    temperature=0.0,
    max_tokens=64,
)

specialization = specialization_response.choices[0].text
print(f'Итак вы являетесь: {specialization}')


level_response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=LEVEL_PROMPT.format(history=chat_history, spec=specialization),
    temperature=0.0,
    max_tokens=64,
)

level = level_response.choices[0].text
print(f'Ваш уровень: {level}')


