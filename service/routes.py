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
from flask import jsonify, abort
from flask import current_app as app
from service.common import status
from service.models import Promotion


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
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# READ A PROMOTION
######################################################################
@app.route("/promotions/<int:promotion_id>", methods=["GET"])
def get_promotion(promotion_id):
    """
    Retrieve a single Promotion

    This endpoint will return a Promotion based on its id
    """
    app.logger.info("Request to retrieve a promotion with id [%s]", promotion_id)

    promotion = Promotion.find(promotion_id)
    if not promotion:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Promotion with id '{promotion_id}' was not found."
        )

    return jsonify(promotion.serialize()), status.HTTP_200_OK


# Todo: Place your REST API code here ...
