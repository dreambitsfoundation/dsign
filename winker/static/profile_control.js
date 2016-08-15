/**
 * Created by Gaurav on 11-07-2016.
 */

$(document).ready(function(){
    $("#pro_progress").animate({
        width:'50%'
    },{speed:'slow',easing:'swing',duration:2000});
    $("#pro_progress").removeClass("active");
    $("#per_progress").animate({
        width:'50%'
    },{speed:'slow',easing:'swing',duration:2000});
    $("#per_progress").removeClass("active");
    $('[data-toggle="popover"]').popover();
    /*$('#profile_navigation').affix({
        offset:10
    });*/
    $('[data-toggle="tooltip"]').tooltip();
});
