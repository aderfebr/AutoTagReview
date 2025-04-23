import json
from datetime import datetime
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from django.core.paginator import Paginator
from .AKE.predict_qwen import predict_qwen
from .AKE.AKE import tfidf,lda,textrank

tokenizer_path = './app/AKE/Qwen2.5-0.5B-Instruct'
path1 = './app/AKE/qwen_sft'
path2 = './app/AKE/Qwen2.5-0.5B-Instruct'

from .models import Taghistory
def compare(request):
    data = json.loads(request.body)
    input_text = data.get('input', '')
    
    def generate_stream():
        res1=tfidf(input_text)
        yield json.dumps({'algorithm': 'tfidf','result': res1}) + '\n'

        res2=lda(input_text)
        yield json.dumps({'algorithm': 'lda','result': res2}) + '\n'

        res3=textrank(input_text)
        yield json.dumps({'algorithm': 'textrank','result': res3}) + '\n'

        res4 = predict_qwen(tokenizer_path, path2, input_text)
        res4 = res4.split("/")
        yield json.dumps({'algorithm': 'llm_wo','result': res4}) + '\n'

        res5 = predict_qwen(tokenizer_path, path1, input_text)
        res5 = res5.split("/")
        yield json.dumps({'algorithm': 'llm_w','result': res5}) + '\n'

        tag = Taghistory(comment=input_text,tfidf='/'.join(res1),lda='/'.join(res2),textrank='/'.join(res3),llm_wo='/'.join(res4),llm_w='/'.join(res5),time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        tag.save()

    return StreamingHttpResponse(generate_stream(), content_type='application/json')

from .models import Review
def review(request):
    product_id = request.GET.get('product_id')
    page_number = request.GET.get('page', 1)
    all = request.GET.get('all')
    
    if all:
        reviews = Review.objects.all()
    else:
        reviews = Review.objects.filter(product_id=product_id)

    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page_number)
    
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': [
            {
                'product_id': i.product_id,
                'review': i.review,
                'time': i.time,
                'nickname': i.nickname,
            } 
            for i in page_obj
        ]
    }
    return JsonResponse(response_data)

from .models import Taghistory
def taghistory(request):
    page_number = request.GET.get('page', 1)
    
    history = Taghistory.objects.all()
    paginator = Paginator(history, 10)
    page_obj = paginator.get_page(page_number)
    
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': [
            {
                'comment': i.comment,
                'tfidf': i.tfidf.split('/'),
                'lda': i.lda.split('/'),
                'textrank': i.textrank.split('/'),
                'llm_wo': i.llm_wo.split('/'),
                'llm_w': i.llm_w.split('/'),
                'time':i.time,
            } 
            for i in page_obj
        ]
    }
    return JsonResponse(response_data)

def cleartaghistory(request):
    deleted_count = Taghistory.objects.all().delete()
    return JsonResponse({
        'status': 'success',
        'message': f'成功清空 {deleted_count} 条历史记录'
    }, status=200)