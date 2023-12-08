from dotenv                 import load_dotenv
from pathlib                import Path
import openai   
import json
import os

from extract                import *
from utilities              import *

env_path =                  Path('.')/'.env'
load_dotenv(dotenv_path=    env_path)
openai.api_key = token=     os.environ['CHAT_TOKEN']

def chat_topic(interviewer, representative, topic, subtopics, rounds, context):
    rounds =                min(len(subtopics), rounds)
    topic =                 topic
    subtopics_string =      format_subtopics_with_quotes(subtopics)
    log_interviewer =       []
    log_representative =    []
    context =               representative.summarize_topic(topic, subtopics, context)

    print("---------Topic---------------")
    question = interviewer.ask_topic(
        topic =             topic,
        subtopics =         subtopics,
        participant =       representative.name
    )
    print(interviewer.name + ": " + question + "\n")
    log_representative.extend([{"role": "user", "content": question}])
    log_interviewer.extend([{"role": "assistant", "content": question}])

    answer = representative.reply(
        topic =             topic,
        subtopics_string =  subtopics_string,
        participant =       interviewer.name,
        conversation_log =  log_representative,
        context =           context,
    )
    print(representative.name + ": " + answer + "\n")
    log_representative.extend([{"role": "assistant", "content": answer}])
    log_interviewer.extend([{"role": "user", "content": answer}])

    
    for i in range(rounds):
        print(f"---------Subtopic {str(i)}---------------")
        question = interviewer.ask_subtopic(
            topic =             topic, 
            subtopics_string =  subtopics_string, 
            participant =       representative.name, 
            conversation_log =  log_interviewer,
        )
        print("\t" + interviewer.name + ": " + question)
        log_representative.extend([{"role": "user", "content": question}])
        log_interviewer.extend([{"role": "assistant", "content": question}])

        answer = representative.reply(
        topic =                 topic,
        subtopics_string =      subtopics_string,
        participant =           interviewer.name,
        conversation_log  =     log_representative,
        context =               context,
        )
        print(representative.name + ": " + answer)
        log_representative.extend([{"role": "assistant", "content": answer}])
        log_interviewer.extend([{"role": "user", "content": answer}])
    return log_representative 
    
