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
Promotion Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Promotion
"""
from flask import jsonify, request, abort
from flask import current_app as app
from service.models import Promotion, DataValidationError, PromotionType
from service.common import status


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Promotion REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# CREATE A NEW PROMOTION
######################################################################
@app.route("/promotions", methods=["POST"])
def create_promotions():
    """Create a Promotion"""
    promotion = Promotion()
    try:
        promotion.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    promotion.create()
    return jsonify(promotion.serialize()), status.HTTP_201_CREATED


######################################################################
# READ A SINGLE PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotions(promotion_id):
    """Read a Promotion"""
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["PUT"])
def update_promotions(promotion_id):
    """Update a Promotion"""
    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found.",
        )
    try:
        promotion.deserialize(request.get_json())
    except DataValidationError as error:
        abort(status.HTTP_400_BAD_REQUEST, str(error))
    promotion.update()
    return jsonify(promotion.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["DELETE"])
def delete_promotions(promotion_id):
    """Deletes a Promotion"""
    app.logger.info("Request to delete Promotion with id: %s", promotion_id)
    promotion = Promotion.find(promotion_id)
    if promotion:
        promotion.delete()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST PROMOTIONS
######################################################################
def _parse_list_filters():
    """Parse and validate query parameters for the list promotions endpoint"""
    filters = {}

    promotion_type = request.args.get("type")
    if promotion_type:
        try:
            filters["promotion_type"] = PromotionType(promotion_type.lower()).value
        except ValueError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid promotion type: {promotion_type}",
            )

    name = request.args.get("name")
    if name:
        filters["name"] = name

    is_active = request.args.get("is_active")
    if is_active is not None:
        if is_active.lower() not in ("true", "false"):
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid value for is_active: {is_active}",
            )
        filters["is_active"] = is_active.lower() == "true"

    product_id = request.args.get("product_id")
    if product_id is not None:
        try:
            filters["product_id"] = int(product_id)
        except ValueError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid product_id: {product_id}",
            )

    return filters


@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all Promotions, optionally filtered by query parameters"""
    app.logger.info("Request to list promotions...")

    filters = _parse_list_filters()

    if filters:
        app.logger.info("Filtering by: %s", filters)
        promotions = Promotion.find_by_filters(**filters)
    else:
        promotions = Promotion.all()

    results = [p.serialize() for p in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK
