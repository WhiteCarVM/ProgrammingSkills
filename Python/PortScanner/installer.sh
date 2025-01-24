python3 -m venv .env
source .env/bin/activate
pip3 install pyqt5
sudo apt install python3-pyinstaller
pyinstaller --onefile -w 'main.py'
cp dist/main ./portscanner
rm -rf build dist env main.spec
clear
./portscanner &
