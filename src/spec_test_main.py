import json

from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from utils.load_openai_client import *
from prompts.prompts import SPEC_PROMPT, CONCLUSION_PROMPT, LEVEL_PROMPT, SALARY_PROMPT
from langchain.chains.openai_functions.extraction import create_extraction_chain

llm = ChatOpenAI()

conversation = ConversationChain(
    prompt=SPEC_PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)
 

for _ in range(3):
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

schema = {
    "properties":{
        "IT Specialization": {'type':'string'}
    }
}

extract_spec = create_extraction_chain(schema,llm)

extracted_sped = extract_spec.run(specialization)

extracted_sped = extracted_sped[0]["IT Specialization"]

print(f'Итак вы являетесь: {extracted_sped}')


level_response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=LEVEL_PROMPT.format(history=chat_history, spec=specialization),
    temperature=0.0,
    max_tokens=64,
)

level = level_response.choices[0].text

print(f'Ваш уровень: {level}')


generate_salary = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=SALARY_PROMPT.format(level=level, spec=specialization),
    temperature=0.0,
    max_tokens=256,
)

salary = generate_salary.choices[0].text
print(f'Зарплаты : {salary}')

def extract_to_json(salary):
    lines = salary.split('\n')

    salaries_list = []
    for line in lines:
        month, value = line.split(' - ')
        salaries_list.append({month: int(value)})

    data_dict = {"salaries": salaries_list}

    # Преобразование словаря в JSON
    json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)