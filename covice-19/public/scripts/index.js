$(document).ready(function () {
    $(".sidenav").sidenav();
    $("#sidenavRight").sidenav({
        edge: "right"
    });
    var array_of_dom_elements = document.querySelectorAll("input[type=range]");
    M.Range.init(array_of_dom_elements);
    $("select").formSelect();
    $('.modal').modal();
});

function RequestService() {
    $.ajax({
        type: "GET",
        url: "url/adho/ajaj",
        contentType: "application/json; charset=utf-8",
        data: "{}",
        dataType: "json",
        success: function (data) {
            SucessCallback(data.d);
        },
        error: function (data) {
            FailureCallBack(data);
        }
    });
}

function SucessCallback(result) {
    $("p").html(
        "Resultado: " + result.Message + " <br /> Descrição: " + result.Description
    );
}

function FailureCallBack(result) {
    alert(result.status + " " + result.statusText);
}