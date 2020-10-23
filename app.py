from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, send_file
from flask_bootstrap import Bootstrap
import os
import subprocess
import platform
import json
from werkzeug.utils import secure_filename
from google.cloud import texttospeech
import requests
import xml.etree.ElementTree as ET
import PostSoap as ps

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'example key'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'asd.json'
exec_head = "./" if platform.system() != "Windows" else ""


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/TTS')
def TTS():
    return render_template('TextToSpeech.html')


@app.route('/OTA')
def OTA():
    return render_template('OWLToACE.html')


@app.route('/OTS')
def OTS():
    return render_template('OWLToSpeech.html')


@app.route('/TTR')
def TTR():
    return render_template('TextToRace.html')


@app.route('/TTR', methods=['POST'])
def PostToRace():
    if request.method == 'POST':
        axioms = request.values['axioms']
        query = request.values['query']
        UseCase = request.values['UseCase']

        url = "http://attempto.ifi.uzh.ch/ws/race/racews.perl"
        headers = {'content-type': 'application/soap+xml'}
        # headers = {'content-type': 'text/xml'}
        # !Use the above if somehow the above^2 doesn't work

        body = ps.MessageForPost(UseCase, axioms, query)
        response = requests.post(url, data=body, headers=headers)
        print(response.text)
        runtime, message, reason, conclusion = ps.DecypherResponse(
            response.text, UseCase, query)
    return jsonify(
        runtime=runtime,
        message=message,
        reason=reason,
        conclusion=conclusion
    )


@app.route('/savetxt', methods=['POST'])
def savetxt():
    if request.method == 'POST':
        file = []
        file = request.files.get('story')
        filename = secure_filename(file.filename)
        file.save('upload/'+filename)
        result = owlverb(filename)
        return jsonify({'result': result})
    return jsonify({'result': "Failed!"})


@app.route('/TTSapi', methods=['POST'])
def TTSapi():
    if request.method == 'POST':
        text = request.values['text']
        filename = request.values['filename']
        pitch = 0
        speed = 1
        lang = 'en-US'
        if(request.values['voice']) == 'male1':
            name = "en-US-Wavenet-D"
            gender = texttospeech.SsmlVoiceGender.MALE
        elif(request.values['voice'] == 'female1'):
            name = "en-US-Wavenet-F"
            gender = texttospeech.SsmlVoiceGender.FEMALE
        elif(request.values['voice'] == 'male2'):
            name = "en-US-Wavenet-A"
            gender = texttospeech.SsmlVoiceGender.MALE
        elif(request.values['voice'] == 'female2'):
            name = "en-US-Wavenet-E"
            gender = texttospeech.SsmlVoiceGender.FEMALE
        elif(request.values['voice'] == 'robot'):
            name = "en-GB-standard-A"
            gender = texttospeech.SsmlVoiceGender.MALE
            speed = 0.66
            pitch = -10.40
            lang = 'en-GB'
        message = json.dumps({
            'lang': lang,
            'inputtext': text,
            'name': name,
            'gender': gender,
            'speed': speed,
            'pitch': pitch
        })
        applic(message, filename)
        return jsonify({'result': True, 'filename': filename})
    return jsonify({'result': False})


def owlverb(storypath):
    result = subprocess.run([f'{exec_head}owl_to_ace.exe', '-xml',
                             f'upload/{storypath}'], capture_output=True, shell=True)
    return result.stdout.decode()


def applic(message, filename):
    client = texttospeech.TextToSpeechClient()
    message = json.loads(message)
    synthesis_input = texttospeech.SynthesisInput(text=message['inputtext'])
    voice = texttospeech.VoiceSelectionParams(
        language_code=message['lang'],
        ssml_gender=message['gender'],
        name=message['name'])
    audio_config = texttospeech.AudioConfig(
        speaking_rate=message['speed'],
        pitch=message['pitch'],
        audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(f'./static/{filename}.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    return send_file(f'./static/{filename}.mp3', attachment_filename=f'{filename}.mp3')


@app.route('/deleteText', methods=['POST'])
def deleteText():
    os.remove('./static/output.mp3')
    return jsonify({'text': "File removed!"})


if __name__ == '__main__':
    app.run(debug=True)
