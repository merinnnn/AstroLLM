import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from huggingface_hub import login
from config import HUGGING_FACE_TOKEN

model_id = "meta-llama/Llama-3.2-3B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)
streamer = TextIteratorStreamer(tokenizer)

prompt = "Explain quantum computing in simple terms."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7, top_p=0.9, streamer=streamer)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
