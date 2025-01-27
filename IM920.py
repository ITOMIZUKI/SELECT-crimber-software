#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
パッケージpyserialをインストールすること
pytho2.x系で動作(python3.*系も動作検証済み)
Creater：Kaname Takano
'''
import serial
import binascii
import signal
import sys
import platform
from serial.tools import list_ports

#platformの切り替え
if platform.system() == 'Windows':  #windows用
    ports = list_ports.comports()
    portnumber = None
    for port in ports:
        if (port.vid == 1027) and (port.pid == 24597): #プロダクトIDとベンダーIDが一致したら接続
            portnumber = port.device
            print("connect to " + portnumber)
            break

    if portnumber == None:
        print("not connetc to im920!")
        sys.exit(1)

elif platform.system() == 'Linux': #Linux用
    portnumber = '/dev/ttyAMA0'

'''
ctrl+cの命令
'''
def signal_handler(signal, frame):
    print('exit')
    sys.exit()

'''
serial.Serialの設定
mybaudrate:ボーレート
'''
def setSerial(mybaudrate):
    com = serial.Serial(
        port     = portnumber,
        baudrate = mybaudrate,
        bytesize = serial.EIGHTBITS,
        parity   = serial.PARITY_NONE,
        timeout  = None,
        xonxoff  = False,
        rtscts   = False,
        writeTimeout = None,
        dsrdtr       = False,
        interCharTimeout = None)

    #bufferクリア
    com.flushInput()
    com.flushOutput()
    return com

'''
固有IDの読み出し
mybaudrate:ボーレート
'''
def Rdid(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'RDID' + b'\r\n')
    com.flushOutput()
    print(com.readline().strip())
    com.close()


'''
ボーレートの設定
mybaudrate:現在のボーレート
setbaudrate:セットするボーレート(文字列でもってくること)
    0 1200bps
    1 2400bps
    2 4800bps
    3 9600bps
    4 19200bps
    5 38400bps
'''
def Sbrt(mybaudrate, setbaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'ENWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'SBRT ' + setbaudrate.encode('utf-8') + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'DSWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.close()

'''
ペアリング
mybaudrate:ボーレート
args:ペアリングしたいID(文字列にすること)
'''
def Srid(mybaudrate, args):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'ENWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'SRID ' + args.encode('utf-8') + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'DSWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.close()

'''
ペアリングの削除
全て削除されるため注意!
mybaudrate:ボーレート
'''
def Erid(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'ENWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'ERID' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.write(b'DSWR' + b'\r\n')
    com.flushOutput()
    com.readline()
    com.close()

'''
送信
mybaudrate:ボーレート
args:送信したい文字列 (数字の場合も文字列型にすること)
'''
def Send(mybaudrate, args):
    com = setSerial(mybaudrate)
    com.flushInput()
    com.write(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n')
    com.flushOutput()
    com.readline()
    com.close()

'''
受信
アスキーコードから文字列に変換したものを返す
mybaudrate:ボーレート
'''
def Reception(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()

    text = ""
    cngtext = ""
    try:
        text = com.readline().decode('utf-8').strip() #受信と空白の削除
        com.close()
        text = text.replace("\r\n","")
        text = text.split(":")[1]
        text = text.split(",")

        for x in text:
            cngtext += chr(int(x,16))

    except Exception:
        print("not input data")

    return cngtext

'''
中継機化
mybaudrate:ボーレート
'''
def Repeater(mybaudrate):
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        data = Reception(mybaudrate)
        if len(data) != 0:
            print("input data:", data)
            Send(19200, data)
