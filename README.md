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


## 使用虛擬環境

```bash
workon 子資料夾

# Deactivating the virtual environment
deactivate
```

## 安裝套件

大部分的套件直接用 pip 就可以安裝好

### Flask 

```bash

pip install Flask 

```
### Bootstrap-Flask

前端用，不安裝也可以(要把code中bootstrap的部分刪除掉)

Flask另外有一個叫Flask-Bootstrap的套件，不過很久沒有更新，安裝時不要安裝錯

### GCP Text-to-Speech

```bash

pip install --upgrade google-cloud-texttospeech

```
 
Google的 Text to Speech API，其他可以用的有Microsoft Azure等等

### Requests

```bash

pip install --upgrade requests

```

To POST the requests in SOAP format for RACE server. 

