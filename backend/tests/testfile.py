import unittest
import json
from app import app


class TestGroupsAPI(unittest.TestCase):

    def setUp(self):
        """ 1. You need to  populate database with imagecreator.py from
            create_test_db first
            2. in backend/.env file chenge MONGODB_DB_NAME=image_service to
            MONGODB_TEST_DB_NAME=image_service_test
            TODO refactor app module to work as app facctory and
            use app.config.fromobject from FLASK
        """
        self.app = app.test_client()

    def test_get_wrong_endpoint(self):

        response = self.app.get('/wrong_end_point')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["code"], 404)
        self.assertEqual(data["name"], "Not Found")
        self.assertEqual(data["description"],
                         "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
                         )

    def test_put_wrong_endpoint(self):

        response = self.app.put('/wrong_end_point')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["code"], 404)
        self.assertEqual(data["name"], "Not Found")
        self.assertEqual(data["description"],
                         "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
                         )

    # check differernt methods
    def test_wrong_method_correct_endpoint1(self):

        response = self.app.put('/groups')
        self.assertEqual(response.status_code, 405)
        data = response.get_json()
        self.assertEqual(data["code"], 405)
        self.assertEqual(data["name"], "Method Not Allowed")
        self.assertEqual(data["description"],
                         "The method is not allowed for the requested URL.",
                         )

    def test_wrong_method_correct_endpoint2(self):

        response = self.app.delete('/groups')
        self.assertEqual(response.status_code, 405)
        data = response.get_json()
        self.assertEqual(data["code"], 405)
        self.assertEqual(data["name"], "Method Not Allowed")
        self.assertEqual(data["description"],
                         "The method is not allowed for the requested URL.",
                         )

    def test_wrong_method_correct_endpoint3(self):

        response = self.app.post('/groups')
        self.assertEqual(response.status_code, 405)
        data = response.get_json()
        self.assertEqual(data["code"], 405)
        self.assertEqual(data["name"], "Method Not Allowed")
        self.assertEqual(data["description"],
                         "The method is not allowed for the requested URL.",
                         )

        def test_get_groups_with_images(self):
            response = self.app.get('/groups')
            self.assertEqual(response.status_code, 200)


class TestImageStatusChangeAPI(unittest.TestCase):

    def setUp(self):
        """ 1. You need to  populate database with imagecreator.py from
            create_test_db first
            2. in backend/.env file chenge MONGODB_DB_NAME=image_service to
            MONGODB_TEST_DB_NAME=image_service_test
            TODO refactor app module to work as app facctory and
            use app.config.fromobject from FLASK
        """
        self.app = app.test_client()

    def test_update_image_status_valid(self):
        # get image Id of the first image in group
        # we know for created that it status is new
        response = self.app.get('/groups')
        data = response.get_json()
        image_id = data[0]['images'][0]['_id']['$oid']

        # define 4valid status
        data_new = {'status': 'new'}
        data_accepted = {'status': 'accepted'}
        data_deleted = {'status': 'deleted'}
        data_review = {'status': 'review'}

        # cehck if we can change status to any valid one
        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_accepted),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_deleted),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_review),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_new),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_new),
                                content_type='application/json',
                                )
        answer = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer['message'], "Requested status is the same as current")

    def test_update_image_status_invalid(self):

        response = self.app.get('/groups')
        data = response.get_json()
        image_id = data[0]['images'][0]['_id']['$oid']

        data_invalid = {'status': 'invalid'}

        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_invalid),
                                content_type='application/json',
                                )
        answer = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(answer['name'], "Invalid status")
        self.assertEqual(answer['description'], "Valid statuses are - ['new', 'review', 'accepted', 'deleted']")
        self.assertEqual(answer['code'], 400)
        self.assertEqual(response.status_code, 400)

    def test_update_image_invalid_id(self):

        data = {'status': 'new'}

        response = self.app.put('/images/notvalidatall',
                                data=json.dumps(data),
                                content_type='application/json',
                                )
        answer = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(answer['name'], "Invalid ObjectId")
        self.assertEqual(answer['description'], "'notvalidatall' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string")
        self.assertEqual(answer['code'], 400)
        self.assertEqual(response.status_code, 400)

    def test_update_image_valid_but_nonexistingid(self):

        data = {'status': 'new'}

        response = self.app.put('/images/123456789012345678901234',
                                data=json.dumps(data),
                                content_type='application/json',
                                )
        answer = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(answer['name'], "Image not found")
        self.assertEqual(answer['description'], "Specified ID was not found in database")
        self.assertEqual(answer['code'], 400)
        self.assertEqual(response.status_code, 400)


class TestImageStatistics(unittest.TestCase):

    def setUp(self):
        """ 1. You need to  populate database with imagecreator.py from
            create_test_db first
            2. in backend/.env file chenge MONGODB_DB_NAME=image_service to
            MONGODB_TEST_DB_NAME=image_service_test
            TODO refactor app module to work as app facctory and
            use app.config.fromobject from FLASK
        """
        self.app = app.test_client()

    def test_get_statistics(self):
        # get statistice remember current values
        response = self.app.get('/statistics')
        answer = response.get_json()
        self.assertEqual(response.status_code, 200)
        # remember current values
        new = answer['new']
        accepted = answer['accepted']

        # find some image
        response = self.app.get('/groups')
        data = response.get_json()
        image_id = data[0]['images'][0]['_id']['$oid']

        # define status change json
        data_new = {'status': 'new'}
        data_accepted = {'status': 'accepted'}

        # change status from new to accepted
        # we suppose that first image in groupe have sgtatus new
        # as we create test database so.
        # TODO we a not suupose to use met information in test need to rewrite
        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_accepted),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        # check if statistics chage correspondingly
        response = self.app.get('/statistics')
        answer = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer['new'],  new - 1)
        self.assertEqual(answer['accepted'],  accepted + 1)

        # set status back to new
        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(data_new),
                                content_type='application/json',
                                )
        self.assertEqual(response.status_code, 200)

        # check statistic again

        response = self.app.get('/statistics')
        answer = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer['new'],  new)
        self.assertEqual(answer['accepted'],  accepted)


if __name__ == '__main__':
    unittest.main()
