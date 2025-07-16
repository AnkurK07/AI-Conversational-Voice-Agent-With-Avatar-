 # Try the most common import patterns
try:
    # Modern LiveKit structure
    from livekit.plugins import openai
    from livekit.plugins import silero
    from livekit.plugins.openai import STT as OpenAISTT
    from livekit.plugins.openai import TTS as OpenAITTS
    USE_DIRECT_IMPORT = True
except ImportError:
    try:
        # Alternative structure
        from livekit.plugins import openai
        from livekit.plugins import silero
        from livekit.plugins.openai import stt as openai_stt
        from livekit.plugins.openai import tts as openai_tts
        USE_DIRECT_IMPORT = False
    except ImportError:
        try:
            # Older structure
            from livekit.plugins import (
                openai,
                openai_stt,
                openai_tts,
                silero,
            )
            USE_DIRECT_IMPORT = False
        except ImportError:
            print("Could not import OpenAI STT/TTS plugins. Please check your LiveKit installation.")
            print("Try: pip install --upgrade livekit livekit-agents livekit-plugins-openai livekit-plugins-silero")
            raise

