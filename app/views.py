import json
from datetime import datetime
from django.http import JsonResponse,HttpResponse,StreamingHttpResponse
from django.core.paginator import Paginator
from bson import ObjectId
from .AKE.AKE import tfidf,lda,textrank
from .AKE.predict_qwen import predict_qwen
from .AKE.visualize import visualize

tokenizer_path = './app/AKE/Qwen2.5-0.5B-Instruct'
llm_w = './app/AKE/qwen_sft'
llm_wo = './app/AKE/Qwen2.5-0.5B-Instruct'

from .models import Taghistory
def tag(request):
    data = json.loads(request.body)
    input_text = data.get('input', '')
    
    def generate_stream():
        res1=tfidf(input_text)
        yield json.dumps({'algorithm': 'tfidf','result': res1}) + '\n'

        res2=lda(input_text)
        yield json.dumps({'algorithm': 'lda','result': res2}) + '\n'

        res3=textrank(input_text)
        yield json.dumps({'algorithm': 'textrank','result': res3}) + '\n'

        res4 = predict_qwen(tokenizer_path, llm_wo, input_text)
        res4 = res4.split("/")
        yield json.dumps({'algorithm': 'llm_wo','result': res4}) + '\n'

        res5 = predict_qwen(tokenizer_path, llm_w, input_text)
        res5 = res5.split("/")
        yield json.dumps({'algorithm': 'llm_w','result': res5}) + '\n'

        tag = Taghistory(comment=input_text,tfidf='/'.join(res1),lda='/'.join(res2),textrank='/'.join(res3),llm_wo='/'.join(res4),llm_w='/'.join(res5),time=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        tag.save()

    return StreamingHttpResponse(generate_stream(), content_type='application/json')

from .models import Product
def product(request):
    page_number = request.GET.get('page', 1)
    all = request.GET.get('all')
    
    if all:
        products = Product.objects.all()
    else:
        type = request.GET.get('type')
        query = request.GET.get('query')
        if type=='product_id':
            products = Product.objects.filter(product_id=query)
        elif type=='title':
            products = Product.objects.filter(title__icontains=query)
        else :
            products = Product.objects.filter(category__icontains=query)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)
    
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
        'results': [
            {
                'category': i.category,
                'product_id': i.product_id,
                'title': i.title,
                'img': i.img,
            } 
            for i in page_obj
        ]
    }
    return JsonResponse(response_data)

from .models import Review
def review(request):
    page_number = request.GET.get('page', 1)
    all = request.GET.get('all')
    
    if all:
        reviews = Review.objects.all()
    else:
        product_id = request.GET.get('product_id')
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
                'id': str(i.id),
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

def visualization(request):
    id = request.GET.get('id')

    history = Taghistory.objects.filter(id=ObjectId(id))[0]
    phrases = {
        'TF-IDF': history.tfidf.split('/'),
        'LDA': history.lda.split('/'),
        'TextRank': history.textrank.split('/'),
        'LLM（无微调）': history.llm_wo.split('/'),
        'LLM（微调）': history.llm_w.split('/'),
    }

    by_type, by_cluster = visualize(phrases)

    response_data = {
        'history': {
        'comment': history.comment,
        'tfidf': history.tfidf.split('/'),
        'lda': history.lda.split('/'),
        'textrank': history.textrank.split('/'),
        'llm_wo': history.llm_wo.split('/'),
        'llm_w': history.llm_w.split('/'),
        },
        'type': by_type, 
        'cluster': by_cluster,
    }
    return JsonResponse(response_data)