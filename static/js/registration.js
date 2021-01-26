try {
    let url = $("#personForm").attr("data-cities-url");
    $(document).ready(function () {
        if ($("#id_country").val() === "1") {
            $("#city2_country").css("display", "none");
            $("#turkey_based").show();
            $.ajax({
                url: url,
                success: function (data) {
                    $("#id_city").html(data);
                }
            }).done(function () {
                let url = $("#personForm").attr("data-districts-url");
                $.ajax({
                    url: url,
                    data: {
                        'city': $("#id_city").val()
                    },
                    success: function (data) {
                        $("#id_district").html(data);
                        let url = $("#personForm").attr("data-towns-url");
                        $.ajax({
                            url: url,
                            data: {
                                'district': $("#id_district").val()
                            },
                            success: function (data) {
                                $("#id_town").html(data);
                            }
                        });
                    }
                });
            });
        } else {
            $("#turkey_based").hide();
            $("#city_country").css("display", "none");
            $("#city2_country").css("display", "block");
        }
    });
    $("#id_country").change(function () {
        if ($("#id_country").val() === "1") {
            $("#turkey_based").show();
            $("#city2_country").css("display", "none");
            $("#city_country").show();
            $.ajax({
                url: url,
                success: function (data) {
                    $("#id_city").html(data);
                }
            });
        } else {
            $("#turkey_based").hide();
            $("#city_country").css("display", "none");
            $("#city2_country").css("display", "block");
        }
    });

} catch (err) {
    console.log(err);
}

try {
    $("#id_city").change(function () {
        let url = $("#personForm").attr("data-districts-url");
        let cityID = $("#id_city").val();
        $.ajax({
            url: url,
            data: {
                'city': cityID
            },
            success: function (data) {
                $("#id_district").html(data);
                let url = $("#personForm").attr("data-towns-url");
                let districtID = $("#id_district").val();
                $.ajax({
                    url: url,
                    data: {
                        'district': districtID
                    },
                    success: function (data) {
                        $("#id_town").html(data);
                    }
                });
            }
        });
    });
} catch (err) {
    console.log(err);
}
try {
    $("#id_district").change(function () {
        let url = $("#personForm").attr("data-towns-url");
        let districtID = $("#id_district").val();
        $.ajax({
            url: url,
            data: {
                'district': districtID
            },
            success: function (data) {
                $("#id_town").html(data);
            }
        });
    });
} catch (err) {
    console.log(err);
}