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
