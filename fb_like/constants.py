import os
from server import settings

POSTS_STR = '%s/posts'
LIKES_STR = '%s/likes?summary=true%s'
SAVE_PATH = os.path.join(settings.BASE_DIR, "mediate_data/%s")