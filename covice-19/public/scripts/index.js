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