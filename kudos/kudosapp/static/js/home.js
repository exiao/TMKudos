$(document).ready(function() {
    var query = $("#main-search").val();
    ajax_search(query);
});

$("#search-button").click(function() {
    var query = $("#main-search").val();
    ajax_search(query);
});

function ajax_search(query) {
    data = {};
    data['q'] = query;
    $.ajax({
      url: "/search/",
      type: "GET",
      cache: false,
      data: data,
      dataType: "text",
      success: function(html){
        $(".search-results-container").html(html);
      }
    });
}