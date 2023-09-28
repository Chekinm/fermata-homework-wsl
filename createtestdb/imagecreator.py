from PIL import Image, ImageDraw
import boto3
import botocore
from pymongo import MongoClient
from datetime import datetime
from config import (AWS_SERVICE_NAME,
                    AWS_ACCESS_KEY_ID,
                    AWS_SECRET_ACCESS_KEY,
                    AWS_BUCKET,
                    AWS_REGION,
                    MONGODB_URI,
                    MONGODB_DB_NAME,
                    MONGODB_IMAGE_COLLECTION_NAME,
                    MONGODB_GROUPS_COLLECTION_NAME,
                    IMAGE_FOLDER_NAME
                    )


# initilize AWS connection
s3_client = boto3.client(AWS_SERVICE_NAME,
                         region_name=AWS_REGION,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         )

# initilise MONGODB database
client = MongoClient(MONGODB_URI)

db = client[MONGODB_DB_NAME]
images_collection = db[MONGODB_IMAGE_COLLECTION_NAME]
groups_collection = db[MONGODB_GROUPS_COLLECTION_NAME]


# clean database
images_collection.delete_many({})
groups_collection.delete_many({})

# create images and database entry
statuses = ["new", "review", "accepted", "deleted"]


def create_image_in_aws(image_number,
                        group_number,
                        aws_client_instance,
                        aws_bucket,
                        aws_service_name,
                        aws_region_name,
                        ):
    """Creates a test image with text containing image number and group number,
    then uploads this image to an AWS S3 bucket with corresponging name

    Args:
        image_number (int): The image number to be included in the
            text and file name.
        group_number (int): The group number to be included
            in the text and file name.
        aws_client_instance (boto3.client): An initialized
            AWS S3 client instance.
        aws_bucket (str): The name of the AWS S3 bucket where the
            image will be uploaded.
        aws_service_name (str): The AWS service name (e.g., 's3').
        aws_region_name (str): The AWS region name,
            where the S3 bucket is located.

    Returns:
        str: The URL of the uploaded image in the following format:
             https://<aws_bucket>.<aws_service_name>.<aws_region_name>.amazonaws.com/<file_name>

    """
    img = Image.new('RGB', (300, 300))
    draw = ImageDraw.Draw(img)
    txt = (f"This is a test image\n"
           f"Image number: {image_number}\n"
           f"Group number: {group_number}"
           )
    draw.text((100, 100), txt, fill=(255, 255, 255))
    file_name = f"{IMAGE_FOLDER_NAME}/group_{group_number}_image_{image_number}.png"
    img.save(file_name)
    try:
        aws_client_instance.upload_file(file_name, aws_bucket, file_name)
        print(f"{file_name} was created and uploaded successfuly")
        # return url of the uploaded file
        return (f"https://{aws_bucket}.{aws_service_name}.{aws_region_name}"
                f".amazonaws.com/{file_name}")
    except botocore.exceptions.ClientError as e:
        print("Upload failed: ", e)


# availabel statuses
statuses = ["new", "review", "accepted", "deleted"]


# create n gropes with m images in each
n = 10  # number of group
m = 10  # number of images

for group_numer in range(n):
    group_id = groups_collection.insert_one(
        {'name': f"Group {group_numer}"}
        ).inserted_id
    for image_number in range(m):
        image_url = create_image_in_aws(image_number,
                                        group_numer,
                                        s3_client,
                                        AWS_BUCKET,
                                        AWS_SERVICE_NAME,
                                        AWS_REGION,
                                        )
        image = {
            'created_at': datetime.utcnow(),
            'url': image_url,
            'status': statuses[image_number % 4],
            'group_id': group_id
        }
        images_collection.insert_one(image)

print("Test database was created")
