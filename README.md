# NEVER MAKE THIS PUBLIC

I have my API keys uploaded so for the love of god may it remain private

## HTBreacher

An AI agent that reads my writeups website (or anything I configure) and gets the text out of it. Then it builds the Knowledge Base and then uses that to make the AI work.

## Setup

Create the venv and install all dependencies

If you don't have ollama install it and then do `ollama pull openhermes`

I use qwen for the local model as of now

After that run this thing so that it.... you know, runs

Also have an ollama api key so that you can use the cloud (which this does btw)

Another thing, there is a line of code for adding content to the knowledge base in `app.py`. Uncomment it and run it only when running the program for the first time. After this, comment it back out. This is meant to be used only after the knowledge base is updated by the scraper.

## GUI

To get the GUI see this [link](https://github.com/agno-agi/agent-ui)

Run the GUI after the CLI is done compiling

## Usage of CLI

To update the kb run scraper.py

Then run the normal app.py to use the offline models, in this mode, u cant use online models

To use the online models do `python app.py online` in this mode you cant use offline models, gemini and deepseek seem to perform best as of now.

## Helpful links

[1](https://docs.ollama.com/cloud)
