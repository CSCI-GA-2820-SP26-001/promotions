"""
Models for Promotion

All of the models are stored in this module
"""

import logging
from enum import Enum
from datetime import date
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Gender(Enum):
    """Enumeration of valid Promotion Genders"""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 3


class PromotionType(Enum):
    """Enumeration of valid Promotion Types"""

    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class Promotion(db.Model):
    """
    Class that represents a Promotion

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(256))
    promo_code = db.Column(db.String(63))
    discount_amount = db.Column(db.Numeric(scale=2), nullable=False)
    promotion_type = db.Column(db.String(63), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    product_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Promotion {self.name} id=[{self.id}]>"

    def create(self) -> None:
        """
        Creates a Promotion to the database
        """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:  # pragma: no cover
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self) -> None:
        """
        Updates a Promotion to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:  # pragma: no cover
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Promotion from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:  # pragma: no cover
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Promotion into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "promo_code": self.promo_code,
            "discount_amount": float(self.discount_amount),
            "promotion_type": self.promotion_type,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "is_active": self.is_active,
            "product_id": self.product_id,
        }

    def deserialize(self, data):
        """
        Deserializes a Promotion from a dictionary

        Args:
            data (dict): A dictionary containing the Promotion data
        """
        try:
            self.name = data["name"]
            self.description = data.get("description")
            self.promo_code = data.get("promo_code")
            self.discount_amount = data["discount_amount"]
            self.promotion_type = data["promotion_type"]
            if isinstance(data["start_date"], str):
                self.start_date = date.fromisoformat(data["start_date"])
            else:
                self.start_date = data["start_date"]
            if isinstance(data["end_date"], str):
                self.end_date = date.fromisoformat(data["end_date"])
            else:
                self.end_date = data["end_date"]
            if isinstance(data["is_active"], bool):
                self.is_active = data["is_active"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [is_active]: "
                    + str(type(data["is_active"]))
                )
            self.product_id = data["product_id"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Promotion: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Promotion: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Promotions in the database"""
        logger.info("Processing all Promotions")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Promotion by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_type(cls, promotion_type):
        """Returns all Promotions with the given type"""
        logger.info("Processing type query for %s ...", promotion_type)
        return cls.query.filter(cls.promotion_type == promotion_type)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Promotions with the given name

        Args:
            name (string): the name of the Promotions you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
