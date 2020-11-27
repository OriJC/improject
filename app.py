from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, send_file
from flask_bootstrap import Bootstrap
import os
import subprocess
import platform
import json
import wave
import ssl
from werkzeug.utils import secure_filename
from google.cloud import texttospeech
import requests
import PostSoap as ps
import web_recognize
import final_result
import globalvar as gl
import weight #deprecated
import use_reasoner
from decimal import Decimal

os.chdir(os.path.dirname(os.path.realpath(__file__)))
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'example key'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'asd.json'
exec_head = "./" if platform.system() != "Windows" else ""

def safe_base64_decode(base64str):
	import base64
	if len(base64str) % 4 == 0:
		decode_base64str = base64.urlsafe_b64decode(base64str)
		return decode_base64str
	else:
		decode_base64str = base64.urlsafe_b64decode(base64str + '=' * (4-len(base64str) % 4))
		return decode_base64str

def make_wav_file(fname, decode_base64str):
	dirName = 'audios'
	if not os.path.exists(dirName):
		os.mkdir(dirName)

	channels = 2
	sampwidth = 2
	rate = 44100   
	
	with wave.open(f'./{dirName}/{fname}', 'wb') as wavefile:
		wavefile.setnchannels(channels)
		wavefile.setsampwidth(sampwidth)
		wavefile.setframerate(rate)
		wavefile.writeframes(decode_base64str)


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
    # render the template texttorace.html
    return render_template('TextToRace.html')


@app.route('/TTR', methods=['POST'])
def PostToRace():
    if request.method == 'POST':
        # get the values that are being posted
        axioms = request.values['axioms']
        query = request.values['query']
        UseCase = request.values['UseCase']

        url = "http://attempto.ifi.uzh.ch/ws/race/racews.perl"
        headers = {'content-type': 'application/soap+xml'}
        # headers = {'content-type': 'text/xml'}
        # !Use the above if somehow the above^2 doesn't work

        # prepare the message to be posted to RACE server
        body = ps.MessageForPost(UseCase, axioms, query)
        # posting the data and accepting the response with variable 'response'
        response = requests.post(url, data=body, headers=headers)
        print(response.text)
        # get the runtime, message etc. from xml response
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


@app.route('/speech-to-text', methods=['GET', 'POST'])
def speech_to_text():
    '''
    get the speech file, send to various speech servers and return text
    '''
    if request.method == 'GET':
        return render_template("speech_to_text.html")
    if request.method == 'POST':
        pass

@app.route('/upload', methods=['POST'])
def upload():
	fname = request.form.get('fname')
	blob = request.form.get('data')[22:]

	decode_blob = safe_base64_decode(blob)
	make_wav_file(fname, decode_blob)

	return ""

@app.route('/recog', methods=['POST'])
def recog():
	fname = request.form.get('fname')
	weight = [Decimal(i) for i in request.form.get('weight').split(',')]
	threshold = Decimal(request.form.get('threshold'))
	use_stem = (request.form.get('use_stem') == 'T')
	lowercast = (request.form.get('lowercast') == 'T')
	way = request.form.get('way')
	results, no_exception, exceed_quota = web_recognize.recognize('./audios/' + fname)
	if no_exception == True:
		alignment, recommendation = results[0], results[0]
        # final_result.to_final_result(results, weight, threshold, way = way, use_stem = use_stem, lowercast = lowercast)
		dic = {"results":results, "no_exception":no_exception, "exceed_quota":exceed_quota, "alignment":alignment, "recommendation":recommendation}
	else:
		if exceed_quota == True:
			results = results[:-1]
			alignment, recommendation = results[0], results[0]
            # final_result.to_final_result(results, weight, threshold, way = way, use_stem = use_stem, lowercast = lowercast)
			dic = {"results":results, "no_exception":no_exception, "exceed_quota":exceed_quota, "alignment":alignment, "recommendation":recommendation}
		else:
			dic = {"no_exception":no_exception}
	return jsonify(dic)

@app.route('/deleteAudios', methods=['POST'])
def deleteAudios():
	fnames = request.form.getlist('fnames')
	for fname in fnames:
		os.remove('./audios/' + fname)
	return ""



if __name__ == '__main__':
    app.run(debug=True)
