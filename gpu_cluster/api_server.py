"""
accelerate launch --multi_gpu --num_processes 3 \
    --machine_rank 1 --main_process_ip 10.8.10.91 \
        --main_process_port 29500 api_server.py
"""


import os
import time
import torch
import transformers
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import torch.distributed as dist
import atexit
from transformers import TextIteratorStreamer
import threading
import asyncio
from fastapi.responses import StreamingResponse

# Initialize torch distributed
if not dist.is_initialized():
    dist.init_process_group(backend="nccl")

local_rank = dist.get_rank()

model_id = "nvidia/Llama-3.1-Nemotron-8B-UltraLong-4M-Instruct"

# Load model + tokenizer
tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="balanced_low_0"
)

print(f"model serving - rank {local_rank}")

# Register clean shutdown
@atexit.register
def cleanup():
    if dist.is_initialized():
        dist.destroy_process_group()
        print(f"Rank {local_rank}: cleaned up distributed process group")

# Rank 0 runs FastAPI
if local_rank == 0:
    app = FastAPI()

    class Query(BaseModel):
        text: str

    @app.post("/ask")
    async def ask(query: Query):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides answers as per the instructions from the user"},
            {"role": "user", "content": query.text},
        ]

        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=4096,
        )

        thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()

        async def stream_response():
            for new_text in streamer:
                yield new_text
                await asyncio.sleep(0.01)

        return StreamingResponse(stream_response(), media_type="text/plain")

    def start_server():
        uvicorn.run(app, host="0.0.0.0", port=5000)

    if __name__ != "__main__":
        import threading
        threading.Thread(target=start_server, daemon=True).start()
    else:
        start_server()

    # Prevent rank 0 from exiting early
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Rank 0: Shutting down...")

else:
    # Other ranks just idle
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"Rank {local_rank}: Shutting down...")
