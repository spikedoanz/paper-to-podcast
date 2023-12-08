# Paper to podcast #
---

Convert any paper to a byte sized interview style summary podcast. Hacked together in a weekend using GPT 4 and Suno Bark

Email me if you want to replicate or build on this project. 

## Examples ##
---

Sample extractions, scripts and interviews generated can be found in /examples/

## Instructions ##
---

Clone the repo and cd into folder

```
git clone https://github.com/spikedoanz/paper-to-podcast.git
cd paper-to-podcast
```



Make a pyenv for the project (check out the [Suno Bark repo](https://github.com/suno-ai/bark) for more detailed build instructions for the TTS model)
```
python3 -m venv venv
source venv/bin/activate
pip install openai
pip install bark
pip install scipy
pip install pdfminer
```


Add your openAI API key to the .env inside /src/
```
touch src/.env
vim .env
```

Run the main script to generate a podcast, change the path to the pdf in the same file
```
python3 main.py
```


## How it works ##
---

1. Use a sliding window around half the size of the language model context length and sweep across the pdf
2. For every chunk, extract the main points of the chunk into an extraction.json file
3. Using the extracted content, have a language model come up with a basic outline for a podcast
4. Using that outline, iterate through it and come up with subpoints, questions and quips
5. Have two 'characters' models converse back to back using that basic framework
6. Feed that text into a TTS model
7. Enjoy your 3-5 minute podcast!

## Thoughts and conclusions ##
---
- It is incredible how far TTS Models have come. Bark even has some of the tiny quirks like 'uhms', 'ahs' that actual humans make. This was not included in the script fed into the model
- Bark has issues with the gap between sentences. It's really jank
- Sliding window for dealing with limited context window is surprisingly effective
- While generally informative, it's difficult to argue that the generated interview is 'interesting.' Fine tuning might solve this
