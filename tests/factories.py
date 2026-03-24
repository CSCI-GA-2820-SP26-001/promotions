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
    name = factory.Faker("catch_phrase")
    description = factory.Faker("sentence")
    promo_code = factory.Faker("bothify", text="PROMO-####")
    discount_amount = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, positive=True, min_value=1, max_value=99
    )
    promotion_type = factory.Faker("random_element", elements=["percentage", "fixed_amount"])
    start_date = factory.LazyFunction(date.today)
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=30))
    is_active = factory.Faker("boolean")
    product_id = factory.Faker("random_int", min=1, max=1000)
