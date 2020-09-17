function uploadText(){
	var text = document.getElementById("output").value;
	var voice = document.getElementById("voicegender").value;
	var up = new FormData();
	up.append('voice',voice);
	up.append('text',text);	
	console.log(text);	
	$.ajax({
		type: 'POST',
		url: '/TTSapi',
		data: up,
		processData: false,
		contentType: false	
	}).done(function(data){
		console.log("Text to Speech upload successful!");
		document.getElementById("audio_source").src="";
		document.getElementById("audio_source").src="{{ url_for('static',filename='output.mp3')}}";
		var aud = document.getElementById("audio");
		aud.load();
		aud.play();
		if(data['result'] == true)
			console.log("Reload successfully!!!");
		else 
			console.log("TTS Failed");
	}).fail(function(jqXHR,textStatus,error){
		console.log("Upload text failed!");
	});
}