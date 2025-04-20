import json
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from django.core.paginator import Paginator
from .AKE.predict_qwen import predict_qwen
from .AKE.AKE import tfidf,lda,textrank

tokenizer_path = './app/AKE/Qwen2.5-0.5B-Instruct'
path1 = './app/AKE/qwen_sft'
path2 = './app/AKE/Qwen2.5-0.5B-Instruct'

def generate_stream(input_text, tokenizer_path, path1, path2):
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
    


def compare(request):
    data = json.loads(request.body)
    input_text = data.get('input', '')

    response = StreamingHttpResponse(generate_stream(input_text, tokenizer_path, path1, path2), content_type='application/json')
    return response


from .models import Review
def review(request):
    product_id = request.GET.get('product_id', 1)
    page_number = request.GET.get('page', 1)
    
    reviews = Review.objects.filter(product_id=product_id)
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page_number)
    
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': [
            {
                'product_id': review.product_id,
                'review': review.review,
            } 
            for review in page_obj
        ]
    }
    
    return JsonResponse(response_data)