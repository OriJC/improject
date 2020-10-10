# improject
以下大部分的過程都在window 10的環境中進行，其他os可能操作和code上會有點不一樣

Python 需要3.7以後的版本 (因為3.7 subprocess.run 有新增 capture_output)

## Submodules <owl-verbalizer>

This submodule is used for the recompilation of `owl_to_ace.exe` if it doesn't work. You could go into the directory and then use the makefile to compile it. Remember to get `SWI-Prolog` installed on your system before compiling. When **git cloning** this repository, you could use

```bash
git clone --recurse-submodule <url> # or the below
git clone --recursive <url>
```

to save the process of doing the process down the line

```bash
git submodule update --init
```

and to compile the `owl_to_ace.exe` file, just type

```bash
sh make_exe.sh
```

if you're in a Linux server environment using bash and move it to the outer file by

```bash
mv owl_to_ace.exe ..
```

## 安裝虛擬環境

```bash
pip install virtualenv #optional if you want to use virtualenv
```

`setup.sh` (Mac OS, Linux, BSD) and `setup.bat` (Windows) are both setup scripts and does create the virtual environment and also install the required pip files

## 架構虛擬環境

在cmd中進入目標資料夾

virtualenv 子資料夾 (這個子資料夾的名稱就自己去取，會作為你之後虛擬環境的名稱)

會生成一個子資料夾作為虛擬環境


## 使用虛擬環境

```bash
workon 子資料夾
```

if you're on the server, use

```bash
source bin/activate
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

### server用cmd

```bash
netstat -npl
nohup program --host=0.0.0.0 &
```
