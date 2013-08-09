

$.ajax({
  url: "/search/",
  type: "GET",
  cache: false,
  dataType: "html"
  success: function(json){
    $("#results").append(html);
  }
});