import os
from dotenv import load_dotenv
load_dotenv()

AWS_SERVICE_NAME = os.environ.get('AWS_SERVICE_NAME')
AWS_REGION = os.environ.get('AWS_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.environ.get('AWS_BUCKET')

MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')
MONGODB_IMAGE_COLLECTION_NAME = os.environ.get('MONGODB_IMAGE_COLLECTION_NAME')
MONGODB_GROUPS_COLLECTION_NAME = os.environ.get(
                                            'MONGODB_GROUPS_COLLECTION_NAME'
                                            )

IMAGE_FOLDER_NAME = os.environ.get('IMAGE_FOLDER_NAME')
