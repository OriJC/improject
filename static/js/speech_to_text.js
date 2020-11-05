var audio_context;
var recorder;
var fnames = [];

function startUserMedia(stream) {
    /**
     * create media stream
     */
    var input = audio_context.createMediaStreamSource(stream);

    // Uncomment if you want the audio to feedback directly
    // Input connected to audio context destination
    // input.connect(audio_context.destination);

    // start a recorder instance (initialise recorder)
    recorder = new Recorder(input);
}

function startRecording(button) {
    /**
     * Start the recording
     */
    audio_context.resume();
    recorder && recorder.record();
    // change the state of the record button as disabled
    button.disabled = true;
    // make the stop button not disabled
    button.nextElementSibling.disabled = false;
}

function stopRecording(button) {
    /**
     * Stop the recording
     */
    recorder && recorder.stop();
    // make the stop button disabled
    button.disabled = true;
    // make the start button not disabled
    button.previousElementSibling.disabled = false;

    // upload to server
    uploadToServer();

    // clear the recorder
    recorder.clear();
}

function uploadToServer() {
    recorder && recorder.exportWAV(function(blob) {
        var last_fname = (new Date().toISOString() + '.wav').replace(/:/g, "_");
        fnames.push(last_fname);

        var reader = new FileReader();
        // this function is triggered once a call to readAsDataURL returns
        reader.onload = function(event){
            var fd = new FormData();
            fd.append('fname', last_fname);
            fd.append('data', event.target.result);
            $.ajax({
                type: 'POST',
                url: '/upload',
                data: fd,
                processData: false,
                contentType: false
            }).done(function(data) {
                // _log('Upload to server successfully.');
            }).fail(function(jqXHR, textStatus, error) {
                // _log('Upload to server failed')
            });

        };      
        // trigger the read from the reader...
        reader.readAsDataURL(blob);

        createAudioHTML(blob);
    });
}

  function createAudioHTML(blob) {
    // create audio and buttons
    var url = URL.createObjectURL(blob);
    var li = document.createElement('li');
    var au = document.createElement('audio');
    var hf = document.createElement('a');

    au.controls = true;
    au.src = url;
    hf.href = url;
    hf.download = fnames[fnames.length - 1];
    hf.innerHTML = hf.download;
    li.appendChild(au);
    li.appendChild(hf);
    
    var recBtn = document.createElement('button');
    var t = document.createTextNode('recognize');
    recBtn.appendChild(t);
    recBtn.onclick = function(){
      // _log("Recognizing...")
      document.getElementById("results").innerHTML = "Recognizing..."
      var fd = new FormData();
      fd.append('fname', hf.download);
      var weight = [];
      for(var i = 0;i < num_of_API;i++){
        weight.push(document.getElementById("weight" + i).value || 1);
      }
      fd.append('weight', weight);
      fd.append('threshold', document.getElementById("threshold").value || 1);
      fd.append('use_stem', document.getElementById("stem").checked ? "T" : "F");
      fd.append('lowercast', document.getElementById("lowercast").checked ? "T" : "F");
      fd.append('way', document.getElementById("ways").value);
      $.ajax({
          type: 'POST',
          url: '/recog',
          data: fd,
          processData: false,
          contentType: false
      }).done(function(data) {
          results_text = document.getElementById("results")
          recommendation_text = document.getElementById("recommendation")
          if (data["no_exception"]) {
            results_text.innerHTML = "google: " + data["results"][0] + '\n' + "ibm: " + data["results"][1] + '\n' + "wit: " + data["results"][2] + '\n' + "hundify: " + data["results"][3]
            results_text.innerHTML += '<hr>'
            results_text.innerHTML += '\n' + data["alignment"]
            recommendation_text.value = recommendation_text.value + data["recommendation"] + '\n'
          }
          else {
            if (data["exceed_quota"]) {
              results_text.innerHTML = "google: " + data["results"][0] + '\n' + "ibm: " + data["results"][1] + '\n' + "wit: " + data["results"][2] + '\n' + "houndify quota exceeded!"
              results_text.innerHTML += '<hr>'
              results_text.innerHTML += '\n' + data["alignment"]
              recommendation_text.value = recommendation_text.value + data["recommendation"] + '\n'
            }
            else {
            results_text.innerHTML = "Your voice is not clear enough, please try again!"
            }
          }
          
          // _log("Complete!")
      }).fail(function(jqXHR, textStatus, error) {
          // _log("Failed!")
      });
    }
    li.appendChild(recBtn);

    recordingslist.appendChild(li);
  }

  function downloadTextFile() {
    var text = document.getElementById("recommendation").value

    if (text != '') {
      var a = document.createElement('a');
      var blob = new Blob([text], {type: "text/plain"})
      var url = window.URL.createObjectURL(blob);
      var filename = (new Date().toISOString() + '.txt').replace(/:/g, "_");
      a.href = url;
      a.download = filename;
      a.click();
      window.URL.revokeObjectURL(url);
    }
  }

  window.onload = function init() {
    try{
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      //navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
      window.URL = window.URL || window.webkitURL;
      
      audio_context = new AudioContext;
      // _log('Audio context set up.');
      // _log('navigator.mediaDevices.getUserMedia ' + (navigator.mediaDevices.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }
    navigator.mediaDevices.getUserMedia({audio: true}).then(startUserMedia).catch(function(e) {
      // _log('No live audio input: ' + e);
    });
  };

  window.onbeforeunload = function() {
    var fd = new FormData();
    for (var i = fnames.length - 1; i >= 0; i--) {
      fd.append('fnames', fnames[i]);
    }
    
    $.ajax({
        type: 'POST',
        url: '/deleteAudios',
        data: fd,
        processData: false,
        contentType: false
    }).done(function(data) {
        
    }).fail(function(jqXHR, textStatus, error) {
        
    });
  }