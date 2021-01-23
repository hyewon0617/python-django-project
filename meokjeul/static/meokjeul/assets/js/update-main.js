$(document).ready(function(){

    let csrf_token = $('[name=csrfmiddlewaretoken]').val();

    $('#restaurantUpdateBtn').on("click", function(){
        let id = $('input[name=id]').val();
        let password = $('input[name=password]').val();

        $.ajax({
            url: "/update/checkPw",
            type: "post",
            data: {
                'id': id,
                'password': password
            },

            beforeSend: function(xhr){
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success: function(result){
                if(result === "match"){
                    $('#restaurantUpdateForm').submit();
                }else{ // not match
                    alert("비밀번호가 일치하지 않습니다.");
                }
            },
            error: function(request, status){
                console.log("code : "+status+"\nmessage : "+request.responseText);
            }
        });
    });

});
