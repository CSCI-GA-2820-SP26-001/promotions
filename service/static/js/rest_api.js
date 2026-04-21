$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    function err_msg(res) {
        if (res.responseJSON && res.responseJSON.message) {
            return res.responseJSON.message;
        }
        return "An unexpected error occurred.";
    }

    function flash_message(message) {
        $("#flash_message").empty().append(message);
    }

    // Build promotion object from the CRUD form fields
    function promotion_from_form() {
        let desc = $("#promotion_description").val().trim();
        let promo = $("#promotion_promo_code").val().trim();
        let av = $("#promotion_is_active").val();
        return {
            "name":             $("#promotion_name").val().trim(),
            "description":      desc  === "" ? null : desc,
            "promo_code":       promo === "" ? null : promo,
            "discount_amount":  parseFloat($("#promotion_discount_amount").val()),
            "promotion_type":   $("#promotion_type").val(),
            "start_date":       $("#promotion_start_date").val(),
            "end_date":         $("#promotion_end_date").val(),
            "is_active":        av === "true",
            "product_id":       parseInt($("#promotion_product_id").val(), 10)
        };
    }

    // Validate the CRUD form; returns the data object or null on failure
    function validate_form() {
        let data = promotion_from_form();

        if (!data.name) {
            flash_message("Name is required.");
            return null;
        }
        if (!data.promotion_type) {
            flash_message("Promotion type is required.");
            return null;
        }
        if (isNaN(data.discount_amount) || data.discount_amount < 0) {
            flash_message("Enter a valid discount amount (0 or greater).");
            return null;
        }
        if (!data.start_date) {
            flash_message("Start date is required.");
            return null;
        }
        if (!data.end_date) {
            flash_message("End date is required.");
            return null;
        }
        if (data.end_date < data.start_date) {
            flash_message("End date must be on or after start date.");
            return null;
        }
        if (isNaN(data.product_id) || data.product_id <= 0) {
            flash_message("Enter a valid Product ID (positive integer).");
            return null;
        }
        return data;
    }

    // Populate the CRUD form from a promotion object
    function update_form_data(res) {
        $("#promotion_id").val(res.id);
        $("#promotion_name").val(res.name);
        $("#promotion_description").val(res.description === null ? "" : res.description);
        $("#promotion_promo_code").val(res.promo_code === null ? "" : res.promo_code);
        $("#promotion_discount_amount").val(res.discount_amount);
        $("#promotion_type").val(res.promotion_type);
        $("#promotion_start_date").val(res.start_date.substring(0, 10));
        $("#promotion_end_date").val(res.end_date.substring(0, 10));
        $("#promotion_is_active").val(res.is_active ? "true" : "false");
        $("#promotion_product_id").val(res.product_id);
    }

    // Clear all CRUD form fields
    function clear_form_data() {
        $("#promotion_id").val("");
        $("#promotion_name").val("");
        $("#promotion_description").val("");
        $("#promotion_promo_code").val("");
        $("#promotion_discount_amount").val("");
        $("#promotion_type").val("percentage");
        $("#promotion_start_date").val("");
        $("#promotion_end_date").val("");
        $("#promotion_is_active").val("true");
        $("#promotion_product_id").val("");
    }

    // Render the results table; each row is clickable and loads the promotion into the CRUD form
    function render_results(data) {
        let tbody = $("#search_results_body");
        tbody.empty();

        if (data.length === 0) {
            tbody.append(
                '<tr><td colspan="7" class="text-center text-muted">' +
                'No promotions found matching your criteria.</td></tr>'
            );
            return;
        }

        for (let i = 0; i < data.length; i++) {
            let p = data[i];
            let row = $([
                '<tr style="cursor:pointer;" title="Click to load into the edit form below">',
                '<td>', p.id,             '</td>',
                '<td>', p.name,           '</td>',
                '<td>', p.promotion_type, '</td>',
                '<td>', p.is_active,      '</td>',
                '<td>', p.product_id,     '</td>',
                '<td>', p.start_date,     '</td>',
                '<td>', p.end_date,       '</td>',
                '</tr>'
            ].join(""));

            // Store the full promotion object on the row element
            row.data("promotion", p);

            row.click(function () {
                update_form_data($(this).data("promotion"));
                flash_message("Promotion loaded into the form. Edit the fields and click Update.");
                $("html, body").animate({ scrollTop: $("#crud-section").offset().top }, 400);
            });

            tbody.append(row);
        }
    }

    // ****************************************
    //  Q U E R Y   /   F I L T E R
    // ****************************************

    $("#search-btn").click(function () {
        let name       = $("#filter_name").val().trim();
        let typeVal    = $("#filter_type").val();
        let is_active  = $("#filter_is_active").val();
        let product_id = $("#filter_product_id").val().trim();

        // Validate filter inputs
        if (product_id && isNaN(parseInt(product_id, 10))) {
            flash_message("Product ID filter must be a valid number.");
            return;
        }

        let params = [];
        if (name)       params.push("name="       + encodeURIComponent(name));
        if (typeVal)    params.push("type="        + encodeURIComponent(typeVal));
        if (is_active !== "") params.push("is_active=" + encodeURIComponent(is_active));
        if (product_id) params.push("product_id=" + encodeURIComponent(product_id));

        let url = params.length > 0 ? "/promotions?" + params.join("&") : "/promotions";

        flash_message("Searching...");

        $.ajax({
            type: "GET",
            url: url,
            contentType: "application/json",
            data: ""
        }).done(function (res) {
            render_results(res);
            if (res.length === 0) {
                flash_message("No promotions found matching your criteria.");
            } else {
                flash_message("Found " + res.length + " promotion(s). Click a row to edit it.");
            }
        }).fail(function (res) {
            flash_message("Query failed: " + err_msg(res));
        });
    });

    // Clear only the query filter fields
    $("#clear-filters-btn").click(function () {
        $("#filter_name").val("");
        $("#filter_type").val("");
        $("#filter_is_active").val("");
        $("#filter_product_id").val("");
        flash_message("");
    });

    // ****************************************
    //  C R E A T E
    // ****************************************

    $("#create-btn").click(function () {
        let data = validate_form();
        if (!data) return;

        flash_message("");

        $.ajax({
            type: "POST",
            url: "/promotions",
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done(function (res) {
            update_form_data(res);
            flash_message("Promotion '" + res.name + "' created successfully.");
        }).fail(function (res) {
            flash_message("Create failed: " + err_msg(res));
        });
    });

    // ****************************************
    //  U P D A T E
    // ****************************************

    $("#update-btn").click(function () {
        let promotion_id = $("#promotion_id").val().trim();
        if (!promotion_id) {
            flash_message("Promotion ID is required to update. Select a row from the results or retrieve a promotion first.");
            return;
        }

        let data = validate_form();
        if (!data) return;

        flash_message("");

        $.ajax({
            type: "PUT",
            url: "/promotions/" + promotion_id,
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done(function (res) {
            update_form_data(res);
            flash_message("Promotion '" + res.name + "' updated successfully.");
        }).fail(function (res) {
            flash_message("Update failed: " + err_msg(res));
        });
    });

    // ****************************************
    //  R E T R I E V E
    // ****************************************

    $("#retrieve-btn").click(function () {
        let promotion_id = $("#promotion_id").val().trim();
        if (!promotion_id) {
            flash_message("Enter a Promotion ID to retrieve.");
            return;
        }

        flash_message("");

        $.ajax({
            type: "GET",
            url: "/promotions/" + promotion_id,
            contentType: "application/json",
            data: ""
        }).done(function (res) {
            update_form_data(res);
            flash_message("Promotion '" + res.name + "' loaded.");
        }).fail(function (res) {
            clear_form_data();
            flash_message("Retrieve failed: " + err_msg(res));
        });
    });

    // ****************************************
    //  D E L E T E
    // ****************************************

    $("#delete-btn").click(function () {
        let promotion_id = $("#promotion_id").val().trim();
        if (!promotion_id) {
            flash_message("Enter a Promotion ID to delete.");
            return;
        }

        flash_message("");

        $.ajax({
            type: "DELETE",
            url: "/promotions/" + promotion_id,
            contentType: "application/json",
            data: ""
        }).done(function () {
            clear_form_data();
            flash_message("Promotion deleted successfully.");
        }).fail(function (res) {
            flash_message("Delete failed: " + err_msg(res));
        });
    });

    // ****************************************
    //  C L E A R   F O R M
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data();
        flash_message("");
    });

    // ****************************************
    //  A C T I V A T E  /  D E A C T I V A T E
    // ****************************************

    function set_active(flag) {
        let promotion_id = $("#promotion_id").val().trim();
        if (!promotion_id) {
            flash_message("Enter or select a Promotion ID first.");
            return;
        }

        flash_message("");

        // Fetch current data, flip is_active, then PUT
        $.ajax({
            type: "GET",
            url: "/promotions/" + promotion_id,
            contentType: "application/json",
            data: ""
        }).done(function (res) {
            res.is_active = flag;
            $.ajax({
                type: "PUT",
                url: "/promotions/" + promotion_id,
                contentType: "application/json",
                data: JSON.stringify(res)
            }).done(function (r) {
                update_form_data(r);
                let action = flag ? "activated" : "deactivated";
                flash_message("Promotion '" + r.name + "' " + action + " successfully.");
            }).fail(function (res) {
                flash_message("Action failed: " + err_msg(res));
            });
        }).fail(function (res) {
            flash_message("Could not load promotion: " + err_msg(res));
        });
    }

    $("#activate-btn").click(function ()   { set_active(true);  });
    $("#deactivate-btn").click(function () { set_active(false); });

});
