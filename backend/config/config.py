import os
from dotenv import load_dotenv


load_dotenv()

# get data from environment variables
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')
MONGODB_IMAGE_COLLECTION_NAME = os.environ.get('MONGODB_IMAGE_COLLECTION_NAME')
MONGODB_GROUPS_COLLECTION_NAME = os.environ.get(
                                            'MONGODB_GROUPS_COLLECTION_NAME'
                                            )

# config flask app
FLASK_DEBUG = False
FLASK_HOST = "127.0.0.1" if FLASK_DEBUG else "0.0.0.0"

# constants
VALID_STATUSES = ['new', 'review', 'accepted', 'deleted']
STATISTIC_NUMBER_OF_DAYS = 30
