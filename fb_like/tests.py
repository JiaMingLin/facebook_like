from django.test import TestCase
from apps import FbAPI

class TestFbAPI(TestCase):
	def setUp(self):
		self.page_name = 'playingforchange'
		self.post_id = '67757651619_10154745877826620'
		self.fb_instance = FbAPI()

	def test_get_token(self):
		token = self.fb_instance.get_token()
		
	def test_get_posts(self):
		posts = self.fb_instance.get_posts(self.page_name)
	
	def test_get_posts_paging(self):
		posts = self.fb_instance.get_posts(self.page_name, index = 1)
		posts = self.fb_instance.get_posts(self.page_name, index = 2)

		
	def test_get_likes(self):
		likes, columns, counts = self.fb_instance.get_likes(self.post_id)
		self.assertEqual(columns, ['id', 'name'])

	def test_get_likes_export(self):
		csv_path = self.fb_instance.get_likes_export(self.post_id)
		import os
		import pandas as pd
		from server import settings
		csv_path, short = os.path.join(settings.BASE_DIR, csv_path)

		df = pd.read_csv(csv_path)
		columns = list(df.columns)
		self.assertEqual(columns, ['id', 'name'])
