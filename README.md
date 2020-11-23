# 福爾摩斯-推論機器人

我們是一群資管大四的專題學生，以下是我們的Code

> 以下大部分的過程都在window 10的環境中進行，其他os可能操作和code上會有點不一樣。Python 需要3.7以後的版本 (因為3.7 subprocess.run 有新增 capture_output)

## 虛擬環境

```bash
# Creating a virtual environment
python -m venv env

# Activating the virtual environment
Scripts\env\activate.bat # Windows
source env/bin/activate # POSIX

# Deactivating the virtual environment
deactivate
```

`setup.sh` (Mac OS, Linux, BSD) and `setup.bat` (Windows) are both setup scripts. They create the virtual environment and also install the required pip files

## 安裝套件

在使用之前需要安裝一些套間

### Python 套件

- Flask
- Bootstrap-Flask: Flask另外有一個叫Flask-Bootstrap的套件，不過很久沒有更新，安裝時不要安裝錯
- google-cloud-texttospeech: Google的 Text to Speech API，其他可以用的有Microsoft Azure等等
- requests: To POST the requests in SOAP format for RACE server

```bash
pip install -r .\requirements.txt # Windows
pip install -r requirements.txt   # Linux
```

### 其他軟體

- swi-prolog: 這個是拿來compile `owl_to_ace.exe` 用的，Windows可以通過[這個鏈接](https://www.swi-prolog.org/) 來安裝，Linux則可以到repositopry裡面找 (Ubuntu的話是 `swi-prolog`)
- owl_to_ace.exe 和 ape.exe： 自己需要去compile，可以通過 `APE/` 和 `owl-verbalizer/` 編譯獲得, 這個會在 `use_reasoner.py` 用到

```bash
# changing directory
cd .\APE\ # windows
cd APE/   # linux

# compile ape.exe
make_exe.bat # windows
make install # linux

# compile owl-verbalizer
make_exe.bat    # windows
sh make_exe.sh  # linux
```

## 啟動

這個程式在啟動的時候，請進入虛擬環境，在Command Line輸入 

```bash
flask run
```

就可以啟動Flask後端，在瀏覽器打 `127.0.0.1：5000` 即可使用。如若是要進行開發，建議使用Development Mode並且瀏覽器設定不存取Cache。

## server用cmd

```bash
netstat -npl
nohup <program> --host=0.0.0.0 &
```

- 在app.py中的asd.json是Google api的連結金鑰，因為有資安的問題所以沒有放到github這邊來，因此可能需要去GCP申請一個帳戶和key，才可以使用到
- replace `<program>` with the application of desire, in our case, `python3 app.py`
