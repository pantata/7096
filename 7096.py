#!/usr/bin/python3

import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSpinBox, QCheckBox, QComboBox, QPushButton


class Settings:
    def __init__(self, str):
        f = str.split(';')
        self.mode = int(f[0])
        self.p1pw1 = int(f[1])
        self.p2pw1 = int(f[2])
        self.p3pw1 = int(f[3])
        self.p4pw1 = int(f[4])
        self.p1pw2 = int(f[5])
        self.p2pw2 = int(f[6])
        self.p3pw2 = int(f[7])
        self.p4pw2 = int(f[8])
        self.pulsetime = int(f[9]) * 10
        self.foodtimer = int(f[10])
        self.moonlight = int(f[11])
        self.stormcycle = int(f[12])
        self.storminterval = int(f[13])
        self.nightmode = int(f[14])
        self.interval = int(f[15])
        self.seqtime = int(f[16])
        self.wavecontroller = int(f[17])
        self.waveperiod = int(f[18]) * 10
        self.waveinverse = int(f[19])
        self.ramptime = int(f[20]) * 100
        self.minflow = int(f[21])
        self.random = int(f[22])
        
    def __str__(self):
        return "%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i;%i" % (self.mode, self.p1pw1, self.p2pw1, self.p3pw1, self.p4pw1, self.p1pw2, self.p2pw2, self.p3pw2, self.p4pw2, int(self.pulsetime / 10), self.foodtimer, int(self.moonlight), int(self.stormcycle), self.storminterval, int(self.nightmode), self.interval, self.seqtime, int(self.wavecontroller), int(self.waveperiod / 10), int(self.waveinverse), int(self.ramptime / 100), int(self.minflow), int(self.random))

