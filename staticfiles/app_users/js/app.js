$(document).ready(function(){

    //function to load user photo on the fly
    $(document).on('change','#id_photo',null,function(){
            
        if (this.files && this.files[0])
        {
            console.log("there is files");
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#userPhoto, #userPhoto2')
                    .attr('src', e.target.result)
                    .width(200)
                    .height(200);
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
    
    
    //code to clear user photo
    $(".clrPhoto").click(function(){

        document.getElementById("id_photo").value = "";

        var photoiconURL = base_url + "static/app_users/img/usericon.svg?timestamp=" + new Date().getTime();
        $("#userPhoto,#userPhoto2").attr('src',photoiconURL)
                        .width(50)
                        .height(50);

       
    
    });
    
    
    
    });