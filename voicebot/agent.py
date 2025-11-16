from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    deepgram,
    google,
    silero,
    noise_cancellation,
)

load_dotenv()

# Agent Instructions (can dynamically change during session)
class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant. Speak concisely and clearly.")

# Entrypoint for Agent Worker
async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt = deepgram.STT(),
        llm=google.LLM(model="gemini-2.5-flash", temperature=0.5),
        tts = deepgram.TTS(),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),  # Optional for self-hosted
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Welcome! I’m your voice assistant. How can I help?"
    )

# Run in CLI or LiveKit cloud
if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
