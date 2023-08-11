from pdfminer.high_level import extract_text
import re
from itertools import chain
import openai
import json
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
openai.api_key = token=os.environ['CHAT_TOKEN']

class Interviewer:
    def __init__(self, name, gender, personality, expertise, brevity, interests, paper, model):
        self.name = name
        self.gender = gender
        self.personality = personality
        self.expertise = expertise
        self.brevity = brevity
        self.interests = interests
        self.record = []
        self.memory = []
        self.model = model
        self.paper = paper
        self.identity = (
            f"You are a {self.gender} interviewer named {self.name}. "
            f"You're known for your {self.personality}. "
            f"As an interviewer, you usually {self.brevity}, and aim for a {self.expertise} audience. "
            f"As a person, you are interested in {self.interests}; "
            f"don't let that show explicitly in your interviewing style, but guide the interview in that direction. "
            f"do NOT explicitly say anything about yourself. Let all of that be inferred through the way that you talk. "
            f"do NOT point out that you're an interviewer, everyone already knows this and it would be annoying to hear it again. "
            f"10/10 writing quality is a top writer and 1/10 writing quality is a terrible writer. You are a 9/10 writer. "
        )

    def chat(self, user_prompt):
        system_prompt = self.identity
        system_prompt += (
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You are interviewing Alex, standin for the writers of the paper. "
            "but don't point this out, just have a normal conversation with her. "
            "Simply start talking, no formating is required. "
            "Let Alex do the talking when it comes into introducing concepts."
        )
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        messages += self.memory
        messages += [{"role": "user", "content": user_prompt}]
        response =  openai.ChatCompletion.create(
                model=self.model,
                messages= messages,
                temperature = 0.8,
                )
        self.record.append(response)
        assistant_response = response['choices'][0]['message']['content']
        self.memorize(user_prompt, assistant_response)
        return assistant_response

    def start_interview(self):
        pass

    def ask_for_citation(self):
        pass  # Implementation of asking for citation

    def draw_comparison(self):
        pass  # Implementation of drawing comparisons

    def ask_clarifying(self):
        pass  # Implementation of asking clarifying questions

    def casual_talk(self):
        pass  # Implementation of casual conversation

    def summarization(self):
        pass  # Implementation of summarization functionality

    def simplify(self):
        pass  # Implementation of simplifying functionality

    def critical_thinking(self):
        pass  # Implementation of critical thinking functionality
    
    def self_introduction(self):
        system_prompt = self.identity
        system_prompt += (
            "Introduce yourself to your audience, who already know you're an interviewer, "
            "and are here for an interview, not to hear about who you are. "
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You are interviewing Alex, standin for the writers of the paper. "
            "but don't point this out, just have a normal conversation with her. "
            "Simply start talking, no formating is required. "
            "Let Alex do the talking when it comes into introducing concepts."
        )
        user_prompt = ("")
        response =  openai.ChatCompletion.create(
                model=self.model,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                temperature = 0.8
                )
        self.record.append(response)
        return response['choices'][0]['message']['content']
    def memorize(self, user_prompt, assistant_response):
        user = {"role" : "user", "content": user_prompt}
        assistant = {"role": "assistant", "content": assistant_response}
        self.memory.append(user)
        self.memory.append(assistant)
    def ask_topic(self, topic):
        system_prompt = self.identity
        system_prompt += (
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You are interviewing Alex, standin for the writers of the paper. "
            "but don't point this out, just have a normal conversation with her. "
            "Simply start talking, no formating is required. "
            "You've already said hi to her, this is the middle of the conversation. "
            "You've already introduced the name of the paper, so don't mention it again. "
            "Let Alex do the talking when it comes into introducing concepts."
            f"It's your turn to talk, ask Alex to explain {topic}"
            "Don't ask multiple questions, stick to a single question per turn. "
        )
        user_prompt = ""
        response =  openai.ChatCompletion.create(
                model=self.model,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                temperature = 1.2
                )
        self.record.append(response)
        return response['choices'][0]['message']['content']