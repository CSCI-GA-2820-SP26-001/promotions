######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
TestPromotion API Service Test Suite
"""
# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Promotion
from tests.factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/promotions"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotionService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Promotion).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_promotions(self, count):
        """Factory method to create promotions for testing"""
        promotions = []
        for i in range(count):
            promotion = Promotion()
            promotion.deserialize(
                {
                    "name": f"Promotion {i}",
                    "description": f"Description {i}",
                    "promo_code": f"SAVE{i}",
                    "discount_amount": 10.0 + i,
                    "promotion_type": "percentage",
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "is_active": True,
                    "product_id": i + 1,
                }
            )
            promotion.create()
            promotions.append(promotion)
        return promotions

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Todo: Add your test cases here...
    def _create_promotions(self, count, promotion_type=None):
        """Factory method to create promotions in bulk"""
        promotions = []
        for _ in range(count):
            test_promotion = PromotionFactory()
            if promotion_type:
                test_promotion.type = promotion_type
            response = self.client.post(BASE_URL, json=test_promotion.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_promotion = response.get_json()
            test_promotion.id = new_promotion["id"]
            promotions.append(test_promotion)
        return promotions

    def test_list_all_promotions(self):
        """It should return all Promotions when no filter is given"""
        self._create_promotions(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_promotions_by_type(self):
        """It should return only Promotions matching the requested type"""
        promotions = self._create_promotions(10)
        target_type = promotions[0].type.name
        count = len([p for p in promotions if p.type.name == target_type])
        response = self.client.get(f"{BASE_URL}?type={target_type}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), count)
        for promotion in data:
            self.assertEqual(promotion["type"], target_type)

    def test_list_promotions_by_type_empty(self):
        """It should return an empty list when no Promotions match the type"""
        self._create_promotions(3, promotion_type=PromotionType.BOGO)
        response = self.client.get(f"{BASE_URL}?type=SALE")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 0)

    def test_list_promotions_invalid_type(self):
        """It should return 400 for an invalid promotion type"""
        response = self.client.get(f"{BASE_URL}?type=INVALID_TYPE")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_method_not_allowed(self):
        """It should return 405 Method Not Allowed"""
        resp = self.client.delete("/")
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        resp = self.client.delete(f"/promotions/{promotion.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_promotion_not_found(self):
        """It should return 204 even when Promotion does not exist"""
        resp = self.client.delete("/promotions/0")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_promotion(self):
        """It should Get a single Promotion"""
        test_promotion = self._create_promotions(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_promotion.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_promotion.name)
        self.assertEqual(data["id"], test_promotion.id)

    def test_get_promotion_not_found(self):
        """It should not Get a Promotion that's not found"""
        response = self.client.get(f"{BASE_URL}/0")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])
