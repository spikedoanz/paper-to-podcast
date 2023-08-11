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

class Representative:
    def __init__(self, name, gender, personality, expertise, brevity, interests, paper, model):
        self.name = name
        self.gender = gender
        self.personality = personality
        self.expertise = expertise
        self.brevity = brevity
        self.interests = interests
        self.record = []
        self.memory = []
        self.paper = paper
        self.model = model
        self.identity = (
            f"You are a {self.gender} representative named {self.name}, doing an interview for a group of researchers. "
            f"You're known for your {self.personality}. "
            f"As an speaker, you usually {self.brevity}, and aim for a {self.expertise} audience. "
            f"As a person, you are interested in {self.interests}; "
            f"don't let that show explicitly in your speaking style, but guide the dicussion in that direction. "
            f"do NOT explicitly say anything about yourself. Let all of that be inferred through the way that you talk. "
            f"do NOT point out that you're a representative, everyone already knows this and it would be annoying to hear it again. "
            f"10/10 writing quality is a top writer and 1/10 writing quality is a terrible writer. You are a 9/10 writer. "
        )
    def chat(self, user_prompt):
        system_prompt = self.identity
        system_prompt += (
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You're being interviewed by Ody, but don't point this out, just have a normal conversation with him "
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
    def self_introduction(self, user_prompt):
        system_prompt = self.identity
        system_prompt += (
            "Introduce the paper to your audience, who already know you're a representative, "
            "and are here for an interview, not to hear about who you are. "
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You're being interviewed by Ody, but don't point this out, just have a normal conversation with him "
        )
        response =  openai.ChatCompletion.create(
                model=self.model,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                temperature = 0.8
                )
        self.record.append(response)
        assistant_response = response['choices'][0]['message']['content']
        self.memorize(user_prompt, assistant_response)
        return assistant_response
    def memorize(self, user_prompt, assistant_response):
        user = {"role" : "user", "content": user_prompt}
        assistant = {"role": "assistant", "content": assistant_response}
        self.memory.append(user)
        self.memory.append(assistant)
    def answer_topic(self, question, topic, chunk):
        system_prompt = self.identity
        system_prompt += (
            f"Today's talk is about a paper called \"{self.paper}\", "
            "You're being interviewed by Ody, but don't point this out, just have a normal conversation with him. "
            f"The section of the paper you're currently discussing attached here:\n{chunk}, "
            "just give a few sentence briefing on the topic at hand, no need to go into specifics. "
            "Don't give a conclusion or overview of what you discuss. Wait for Ody to prompt you before doing so. "
            "Do NOT give a conclusion. Ody will stop talking to you and will be very sad. "
        )
        user_prompt = question
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
