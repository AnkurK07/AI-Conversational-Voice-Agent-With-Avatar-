
"""Let's Create AI Voice Agent and make user more engaging"""

# This is AI Voice Assistant  with some basic tool integration 

from __future__ import annotations

import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai
from livekit.plugins import deepgram
from livekit.plugins import assemblyai
from livekit.plugins import silero
from livekit.plugins import bey
from livekit.agents.llm import LLMStream
from livekit.agents.tts import SynthesizedAudio
from livekit.agents.stt import SpeechEvent, SpeechEventType
from prompts import WELCOME_MESSAGE, INSTRUCTIONS, LOOKUP_VIN_MESSAGE
from tools import (
    lookup_vin,
    get_weather,
    schedule_appointment,
    get_service_history,
    check_parts_availability
)

load_dotenv()


class EnhancedVoiceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=INSTRUCTIONS,
            tools=[
                lookup_vin,
                get_weather,
                schedule_appointment,
                get_service_history,
                check_parts_availability
            ]
        )
    
    async def entrypoint(self, ctx: agents.JobContext):
        """Agent entrypoint with enhanced integrations"""
        await ctx.connect()
        
        # Wait for participant to join
        await ctx.wait_for_participant()
        
        # Create session with enhanced integrations:
        # 1. AssemblyAI STT - High accuracy speech recognition
        # 2. Cerebras LLM via OpenAI plugin - Fast inference with large models
        # 3. Deepgram TTS - High quality text-to-speech
        # 4. Beyond Presence Avatar Integration - Realistic Avatar
        # 5. Voice Activity Detection (VAD) selerio 
        # 6. End of End of Turn Utterance (Assembly.AI)
        session = AgentSession(
            # AssemblyAI Speech-to-Text
            stt=assemblyai.STT(
                end_of_turn_confidence_threshold=0.7,
                min_end_of_turn_silence_when_confident=160,
                max_turn_silence=2400,
            ),
            turn_detection="stt",
            # Cerebras LLM via OpenAI plugin
            llm=openai.LLM.with_cerebras(
                model="llama3.1-8b",
                temperature=0.7,
                #max_tokens=1000,
                # Optional parameters
                #top_p=0.9,
                # You can also try other models like:
                # model="llama3.1-70b"  # For more complex reasoning
            ),
            
            # Deepgram Text-to-Speech
            tts=deepgram.TTS(
                model="aura-asteria-en",  # High quality voice
                # You can try other voices:
                # model="aura-luna-en"
                # model="aura-stella-en"
                # model="aura-athena-en"
                # model="aura-hera-en"
                # model="aura-orion-en"
                # model="aura-arcas-en"
                # model="aura-perseus-en"
                # model="aura-angus-en"
                # model="aura-orpheus-en"
                # model="aura-helios-en"
                # model="aura-zeus-en"
            ),
            
            # Voice Activity Detection (can use AssemblyAI's VAD or default)
            vad=silero.VAD.load(),
        )
        
        # --- Beyond Presence Avatar Integration ---
        avatar = bey.AvatarSession(
            avatar_id=os.environ.get("b9be11b8-89fb-4227-8f86-4a881393cbdb"),  # <-- Set this in your .env
            # Optionally: avatar_participant_name="Agent", avatar_participant_identity="agent1"
        )
        await avatar.start(session, room=ctx.room)
        # ------------------------------------------

        await session.start(
            room=ctx.room,
            agent=self,
        )
        await session.say(WELCOME_MESSAGE)
        

    async def on_speech_event(self, event: SpeechEvent):
        """Handle speech events with enhanced processing"""
        if event.type == SpeechEventType.START_OF_SPEECH:
            print("🎤 User started speaking")
        elif event.type == SpeechEventType.END_OF_SPEECH:
            print("✋ User stopped speaking")
        elif event.type == SpeechEventType.INTERIM_TRANSCRIPT:
            print(f"📝 Interim: {event.transcript}")
        elif event.type == SpeechEventType.FINAL_TRANSCRIPT:
            print(f"✅ Final: {event.transcript}")

    async def on_llm_stream(self, stream: LLMStream):
        """Handle LLM streaming responses"""
        async for chunk in stream:
            print(f"🤖 LLM: {chunk.text}")

    async def on_tts_audio(self, audio: SynthesizedAudio):
        """Handle TTS audio generation"""
        print(f"🔊 Generated audio: {audio.duration}s")

async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint function"""
    assistant = EnhancedVoiceAssistant()
    await assistant.entrypoint(ctx)

if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )