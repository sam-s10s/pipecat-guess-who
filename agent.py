#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import argparse
import os

from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_response import (
    LLMUserAggregatorParams,
)
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
from pipecat.services.openai.base_llm import BaseOpenAILLMService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.speechmatics.stt import SpeechmaticsSTTService
from pipecat.transcriptions.language import Language
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.services.daily import DailyParams

load_dotenv()


transport_params = {
    "daily": lambda: DailyParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
    ),
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
    ),
}


async def run_example(
    transport: BaseTransport, _: argparse.Namespace, handle_sigint: bool
):
    """Run Guess Who using Speechmatics STT.

    This uses the diarization feature of the Speechmatics STT engine to give the LLM
    context about who has spoken. This is a simple example of how to use diarization
    with Pipecat.

    The agent will know who is speaking and can use this information to respond
    appropriately. Try speaking out of turn and you should hear the agent tell you
    that it's not your turn!
    """
    logger.info("Starting bot")

    # Load the full system context from file
    AGENT_CONTEXT = open("agent.md", "r").read()

    # Initialize the Speechmatics STT service
    stt = SpeechmaticsSTTService(
        api_key=os.getenv("SPEECHMATICS_API_KEY"),
        language=Language.EN,
        enable_speaker_diarization=True,
        text_format="<{speaker_id}>{text}</{speaker_id}>",
    )

    # Initialize the OpenAI LLM service
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"),
        params=BaseOpenAILLMService.InputParams(temperature=0.75),
    )

    # Initialize the TTS service
    tts = ElevenLabsTTSService(
        api_key=os.getenv("ELEVENLABS_API_KEY"),
        voice_id="97U3B7htAA7UsCIDST8b",
        model="eleven_turbo_v2_5",
    )

    # Setup the messages using the context
    messages = [
        {"role": "system", "content": AGENT_CONTEXT},
    ]

    # Initialize the OpenAI LLM context
    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(
        context,
        user_params=LLMUserAggregatorParams(aggregation_timeout=0.005),
    )

    # Initialize the agent pipeline
    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            context_aggregator.user(),
            llm,
            tts,
            transport.output(),
            context_aggregator.assistant(),
        ]
    )

    # Initialize the pipeline task
    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )

    # Handle client connection
    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Client connected")
        messages.append(
            {
                "role": "system",
                "content": "Say a short hello and find out who's up for playing.",
            }
        )
        await task.queue_frames([context_aggregator.user().get_context_frame()])

    # Handle client disconnection
    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    # Initialize the pipeline runner
    runner = PipelineRunner(handle_sigint=handle_sigint)

    # Run the pipeline
    await runner.run(task)


if __name__ == "__main__":
    from pipecat.examples.run import main

    main(run_example, transport_params=transport_params)
