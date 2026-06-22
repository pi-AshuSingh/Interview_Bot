from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field
from pprint import pprint
import random

class Option(BaseModel):
    text: str = Field(description="The text of the option")
    isCorrect: bool = Field(description="Indicator if the option is correct or not")

class MCQ(BaseModel):
    question: str = Field(description="The statement of the question")
    options: list[Option] = Field(description="List of answer options with correctness indicated")

class MCQGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def chat_model(self, temperature: float):
        return GoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            api_key=self.api_key,
            temperature=temperature,
            max_tokens=8000,
        )

    def generate(self, level: str, topic: str, number_of_questions: int):
        generation_system_message_content = '''You are an expert in generating diverse and high-quality Multiple Choice Questions (MCQs) for interview preparation. 
        Your vast and comprehensive knowledge allows you to cover a wide range of topics without repetition. 
        You provide clear, concise, and relevant questions that are appropriately challenging based on the specified difficulty level. 
        Ensure that the questions are varied and never repeat the same question twice. Always return the response strictly in JSON format.\n\n'''

        human_message_content = '''
        **Generate Multiple Choice Questions (MCQs)**

        **Topic:** {topic}

        **Difficulty Level:** {level}

        **Number of questions:** {number_of_questions}

        **Instructions:** Generate {number_of_questions} multiple-choice questions (MCQ) on the topic of {topic} at the specified difficulty level. 
                        The questions should have four options, with one correct answer and three distractors. 
                        Ensure the questions are clear, concise, and relevant to the Topic. 
                        Return the MCQ in JSON format with the following structure:
                      
        ]

        {format_instructions}
        '''

        prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=generation_system_message_content),
            HumanMessagePromptTemplate.from_template(human_message_content)
        ])

        parser = JsonOutputParser(pydantic_object=MCQ)

        return self._completion(prompt_template, level, topic, number_of_questions, parser)

    def _completion(self, prompt, level, topic, number_of_questions, parser):
        temp = random.uniform(0.1, 1)
        llm = self.chat_model(temp)
        llm_chain = prompt | llm | parser

        parameters = {
            'level': level,
            'topic': topic,
            'number_of_questions': number_of_questions,
            'format_instructions': parser.get_format_instructions()
        }

        response = llm_chain.invoke(parameters)
        pprint(response)
        return response