$(document).ready(function () {
    let output = $("#outputExplore")

    $(".hero-image").click(function () {

        let hero_id = $(this).data("heroid");
        let url = `/stats/${hero_id}` 
        $.get(url , function (data) {

            let s = JSON.stringify(data);
            output.val(s);
        });
    })

}
)