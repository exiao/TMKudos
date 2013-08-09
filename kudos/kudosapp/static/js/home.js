

$.ajax({
  url: "/",
  type: "GET",
  cache: false,
  success: function(html){
    $("#results").append(html);
  }
});