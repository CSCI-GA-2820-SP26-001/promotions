$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    function err_msg(res) {
        if (res.responseJSON && res.responseJSON.message) {
            return res.responseJSON.message;
        }
        return "Error";
    }

    function promotion_from_form() {
        let desc = $("#pet_category").val();
        let promo = $("#promo_code").val();
        let av = $("#pet_available").val();
        return {
            "name": $("#pet_name").val(),
            "description": desc === "" ? null : desc,
            "promo_code": promo === "" ? null : promo,
            "discount_amount": parseFloat($("#discount_amount").val()),
            "promotion_type": $("#pet_gender").val(),
            "start_date": $("#pet_birthday").val(),
            "end_date": $("#end_date").val(),
            "is_active": av === "" ? true : (av == "true"),
            "product_id": parseInt($("#product_id").val(), 10)
        };
    }

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#pet_id").val(res.id);
        $("#pet_name").val(res.name);
        $("#pet_category").val(res.description === null ? "" : res.description);
        $("#promo_code").val(res.promo_code === null ? "" : res.promo_code);
        $("#discount_amount").val(res.discount_amount);
        $("#pet_gender").val(res.promotion_type);
        $("#pet_birthday").val(res.start_date.substring(0, 10));
        $("#end_date").val(res.end_date.substring(0, 10));
        if (res.is_active == true) {
            $("#pet_available").val("true");
        } else {
            $("#pet_available").val("false");
        }
        $("#product_id").val(res.product_id);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#pet_name").val("");
        $("#pet_category").val("");
        $("#promo_code").val("");
        $("#discount_amount").val("");
        $("#pet_gender").val("percentage");
        $("#pet_birthday").val("");
        $("#end_date").val("");
        $("#pet_available").val("true");
        $("#product_id").val("");

        // Reset toggle buttons
        $("#active-true").addClass("active");
        $("#active-false").removeClass("active");
        $("#type-percentage").addClass("active");
        $("#type-fixed").removeClass("active");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Validation Functions
    // ****************************************

    function validate_required_fields(fields) {
        for (let field of fields) {
            if (!field.value || field.value.trim() === "") {
                return "Please fill in all required fields: " + field.label;
            }
        }
        return null;
    }

    function validate_numeric_field(value, fieldName) {
        if (isNaN(value) || value === "") {
            return `Please enter a valid ${fieldName}`;
        }
        return null;
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        let data = promotion_from_form();
        
        // Validate required fields
        let requiredFields = [
            { value: $("#pet_name").val(), label: "Name" },
            { value: $("#discount_amount").val(), label: "Discount Amount" },
            { value: $("#pet_birthday").val(), label: "Start Date" },
            { value: $("#end_date").val(), label: "End Date" }
        ];

        let validationError = validate_required_fields(requiredFields);
        if (validationError) {
            flash_message(validationError);
            return;
        }

        // Validate promotion type
        if (!data.promotion_type) {
            flash_message("Select a promotion type (not Any)");
            return;
        }

        // Validate numeric fields
        let discountError = validate_numeric_field(data.discount_amount, "discount amount");
        if (discountError) {
            flash_message(discountError);
            return;
        }

        let productIdError = validate_numeric_field(data.product_id, "product ID");
        if (productIdError) {
            flash_message(productIdError);
            return;
        }

        // Validate discount amount is positive
        if (data.discount_amount <= 0) {
            flash_message("Discount amount must be greater than 0");
            return;
        }

        // Validate product ID is positive
        if (data.product_id <= 0) {
            flash_message("Product ID must be greater than 0");
            return;
        }

        // Validate date range
        if (new Date(data.start_date) >= new Date(data.end_date)) {
            flash_message("Start date must be before end date");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(err_msg(res))
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        let pet_id = $("#pet_id").val();
        
        // Validate ID is provided
        if (!pet_id || pet_id.trim() === "") {
            flash_message("Please enter a Promotion ID to update");
            return;
        }

        let data = promotion_from_form();
        
        // Validate required fields
        let requiredFields = [
            { value: $("#pet_name").val(), label: "Name" },
            { value: $("#discount_amount").val(), label: "Discount Amount" },
            { value: $("#pet_birthday").val(), label: "Start Date" },
            { value: $("#end_date").val(), label: "End Date" }
        ];

        let validationError = validate_required_fields(requiredFields);
        if (validationError) {
            flash_message(validationError);
            return;
        }

        // Validate promotion type
        if (!data.promotion_type) {
            flash_message("Select a promotion type (not Any)");
            return;
        }

        // Validate numeric fields
        let discountError = validate_numeric_field(data.discount_amount, "discount amount");
        if (discountError) {
            flash_message(discountError);
            return;
        }

        let productIdError = validate_numeric_field(data.product_id, "product ID");
        if (productIdError) {
            flash_message(productIdError);
            return;
        }

        // Validate discount amount is positive
        if (data.discount_amount <= 0) {
            flash_message("Discount amount must be greater than 0");
            return;
        }

        // Validate product ID is positive
        if (data.product_id <= 0) {
            flash_message("Product ID must be greater than 0");
            return;
        }

        // Validate date range
        if (new Date(data.start_date) >= new Date(data.end_date)) {
            flash_message("Start date must be before end date");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/promotions/${pet_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(err_msg(res))
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        let pet_id = $("#pet_id").val();

        // Validate ID is provided
        if (!pet_id || pet_id.trim() === "") {
            flash_message("Please enter a Promotion ID to retrieve");
            return;
        }

        // Validate ID is numeric
        if (isNaN(pet_id)) {
            flash_message("Promotion ID must be a valid number");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${pet_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(err_msg(res))
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        let pet_id = $("#pet_id").val();

        // Validate ID is provided
        if (!pet_id || pet_id.trim() === "") {
            flash_message("Please enter a Promotion ID to delete");
            return;
        }

        // Validate ID is numeric
        if (isNaN(pet_id)) {
            flash_message("Promotion ID must be a valid number");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/promotions/${pet_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for Promotions
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let typeVal = $("#pet_gender").val();
        let is_active = $("#pet_available").val();
        let product_id = $("#product_id").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + encodeURIComponent(name)
        }
        // Only add type filter if it's not set to "all"
        if (typeVal && typeVal !== "all") {
            if (queryString.length > 0) {
                queryString += '&type=' + encodeURIComponent(typeVal)
            } else {
                queryString += 'type=' + encodeURIComponent(typeVal)
            }
        }
        // Only add is_active filter if it's not empty and not set to "all"
        if (is_active && is_active !== "" && is_active !== "all") {
            if (queryString.length > 0) {
                queryString += '&is_active=' + encodeURIComponent(is_active)
            } else {
                queryString += 'is_active=' + encodeURIComponent(is_active)
            }
        }
        if (product_id) {
            if (queryString.length > 0) {
                queryString += '&product_id=' + encodeURIComponent(product_id)
            } else {
                queryString += 'product_id=' + encodeURIComponent(product_id)
            }
        }

        $("#flash_message").empty();

        let listUrl = queryString ? `/promotions?${queryString}` : "/promotions";

        let ajax = $.ajax({
            type: "GET",
            url: listUrl,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Type</th>'
            table += '<th class="col-md-1">Active</th>'
            table += '<th class="col-md-1">Product</th>'
            table += '<th class="col-md-2">Start</th>'
            table += '<th class="col-md-2">End</th>'
            table += '</tr></thead><tbody>'
            let firstPet = "";
            for(let i = 0; i < res.length; i++) {
                let p = res[i];
                table +=  `<tr id="row_${i}"><td>${p.id}</td><td>${p.name}</td><td>${p.promotion_type}</td><td>${p.is_active}</td><td>${p.product_id}</td><td>${p.start_date}</td><td>${p.end_date}</td></tr>`;
                if (i == 0) {
                    firstPet = p;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(err_msg(res))
        });

    });

    // ****************************************
    // Activate / Deactivate Promotion
    // ****************************************

    function put_is_active(flag) {
        let pet_id = $("#pet_id").val();
        if (!pet_id) {
            flash_message("Enter promotion ID");
            return;
        }
        $("#flash_message").empty();
        let ajax = $.ajax({
            type: "GET",
            url: `/promotions/${pet_id}`,
            contentType: "application/json",
            data: ''
        });
        ajax.done(function(res){
            res.is_active = flag;
            let putAjax = $.ajax({
                type: "PUT",
                url: `/promotions/${pet_id}`,
                contentType: "application/json",
                data: JSON.stringify(res)
            });
            putAjax.done(function(r){
                update_form_data(r);
                flash_message("Success");
            });
            putAjax.fail(function(res){
                flash_message(err_msg(res));
            });
        });
        ajax.fail(function(res){
            flash_message(err_msg(res));
        });
    }

    $("#activate-btn").click(function () {
        put_is_active(true);
    });

    $("#deactivate-btn").click(function () {
        put_is_active(false);
    });

})
