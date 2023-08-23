import os
import re
import json
import openai
import requests

from pathlib                    import  Path
from itertools                  import  chain
from dotenv                     import  load_dotenv
from pdfminer.high_level        import  extract_text
from bark                       import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile           import write as write_wav
from IPython.display            import Audio

from representative             import  Representative
from interviewer                import  Interviewer
from extract                    import  *
from utilities                  import  *
from chat                       import  *
from voice                      import  * 

env_path =                      Path('.')/'.env'
load_dotenv(dotenv_path =       env_path)
openai.api_key =                token = os.environ['CHAT_TOKEN']

def create_conversation(extraction_path, time, interviewer, representative, chunk_count=3, skip = False):
    if skip == True:
        return None
    record =                    []
    data =                      load_extraction(extraction_path)
    extraction =                data['data']
    question, answer =          "", ""
    sentences =                 get_sentences(paper_path)
    chunks =                    list(get_windows(sentences))

    for i, chunk in enumerate(chunks[:chunk_count]):
        curr =                  extraction[i]
        groups =                curr[0]
        for _ in groups:
            print(_)
            if (type(_) == type('')):
                topic = _
                subtopics = ['']
            else:
                topic =             _['topic']
                subtopics =         _['subtopics']
            subtopics_string =  format_subtopics_with_quotes(subtopics)
            log = chat_topic(interviewer, representative, topic, subtopics, 0, chunk)
            record.extend(log)
            print(record)
    

    # 3 - Save the converastion to a json file
    # todo: Add more information in here, like all the prompts used to geneate the characters or something like that

    record_data =               {
                                "record": record
    }
    logname = f"{time}_conversation.json"
    savepath =                  f"./conversations/{logname}"
    print(record_data)
    with open(savepath, "w") as f:
        json.dump(record_data, f)
    interviewer.tokens_used()
    representative.tokens_used()
 
if __name__ == "__main__":
    # Step 0: Config - choose model, paper, paper title, itv + rep definitions
    model =                     "gpt-3.5-turbo-16k"
    time = formatted_time()

    #time = "18-53-22-08-2023"

    extraction_file = f"{time}_extraction.json"
    extraction_path = "./cache/" + extraction_file

    conversation_file = f"{time}_conversation.json"
    conversation_path = f"./conversations/{conversation_file}" 

    recording_file = time + "_recording.wav"
    recording_path = f"./recordings/{recording_file}"

    skip_conversation = False


    paper_paths = [
        './pdf/attention_is_all_you_need.pdf',
        './pdf/lbdl.pdf',
        './pdf/voyager.pdf',
        './pdf/FacTool.pdf',
        './pdf/2303.13506.pdf',
        './pdf/2209.01188.pdf',
    ]
    paper_list = [
        "Attention is all you need",
        "The little book of deep learning",
        "VOYAGER: An Open-Ended Embodied Agent with Large Language Models",
        "FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios",
        'The Quantization Model of Neural Scaling',
        'Petals: a model for distributed computation of language models',
    ]
    paper_index =               5
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
                                "seeking to uncover deeper truths and insights, "
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
    
    # Make a conversation with the extraction
    extract_doc(paper_path, extraction_path)
    create_conversation(extraction_path, time, interviewer,representative, chunk_count = 2, skip = skip_conversation)
    create_recording(conversation_path, recording_path)
    # Make a recording using the conversation
    
