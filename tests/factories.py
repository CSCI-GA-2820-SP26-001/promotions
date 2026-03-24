"""
Test Factory to make fake objects for testing
"""

from datetime import date
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Gender, Promotion


class PromotionFactory(factory.Factory):
    """Creates fake promotions that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Promotion

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    category = FuzzyChoice(choices=["dog", "cat", "bird", "fish"])
    available = FuzzyChoice(choices=[True, False])
    gender = FuzzyChoice(choices=[Gender.MALE, Gender.FEMALE, Gender.UNKNOWN])
    birthday = FuzzyDate(date(2008, 1, 1))
