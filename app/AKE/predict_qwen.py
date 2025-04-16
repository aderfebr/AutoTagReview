from transformers import AutoModelForCausalLM, AutoTokenizer

def predict_qwen(tokenizer_path,model_path,input):
    ins='''你是一个专业的关键词提取助手，我将提供一条电商产品的用户评论，你需要提取其中的关键词。
    注意事项：每个关键词尽可能以名词+副词的形式给出，关键词应具有差异性，各个关键词之间以\分割，只输出答案，不要输出其他内容。
    正例：
    输入：手机不仅好看价格也便宜，还有屏幕音效的效果也很好
    输出：外观好看/价格便宜/屏幕效果好/音效效果好
    解释：除结果之外没有多余的文字，提取的关键词准确且具有差异性
    反例：
    输入：这个鼠标紫色颜色特别喜欢，性能出色，按键清脆，大小合适手感不错很舒服，握半天不累，反应速度快。精准度很高，外观漂亮，性价比高。
    输出：好的，以下是一种可能的关键词提取结果：鼠标紫色/外观漂亮/按键清脆/大小合适/手感不错/很舒服/反应速度快/精准度高/外观漂亮/性价比高
    解释：在结果之前有无关的文字，提取的关键词中外观漂亮重复了两次，颜色可被归为外观漂亮
    请对以下商品评论进行关键词提取:
    '''
    messages = [
        {"role": "user", "content": ins+input}
    ]

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, trust_remote_code=True)
    
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", trust_remote_code=True).eval()
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    res = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return res