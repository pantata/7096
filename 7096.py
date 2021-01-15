from PyQt5 import QtWidgets, QtSerialPort, QtCore, uic
import t7096ui
import sys
import time
import serial

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

class SerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SerDialog, self).__init__(parent)
        self.portname_comboBox = QtWidgets.QComboBox()

        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            self.portname_comboBox.addItem(info.portName())

        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.setOrientation(QtCore.Qt.Horizontal)
        buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        lay = QtWidgets.QFormLayout(self)
        lay.addRow("Port Name:", self.portname_comboBox)
        lay.addRow(buttonBox)
        self.setFixedSize(self.sizeHint())

    def get_results(self):
        return self.portname_comboBox.currentText()

class t7096App(QtWidgets.QMainWindow, t7096ui.Ui_MainWindow):
    def setWidgetValfromSettings(self):

        if self.settings.mode == 0:
            self.radioPulse.toggle()
        elif self.settings.mode == 1:
            self.radioInterval.toggle()
        else:
            self.radioSeq.toggle()

        self.intervalMinutes.setValue(self.settings.interval%60)
        self.intervalHour.setValue(int(self.settings.interval/60))

        self.seqSec.setValue(self.settings.seqtime)
        self.minFlowOff.setChecked(self.settings.minflow)

        self.pwr1_1.setValue(self.settings.p1pw1)
        self.pwr1_2.setValue(self.settings.p2pw1)
        self.pwr1_3.setValue(self.settings.p3pw1)
        self.pwr1_4.setValue(self.settings.p4pw1)
        self.pwr2_1.setValue(self.settings.p1pw2)
        self.pwr2_2.setValue(self.settings.p2pw2)
        self.pwr2_3.setValue(self.settings.p3pw2)
        self.pwr2_4.setValue(self.settings.p4pw2)        

        self.pls_flow.setValue(self.settings.pulsetime/1000)
        self.ramp.setValue(self.settings.ramptime/1000)
        self.random_flow.setChecked(self.settings.random)

        self.foodtimer.setValue(self.settings.foodtimer)
        self.moonlight.setChecked(self.settings.moonlight)
        self.nightmode.setChecked(self.settings.nightmode)
        self.stormcycle.setChecked(self.settings.stormcycle)
        self.stormCycleTimeHour.setValue(self.settings.storminterval%24)
        self.stormCycleTimeDays.setValue(int(self.settings.storminterval/24))

        self.wavecontroller.setChecked(self.settings.wavecontroller)
        self.wave34.setValue(self.settings.waveperiod/1000)
        self.inverse.setChecked(self.settings.waveinverse)

    def setSettingsfromWidget(self):

        if self.radioPulse.isChecked():
            self.settings.mode = 0
        elif self.radioInterval.isChecked():
            self.settings.mode = 1
        else:
            self.settings.mode = 2
        
        self.settings.interval = self.intervalHour.value()*60 + self.intervalMinutes.value()
        self.settings.seqtime = self.seqSec.value()
        self.settings.minflow = self.minFlowOff.isChecked()
                
        self.settings.p1pw1 = self.pwr1_1.value()
        self.settings.p2pw1 = self.pwr1_2.value()
        self.settings.p3pw1 = self.pwr1_3.value()
        self.settings.p4pw1 = self.pwr1_4.value()

        self.settings.p1pw2 = self.pwr2_1.value()
        self.settings.p2pw2 = self.pwr2_2.value()    
        self.settings.p3pw2 = self.pwr2_3.value()
        self.settings.p4pw2 = self.pwr2_4.value()

        self.settings.pulsetime = self.pls_flow.value()*1000
        self.settings.ramptime = self.ramp.value()*1000
        self.settings.random = self.random_flow.isChecked()

        self.settings.foodtimer = self.foodtimer.value()
        self.settings.moonlight = self.moonlight.isChecked()
        self.settings.nightmode = self.nightmode.isChecked()

        self.settings.stormcycle = self.stormcycle.isChecked()
        self.settings.storminterval = self.stormCycleTimeDays.value()*24 + self.stormCycleTimeHour.value()
        
        self.settings.wavecontroller = self.wavecontroller.isChecked()
        self.settings.waveperiod = self.wave34.value()*1000
        self.settings.waveinverse = self.inverse.isChecked()
        
        print("New settings:     %s" % self.settings)

    #save settings to file
    def on_savefile(self):
        self.setSettingsfromWidget()
        name,filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File','', "(*.txt)")
        if name:
            try:
                file = open(name,'w')
                try:
                    file.write("%s" % self.settings)
                except:
                    pass
                finally:
                    file.close()
            except Exception as e:
                print(e)

    #read settings from file
    def on_readfile(self):
        name,filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', "(*.txt)")
        if name:
            try:
                file = open(name,'r')
                try:
                    with file:
                        text = file.read()
                        self.settings = Settings(text)
                        print("Current settings: %s" % self.settings)
                        self.setWidgetValfromSettings()
                except Exception as e:
                    print(e)
                finally:
                    file.close()
            except Exception as e:
                print(e)

    #read  response from unit
    def get_response(self):
        l = self.ser.read(256)
        if l[0] != 0x02:
            raise RuntimeError("Missing start of data!")
        elif l[-2] != 0x03:
            raise RuntimeError("Missing end of data!")
        return(l[1:-2])

    #receive data from unit
    def on_receive(self):
        # Get model number and firmware version
        self.ser.write(b'\x02?\x03\r')
        r = self.get_response()
        model = r.decode('UTF-8')
        print("Found %s" % model)
        self.statusbar.showMessage("Port: "+ self.portname + " - " + model)
        # Get current settings
        self.ser.write(b'\x020data\x03\r')
        r = self.get_response()
        # Convert responce to string and parse it to a settings object
        self.settings = Settings(r.decode('UTF-8'))
        print("Current settings: %s" % self.settings)
        self.setWidgetValfromSettings()

    #connect to unit
    def on_connect(self):
        if self.connected == False:
            dialog = SerDialog()
            if dialog.exec_():
                self.portname = dialog.get_results()
                self.statusbar.clearMessage()
                try:
                    # Open serial port and do initialization sequence needed to wake up 7096
                    self.ser = serial.Serial(port="/dev/"+self.portname, baudrate=self.baudrate, timeout=self.timeout, rtscts=False, dsrdtr=False)
                    self.ser.setRTS(0)
                    self.ser.setDTR(0)
                    self.ser.setRTS(1)
                    time.sleep(0.1)
                    self.ser.setRTS(0)
                    time.sleep(0.5)
                    self.sendToUnit.setEnabled(True)
                    self.receiveFromUnit.setEnabled(True)
                    self.on_receive()
                    self.connected = True
                    self.connect.setText("Connect")                    
                    self.autoStart.setEnabled(True)
                except Exception as e:
                    print(e)
        else:
            self.ser.close()
            self.connect.setText("Connect")
            self.connected = False

    #send values to unit
    def on_send(self):
        self.setSettingsfromWidget()
        try:
            self.ser.write(b'\x02')
            self.ser.write(str(self.settings).encode('ascii'))
            self.ser.write(b'\x03\r')
            self.statusbar.showMessage("Data send to unit ...",2000) 
        except Exception as e:
            print(e)


    #widget enable/disable
    def on_randomflow(self, ch):
        if ch.isChecked():
            self.pls_flow.setEnabled(False)
        else:
            self.pls_flow.setEnabled(True)

    #widget enable/disable
    def on_wavecontroller(self,ch):
        if ch.isChecked():
            self.socket34.setEnabled(True)
            self.pwr2_3.setEnabled(False)
            self.pwr2_4.setEnabled(False)
            self.pwr1_3.setEnabled(False)
            self.pwr1_4.setEnabled(False)
            self.pwr2_3.setValue(100)
            self.pwr2_4.setValue(100)
            self.pwr1_3.setValue(0)
            self.pwr1_4.setValue(0)
            self.rampValidator(self.ramp)
        else:
            self.socket34.setEnabled(False)
            self.pwr2_3.setEnabled(True)
            self.pwr2_4.setEnabled(True)
            self.pwr1_3.setEnabled(True)
            self.pwr1_4.setEnabled(True)
        if self.connected == False:
            self.autoStart.setEnabled(False)    
        self.autoStop.setEnabled(False)
    
    #set pwr for inverse wave
    def on_inverse(self,ch):
        if ch.isChecked():
            self.pwr2_4.setValue(0)
            self.pwr1_4.setValue(100)
        else:
            self.pwr2_4.setValue(100)
            self.pwr1_4.setValue(0)

    #widget enable/disable
    def on_stormcycle(self,ch):
        if ch.isChecked():
            self.stormCycleTimeHour.setEnabled(True)
            self.stormCycleTimeDays.setEnabled(True)
        else:
            self.stormCycleTimeHour.setEnabled(False)
            self.stormCycleTimeDays.setEnabled(False)            

    #TODO button to autoadjust wave
    def on_autoStart(self):
        self.autoStart.setEnabled(False)
        self.autoStop.setEnabled(True)
        self.wave34.setEnabled(False)
         # Initialize timer
        self.timer = QtCore.QTimer()
        self.now = 0
        self.timer.timeout.connect(self.tick_timer)
        # Start timer and update display
        self.timer.start(3000)
        self.update_timer()

    def on_autoStop(self):
        self.autoStart.setEnabled(True)
        self.autoStop.setEnabled(False)
        self.wave34.setEnabled(True)
        # send 0x04
        self.timer.stop()
        self.ser.write(b'\x04')
        self.statusbar.showMessage("Stop autoadjust",2000)

    def tick_timer(self):
        self.now += 1
        self.update_timer()

    def update_timer(self):
        #send 0x02 0x02 2 5 0 ; 1 0x03 /r            
        self.ser.write(b'\x02\x02%d;%d\x03\r' % (self.wave34.value()*100,1 if self.inverse.isChecked() else 0 ))
        self.statusbar.showMessage("Set pulse %.2f sec" % self.wave34.value())
        if (self.wave34.value() * 100) < 250:
            self.wave34.setValue(self.wave34.value() + 0.01)
        else:
            self.wave34.setValue(0.30)

    #switch wave mode
    def on_modeSwitch(self, r):
        if r.isChecked() and r.objectName() == "radioPulse":
            self.minFlowOff.setDisabled(True)
            self.intervalMinutes.setDisabled(True)
            self.intervalHour.setDisabled(True)
            self.seqSec.setDisabled(True)
            self.label_interval_1.setDisabled(True)
            self.label_interval_2.setDisabled(True)
            self.label_interval_3.setDisabled(True)
            self.label_seq.setDisabled(True)

        elif r.isChecked() and r.objectName() == "radioInterval":
            self.minFlowOff.setDisabled(False)
            self.intervalMinutes.setDisabled(False)
            self.intervalHour.setDisabled(False)
            self.seqSec.setDisabled(True)
            self.label_interval_1.setDisabled(False)
            self.label_interval_2.setDisabled(False)
            self.label_interval_3.setDisabled(False)
            self.label_seq.setDisabled(True)
        else:
            self.minFlowOff.setDisabled(False)
            self.intervalMinutes.setDisabled(True)
            self.intervalHour.setDisabled(True)
            self.seqSec.setDisabled(False)
            self.label_interval_1.setDisabled(True)
            self.label_interval_2.setDisabled(True)
            self.label_interval_3.setDisabled(True)            
            self.label_seq.setDisabled(False)

    #ramp max 80% of pulse time
    def rampValidator(self,input):
        if self.wavecontroller.isChecked():
            pulsetime = self.wave34.value() if self.wave34.value() <  self.pls_flow.value() else self.pls_flow.value()
        else:
            pulsetime  = self.pls_flow.value()
        maxramptime  = int(((pulsetime * 1000) * 0.8) / 100) / 10
        if self.ramp.value() >= maxramptime: 
            self.ramp.setValue(maxramptime)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connected = False
        self.settings = Settings("0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;")

        #button state
        self.saveToFile.clicked.connect(self.on_savefile)
        self.restoreFromFile.clicked.connect(self.on_readfile)
        self.connect.clicked.connect(self.on_connect)
        self.sendToUnit.clicked.connect(self.on_send)
        self.receiveFromUnit.clicked.connect(self.on_receive)
        self.sendToUnit.setEnabled(False)
        self.receiveFromUnit.setEnabled(False)

        #mode state
        self.radioPulse.toggled.connect(lambda:self.on_modeSwitch(self.radioPulse))
        self.radioInterval.toggled.connect(lambda:self.on_modeSwitch(self.radioInterval))
        self.radioSeq.toggled.connect(lambda:self.on_modeSwitch(self.radioSeq))

        self.radioPulse.toggle()

        #other stuff
        self.ramp.valueChanged.connect(lambda:self.rampValidator(self.ramp))
        self.random_flow.stateChanged.connect(lambda:self.on_randomflow(self.random_flow))        

        self.stormcycle.stateChanged.connect(lambda:self.on_stormcycle(self.stormcycle))
        self.stormCycleTimeHour.setEnabled(False)
        self.stormCycleTimeDays.setEnabled(False)

        self.socket34.setEnabled(False)
        self.wavecontroller.stateChanged.connect(lambda:self.on_wavecontroller(self.wavecontroller))
        self.inverse.stateChanged.connect(lambda:self.on_inverse(self.inverse))
        self.autoStart.clicked.connect(self.on_autoStart)
        self.autoStop.clicked.connect(self.on_autoStop)

        #serial params
        self.portname = ""
        self.baudrate = 19200
        self.timeout = 0.25

        self.connect.setFocus()
        self.statusbar.showMessage("Started ...",2000)

def main():
    sys.stdout = sys.stdout
    app = QtWidgets.QApplication(sys.argv)
    window = t7096App()
    window.setWindowTitle("Tunze 7096 tool")
    window.show()
    try:
        app.exec_()
    except:
        pass
    finally:
        if window.connected:
            window.ser.close()

if __name__ == '__main__':
    main()