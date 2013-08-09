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
                            .:: TYPE DROPDOWN ::. (ci2a)
    =========================================================================== */
    var $currToggle = '';
	$('.dropdown-toggle').toggle(function(){
		if($currToggle !== ''){
			$currToggle.click();
		}
		$this = $(this);
		var btnid = $this.attr('id');
		$currToggle = $this;
    	$dropmenu = $this.parent().find('.drop-menu');
    	$dropmenu.removeClass('hidden');
    	$dropmenu.animate({ 'opacity' : '1', 'margin' : '50px auto'}, 300);
    }, function(){
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
    	var default_text = ['Department', 'Search Type', 'Sort By', 'Category'];
    	if($.inArray(option, default_text) > -1){
    		$btn_group.find('.btn').removeClass('btn-dark').addClass('btn-primary');
    	}else{
    		$btn_group.find('.btn').removeClass('btn-primary').addClass('btn-dark');
    	}
    });
});