# Image service Flask App README

This README provides an overview of a Flask application and its primary routes and functionalities. The application is designed to manage and retrieve data related to groups and images. Images are stored in AWS S3. Image information sored in MondgoDB living in Atlas cloud.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Routes and Functionalities](#routes-and-functionalities)
  - [Get Groups with Images](#get-groups-with-images)
  - [Update Image Status](#update-image-status)
  - [Get Statistics](#get-statistics)
- [Error Handling](#error-handling)

---

## Introduction

This Flask application serves as a RESTful API for managing groups and images. It provides endpoints for retrieving groups with associated images, updating the status of an image, and retrieving statistics for images statuses created in the last 30 days.

The application utilizes a MongoDB database to store and retrieve data, including groups and images. It also includes error handling for common HTTP exceptions.
IT supposed that you have MongoFB up and running somewhere.
It also uses AWS S3 for demonstaration purposes. So you also need a basket there.

---

## Installation

Before running the application, ensure you have Python and MongoDB installed on your system. 

You can set up a virtual environment and install the required packages using the following commands:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

Before run the application you need to tne .env file.
Open .envdemo file. Fill it with your specific information and save as .env file.
To run the application, execute the following command:

```bash
gunicorn --config gunicorn_config.py app:app
```

The application should now be running and accessible at `http://localhost:5000`.

---

## Routes and Functionalities

### Get Groups with Images

- **Endpoint:** `/groups`
- **HTTP Method:** GET

This endpoint retrieves a list of groups with associated images. It performs the following actions:

1. Joins the 'groups' collection with the 'images' collection based on the 'group_id' field.
2. Sorts and filters the list of images, if necessary.
3. Groups the images by their associated group and counts them.
4. Returns a JSON response with the grouped data.

#### Request Parameters

- `status` (optional): Filters the images by status. If provided and valid, the response will only include images with the specified status.

- `page` (optional): Pagination paramter. If specified paginated response returned.
    starting group number would be (page * groups_to_return). You can specify default number groups_to_return in config.py. If not specified no paginating occurs.

- `groups_to_return` (optional): Specify the number of groups to return if page parameter is specified.
    If groups_to_return is missed in request - default value from config.py is used.

#### Example Usage

```http
GET /groups?status=approved&page=0&groups_to_return=2
```

#### Response

```json
[
    {
        "_id": {
                "$oid": "65071d4096b52de451f914e0"
            },
        "name": "Group 1",
        "images": [
            {
                "_id": {
                    "$oid": "65071d3c96b52de451f914d9"
                    },
                "status": "approved",
                "created_at": "2023-09-18T12:00:00Z",
                "last_updated_at": "2023-09-28T13:00:00Z"
            },
            {
                "_id": {
                    "$oid": "65071d3a96b52de451f914d6"
                    },  
                "status": "approved",
                "created_at": "2023-09-18T13:00:00Z",
                "last_updated_at": "2023-09-28T13:01:00Z"
            }
        ],
        "count": 2
    },
    {
        "_id": {
                "$oid": "65071d3b96b52de451f914d8"
            },
        "name": "Group 2",
        "images": [
            {
                "_id": {
                    "$oid": "65071d3b96b52de451f914d7"
                    },
                "status": "approved",
                "created_at": "2023-09-18T14:00:00Z",
                "last_updated_at": "2023-09-28T13:02:00Z"
            }
        ],
        "count": 1
    }
]
```

### Update Image Status

- **Endpoint:** `/images/<image_id>`
- **HTTP Method:** PUT

This endpoint allows you to update the status of an image identified by its unique identifier (`image_id`). The image status is modified based on the data provided in the request JSON.

#### Request Parameters

- `image_id`: The unique identifier of the image (in ObjectId format).

#### Request JSON

```json
{
    "status": "new_status"
}
```

- `status`: The new status to assign to the image. It must be one of the valid statuses.
-  Valid statuses are 'new', 'review', 'accepted' and 'deleted']

#### Example Usage

```http
PUT /images/5f76b5c5a548ebe57f213b3a
```

#### Response (Success)

```json
{
    "message": "Image status updated"
}
```

#### Response (Invalid ObjectId)

```json
{
    "code": 400,
    "name": "Invalid ObjectId",
    "description": "Object ID is in the wrong format"
}
```

#### Response (Invalid Status)

```json
{
    "code": 400,
    "name": "Invalid status",
    "description": "Valid statuses are -  ['new', 'review', 'accepted', 'deleted']"
}
```

#### Response (Image Not Found)

```json
{
    "code": 400,
    "name": "Image not found",
    "description": "Specified ID was not found in the database"
}
```

#### Response (Database Exception)

```json
{
    "code": 500,
    "name": "MongoDB exception occurred",
    "description": "An error occurred while updating the image status"
}
```

### Get Statistics

- **Endpoint:** `/statistics`
- **HTTP Method:** GET

This endpoint retrieves statistics for images created in the last 30 days. It calculates statistics based on images' creation dates within the specified time frame and groups them by their 'status' field.

#### Example Usage

```http
GET /statistics
```

#### Response

```json
{
    "approved": 12,
    "rejected": 5,
    "pending": 8
}
```

**Notes:**
- The endpoint uses a default period of the last 30 days to calculate statistics.
- Images outside this time frame are excluded from the statistics.

---

## Error Handling

The application includes an error handler that converts HTTP exceptions into JSON responses. This error handler ensures that error responses are in JSON format rather than HTML.

It transforms HTTP exceptions into JSON responses containing error information, including the HTTP status code, status name, and a description of the error.

---

Feel free to explore and use this Flask application for managing groups, images, and viewing statistics. If you have any questions or encounter issues, please refer to the documentation or contact the application developer for assistance.


## Running the Test

Follow these steps to run the test:

1. Navigate to the `create_test_db` directory.

2. Create a virtual environment and activate it. Ensure that this environment is different from your standard environment as it is configured for use with AWS. Use the following commands:

    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment (macOS/Linux)
    source venv/bin/activate

    # Install the required packages
    pip install -r requirements.txt
    ```

3. Edit the `createtestdb/.envdemo` file with your specific information and save it as `.env`.

4. Execute the database creation script:

    ```bash
    python imagecreator.py
    ```

5. Change your virtual environment to the backend directory.

6. Modify the `MONGODB_DB_NAME` variable to `image_service_test`.

7. Run the unit tests using the following command:

    ```bash
    python -m unittest tests/testfile.py
    ```

By following these steps, you should be able to run the test successfully. Ensure that you have the necessary dependencies and configurations in place before executing these commands.


## Task description

Спроектировать backend с использованием python 3 и mongo db для сервиса обработки изображений. Изображения будет собирать другой сервис, этот же сервис будет формировать данные и записывать их в mongo db. Фронтенд будет иметь две страницы: статистика количества изображений по каждому статусу за последние 30 дней и страница со списком групп и изображений с возможностью изменить их статус.

Требования:
Изображение должно иметь следующие свойства:
 ⁃ Created at
 ⁃ Url
 ⁃ Status: new, review, accepted, deleted

Изображения собраны в группы. Группа имеет следующие свойства:
 ⁃ Name

Изображений в группе будет несколько десятков. Групп может быть бесконечное количество.

Нужно реализовать endpoint’ы для: 
 ⁃ запроса списка изображений
    • В ответе api должен быть массив групп, в каждой из которых должен быть массив изображений, относящихся к этой группе
    • Данные должны быть отсортированы по дате изменения данных изображения desc
    • Возможность фильтрации по статусу изображения
    • В ответе api у групп помимо поля name еще должно быть поле count с общим количеством изображений в группе
 ⁃ обновления статуса изображения
 ⁃ запроса статистики.
    • данные за последние 30 дней
    • Ответ api d виде:
    { <имя статуса>: количество изображений, … }

Все трансформации данных: фильтрация, группировка данных для статистики, вычисляемые поля должны быть сделаны с помощью mongo aggregation pipelines

Написать несколько тестов
