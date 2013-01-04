function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "&nbsp;");
}

var select_station = function(station) {
  svg.selectAll(".line_branch, .station")
     .classed("active", false);
  $(station.lines).each(function(i, e) {
    svg.selectAll(".line_branch.line_" + e + ", .station.line_" + e )
    .classed("active", true);
  });
  $(".help").hide();
  $(".infos_station").show();
  $(".infos_station h3 span").html(station.name);
  $(".infos_station .trafic").html(numberWithCommas(station.trafic));
  $(".infos_station .latitude").html(station.latitude);
  $(".infos_station .longitude").html(station.longitude);
  $(".infos_station .rank").html(station.rank);
}

var deselect_station = function(station) {
  svg.selectAll(".line_branch, .station")
     .classed("active", true);
  $(".help").show();
  $(".infos_station").hide();
}

var select_line = function(line) {
  svg.selectAll(".line_branch, .station")
     .classed("active", false);
  svg.selectAll(".line_branch.line_" + line.key + ", .station.line_" + line.key )
    .classed("active", true);
  $(".help").hide();
  $(".infos_line").show();
  $(".infos_line h3 span").html("Ligne <span class='sign line_" + line.key + "'>" + line.key + "</line>");
  var sum = 0;
  var ul = $(".infos_line ul");
  ul.empty();
  $(svg.selectAll(".station.line_" + line.key).sort(function(x1, x2) { return x1.trafic < x2.trafic }).data()).each(function(i, e) {
    ul.append('<li>' + e.name + "&nbsp;: " +
                                    '' + numberWithCommas(e.trafic) + "</li>");
    sum += e.trafic;
  });
  $(".infos_line .trafic").html(numberWithCommas(sum));
}

var deselect_line = function(line) {
  svg.selectAll(".line_branch, .station")
     .classed("active", true);
  $(".help").show();
  $(".infos_line").hide();
}
