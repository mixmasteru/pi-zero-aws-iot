# pi-zero-aws-iot
## AWS IoT on raspberry pi zero

### install dependencies:
```bash
sudo apt-get update
apt-get install -y build-essential python-pip python-dev python-smbus git
pip install AWSIoTPythonSDK
pip install pyserial
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT/
sudo python setup.py install
cd
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
cd
git clone https://github.com/adafruit/Adafruit_Python_BME280.git
cd Adafruit_Python_BME280
sudo python setup.py install
```

for BME280 enable i2c with raspi-config tool
check i2c address with command
```bash
sudo i2cdetect -y 1
```
change i2c address in config