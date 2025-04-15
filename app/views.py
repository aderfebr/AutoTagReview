import json
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from .qwen.predict_qwen import predict_qwen

def compare(request):
    data = json.loads(request.body)
    input_text = data.get('input', '')

    tokenizer_path = './app/qwen/Qwen2.5-0.5B-Instruct'
    path1 = './app/qwen/qwen_sft'
    path2 = './app/qwen/Qwen2.5-0.5B-Instruct'

    def generate_stream():
        res = predict_qwen(tokenizer_path, path2, input_text)
        res = res.split("/")
        yield json.dumps({'res_wo': res}) + '\n'

        res = predict_qwen(tokenizer_path, path1, input_text)
        res = res.split("/")
        yield json.dumps({'res_w': res}) + '\n'
    
    response = StreamingHttpResponse(generate_stream(), content_type='application/json')
    return response