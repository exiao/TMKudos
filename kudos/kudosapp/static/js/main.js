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
    var query = $("#main-search").val();
    ajax_search(query);

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

	$("#search-button").click(function() {
	    var query = $("#main-search").val();
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
    	var default_text = ['All Departments', 'All Sender Types', 'Latest Kudos', 'All Categories'];
    	if($.inArray(option, default_text) > -1){
    		$btn_group.find('.btn').removeClass('btn-dark').addClass('btn-primary');
    	}else{
    		$btn_group.find('.btn').removeClass('btn-primary').addClass('btn-dark');
    	}
    });
});