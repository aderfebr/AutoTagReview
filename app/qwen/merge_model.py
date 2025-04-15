from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model_path = 'Qwen2.5-0.5B-Instruct'
lora_path = 'qwen_lora'

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True).eval()
lora_model = PeftModel.from_pretrained(base_model, model_id=lora_path)

merge_model = lora_model.merge_and_unload()
merge_model.save_pretrained('qwen_sft')