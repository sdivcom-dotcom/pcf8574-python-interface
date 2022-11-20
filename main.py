import os
import subprocess
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

command_lsusb = "lsusb | grep 'Silicon Labs CP2112 HID I2C Bridge'"
command_find_i2c_line  = "i2cdetect -l | grep 'CP2112 SMBus Bridge'"
command_find_addr = "i2cdetect -r -y "
command_set = "i2cset -y "
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        ch0 = QPushButton('CH0', self)
        ch1 = QPushButton('CH1', self)
        ch2 = QPushButton('CH2', self)
        ch3 = QPushButton('CH3', self)
        ch4 = QPushButton('CH4', self)
        ch5 = QPushButton('CH5', self)
        ch6 = QPushButton('CH6', self)
        ch7 = QPushButton('CH7', self)
        flush_button = QPushButton('Flush chip', self)

        ch0.move(20, 20)
        ch1.move(20, 40)
        ch2.move(20, 60)
        ch3.move(20, 80)
        ch4.move(20, 100)
        ch5.move(20, 120)
        ch6.move(20, 140)
        ch7.move(20, 160)
        flush_button.move(20, 180)

        ch0.clicked.connect(self.ch0_action)
        ch1.clicked.connect(self.ch1_action)
        ch2.clicked.connect(self.ch2_action)
        ch3.clicked.connect(self.ch3_action)
        ch4.clicked.connect(self.ch4_action)
        ch5.clicked.connect(self.ch5_action)
        ch6.clicked.connect(self.ch6_action)
        ch7.clicked.connect(self.ch7_action)
        flush_button.clicked.connect(self.flush_action)



        self.setGeometry(100, 100, 160, 220)
        self.setWindowTitle('PCF8574-OUTPUT-Interface 0.1')
        self.show()

    def lsusb_find(self):
        val = os.system(command_lsusb)
        if val == 0:
            value = 1
        else:
            value = 0
        return value

    # Find i2c line cp2112
    def find_i2c_line(self):
        val = os.system(command_find_i2c_line)
        if val == 0:
            value = subprocess.check_output(command_find_i2c_line, shell=True)
            value = (value[4:6])
        else:
            value = 0
        return value

# Find address chip
    def find_address(self):
        bus_find = self.find_i2c_line()
        bus_find = str(bus_find, encoding="utf-8")
        command_find_address = command_find_addr + bus_find
        val = subprocess.check_output(command_find_address, shell=True)
        value = str(val, encoding="utf-8")

        index1 = value.find("21")
        index2 = value.find("22")
        index3 = value.find("23")
        index4 = value.find("24")
        index5 = value.find("25")
        index6 = value.find("26")
        index7 = value.find("27")

        if index1 >= 10:
            address = 21

        elif index2 >= 10:
            address = 22

        elif index3 >= 10:
            address = 23

        elif index4 >= 10:
            address = 24

        elif index5 >= 10:
            address = 25

        elif index6 >= 10:
            address = 26

        elif index7 >= 10:
            address = 27

        else:
            address = 00
        return address
    def send_i2c(self, message):
        addr = self.find_address()
        bus_a = self.find_i2c_line()
        addr = str(addr)
        bus = int(bus_a)
        bus = str(bus)
        message = str(message)
        command_set_i2c = command_set + bus + " 0x" + addr + " 0x" + message
        os.system(command_set_i2c)

    def ch0_action(self):
        message = '01'
        self.send_i2c(message)
    def ch1_action(self):
        message = '03'
        self.send_i2c(message)
    def ch2_action(self):
        message = '07'
        self.send_i2c(message)
    def ch3_action(self):
        message = '0f'
        self.send_i2c(message)
    def ch4_action(self):
        message = '1f'
        self.send_i2c(message)
    def ch5_action(self):
        message = '3f'
        self.send_i2c(message)
    def ch6_action(self):
        message = '7f'
        self.send_i2c(message)
    def ch7_action(self):
        message = 'ff'
        self.send_i2c(message)
    def flush_action(self):
        message = '00'
        self.send_i2c(message)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()