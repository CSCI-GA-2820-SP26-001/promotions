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
Test cases for Pet Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from datetime import date, timedelta
from wsgi import app
from service.models import Promotion, DataValidationError, db
from .factories import PromotionFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Promotion   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPromotion(TestCase):
    """Test Cases for Promotion Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Promotion).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_promotion(self):
        """It should Create a Promotion and assert that it exists"""
        promotion = Promotion(
            name="Summer Sale",
            description="Big summer discounts",
            promo_code="SUMMER20",
            discount_amount=20.00,
            promotion_type="percentage",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            is_active=True,
            product_id=1,
        )
        self.assertEqual(promotion.name, "Summer Sale")
        self.assertIn("Summer Sale", repr(promotion))

    def test_add_a_promotion(self):
        """It should Create a Promotion and add it to the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        promotion = PromotionFactory()
        promotion.create()
        self.assertIsNotNone(promotion.id)
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)

    def test_read_a_promotion(self):
        """It should Read a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        found = Promotion.find(promotion.id)
        self.assertEqual(found.id, promotion.id)
        self.assertEqual(found.name, promotion.name)

    def test_update_a_promotion(self):
        """It should Update a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertIsNotNone(promotion.id)
        promotion.name = "Updated Sale"
        original_id = promotion.id
        promotion.update()
        self.assertEqual(promotion.id, original_id)
        self.assertEqual(promotion.name, "Updated Sale")
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 1)
        self.assertEqual(promotions[0].name, "Updated Sale")

    def test_update_no_id(self):
        """It should not Update a Promotion with no id"""
        promotion = PromotionFactory()
        promotion.id = None
        self.assertRaises(DataValidationError, promotion.update)

    def test_delete_a_promotion(self):
        """It should Delete a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        self.assertEqual(len(Promotion.all()), 1)
        promotion.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_list_all_promotions(self):
        """It should List all Promotions in the database"""
        promotions = Promotion.all()
        self.assertEqual(promotions, [])
        for _ in range(5):
            promotion = PromotionFactory()
            promotion.create()
        promotions = Promotion.all()
        self.assertEqual(len(promotions), 5)

    def test_serialize_a_promotion(self):
        """It should Serialize a Promotion"""
        promotion = PromotionFactory()
        promotion.create()
        data = promotion.serialize()
        self.assertIsNotNone(data)
        self.assertIn("id", data)
        self.assertEqual(data["name"], promotion.name)

    def test_deserialize_a_promotion(self):
        """It should Deserialize a Promotion"""
        data = {
            "name": "Flash Sale",
            "description": "Quick discount",
            "promo_code": "FLASH10",
            "discount_amount": 10.00,
            "promotion_type": "fixed_amount",
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=7)).isoformat(),
            "is_active": True,
            "product_id": 42,
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertEqual(promotion.name, "Flash Sale")

    def test_deserialize_with_date_objects(self):
        """It should Deserialize a Promotion with date objects instead of strings"""
        data = {
            "name": "Flash Sale",
            "description": "Quick discount",
            "promo_code": "FLASH10",
            "discount_amount": 10.00,
            "promotion_type": "fixed_amount",
            "start_date": date.today(),
            "end_date": date.today() + timedelta(days=7),
            "is_active": True,
            "product_id": 42,
        }
        promotion = Promotion()
        promotion.deserialize(data)
        self.assertEqual(promotion.name, "Flash Sale")

    def test_deserialize_missing_data(self):
        """It should not Deserialize a Promotion with missing data"""
        data = {"name": "Incomplete Sale"}
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not Deserialize a Promotion with bad data"""
        data = "this is not a dictionary"
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_deserialize_bad_is_active(self):
        """It should not Deserialize a Promotion with bad is_active"""
        data = {
            "name": "Bad Sale",
            "description": "Test",
            "promo_code": "BAD",
            "discount_amount": 10.00,
            "promotion_type": "percentage",
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=7)).isoformat(),
            "is_active": "yes",
            "product_id": 1,
        }
        promotion = Promotion()
        self.assertRaises(DataValidationError, promotion.deserialize, data)

    def test_find_promotion(self):
        """It should Find a Promotion by ID"""
        promotions = PromotionFactory.create_batch(5)
        for promotion in promotions:
            promotion.create()
        target = promotions[2]
        found = Promotion.find(target.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, target.id)

    def test_find_by_name(self):
        """It should Find Promotions by Name"""
        promotions = PromotionFactory.create_batch(10)
        for promotion in promotions:
            promotion.create()
        name = promotions[0].name
        count = len([p for p in promotions if p.name == name])
        found = Promotion.find_by_name(name)
        self.assertEqual(found.count(), count)
