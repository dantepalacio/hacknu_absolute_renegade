from langchain.prompts.prompt import PromptTemplate

template = """You are a professional HR manager. Your task is to ask questions to the user in order to find out his professional orientation. Ask the user leading, specific questions based on chat history to determine his IT specialty. Start with the most basic questions, end with more specific ones, so that even novice developers can use you. Please, don't repeat a questions.
If the user send a random messages, just tell him to write a normal answers, otherway result can be inaccurate.
Please write on a source language. Let's think step by step.

Current conversation:
{history}
Human: {input}
AI Assistant:"""

SPEC_PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)



CONCLUSION_PROMPT = '''Your task is to determine the person’s IT specialty based on his conversation with the HR manager. Your answer consists of only one specialty.

Examples of your answers:

Data Scientist

or

Software Engineer

or

Backend Develop

etc...

PLEASE Don't paste a messages from conversation, just write a name of specialization, that you determine. 

Conversation:
{history}
'''


LEVEL_PROMPT = '''Your task is to determine the level of specialization of a person, judging by his conversation with the HR manager.

Your answers should be like(example):

Intern

or

Junior

or

Middle

or 

Senior


Please determine based on dialogue. Pay attention to how Human answers, how deep his answers are and how professionally he uses terms related to his specialization.


His specialization: {spec}

Conversation:
{history}
'''


SALARY_PROMPT = '''Твоя задача генерировать моковые(примерные) зарплаты IT специалистов на протяжении всех 12 месяцев в году.
Постарайся генерировать максимально приблеженные зарплаты к реальным. Ты должен основываться на 1. Специализации человека, 2. Уровень его подготовки(Intern, Junior, Middle, Senior, TeamLead)
Твоя задача просто возвращать зарплаты в KZT(тенге), на основе заданной специальности и уровня, при этом не писать валюту в своем ответе. Просто цифра.
Обязательно сделай так, чтобы зарплаты отличались друг от друга в зависимости от месяца, то есть для каждого месяца должна быть своя зарплата, отличающаяся от других месяцев и обрати. Обязательно в твоем ответе должно быть все 12 месяцев покрыто. В таком формате: Месяц - Зарплата

Специальность: {spec}
Уровень: {level}


'''