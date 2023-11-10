import unittest
import json
from app import app
from config.config import VALID_STATUSES


class TestGroupsAPI(unittest.TestCase):

    def setUp(self):
        """ 1. You need to  populate database with imagecreator.py from
            create_test_db first
            2. in backend/.env file change MONGODB_DB_NAME=image_service to
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

    def test_valid_endpoint_valid_method(self):
        response = self.app.get('/groups')
        self.assertEqual(response.status_code, 200)

    # test filtering
    def test_filter_by_valid_status(self):

        for status in VALID_STATUSES:

            response = self.app.get('/groups?status='+status)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            print(data[0]['count'])
            self.assertEqual(data[0]['count'], 3)
            # self.assertEqual(data["name"], "Method Not Allowed")
            # self.assertEqual(data["description"],
            #                 "The method is not allowed for the requested URL.",
            #                 )


class TestImageStatusChangeAPI(unittest.TestCase):

    def setUp(self):
        """ 1. You need to  populate database with imagecreator.py from
            create_test_db first
            2. in backend/.env file change MONGODB_DB_NAME=image_service to
            MONGODB_TEST_DB_NAME=image_service_test
            TODO refactor app module to work as app facctory and
            use app.config.fromobject from FLASK
        """
        self.app = app.test_client()

    def test_update_image_status_valid(self):
        # get image Id of the first image in group
        # we know that for newly created db
        # status of the first image is new
        response = self.app.get('/groups')
        data = response.get_json()
        image_id = data[0]['images'][0]['_id']['$oid']

        # define four valid statuses
        # new is is last as current is new
        valid_data_to_put = [{'status': 'accepted'},
                             {'status': 'deleted'},
                             {'status': 'review'},
                             {'status': 'new'},
                             ]

        # check if we can change status to any valid one
        for data_to_put in valid_data_to_put:

            response = self.app.put(f'/images/{image_id}',
                                    data=json.dumps(data_to_put),
                                    content_type='application/json',
                                    )
            self.assertEqual(response.status_code, 200)

        # to change status one more time to check same
        # status handling
        response = self.app.put(f'/images/{image_id}',
                                data=json.dumps(valid_data_to_put[3]),
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
        invalid_object_id_url = '/images/notvalidatall'

        response = self.app.put(invalid_object_id_url,
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
        non_existaning_object_url = '/images/123456789012345678901234'

        response = self.app.put(non_existaning_object_url,
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
            2. in backend/.env file change MONGODB_DB_NAME=image_service to
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
        # we suppose that first image in group have status new
        # as we create test database so.
        # TODO better not to use meta information in tests need to rewrite
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
