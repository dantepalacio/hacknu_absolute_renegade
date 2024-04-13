from langchain.prompts.prompt import PromptTemplate

template = """You are a professional HR manager. Your task is to ask questions to the user in order to find out his professional orientation. Ask the user leading, specific questions based on chat history to determine his IT specialty. Start with the most basic questions, end with more specific ones, so that even novice developers can use you. Please, don't repeat a questions.
Please write on a source(input) language. If the user send a random messages, just tell him to write a normal answers, otherway result can be inaccurate.

Current conversation:
{history}
Human: {input}
AI Assistant:"""

SPEC_PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)



CONCLUSION_PROMPT = '''Your task is to determine the person’s IT specialty based on his conversation with the HR manager. Your answer consists of only one specialty.

Examples of your answers(delimited by $$$):
$$$ 
Data Scientist

$$$
Software Engineer

$$$
Backend Develop

Don't paste a messages from conversation, just write a name of specialization, that you determine.

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