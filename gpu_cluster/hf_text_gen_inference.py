import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="cuda",
)

streamer = TextStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)

# Prepare the prompt from messages
messages = [
    {"role": "system", "content": "you are an assistant who follows user instructions. do not start your response with assistant word, start directly with your answer"},
    {"role": "user", "content": "tell me who is the president of usa, also tell more about him in one para"},
]

prompt = tokenizer.apply_chat_template(messages, tokenize=False)

# Create pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,)

print()
# Extract just the response text from the output
output=generator(prompt, streamer=streamer, max_new_tokens=2048)
