from bson import json_util
import json


def sanitize_json(mongo_db_data):
    """
    Sanitize MongoDB data for safe JSON serialization.

    This function takes MongoDB data, typically retrieved from a MongoDB
    It ensures that special MongoDB data types, such as ObjectId and datetime,
    are properly converted to JSON.

    Args:
        mongo_db_data (dict): MongoDB data to be sanitized.

    Returns:
        dict: A sanitized JSON-serializable version of the input data.

    Example:
        Given a MongoDB document like:
        {
            "_id": ObjectId("5f7d7b9932f03958701e3204"),
            "name": "John Doe",
            "birth_date": datetime.datetime(1990, 5, 15, 0, 0)
        }

        Calling sanitize_json(document) would return:
        {
            "_id": "5f7d7b9932f03958701e3204",
            "name": "John Doe",
            "birth_date": "1990-05-15T00:00:00Z"
        }
    """

    json_sanitized = json.loads(json_util.dumps(mongo_db_data))
    return json_sanitized
