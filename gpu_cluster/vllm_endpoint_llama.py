"""
python3 -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --block-size 32 \
    --max-model-len 1024 \
    --max-num-seqs 512 \
    --disable-log-requests
"""

import requests
import json

def stream_response():
    response = requests.post(
        "http://10.8.10.91:8000/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "meta-llama/Llama-3.1-8B-Instruct",
            "messages": [{"role": "user", "content": "tell me who is president of india, tell me more about him"}],
            "max_tokens": 900,
            "stream": True  # Enable streaming
        },
        stream=True  # Enable streaming at the request level
    )
    
    # Process the streamed response
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8')
            # Skip the "data: " prefix and empty lines
            if line_text.startswith('data: '):
                data_str = line_text[6:]  # Remove 'data: ' prefix
                if data_str.strip() == '[DONE]':
                    break
                try:
                    data = json.loads(data_str)
                    # Extract and print the content delta
                    if 'choices' in data and len(data['choices']) > 0:
                        delta = data['choices'][0].get('delta', {})
                        if 'content' in delta and delta['content']:
                            print(delta['content'], end='', flush=True)
                except json.JSONDecodeError:
                    pass

# Call the function
stream_response()
print()  # Add a new line at the end










# Script
"""python3 -m vllm.entrypoints.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --dtype bfloat16 \
    --gpu-memory-utilization 0.85 \
    --block-size 32 \
    --max-model-len 4096 \
    --max-num-seqs 512 \
    --disable-log-requests
"""

from vllm import LLM

# Initialize LLM with your custom settings
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",   # path to your model folder
    dtype="float16",                 # force float16 for saving memory
    gpu_memory_utilization=0.8,      # use 70% of VRAM
    block_size=16,                   # smaller block size for fitting in 24GB
    max_model_len=1024               # smaller context window
)

# Now you can generate text
outputs = llm.generate(["Hello, how are you?"])

for output in outputs:
    print(output.outputs[0].text)
