$(document).ready(function(){
	$('.main-row').on('click', function(){
		$content = $(this).find('.main-row-content');
		if(!$content.hasClass('display-content')){
			$content.slideDown(500, 'easeOutBack').addClass('display-content');
		}else{
			$content.slideUp(500, 'easeOutBack').removeClass('display-content');
		}
	});
});