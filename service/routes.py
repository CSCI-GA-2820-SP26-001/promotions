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
YourResourceModel Service

This service implements a REST API that allows you to Create, Read, Update
and Delete YourResourceModel
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import YourResourceModel
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Todo: Place your REST API code here ...
######################################################################
# LIST PROMOTIONS BY TYPE
######################################################################
@app.route("/promotions", methods=["GET"])
def list_promotions():
    """Returns all Promotions, optionally filtered by type"""
    app.logger.info("Request to list promotions...")

    promotion_type = request.args.get("type")

    if promotion_type:
        app.logger.info("Filtering by type: %s", promotion_type)
        try:
            type_enum = PromotionType[promotion_type.upper()]
        except KeyError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid promotion type: {promotion_type}",
            )
        promotions = Promotion.find_by_type(type_enum)
    else:
        promotions = Promotion.all()

    results = [p.serialize() for p in promotions]
    app.logger.info("Returning %d promotions", len(results))
    return jsonify(results), status.HTTP_200_OK
