import os
import re
import json
import openai

from pathlib                    import  Path
from itertools                  import  chain
from dotenv                     import  load_dotenv
from pdfminer.high_level        import  extract_text

from representative             import  Representative
from interviewer                import  Interviewer
from extract                    import  *
from utilities                  import  *
from chat                       import  *

env_path =                      Path('.')/'.env'
load_dotenv(dotenv_path =       env_path)
openai.api_key =                token = os.environ['CHAT_TOKEN']

if __name__ == "__main__":
    model =                     "gpt-3.5-turbo-16k"

    paper_paths = [
        './pdf/attention_is_all_you_need.pdf',
        './pdf/lbdl.pdf',
        './pdf/voyager.pdf',
        './pdf/FacTool.pdf',
    ]
    paper_list = [
        "Attention is all you need",
        "The little book of deep learning",
        "VOYAGER: An Open-Ended Embodied Agent with Large Language Models",
        "FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios",
    ]
    paper_index =               3
    paper =                     paper_list[paper_index]
    paper_path =                paper_paths[paper_index]

    interviewer = Interviewer(
        name =                  "Ody",
        gender =                "male",
        personality =           "logical, strategic thinking, wisdom and considerate of ethics",
        expertise =             "well informed, but eager to learn",
        interests =             "exploration, problem solving, human nature, leadership and history",
        brevity = (
                                "be brief, only say around 5-6 sentences every time you talk, "
                                "lean towards asking inquisitive and probing questions, "
                                "seeking to uncover deeper truths and insightsmm, "
                                "and don't say \"thank you\" too often"
        ),
        paper =                 paper,
        model =                 model,
    )
    representative = Representative(
        name =                  "Alex",
        gender =                "female",
        personality =           "caring. compassionate, very slightly spiritual but overall highly educated and logical",
        expertise =             "casual audience who aren't afraid of a tangent or two",
        interests =             "math, computer science, love, emotions, the nature of consciousness and reality",
        brevity = (
                                "are eloquent and clear. Only say about 5-6 sentences every time you talk. "
                                "Lean towards drawing listeners into the topic of the interview."
        ),
        paper =                 paper, 
        model =                 model,
    )

    # Start pipeline ------------------
    
    
    

    # 1 - Extract doc into topics
    extraction_path =           "./cache/factool.json"
    extract_doc(paper_path, extraction_path)

    question, answer =          "", ""
    sentences =                 get_sentences(paper_path)
    chunks =                    list(get_windows(sentences))
    
    data =                      load_extraction(extraction_path)
    topic_arr =                 []
    temp_extraction =           data['data']
    test_conversation =         False
    test_summarizing =          False
    test_subtopic_integration = False
    test_converse =             False

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
    if (test_converse == True):
        chunk_index = 1
        chunk = chunks[chunk_index]
        example = temp_extraction[chunk_index]         
        sample_data = example[0]
        for sample in sample_data[:3]:
            topic = sample['topic']
            subtopics = sample['subtopics']
            subtopics_string = format_subtopics_with_quotes(subtopics)
            chat_topic(interviewer, representative, topic, subtopics, 0, chunk)
    
    
    # 2 - Generate a conversation using the extracted topics
    record =                    []
    data =                      load_extraction(extraction_path)
    extraction =                data['data']
    question, answer =          "", ""
    sentences =                 get_sentences(paper_path)
    chunks =                    list(get_windows(sentences))

    for i, chunk in enumerate(chunks[:3]):
        curr =                  extraction[i]
        groups =                curr[0]
        for _ in groups:
            topic =             _['topic']
            subtopics =         _['subtopics']
            subtopics_string =  format_subtopics_with_quotes(subtopics)
            log = chat_topic(interviewer, representative, topic, subtopics, 0, chunk)
            record.extend(log)
    

    # 3 - Save the converastion to a json file
    # todo: Add more information in here, like all the prompts used to geneate the characters or something like that
    time =                      formatted_time()
    record_data =               {
                                "record": record
    }
    savepath =                  f"./examples/{formatted_time()}.json"
    print(record_data)
    with open(savepath, "w") as f:
        json.dump(record_data, f)
    interviewer.tokens_used()
    representative.tokens_used()