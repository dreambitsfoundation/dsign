/**
 * Created by Gaurav on 04-08-2016.
 */

$(document).ready(function(){
    $("button[prop]").click(function(){
        var operation=$(this).attr("prop");
        var element=$(this);
        if(operation == "personal_phone" || operation == "personal_mail" || operation == "personal_address" || operation == "personal_gender" || operation == "pro_phone" || operation == "pro_mail" || operation == "profile_phone" || operation == "profile_mail" || operation == "profile_address" || operation == "profile_gender" || operation == "profile_dob"){
            $.ajax({
                type:'POST',
                url:"/privacy_control",
                dataType:'json',
                data:{
                    'operation':operation,
                    'csrfmiddlewaretoken':csrfmiddlewaretoken
                },
                success:function(data){
                    if(data.report){
                        if(data.status){
                            element.removeClass("btn-success");
                            element.children().removeClass("glyphicon-ok");
                            element.addClass("btn-danger");
                            element.children().addClass("glyphicon-remove");
                            var strong=$("strong[prop="+operation+"]");
                            var p=$("p[prop="+operation+"]");
                            strong.html("Hide My "+element.attr("info"));
                            p.html(" <b>Now: </b><span class='glyphicon glyphicon-eye-open'></span> Visible");
                        }else{
                            element.removeClass("btn-danger");
                            element.children().removeClass("glyphicon-remove");
                            element.addClass("btn-success");
                            element.children().addClass("glyphicon-ok");
                            var strong=$("strong[prop="+operation+"]");
                            var p=$("p[prop="+operation+"]");
                            strong.html("Show My "+element.attr("info"));
                            p.html(" <b>Now: </b><span class='glyphicon glyphicon-eye-close'></span> Invisible");
                        }
                    }else{
                        alert("Error occoured!");
                    }
                }
            })
        }
    })
});