$(document).ready(function(){
    $('.main-row').on('click', function(){
        $content = $(this).find('.main-row-content');
        if(!$content.hasClass('display-content')){
            $content.slideDown(500, 'easeOutBack').addClass('display-content');
        }else{
            $content.slideUp(500, 'easeOutBack').removeClass('display-content');
        }
    });

    /* ===========================================================================
                            .:: SEARCH ::. 
    =========================================================================== */
    ajax_search();

    function ajax_search() {
        /*var keywords = $('#portal-searchbox').val();
        var type = $('#search-type').text();
        var sort = $('#search-sort').text();
        var industry = $('#search-industry').text();
        var salary = $('#search-salary').text();
        data = {};
        data['keywords'] = keywords;
        data['type'] = type;
        data['sort'] = sort;
        data['industry'] = industry;
        data['salary'] = salary;
        data['jobapps'] = global_user_jobapps;
        data['bookmarkapps'] = global_user_bookmarkapps;
        $.ajax({
            type: "POST",
            url: "processsearch.php",
            data: data,
            success: function(results){
                $('#all-posts').html(results);
                hideDescrip();
            }
        });*/
        var query = $("#main-search").val();
        var dept = $('#btn-dept span').text();
        var type = $('#btn-type span').text(); //top senders/receivers
        var category = $('#btn-cat span').text(); //tags

        data = {};
        data['q'] = query;
        data['dept'] = dept;
        data['type'] = type;
        data['category'] = category;

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

    $("#search-button").click(function() {
        ajax_search(query);
    });
    $('#main-search').live('keypress', function(event){
        if(event.keyCode == 13){
            $('#search-button').click();
        }
    });
    /* ===========================================================================
                            .:: TYPE DROPDOWN ::. 
    =========================================================================== */
    var $currToggle = '';
    $('.dropdown-toggle').toggle(function(){
        if($currToggle !== '' && $currToggle.attr('id') !== $(this).attr('id')){
            $currToggle.click();
        }
        $this = $(this);
        var btnid = $this.attr('id');
        $currToggle = $this;
        $dropmenu = $this.parent().find('.drop-menu');
        $dropmenu.removeClass('hidden');
        $dropmenu.animate({ 'opacity' : '1', 'margin' : '50px auto'}, 300);
    }, function(){
        $currToggle = '';
        $dropmenu = $(this).parent().find('.drop-menu');
        $dropmenu.stop().animate({ 'opacity' : '0', 'margin' : '35px auto'}, 150, function(){
            $(this).addClass('hidden');
        });
    });
    $('.drop-menu li').live('click', function(){
        var option = $(this).find('span').text();
        $btn_group = $(this).parent().parent();
        $btn_group.find('.btn-option').text(option);
        $btn_group.find('.dropdown-toggle').click();
        var default_text = ['All Departments', 'Latest Kudos', 'All Categories'];
        if($.inArray(option, default_text) > -1){
            $btn_group.find('.btn').removeClass('btn-dark').addClass('btn-primary');
        }else{
            $btn_group.find('.btn').removeClass('btn-primary').addClass('btn-dark');
        }
        ajax_search();
    });
});