python3 -m venv env
source env/bin/activate
pip3 install pyqt5
pyinstaller --onefile -w 'main.py'
cp dist/main ./portscanner
rm -rf build dist env main.spec
clear
