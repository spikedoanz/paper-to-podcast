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

from representative import Representative
from interviewer import Interviewer
from extract import *
from utilities import *
from chat import *

if __name__ == "__main__":
    file_paths = [
        './pdf/attention_is_all_you_need.pdf',
        './pdf/lbdl.pdf',
        './pdf/voyager.pdf'
    ]
    paper_list = [
        "Attention is all you need",
        "The little book of deep learning",
        "VOYAGER: An Open-Ended Embodied Agent with Large Language Models",
    ]
    paper_index = 2
    paper = [paper_index]
    filepath = file_paths[paper_index]
    model = "gpt-3.5-turbo-16k"
    extraction_path = "./cache/voyager.json"



    interviewer = Interviewer(
        name = "Ody",
        gender = "male",
        personality = "logical, strategic thinking, wisdom and considerate of ethics",
        expertise = "well informed, but eager to learn",
        interests = "exploration, problem solving, human nature, leadership and history",
        brevity = (
            "be brief, only say around 5-6 sentences every time you talk, "
            "lean towards asking inquisitive and probing questions, "
            "seeking to uncover deeper truths and insightsmm, "
            "and don't say \"thank you\" too often"
        ),
        paper = paper,
        model = model,
    )
    representative = Representative(
        name = "Alex",
        gender = "female",
        personality = "caring. compassionate, very slightly spiritual but overall highly educated and logical",
        expertise = "casual audience who aren't afraid of a tangent or two",
        interests = "math, computer science, love, emotions, the nature of consciousness and reality",
        brevity = (
            "are eloquent and clear. Only say about 5-6 sentences every time you talk. "
            "Lean towards drawing listeners into the topic of the interview."
        ),
        paper = paper, 
        model = model,
    )
    """
    question = interviewer.self_introduction()
    print(f"Ody: {question}\n")
    response= representative.self_introduction(question)
    print(f"Alex: {response}\n")
    inp = input("Continue? (Y/n): ")
    inp = ('n')
    while (inp not in ['n', 'N']):
        question = interviewer.chat(response)
        print(f"Ody: {question}\n")
        response = representative.chat(question)
        print(f"Alex: {response}\n")
        inp = input("Continue? (Y/n): ")
    print(print_list(interviewer.memory))
    """


    question, answer = "", ""
    sentences = get_sentences(filepath)
    chunks = list(get_windows(sentences))
    
    data = load_extraction(extraction_path)
    topic_arr = []
    temp_extraction = data['data']
    test_conversation = False
    test_summarizing = False
    test_subtopic_integration = False 
    if (test_conversation == True):
        for i in temp_extraction:
            topics = i[0]
            chunk_ind = i[4]
            chunk = chunks[chunk_ind]
            for j in topics[:15]:
                #print(j, chunk)
                topic_name = j['topic']
                subtopics = j['subtopics']
                #print(subtopics)
                #question = interviewer.ask_topic(topic_name)
                print("\n\n\n---------Question----------")
                print("Ody: " + question)
                #answer = representative.answer_topic(question, topic_name, chunk)
                print("\n--------Answer----------")
                print("Alex: " + answer)
    if (test_summarizing == True):
        chunk_index = 1
        chunk = chunks[chunk_index]
        example = temp_extraction[chunk_index]         
        sample_data = example[0]
        for sample in sample_data:
            topic = sample['topic']
            subtopics = format_subtopics_with_quotes(sample['subtopics']) 
            summary = representative.summarize_topic(topic, subtopics, chunk)
            print("------ Summmary-------")
            print("Topic: " + topic)
            print("Subtopics: " + subtopics)
            print(summary)
    if (test_subtopic_integration==True):
        chunk_index = 1
        chunk = chunks[chunk_index]
        example = temp_extraction[chunk_index]         
        sample_data = example[0]
        for sample in sample_data:
            topic = sample['topic']
            subtopics = format_subtopics_with_quotes(sample['subtopics']) 
            question = interviewer.chat_topic(topic, subtopics, "Alex") 
            print("------Question-------")
            print(question) 


    chunk_index = 1
    chunk = chunks[chunk_index]
    example = temp_extraction[chunk_index]         
    sample_data = example[0]
    for sample in sample_data[:3]:
        topic = sample['topic']
        subtopics = sample['subtopics']
        subtopics_string = format_subtopics_with_quotes(subtopics)
        chat_topic(interviewer, representative, topic, subtopics, 0, chunk)

    interviewer.tokens_used()
    representative.tokens_used()