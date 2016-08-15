/**
 * Created by Gaurav on 10-07-2016.
 */

$(document).ready(function(){
    $("#id_email").focus();
    $("#email").addClass("active");

    $("#id_email").focus(function(){
       $("#email").addClass("active")
   });
    $("#id_password").focus(function(){
       $("#password").addClass("active")
   });
    $("#id_email").blur(function(){
       $("#email").removeClass("active")
   });
    $("#id_password").blur(function(){
       $("#password").removeClass("active")
   });
})
