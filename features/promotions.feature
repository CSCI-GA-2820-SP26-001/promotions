Feature: Promotion Service
    As a user of the promotion service
    I need to be able to manage promotions
    So that I can create, read, update, delete, list, query and perform actions on promotions

    Background:
        Given the following promotions exist
            | name          | description      | promo_code | discount_amount | promotion_type | start_date | end_date   | is_active | product_id |
            | Summer Sale   | Summer discount  | SUMMER10   | 10.00           | percentage     | 2025-01-01 | 2025-12-31 | True      | 1          |
            | Winter Deal   | Winter discount  | WINTER20   | 20.00           | fixed_amount   | 2025-01-01 | 2025-12-31 | False     | 2          |
            | Spring Promo  | Spring discount  | SPRING15   | 15.00           | percentage     | 2025-01-01 | 2025-12-31 | True      | 3          |

    # ----------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------
    Scenario: Create a new promotion
        When I create a promotion with the following data
            | name        | description     | promo_code | discount_amount | promotion_type | start_date | end_date   | is_active | product_id |
            | Flash Sale  | Flash discount  | FLASH25    | 25.00           | percentage     | 2025-01-01 | 2025-12-31 | True      | 4          |
        Then the response status code should be 201
        And the promotion should have name "Flash Sale"

    Scenario: Create a promotion with missing required fields
        When I create a promotion with invalid data
            | name        |
            | Broken Sale |
        Then the response status code should be 400

    # ----------------------------------------------------------
    # READ
    # ----------------------------------------------------------
    Scenario: Read a single promotion
        When I retrieve the promotion named "Summer Sale"
        Then the response status code should be 200
        And the promotion should have name "Summer Sale"

    Scenario: Read a promotion that does not exist
        When I retrieve the promotion with id 0
        Then the response status code should be 404

    # ----------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------
    Scenario: Update an existing promotion
        When I update the promotion named "Summer Sale" with name "Updated Sale"
        Then the response status code should be 200
        And the promotion should have name "Updated Sale"

    Scenario: Update a promotion that does not exist
        When I update the promotion with id 0 with name "Ghost Sale"
        Then the response status code should be 404

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------
    Scenario: Delete an existing promotion
        When I delete the promotion named "Winter Deal"
        Then the response status code should be 204

    Scenario: Delete a promotion that does not exist
        When I delete the promotion with id 0
        Then the response status code should be 204

    # ----------------------------------------------------------
    # LIST
    # ----------------------------------------------------------
    Scenario: List all promotions
        When I list all promotions
        Then the response status code should be 200
        And the response should contain 3 promotions

    # ----------------------------------------------------------
    # QUERY
    # ----------------------------------------------------------
    Scenario: Query promotions by type
        When I query promotions by type "percentage"
        Then the response status code should be 200
        And all promotions should have type "percentage"

    Scenario: Query promotions by is_active
        When I query promotions by is_active "true"
        Then the response status code should be 200
        And all promotions should have is_active True

    # ----------------------------------------------------------
    # ACTION
    # ----------------------------------------------------------
    Scenario: Activate a promotion
        When I activate the promotion named "Winter Deal"
        Then the response status code should be 200
        And the promotion should have is_active True

    Scenario: Deactivate a promotion
        When I deactivate the promotion named "Summer Sale"
        Then the response status code should be 200
        And the promotion should have is_active False