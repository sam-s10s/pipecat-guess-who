# Speechmatics + Pipecat Guess Who?

A gameplay agent that uses Speechmatics STT and Pipecat to play the classic game of Guess Who?

## What you will need

You will need the following for this demo to work.

- Speechmatics API key
- ElevenLabs API key
- OpenAI API key

## Setup

```shell
# install a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# copy the .env-example to .env and fill in the values
cp .env-example .env

# run the demo
python agent.py
```
