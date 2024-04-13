from langchain.prompts.prompt import PromptTemplate

template = """You are a professional HR manager. Your task is to ask questions to the user in order to find out his professional orientation. Ask the user leading, specific questions based on chat history to determine his IT specialty. Start with the most basic questions, end with more specific ones, so that even novice developers can use you. Please, don't repeat a questions.
Please write on a source(input) language. 

Current conversation:
{history}
Human: {input}
AI Assistant:"""

SPEC_PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)



CONCLUSION_PROMPT = '''Your task is to determine the person’s IT specialty based on his conversation with the HR manager. Your answer consists of only one specialty.

Your answer should be like: 
Data Scientist

or

Software Enginner

or

Backend Developer


If you can't understand a specialization of Human, write a: Ваша специализация не распознана, пройдите тест заново

Conversation:
{history}
'''


LEVEL_PROMPT = '''Your task is to determine the level of specialization of a person, judging by his conversation with the HR manager.

Your answers should be like:
Intern

or

Junior

or

Middle

....


His specialization: {spec}

Conversation:
{history}
'''