$(document).ready(

  function(){

    $('#next').click(
      function(){
        if($('.pt-page-current').next().attr('class').indexOf('pt-page')<0 ){}
        else{
        var n = $('.pt-page-current');
        $('.pt-page-current').removeClass('pt-page-current');
        n.next('.pt-page').addClass('pt-page-current');
      }
}
    );
    $('#previous').click(
      function(){
        if($('.pt-page-current').prev().attr('class').indexOf('pt-page')<0){

        }
        else{
        var n = $('.pt-page-current');
        $('.pt-page-current').removeClass('pt-page-current');
        n.prev('.pt-page').addClass('pt-page-current');
      }
      }
    );

  }


);
