import json
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from .AKE.predict_qwen import predict_qwen
from .AKE.AKE import tfidf,lda,textrank

def compare(request):
    data = json.loads(request.body)
    input_text = data.get('input', '')

    tokenizer_path = './app/AKE/Qwen2.5-0.5B-Instruct'
    path1 = './app/AKE/qwen_sft'
    path2 = './app/AKE/Qwen2.5-0.5B-Instruct'

    def generate_stream():
        res=tfidf(input_text)
        yield json.dumps({'algorithm': 'tfidf','result': res}) + '\n'

        res=lda(input_text)
        yield json.dumps({'algorithm': 'lda','result': res}) + '\n'

        res=textrank(input_text)
        yield json.dumps({'algorithm': 'textrank','result': res}) + '\n'

        res = predict_qwen(tokenizer_path, path2, input_text)
        res = res.split("/")
        yield json.dumps({'algorithm': 'llm_wo','result': res}) + '\n'

        res = predict_qwen(tokenizer_path, path1, input_text)
        res = res.split("/")
        yield json.dumps({'algorithm': 'llm_w','result': res}) + '\n'
    
    response = StreamingHttpResponse(generate_stream(), content_type='application/json')
    return response