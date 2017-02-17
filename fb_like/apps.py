from __future__ import unicode_literals

import os
import json
import urllib2
import pandas as pd
import utils.config as Config

from constants import *
from facepy import utils,GraphAPI
from itertools import islice
from datetime import datetime
from django.apps import AppConfig

class FbLikeConfig(AppConfig):
    name = 'fb_like'


class FbAPI(object):
	def __init__(self):
		app_id = Config.get_value('authentication', 'app_id')
		app_secret = Config.get_value('authentication', 'app_secret')

		self.oath_access_token = None
		if self.oath_access_token is None:
			self.oath_access_token = utils.get_application_access_token(app_id, app_secret)

		self.graph = GraphAPI(self.oath_access_token)

	def get_token(self):
		return self.oath_access_token

	def get_posts(self, page_name, index = 0):

		post_page = self.graph.get(POSTS_STR % page_name, page = True, limit=25)
		data = next(islice(post_page, index, index+1))['data']
		df = pd.DataFrame(data).fillna('')
		source_format = '%Y-%m-%dT%H:%M:%S'
		target_format = '%Y/%m/%d %H:%M:%S'
		datetime_parser = lambda d: (datetime.strptime(str(d)[:-5], source_format)).strftime(target_format)
		df['created_time'] = df['created_time'].apply(datetime_parser)

		return df.values.tolist(), list(df.columns)

	def get_likes(self, post_id):
		index = 0
		like_list = self.graph.get(LIKES_STR % (post_id, ''), page = True, limit=25, summary = 1)
		response = next(islice(like_list, index, index+1))
		data = response['data']
		df = pd.DataFrame(data).fillna('')

		counts = int(response['summary']['total_count'])
		return df.values.tolist(), list(df.columns), counts

	def get_likes_export(self, post_id):
		query_url = "https://graph.facebook.com/%s/likes?summary=true&limit=1000000&access_token=%s" % (
				post_id,
				self.oath_access_token
			)
		web_response = urllib2.urlopen(query_url)
		json_obj = json.loads(web_response.read())
		df = pd.DataFrame(json_obj['data']).fillna('')

		file_name = 'likes_lst_post_id_%s.csv' % post_id
		full_path = SAVE_PATH % file_name
		df.to_csv(full_path, index = False, encoding='utf-8')

		return full_path, file_name