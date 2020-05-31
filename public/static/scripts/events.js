
$(document).ready(() =>{
    $("input,select").change(()=>{
        $.post("/submit", {
            density:$("#idDensity").val(),
            isolation:$("#idIsolation").val(),
            air:$("#idAir").val(),
            icu:$("#idICU").val()
        }).done(function (reply) {
            $("#idResult").text(reply);
            $("#sidenavRight").sidenav("open");
        });
    });
});
