import asyncio
import json
import time
import threading
import queue

import numpy as np
import pyaudio
import webrtcvad
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import google.generativeai as genai

# ─── Configuration ─────────────────────────────────────────────────────────────

DEEPGRAM_API_KEY = ""
GEMINI_API_KEY   = ""

FORMAT          = pyaudio.paInt16
CHANNELS        = 1
RATE            = 16000
CHUNK           = 1024
SILENCE_TIMEOUT = 1.75
MAX_RECORD_TIME = 10.0

# ─── Globals & Setup ────────────────────────────────────────────────────────

current_transcript = ""
final_transcript   = ""
is_recording       = True
transcript_ready   = asyncio.Event()

# Configure LLM
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Deepgram STT client
deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# VAD for endpointing
vad = webrtcvad.Vad(2)

# ─── Streaming TTS Class ───────────────────────────────────────────────────────

class StreamingTTS:
    def __init__(self):
        self.pyaudio        = pyaudio.PyAudio()
        self.stream         = None
        self.text_queue     = queue.Queue()
        self.audio_queue    = queue.Queue()
        self.ws             = None
        self.running        = False
        self.seq_counter    = 0
        self.flush_event    = threading.Event()
        self.pending_sequences = set()  # Track pending sequences
        self.sequence_lock = threading.Lock()

    def _next_seq(self):
        self.seq_counter += 1
        return self.seq_counter

    def start(self):
        self.running = True
        # Open audio output
        self.stream = self.pyaudio.open(
            format=FORMAT, channels=CHANNELS,
            rate=RATE, output=True, frames_per_buffer=CHUNK
        )
        # Connect WebSocket
        url = (
            f"wss://api.deepgram.com/v1/speak?"
            f"model=aura-2-thalia-en&encoding=linear16&sample_rate={RATE}"
        )
        self.ws = connect(url, additional_headers={
            "Authorization": f"Token {DEEPGRAM_API_KEY}"
        })

        # Start background threads
        threading.Thread(target=self._send_loop,   daemon=True).start()
        threading.Thread(target=self._recv_loop,   daemon=True).start()
        threading.Thread(target=self._player_loop, daemon=True).start()

    def speak(self, text: str):
        """Queue a new sentence (with a unique seq_id)."""
        if not self.running:
            return
        seq = self._next_seq()
        with self.sequence_lock:
            self.pending_sequences.add(seq)
        self.text_queue.put((seq, text))
        return seq

    def _send_loop(self):
        while self.running:
            try:
                seq, txt = self.text_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self.ws.send(json.dumps({
                    "type": "Speak",
                    "text": txt,
                    "sequence_id": seq
                }))
                print(f"🔊 TTS Sent: {txt} (seq {seq})")
            except Exception as e:
                print("❌ TTS send error:", e)
                self._reconnect()

    def _recv_loop(self):
        while self.running:
            try:
                msg = self.ws.recv()
            except ConnectionClosed as e:
                # If the socket is closed unexpectedly here, reconnect
                print("🔄 TTS WS closed, reconnecting…")
                self._reconnect()
                continue
            except Exception as e:
                print("❌ TTS recv error:", e)
                time.sleep(0.1)
                continue

            # Binary = audio, Text = control
            if isinstance(msg, bytes):
                self.audio_queue.put(msg)
            else:
                data = json.loads(msg)
                if data.get("type") == "Flushed":
                    print("🔊 TTS Flushed ack")
                    self.flush_event.set()
                elif data.get("type") == "SpeakComplete":
                    # Remove completed sequence from pending
                    seq_id = data.get("sequence_id")
                    if seq_id:
                        with self.sequence_lock:
                            self.pending_sequences.discard(seq_id)
                        print(f"🔊 TTS Complete: seq {seq_id}")

    def _player_loop(self):
        while self.running:
            try:
                chunk = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.stream.write(chunk)
            except Exception as e:
                print("❌ Audio play error:", e)

    def wait_for_all_sent(self, timeout_sec=5):
        """Wait until all queued sentences are actually sent."""
        start_time = time.time()
        while self.running and (time.time() - start_time) < timeout_sec:
            if self.text_queue.empty():
                return True
            time.sleep(0.1)
        return False

    def flush(self, timeout_sec=10):
        """Send a single Flush after all Speak messages are sent."""
        if not self.running:
            return
        
        # First wait for all sentences to be sent
        if not self.wait_for_all_sent():
            print("⚠️ Timeout waiting for all sentences to be sent")
            return
        
        # Small delay to ensure all are processed
        time.sleep(0.2)
        
        self.flush_event.clear()
        try:
            self.ws.send(json.dumps({"type": "Flush"}))
            print("🚰 Flush sent, waiting for ack…")
        except Exception as e:
            print("❌ Flush send error:", e)
            return
        if not self.flush_event.wait(timeout_sec):
            print("⚠️ Flush timeout")
        else:
            print("✅ Flush acknowledged")

    def _reconnect(self):
        """Reconnect the WebSocket if it drops."""
        try:
            if self.ws:
                self.ws.close()
        except:
            pass

        url = (
            f"wss://api.deepgram.com/v1/speak?"
            f"model=aura-2-thalia-en&encoding=linear16&sample_rate={RATE}"
        )
        try:
            self.ws = connect(url, additional_headers={
                "Authorization": f"Token {DEEPGRAM_API_KEY}"
            })
            print("🔄 TTS WS reconnected")
        except Exception as e:
            print("❌ Reconnect failed:", e)

    def stop(self):
        self.running = False
        try: self.ws.close()
        except: pass
        try: self.stream.close()
        except: pass
        self.pyaudio.terminate()

