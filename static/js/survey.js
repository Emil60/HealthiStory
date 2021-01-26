try {
    console.log("woman problems")
    $(document).ready(function () {
        if ($("#id_gender").val() === "female") {
            $("#female-only-survey").show();
        } else {
            $("#female-only-survey").hide();
        }

        $("#id_gender").change(function () {
            if ($("#id_gender").val() === "female") {
                $("#female-only-survey").show();
            } else {
                $("#female-only-survey").hide();
            }
        })

    });
} catch (err) {
    console.log("survey error");
}