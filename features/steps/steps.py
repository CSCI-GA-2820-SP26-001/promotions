"""
Step definitions for Promotion BDD tests
"""
from behave import given, when, then
from service.models import Promotion, db
import json

BASE_URL = "/promotions"


@given('the following promotions exist')
def step_create_promotions(context):
    """Create promotions from the table in the feature file"""
    for row in context.table:
        promotion = Promotion()
        promotion.deserialize({
            "name": row["name"],
            "description": row["description"],
            "promo_code": row["promo_code"],
            "discount_amount": float(row["discount_amount"]),
            "promotion_type": row["promotion_type"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "is_active": row["is_active"] == "True",
            "product_id": int(row["product_id"]),
        })
        promotion.create()


@when('I create a promotion with the following data')
def step_create_promotion(context):
    """Create a promotion with the given data"""
    row = context.table[0]
    data = {
        "name": row["name"],
        "description": row["description"],
        "promo_code": row["promo_code"],
        "discount_amount": float(row["discount_amount"]),
        "promotion_type": row["promotion_type"],
        "start_date": row["start_date"],
        "end_date": row["end_date"],
        "is_active": row["is_active"] == "True",
        "product_id": int(row["product_id"]),
    }
    context.response = context.client.post(
        BASE_URL,
        json=data,
        content_type="application/json"
    )


@when('I create a promotion with invalid data')
def step_create_promotion_invalid(context):
    """Create a promotion with invalid data"""
    row = context.table[0]
    data = {"name": row["name"]}
    context.response = context.client.post(
        BASE_URL,
        json=data,
        content_type="application/json"
    )


@when('I retrieve the promotion named "{name}"')
def step_get_promotion_by_name(context, name):
    """Retrieve a promotion by name"""
    response = context.client.get(f"{BASE_URL}?name={name}")
    data = response.get_json()
    promotion_id = data[0]["id"]
    context.response = context.client.get(f"{BASE_URL}/{promotion_id}")


@when('I retrieve the promotion with id {promotion_id:d}')
def step_get_promotion_by_id(context, promotion_id):
    """Retrieve a promotion by id"""
    context.response = context.client.get(f"{BASE_URL}/{promotion_id}")


@when('I update the promotion named "{name}" with name "{new_name}"')
def step_update_promotion(context, name, new_name):
    """Update a promotion by name"""
    response = context.client.get(f"{BASE_URL}?name={name}")
    data = response.get_json()
    promotion = data[0]
    promotion["name"] = new_name
    context.response = context.client.put(
        f"{BASE_URL}/{promotion['id']}",
        json=promotion,
        content_type="application/json"
    )


@when('I update the promotion with id {promotion_id:d} with name "{new_name}"')
def step_update_promotion_by_id(context, promotion_id, new_name):
    """Update a promotion by id"""
    context.response = context.client.put(
        f"{BASE_URL}/{promotion_id}",
        json={"name": new_name},
        content_type="application/json"
    )


@when('I delete the promotion named "{name}"')
def step_delete_promotion_by_name(context, name):
    """Delete a promotion by name"""
    response = context.client.get(f"{BASE_URL}?name={name}")
    data = response.get_json()
    promotion_id = data[0]["id"]
    context.response = context.client.delete(f"{BASE_URL}/{promotion_id}")


@when('I delete the promotion with id {promotion_id:d}')
def step_delete_promotion_by_id(context, promotion_id):
    """Delete a promotion by id"""
    context.response = context.client.delete(f"{BASE_URL}/{promotion_id}")


@when('I list all promotions')
def step_list_all_promotions(context):
    """List all promotions"""
    context.response = context.client.get(BASE_URL)


@when('I query promotions by type "{promotion_type}"')
def step_query_promotions_by_type(context, promotion_type):
    """Query promotions by type"""
    context.response = context.client.get(f"{BASE_URL}?type={promotion_type}")


@when('I query promotions by is_active "{is_active}"')
def step_query_promotions_by_is_active(context, is_active):
    """Query promotions by is_active"""
    context.response = context.client.get(f"{BASE_URL}?is_active={is_active}")


@when('I activate the promotion named "{name}"')
def step_activate_promotion(context, name):
    """Activate a promotion"""
    response = context.client.get(f"{BASE_URL}?name={name}")
    data = response.get_json()
    promotion = data[0]
    promotion["is_active"] = True
    context.response = context.client.put(
        f"{BASE_URL}/{promotion['id']}",
        json=promotion,
        content_type="application/json"
    )


@when('I deactivate the promotion named "{name}"')
def step_deactivate_promotion(context, name):
    """Deactivate a promotion"""
    response = context.client.get(f"{BASE_URL}?name={name}")
    data = response.get_json()
    promotion = data[0]
    promotion["is_active"] = False
    context.response = context.client.put(
        f"{BASE_URL}/{promotion['id']}",
        json=promotion,
        content_type="application/json"
    )


@then('the response status code should be {status_code:d}')
def step_check_status_code(context, status_code):
    """Check the response status code"""
    assert context.response.status_code == status_code, \
        f"Expected {status_code} but got {context.response.status_code}"


@then('the promotion should have name "{name}"')
def step_check_promotion_name(context, name):
    """Check the promotion name"""
    data = context.response.get_json()
    assert data["name"] == name, f"Expected {name} but got {data['name']}"


@then('the response should contain {count:d} promotions')
def step_check_promotion_count(context, count):
    """Check the number of promotions returned"""
    data = context.response.get_json()
    assert len(data) == count, f"Expected {count} but got {len(data)}"


@then('all promotions should have type "{promotion_type}"')
def step_check_promotion_type(context, promotion_type):
    """Check all promotions have the given type"""
    data = context.response.get_json()
    for promotion in data:
        assert promotion["promotion_type"] == promotion_type, \
            f"Expected {promotion_type} but got {promotion['promotion_type']}"


@then('all promotions should have is_active {is_active}')
def step_check_promotion_is_active(context, is_active):
    """Check all promotions have the given is_active value"""
    data = context.response.get_json()
    expected = is_active == "True"
    for promotion in data:
        assert promotion["is_active"] == expected, \
            f"Expected {expected} but got {promotion['is_active']}"


@then('the promotion should have is_active {is_active}')
def step_check_single_promotion_is_active(context, is_active):
    """Check a single promotion has the given is_active value"""
    data = context.response.get_json()
    expected = is_active == "True"
    assert data["is_active"] == expected, \
        f"Expected {expected} but got {data['is_active']}"