var lastCountry = null;

resetInfo = () => {
    $("#idDensity").val(100);
    $("#idIsolation").val(50);
    $("#idAir").val(50);
    $("#idICU").val(50);
};

am4core.ready(function () {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create map instance
    var chart = am4core.create("chartdiv", am4maps.MapChart);
    chart.projection = new am4maps.projections.Miller();

    // Create map polygon series for world map
    var worldSeries = chart.series.push(new am4maps.MapPolygonSeries());
    worldSeries.useGeodata = true;
    worldSeries.geodata = am4geodata_worldLow;
    worldSeries.exclude = ["AQ"];

    var worldPolygon = worldSeries.mapPolygons.template;
    worldPolygon.tooltipText = "{name}";
    worldPolygon.nonScalingStroke = true;
    worldPolygon.strokeOpacity = 0.5;
    worldPolygon.fill = am4core.color("#eee");
    worldPolygon.propertyFields.fill = "color";

    var hs = worldPolygon.states.create("hover");
    hs.properties.fill = chart.colors.getIndex(9);

    var activeState = worldPolygon.states.create("active");
    activeState.properties.fill = chart.colors.getIndex(9);

    // Create country specific series (but hide it for now)
    var countrySeries = chart.series.push(new am4maps.MapPolygonSeries());
    countrySeries.useGeodata = true;
    countrySeries.hide();
    countrySeries.geodataSource.events.on("done", function (ev) {
        worldSeries.hide();
        countrySeries.show();
    });

    var countryPolygon = countrySeries.mapPolygons.template;
    countryPolygon.tooltipText = "{name}";
    countryPolygon.nonScalingStroke = true;
    countryPolygon.strokeOpacity = 0.5;
    countryPolygon.fill = am4core.color("#eee");

    var hs = countryPolygon.states.create("hover");
    hs.properties.fill = chart.colors.getIndex(9);

    countryPolygon.events.on("hit", function (ev) {
        ev.target.isActive = !ev.target.isActive;
    });

    // Set up click events
    worldPolygon.events.on("hit", function (ev) {
        ev.target.series.chart.zoomToMapObject(ev.target);
        ev.target.isActive = true;

        if (lastCountry != null) {
            lastCountry.isActive = false;
        }

        if (lastCountry == ev.target) {
            lastCountry = null;
            $("#nameCountry").css('font-size', '14px');
            $("#nameCountry").text("No selected");
            chart.goHome();
            resetInfo()
        } else {
            $("#sidenavRight").sidenav("open");
            lastCountry = ev.target;
            let name = ev.target.dataItem.dataContext.name;
            if(name.length > 22){
                $("#nameCountry").css('font-size', '11px');
            }else{
                $("#nameCountry").css('font-size', '14px');
            }
            $("#nameCountry").text(name);
        }

        // get info from country
        // ajax requisao
        
    });

    // Zoom control
    chart.zoomControl = new am4maps.ZoomControl();
}); // end am4cnd am4core.ready()