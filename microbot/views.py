import json
import datetime
from django.http import JsonResponse
from Crawling.Crawl import Crawl
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def crawl(request):
        req = (request.body.decode('utf-8'))
        return_json_str = json.loads(req)
        mid = return_json_str['mid']

        obj = Crawl(mid)
        obj.main()

        F_json = {'time': str(datetime.datetime.now()), 'api': 'item_detail', 'data': obj.data_list}

        return JsonResponse(F_json)
