# Speechmatics + Pipecat Guess Who?

A voice-powered AI agent that plays the classic game of Guess Who? using [Speechmatics](https://www.speechmatics.com/) for real-time speech recognition, [Pipecat](https://github.com/pipecat-ai/pipecat) for conversational AI pipeline orchestration, and OpenAI for intelligent gameplay.

## About This Demo

This demo showcases how to build a conversational AI game using:

- **Speechmatics STT** for accurate real-time speech-to-text with speaker diarization
- **Pipecat framework** for managing the conversational AI pipeline
- **OpenAI GPT** for intelligent game logic and responses
- **ElevenLabs TTS** for natural voice synthesis

The agent can understand speech, maintain game state, ask strategic questions, and make educated guesses about your chosen character.

## Prerequisites

You'll need API keys for the following services:

- **Speechmatics API key** - Get yours at [portal.speechmatics.com](https://portal.speechmatics.com)
- **ElevenLabs API key** - For voice synthesis at [elevenlabs.io](https://elevenlabs.io)
- **OpenAI API key** - For ChatGPT models at [platform.openai.com](https://platform.openai.com)

## Quick Start

```shell
# Clone and navigate to the project
git clone <repository-url>
cd pipecat-guess-who

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env-example .env
# Edit .env with your API keys

# Run the demo
python agent.py
```

## Configuration

Edit the `.env` file with your API credentials:

```env
SPEECHMATICS_API_KEY=your-speechmatics-api-key-here
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

## How to Play

1. Start the application with `python agent.py`
2. Think of a character from the classic Guess Who? game
3. The AI will ask yes/no questions about your character
4. Answer with "yes" or "no"
5. The AI will try to guess your character!

## Technical Details

- Uses Speechmatics' WebSocket API for real-time transcription
- Leverages speaker diarization to distinguish between user and agent speech
- Built on the Pipecat framework for robust conversational AI pipelines
- Supports both Daily.co and WebRTC transport layers

## Resources

- [Speechmatics API Documentation](https://docs.speechmatics.com/api-ref/realtime-transcription-websocket)
- [Pipecat Framework](https://github.com/pipecat-ai/pipecat)
- [Speechmatics STT Plugin](https://github.com/pipecat-ai/pipecat/blob/main/src/pipecat/services/speechmatics/stt.py)
