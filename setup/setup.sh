git submodule update --init --recursive

cd APE/
make install
mv ape.exe ..

cd ../owl-verbalizer
sh make_exe.sh
mv owl_to_ace.exe ..

cd ..
python3 -m venv env
source env/bin/activate
pip3 install --upgrade -r requirements.txt