# ─── Helpers: VAD, STT callbacks ────────────────────────────────────────────────

def detect_speech_fast(audio_np: np.ndarray) -> bool:
    if len(audio_np) < 320:
        return False
    audio_int16 = np.clip(audio_np*32768, -32768, 32767).astype(np.int16)
    speech, total = 0, 0
    for i in range(0, len(audio_int16)-320, 160):
        if vad.is_speech(audio_int16[i:i+320].tobytes(), RATE):
            speech += 1
        total += 1
        if total >= 3:
            break
    return (speech/total) > 0.4 if total else False

def on_transcript(_, result, **__):
    """Deepgram STT callback for each transcript event."""
    global final_transcript, is_recording
    text = result.channel.alternatives[0].transcript
    if not text:
        return
    kind = "Final" if result.is_final else "Interim"
    print(f"📝 {kind}: {text}")
    if result.is_final:
        final_transcript = text
        is_recording     = False
        transcript_ready.set()
        print(f"✅ Final transcript: {final_transcript}")

def on_error(_, error, **__):
    # Ignore Deepgram's "net0001" internal‐timeout close
    msg = getattr(error, "message", "") or error.get("message", "")
    if "net0001" in msg:
        return
    print("❌ STT Error:", error)

# ─── Async Tasks: stream_audio & stream_llm_response ──────────────────────────

async def stream_audio():
    """Record mic → Deepgram STT with aggressive endpointing."""
    global is_recording
    print("🎤 Starting ultra-fast recording…")
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS,
                     rate=RATE, input=True, frames_per_buffer=CHUNK)

    dg_conn = deepgram.listen.websocket.v("1")
    dg_conn.on(LiveTranscriptionEvents.Transcript, on_transcript)
    dg_conn.on(LiveTranscriptionEvents.Error,      on_error)

    opts = LiveOptions(
        model="nova-2", language="en-US", encoding="linear16",
        channels=1, sample_rate=RATE, interim_results=True,
        punctuate=True, smart_format=True, endpointing=100
    )

    is_recording = True
    start_time   = time.time()

    if dg_conn.start(opts):
        try:
            while is_recording and (time.time()-start_time)<MAX_RECORD_TIME:
                data = stream.read(CHUNK, exception_on_overflow=False)
                dg_conn.send(data)
                # we rely on Deepgram endpointing, so we just keep feeding
                await asyncio.sleep(0.001)
        except Exception as e:
            print("❌ Recording error:", e)
        finally:
            dg_conn.finish()

    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("🛑 Recording stopped")

async def stream_llm_response(prompt: str, tts: StreamingTTS):
    """Generate LLM answer → queue all sentences → wait for all to be sent → then flush."""
    print(f"💭 Generating answer for: {prompt}")
    chat = model.start_chat()
    stream = chat.send_message(f"Answer briefly in 2–3 short sentences: {prompt}", stream=True)

    buffer = ""
    count  = 0

    for chunk in stream:
        buffer += chunk.text
        while True:
            idxs = [buffer.find(p) for p in (".","!","?") if buffer.find(p)>=0]
            if not idxs:
                break
            idx = min(idxs)
            sent = buffer[:idx+1].strip()
            buffer = buffer[idx+1:].strip()
            if len(sent) > 3:
                count += 1
                print(f"💬 Sentence {count}: {sent}")
                tts.speak(sent)

    if buffer.strip():
        count += 1
        print(f"💬 Sentence {count}: {buffer.strip()}")
        tts.speak(buffer.strip())

    print(f"✅ Generated {count} sentences; now waiting for all to be sent…")
    
    # Wait for all sentences to be sent, then flush
    tts.flush()

    # wait for the audio queue to drain
    while not tts.audio_queue.empty():
        await asyncio.sleep(0.05)

# ─── Main ─────────────────────────────────────────────────────────────────────

async def main():
    print("🚀 Voice Assistant Starting…")
    tts = StreamingTTS()
    tts.start()

    record_task = asyncio.create_task(stream_audio())
    await transcript_ready.wait()

    if final_transcript:
        print(f"⚡ Transcript ready: {final_transcript}")
        await stream_llm_response(final_transcript, tts)
    else:
        print("❌ No transcript received")

    await record_task
    tts.stop()
    print("✅ Voice Assistant finished")

if __name__ == "__main__":
    asyncio.run(main())