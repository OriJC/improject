# improject
以下大部分的過程都在window 10的環境中進行，其他os可能操作和code上會有點不一樣

Python 需要3.7以後的版本 (因為3.7 subprocess.run 有新增 capture_output)
## 安裝虛擬環境

```bash
pip install virtualenv # optional if you want to use virtualenv
```

`setup.sh` (Mac OS, Linux, BSD) and `setup.bat` (Windows) are both setup scripts. They create the virtual environment and also install the required pip files

## 架構虛擬環境

1. 在cmd中進入目標資料夾
2. virtualenv 子資料夾 (這個子資料夾的名稱就自己去取，會作為你之後虛擬環境的名稱)
3. 會生成一個子資料夾作為虛擬環境
4. workon 子資料夾

```bash
cd <dir>

# Creating a virtual environment
virtualenv . # You could either do it the virtualenv way
python -m venv . # Or use python's own venv environment

# Activating the virtual environment
Scripts\activate.bat # Windows
source bin/activate # POSIX

# Deactivating the virtual environment
deactivate
```

## 安裝套件

```bash
pip install --upgrade google-cloud-texttospeech flask requests
```

- Flask: To run the web server
- google-cloud-texttospeech: To provide text to speech capabilities 
- requests: to post SOAP messages to the RACE server

## Run

```bash
# Windows --optional
set FLASK_ENV=development
set FLASK_APP=app.py

# POSIX --optional
export FLASK_APP=app.py
export FLASK_ENV=development

# Run Flask
flask run
```