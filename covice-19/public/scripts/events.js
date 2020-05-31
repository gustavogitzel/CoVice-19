$(document).ready(() =>{
    var url = "/submit"; // miller poe a url
    $("#buttonSubmit").click(()=>{
        $.post("/submit", {
            density:$("#idDensity").val(),
            isolation:$("#idIsolation").val(),
            air:$("#idAir").val(),
            icu:$("#idICU").val()
        }).done(function (reply) {
            // atualiza pagina de acordo com oq veio
            $("#sidenavRight").sidenav("open");
        });
    });
});