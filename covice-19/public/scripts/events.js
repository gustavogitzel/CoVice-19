var phrases = [
    ' demographic density',
    ' number of hospital beds',
    ' number of population ages 65 and above',
    ' number of urban population'
];

get_situation = ()=>{
    var link = "https://egg-wave.herokuapp.com/submit"; 
        var data = {
        'density':$("#idDensity").val(),
        'icu':$("#idICU").val(),
        'elder':$("#idOld").val(),
        'population':$("#idUrban").val()
        };

        $.ajax({
            type: "GET",
            url: link,
            data: data,
            success: (data)=>{
                let situation = data[0].toLowerCase();
                let suggestionIndex = data[1];

                let wordKey = "Low ";
                if(suggestionIndex < 0){
                    wordKey = "High ";
                    suggestionIndex *= -1;
                }

                let text = phrases[suggestionIndex - 1]
                $("#situation").text(situation);
                $("#suggestionText").text(wordKey + text);
                if(situation == "below"){
                    $("#situationSentence").text("You are safe, but remember, always be careful!");
                    $("#riskCountry").hide();
                }else{
                    $("#situationSentence").text("You are at risk zone. Please, keep calm and stay home!");
                    $("#riskCountry").show();
                }
                $("#sidenavRight").sidenav("open");
            },
            error: (erro)=>{
                console.log(erro);
            }
          });
};

$(document).ready(() =>{

    $.ajaxSetup({
        scriptCharset: "utf-8", //or "ISO-8859-1"
        contentType: "application/json; charset=utf-8"
    });

    
    $("#buttonSubmit").click(()=>{
        get_situation();
    });
});