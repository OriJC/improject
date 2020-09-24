function uploadTextTTR(){
    var text = document.getElementById("output").value;
    var UseCase = document.getElementById("UseCase").value;
    var up = new FormData();
    up.append('text', text);
    up.append('UseCase', UseCase);
    console.log(text);
    $.ajax({
        type: 'POST',
        url: '/TTRA',
        data: up,
        processData: false,
        contentType: false	
    }).done(function(data){
    console.log("Text to Race upload successful!");
    if(data['result'] == true)
        console.log("Reload successfully!!!");
    else 
        console.log("TTR Failed");

    }).fail(function(jqXHR,textStatus,error){
        console.log("Upload text failed!");
    });

    }