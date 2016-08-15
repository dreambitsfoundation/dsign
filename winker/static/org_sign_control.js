/**
 * Created by Gaurav on 11-08-2016.
 */

$(document).ready(function(){
    $("a[key]").click(function(){
        alert($(this).attr("key"));
        var key=$(this).attr("key");
        var element=$(this);
        var action=$(this).attr("id");
        var invalidation_reason=$("#invalidation_reason").val();

    });
    $("a[code]").click(function(){
        var element=$(this);
        var key=$(this).attr("code");
        $(".invalidator").attr("key",key);
        $("#invalidation_reason").val("");
        $("#invalidation_popup").fadeIn();
    });
    $("#invalidation_window_close").click(function(){
        $("#invalidation_reason").val("");
        $("#invalidation_popup").fadeOut();
    })
});
function control_request(key,action){
     $.ajax({
        type:'POST',
        url:"/org_admin/sign_control",
        data:{
            'key':key,
            'action':action,
            'csrfmiddlewaretoken':csrfmiddlewaretoken
        },
        dataType:'json',
        success:function(data){
            if(data.result){
                if(data.action="grant_user_permission"){
                    alert("Permission Granted");
                    var element_key=data.key;
                    alert(element_key);
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                    var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="revoke_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'revoke_user_permission\')"></a>').html('<span class="glyphicon glyphicon-remove text-danger"></span> Revoke Usage Permission');
                    link1.append(link1a);
                    var link2=$('<li role="separator" class="divider"></li>');
                    var link3=$('<li></li>');
                    var link3a=$('<a key="'+element_key+'" id="unhault" onclick="control_request(key=\''+element_key+'\',action=\'unhault\')"></a>').html('<span class="glyphicon glyphicon-ok-circle text-success"></span> Un-Hault');
                    link3.append(link3a);
                    var link4=$('<li role="separator" class="divider"></li>');
                    var link5=$('<li></li>');
                    var link5a=$('<a code="'+element_key+'" id="invalidate" onclick="invalidation_request(key=\''+element_key+'\',action=\'invalidate\')"></a>').html('<span class="glyphicon glyphicon-ban-circle text-danger"></span> Invalidate');
                    link5.append(link5a);
                    this_element.append(link1,link2,link3,link4,link5);
                }
                if(data.action=="revoke_user_permission"){
                    alert("Permission Revoked");
                    var element_key=data.key;
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                    var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="grant_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'grant_user_permission\')"></a>').html('<span class="glyphicon glyphicon-ok text-success"></span> Grant Usage Permission');
                    link1.append(link1a);
                    var link2=$('<li role="separator" class="divider"></li>');
                    var link3=$('<li></li>');
                    var link3a=$('<a key="'+element_key+'" id="unhault" onclick="control_request(key=\''+element_key+'\',action=\'unhault\')"></a>').html('<span class="glyphicon glyphicon-ok-circle text-success"></span> Un-Hault');
                    link3.append(link3a);
                    var link4=$('<li role="separator" class="divider"></li>');
                    var link5=$('<li></li>');
                    var link5a=$('<a key="'+element_key+'" id="invalidate" onclick="invalidation_request(key=\''+element_key+'\',action=\'invalidate\')"></a>').html('<span class="glyphicon glyphicon-ban-circle text-danger"></span> Invalidate');
                    link5.append(link5a);
                    this_element.append(link1,link2,link3,link4,link5);
                }
                if(data.action=="invalidate"){
                    alert("Invalidated");
                    var element_key=data.key;
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                    var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="delete" onclick="control_request(key=\''+element_key+'\',action=\'delete\')"></a>').html('<span class="glyphicon glyphicon-trash text-danger"></span> Delete Signature');
                    link1.append(link1a);
                }
                if(data.action=="hault_grant_user_permission"){
                    var element_key=data.key;
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                   var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="revoke_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'revoke_user_permission\')"></a>').html('<span class="glyphicon glyphicon-remove text-danger"></span> Revoke Usage Permission');
                    link1.append(link1a);
                    var link2=$('<li role="separator" class="divider"></li>');
                    var link3=$('<li></li>');
                    var link3a=$('<a key="'+element_key+'" id="unhault" onclick="control_request(key=\''+element_key+'\',action=\'unhault\')"></a>').html('<span class="glyphicon glyphicon-ok-circle text-success"></span> Un-Hault');
                    link3.append(link3a);
                    var link4=$('<li role="separator" class="divider"></li>');
                    var link5=$('<li></li>');
                    var link5a=$('<a key="'+element_key+'" id="invalidate" onclick="invalidation_request(key=\''+element_key+'\',action=\'invalidate\')"></a>').html('<span class="glyphicon glyphicon-ban-circle text-danger"></span> Invalidate');
                    link5.append(link5a);
                    this_element.append(link1,link2,link3,link4,link5);
                    $("tr[key="+element_key+"]").removeClass("success").addClass("warning");
                }
                if(data.action=="hault_revoke_user_permission"){
                    var element_key=data.key;
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                    var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="grant_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'grant_user_permission\')"></a>').html('<span class="glyphicon glyphicon-ok text-success"></span> Grant Usage Permission');
                    link1.append(link1a);
                    var link2=$('<li role="separator" class="divider"></li>');
                    var link3=$('<li></li>');
                    var link3a=$('<a key="'+element_key+'" id="unhault" onclick="control_request(key=\''+element_key+'\',action=\'unhault\')"></a>').html('<span class="glyphicon glyphicon-ok-circle text-success"></span> Un-Hault');
                    link3.append(link3a);
                    var link4=$('<li role="separator" class="divider"></li>');
                    var link5=$('<li></li>');
                    var link5a=$('<a key="'+element_key+'" id="invalidate" onclick="control_request(key=\''+element_key+'\',action=\'invalidate\')"></a>').html('<span class="glyphicon glyphicon-ban-circle text-danger"></span> Invalidate');
                    link5.append(link5a);
                    this_element.append(link1,link2,link3,link4,link5);
                    $("tr[key="+element_key+"]").removeClass("success").addClass("warning");
                }
                if(data.action=="delete"){
                    var element_key=data.key;
                    $("tr[key="+element_key+"]").remove();
                }
                if(data.action=='unhault'){
                    var element_key=data.key;
                    var this_element=$("a[key="+element_key+"]").parent().parent();
                    this_element.empty();
                    var link1=$("<li></li>");
                    var link1a=$('<a key="'+element_key+'" id="hault_grant_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'hault_grant_user_permission\')"></a>').html('<span class="glyphicon glyphicon-ok text-success"></span> Hault and Grant Usage Permission');
                    link1.append(link1a);
                    var link2=$("<li></li>");
                    var link2a=$('<a key="'+element_key+'" id="hault_revoke_user_permission" onclick="control_request(key=\''+element_key+'\',action=\'hault_revoke_user_permission\')"></a>').html('<span class="glyphicon glyphicon-remove text-danger"></span> Hault and Revoke Usage Permission');
                    link2.append(link2a);
                    this_element(link1,link2);
                    $("tr[key="+element_key+"]").removeClass("warning");
                }
            }else{
                alert("False");
            }

        }
    });
}