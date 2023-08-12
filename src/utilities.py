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

def format_subtopics_with_quotes(subtopics: list[str]) -> str:
    if (len(subtopics) == 0):
        return "<|no subtopics|>"
    if (len(subtopics) == 1):
        return subtopics[0]
    formatted_string = ""
    for subtopic in subtopics[:-1]:
       formatted_string += f"\"{subtopic}\", " 
    formatted_string += f"and \"{subtopics[-1]}\""
    return formatted_string
def format_subtopics(subtopics: list[str]) -> str:
    if (len(subtopics) == 0):
        return "<|no subtopics|>"
    if (len(subtopics) == 1):
        return subtopics[0]
    formatted_string = ""
    for subtopic in subtopics[:-1]:
       formatted_string += f"{subtopic}, " 
    formatted_string += f"and {subtopics[-1]}"
    return formatted_string


if __name__ == "__main__":
    subtopics = ["one", 'two', 'three']
    print(format_subtopics(subtopics))