class MainWindow(QWidget):
    def get_responce(self):
        l = self.ser.read(256)
        if l[0] != 0x02:
            raise RuntimeError("Missing start of data!")
        elif l[-2] != 0x03:
            raise RuntimeError("Missing end of data!")
        return(l[1:-2])

    def changeMode(self, mode):
        if mode == 0:
            self.interval.setEnabled(False)
            self.seqtime.setEnabled(False)
            self.minflow.setEnabled(False)            
        if mode == 1:
            self.interval.setEnabled(True)
            self.seqtime.setEnabled(False)
            self.minflow.setEnabled(True)
        if mode == 2:
            self.interval.setEnabled(False)
            self.seqtime.setEnabled(True)
            self.minflow.setEnabled(True)
    
    def changeRandom(self, state):
        self.pulsetime.setEnabled(not state)

    def changeStormcycle(self, state):
        self.storminterval.setEnabled(state)

    def changeWaveinverse(self, state):
        self.p3pw1.setValue(0)
        self.p3pw2.setValue(100)
        if state:
            self.p4pw1.setValue(100)
            self.p4pw2.setValue(0)        
        else:
            self.p4pw1.setValue(0)
            self.p4pw2.setValue(100)

    def changeWavecontroller(self, state):
        self.p3pw1.setEnabled(not state)
        self.p3pw2.setEnabled(not state)
        self.p4pw1.setEnabled(not state)
        self.p4pw2.setEnabled(not state)
        self.waveperiod.setEnabled(state)
        self.waveinverse.setEnabled(state)
        if state:
            self.changeWaveinverse(self.waveinverse.isChecked())

    def save(self):
        self.settings.mode = self.mode.currentIndex()
        self.settings.p1pw1 = self.p1pw1.value()
        self.settings.p1pw2 = self.p1pw2.value()
        self.settings.p2pw1 = self.p2pw1.value()
        self.settings.p2pw2 = self.p2pw2.value()    
        self.settings.p3pw1 = self.p3pw1.value()
        self.settings.p3pw2 = self.p3pw2.value()
        self.settings.p4pw1 = self.p4pw1.value()
        self.settings.p4pw2 = self.p4pw2.value()
        self.settings.pulsetime = self.pulsetime.value()
        self.settings.foodtimer = self.foodtimer.value()
        self.settings.moonlight = self.moonlight.isChecked()
        self.settings.stormcycle = self.stormcycle.isChecked()
        self.settings.storminterval = self.storminterval.value()
        self.settings.nightmode = self.nightmode.isChecked()
        self.settings.interval = self.interval.value()
        self.settings.seqtime = self.seqtime.value()
        self.settings.wavecontroller = self.wavecontroller.isChecked()
        self.settings.waveperiod = self.waveperiod.value()
        self.settings.waveinverse = self.waveinverse.isChecked()
        self.settings.ramptime = self.ramptime.value()
        self.settings.minflow = self.minflow.isChecked()
        self.settings.random = self.random.isChecked()
        print("New settings:     %s" % self.settings)
        self.ser.write(b'\x02')
        self.ser.write(str(self.settings).encode('ascii'))
        self.ser.write(b'\x03\r')        

    def __init__(self):
        super(MainWindow, self).__init__()

        # Use serial port specified on command line, or /dev/ttyUSB0 if none specified
        if len(sys.argv) > 1:
            port = sys.argv[1]
        else:
            port = '/dev/ttyUSB0'

        # Open serial port and do initialization sequence needed to wake up 7096
        self.ser = serial.Serial(port=port, baudrate=19200, timeout=0.25, rtscts=False, dsrdtr=False)
        self.ser.setRTS(0)
        self.ser.setDTR(0)
        self.ser.setRTS(1)
        time.sleep(0.1)
        self.ser.setRTS(0)
        time.sleep(0.5)

        # Get model number and firmware version
        self.ser.write(b'\x02?\x03\r')
        r = self.get_responce()
        model = r.decode('UTF-8')
        print("Found %s" % model)

        # Get current settings
        self.ser.write(b'\x020data\x03\r')
        r = self.get_responce()
        # Convert responce to string and parse it to a settings object
        self.settings = Settings(r.decode('UTF-8'))

        print("Current settings: %s" % self.settings)

        # Initialize the main window
        self.resize(480, 570)
        self.setWindowTitle("7096 Tool - %s" % model)

        # Draw all the widgets
        # First some labels
        power1lbl = QLabel('Power 1:', self)
        power1lbl.move(10, 44)
        power2lbl = QLabel('Power 2:', self)
        power2lbl.move(10, 74)

        pump1lbl = QLabel('Pump 1', self)
        pump1lbl.move(100, 10)
        pump2lbl = QLabel('Pump 2', self)
        pump2lbl.move(200, 10)
        pump3lbl = QLabel('Pump 3', self)
        pump3lbl.move(300, 10)
        pump4lbl = QLabel('Pump 4', self)
        pump4lbl.move(400, 10)

        # Pump power levels
        self.p1pw1 = QSpinBox(self)
        self.p1pw1.setMinimum(0)
        self.p1pw1.setMaximum(100)
        self.p1pw1.setValue(self.settings.p1pw1)
        self.p1pw1.move(100, 40)
        
        self.p1pw2 = QSpinBox(self)
        self.p1pw2.setMinimum(0)
        self.p1pw2.setMaximum(100)
        self.p1pw2.setValue(self.settings.p1pw2)
        self.p1pw2.move(100, 70)
        
        self.p2pw1 = QSpinBox(self)
        self.p2pw1.setMinimum(0)
        self.p2pw1.setMaximum(100)
        self.p2pw1.setValue(self.settings.p2pw1)
        self.p2pw1.move(200, 40)
        
        self.p2pw2 = QSpinBox(self)
        self.p2pw2.setMinimum(0)
        self.p2pw2.setMaximum(100)
        self.p2pw2.setValue(self.settings.p2pw2)
        self.p2pw2.move(200, 70)
        
        self.p3pw1 = QSpinBox(self)
        self.p3pw1.setMinimum(0)
        self.p3pw1.setMaximum(100)
        self.p3pw1.setValue(self.settings.p3pw1)
        self.p3pw1.move(300, 40)
        
        self.p3pw2 = QSpinBox(self)
        self.p3pw2.setMinimum(0)
        self.p3pw2.setMaximum(100)
        self.p3pw2.setValue(self.settings.p3pw2)
        self.p3pw2.move(300, 70)
        
        self.p4pw1 = QSpinBox(self)
        self.p4pw1.setMinimum(0)
        self.p4pw1.setMaximum(100)
        self.p4pw1.setValue(self.settings.p4pw1)
        self.p4pw1.move(400, 40)
        
        self.p4pw2 = QSpinBox(self)
        self.p4pw2.setMinimum(0)
        self.p4pw2.setMaximum(100)
        self.p4pw2.setValue(self.settings.p4pw2)
        self.p4pw2.move(400, 70)

        # Mode of operation
        nightmodelbl = QLabel('Mode:', self)
        nightmodelbl.move(10, 124)
        self.mode = QComboBox(self)
        self.mode.addItem('Pulse')
        self.mode.addItem('Interval')
        self.mode.addItem('Sequence')
        self.mode.setCurrentIndex(self.settings.mode)
        self.mode.currentIndexChanged.connect(self.changeMode)
        self.mode.move(150, 122)

        # Time interval for Interval mode
        intervallbl = QLabel('Interval:', self)
        intervallbl.move(10, 154)
        self.interval = QSpinBox(self)
        self.interval.setMinimum(1)
        self.interval.setMaximum(779)
        self.interval.setValue(self.settings.interval)
        self.interval.move(150, 150)
        intervallbl2 = QLabel('minutes', self)
        intervallbl2.move(210, 154)

        # Time interval for Sequence mode
        seqtimelbl = QLabel('Sequence time:', self)
        seqtimelbl.move(10, 184)
        self.seqtime = QSpinBox(self)
        self.seqtime.setMinimum(1)
        self.seqtime.setMaximum(779)
        self.seqtime.setValue(self.settings.seqtime)
        self.seqtime.move(150, 180)
        seqtimelbl2 = QLabel('seconds', self)
        seqtimelbl2.move(210, 184)

        # Maintain minimum flow for powered of pumps (Interval and Sequence modes)
        minflowlbl = QLabel('Maintain min flow:', self)
        minflowlbl.move(10, 214)
        self.minflow = QCheckBox(self)
        self.minflow.setChecked(self.settings.minflow)
        self.minflow.move(150, 212)

        # Enable/disable all mode dependent controlls
        self.changeMode(self.settings.mode)

        # Pulse time
        pulsetimelbl = QLabel('Pulse time:', self)
        pulsetimelbl.move(10, 244)
        self.pulsetime = QSpinBox(self)
        self.pulsetime.setMinimum(0)
        self.pulsetime.setMaximum(8000)
        self.pulsetime.setSingleStep(10)
        self.pulsetime.setValue(self.settings.pulsetime)
        self.pulsetime.move(150, 240)
        pulsetimelbl2 = QLabel('ms', self)
        pulsetimelbl2.move(215, 244)

        self.random = QCheckBox('Randomize', self)
        self.random.setChecked(self.settings.random)
        self.random.stateChanged.connect(self.changeRandom)
        self.random.move(240, 242)
        if self.settings.random:
            self.pulsetime.setEnabled(False)

        # Ramp time (soft start)
        ramptimelbl = QLabel('Ramp time:', self)
        ramptimelbl.move(10, 274)
        self.ramptime = QSpinBox(self)
        self.ramptime.setMinimum(0)
        self.ramptime.setMaximum(200)
        self.ramptime.setSingleStep(100)
        self.ramptime.setValue(self.settings.ramptime)
        self.ramptime.move(150, 270)
        ramptimelbl2 = QLabel('ms', self)
        ramptimelbl2.move(215, 274)

        # Night mode
        nightmodelbl = QLabel('Night mode:', self)
        nightmodelbl.move(10, 304)
        self.nightmode = QCheckBox(self)
        self.nightmode.setChecked(self.settings.nightmode)
        self.nightmode.move(150, 302)

        # Moonlight
        moonlightlbl = QLabel('Moonlight:', self)
        moonlightlbl.move(10, 334)
        self.moonlight = QCheckBox(self)
        self.moonlight.setChecked(self.settings.moonlight)
        self.moonlight.move(150, 332)

        # Food timer
        foodtimerlbl = QLabel('Food timer:', self)
        foodtimerlbl.move(10, 364)
        self.foodtimer = QSpinBox(self)
        self.foodtimer.setMinimum(0)
        self.foodtimer.setMaximum(15)
        self.foodtimer.setValue(self.settings.foodtimer)
        self.foodtimer.move(150, 360)
        foodtimerlbl2 = QLabel('minutes', self)
        foodtimerlbl2.move(205, 364)

        # Storm cycle
        stormcyclelbl = QLabel('Storm cycle:', self)
        stormcyclelbl.move(10, 394)
        self.stormcycle = QCheckBox('Enable', self)
        self.stormcycle.setChecked(self.settings.stormcycle)
        self.stormcycle.move(150, 392)
        self.stormcycle.stateChanged.connect(self.changeStormcycle)
        self.storminterval = QSpinBox(self)
        self.storminterval.setMinimum(1)
        self.storminterval.setMaximum(191)
        self.storminterval.setValue(self.settings.storminterval)
        self.storminterval.move(230, 390)
        stormintervallbl = QLabel('hours', self)
        stormintervallbl.move(290, 394)

        # Enable/disable storm cycle dependent controlls
        self.changeStormcycle(self.settings.stormcycle)

        # Wave controller
        wavecontrollerlbl = QLabel('Use pump 3&4 as Wave controller:', self)
        wavecontrollerlbl.move(10, 444)
        self.wavecontroller = QCheckBox(self)
        self.wavecontroller.setChecked(self.settings.wavecontroller)
        self.wavecontroller.stateChanged.connect(self.changeWavecontroller)
        self.wavecontroller.move(250, 442)
        
        waveperiodlbl = QLabel('Period:', self)
        waveperiodlbl.move(30, 474)
        self.waveperiod = QSpinBox(self)
        self.waveperiod.setMinimum(300)
        self.waveperiod.setMaximum(2500)
        self.waveperiod.setSingleStep(10)
        self.waveperiod.setValue(self.settings.waveperiod)
        self.waveperiod.move(100, 470)
        waveperiodlbl2 = QLabel('ms', self)
        waveperiodlbl2.move(170, 474)
        
        waveinverselbl = QLabel('Inverse:', self)
        waveinverselbl.move(30, 504)
        self.waveinverse = QCheckBox(self)
        self.waveinverse.setChecked(self.settings.waveinverse)
        self.waveinverse.stateChanged.connect(self.changeWaveinverse)
        self.waveinverse.move(100, 502)
        # If wave controller is enabled, update pump power levels
        if self.settings.wavecontroller:
            self.changeWaveinverse(self.settings.waveinverse)

        # Enable/disable wave controller dependent controlls
        self.changeWavecontroller(self.settings.wavecontroller)

        # The Save button
        savebutton = QPushButton('Save', self)
        savebutton.move(380, 530)
        savebutton.clicked.connect(self.save)

        # Show the main window
        self.show()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    return(app.exec_())

if __name__ == '__main__':
    main()
