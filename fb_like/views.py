import json
from apps import FbAPI
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import pandas as pd

# Create your views here.
facebook = FbAPI()

def index(request):
	return render(request, 'index.html', {
		'current_time': str(datetime.now()),
	})

def get_posts(request):
	if request.is_ajax() is False:
		return HttpResponse("The API can only be called from ajax.")

	request_data = request.POST
	page_name = request_data['page_name']
	index = request_data['index'] if 'index' in request_data.keys() else 0
	index = int(index)
	result = {}
	if len(page_name) > 0:
		data, columns = facebook.get_posts(page_name, index = index)
		result['columns'] = [{'title': col} for col in columns]
		result['data'] = data

	return HttpResponse(json.dumps(result), content_type='application/json')

def get_likes(request):
	if request.is_ajax() is False:
		return HttpResponse("The API can only be called from ajax.")

	request_data = request.POST
	post_id = request_data['post_id']
	data, columns, counts = facebook.get_likes(post_id)
	file_path, short_path = facebook.get_likes_export(post_id)
	result = {}
	result['columns'] = [{'title': col} for col in columns]
	result['data'] = data
	result['counts'] = counts
	result['path'] = short_path

	return HttpResponse(json.dumps(result), content_type='application/json')

