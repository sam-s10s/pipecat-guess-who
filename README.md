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
cp dot-env.template .env
# Edit .env with your API keys

# Run the demo
python agent.py
```

### Running on an ESP32

As with most audio agents created using Pipecat, it is possible to use an ESP32 device as the audio interface. For further information on this, please see the [Pipecat Docs](https://github.com/pipecat-ai/pipecat-esp32).

Change the host IP address (`0.0.0.0`) to the IP address of the machine you run this command on. You will also need to make sure both your machine and the ESP32 device are on the same network and the ESP32 device has been flashed with the custom firmware.

**NOTE:** By default, the ESP32 will mute the microphone while the agent is speaking. This means that it is not possible to interrupt the agent. We will be releasing an update to this in the future.

```shell
# Start the agent for ESP32 access
python agent.py --host 0.0.0.0 --esp32
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
2. Go to `http://localhost:7860/` in your browser
3. Think of a character from the classic Guess Who? game
4. The AI will ask yes/no questions about your character
5. Answer with "yes" or "no"
6. The AI will try to guess your character!

## Run using Daily

If you are unable to use WebRTC directly (depending on your system's security), you can use the Daily platform instead. You will need to have a [Daily account](https://daily.co) and create a room that the agent can join.

Add the following to your `.env` file:

```env
DAILY_API_KEY=your-daily-api-key-here
DAILY_SAMPLE_ROOM_URL=your-daily-room-url-here
```

Now run the agent with the `--transport daily` flag:

```shell
# Run using Daily
python agent.py --transport daily
```

## Technical Details

- Uses Speechmatics' WebSocket API for real-time transcription
- Leverages speaker diarization to distinguish between user and agent speech
- Built on the Pipecat framework for robust conversational AI pipelines
- Supports both Daily.co and WebRTC transport layers

## Resources

- [Speechmatics API Documentation](https://docs.speechmatics.com/api-ref/realtime-transcription-websocket)
- [Pipecat Framework](https://github.com/pipecat-ai/pipecat)
- [Speechmatics STT Plugin](https://github.com/pipecat-ai/pipecat/blob/main/src/pipecat/services/speechmatics/stt.py)
