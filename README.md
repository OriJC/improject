# improject
以下大部分的過程都在window 10的環境中進行，其他os可能操作和code上會有點不一樣

Python 需要3.7以後的版本 (因為3.7 subprocess.run 有新增 capture_output)
## 安裝虛擬環境

```bash
pip install virtualenv #optional if you want to use virtualenv
pip install --upgrade google-cloud-texttospeech flask
```

`setup.sh` (Mac OS, Linux, BSD) and `setup.bat` (Windows) are both setup scripts and does create the virtual environment and also install the required pip files

## 架構虛擬環境

在cmd中進入目標資料夾

virtualenv 子資料夾 (這個子資料夾的名稱就自己去取，會作為你之後虛擬環境的名稱)

會生成一個子資料夾作為虛擬環境

workon 子資料夾

## 安裝套件

