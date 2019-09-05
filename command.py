# -*- Coding: utf-8 -*-

import time
import serial
import binascii
import signal
import sys

def signal_handler(signal, frame):
    sys.exit()

def setSerial(mybaudrate):
    com = serial.Serial(
        port     = '/dev/ttyAMA0',
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
    com.write(b'SBRT ' + setbaudrate + b'\r\n')
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
    com.write(b'SRID ' + args + b'\r\n')
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
    com.write(str.encode(b'TXDA' + binascii.b2a_hex(args.encode('utf-8')) + b'\r\n'))
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
    text = com.readline().decode('utf-8').strip() #受信と空白の削除
    text = text.replace("\r\n","")
    text = text.split(":")[1]
    text = text.split(",")
 
    cngtext = ""
    for x in text:
        cngtext += chr(int(x,16))
 
    com.close()
    return cngtext
 
'''
中継機化
mybaudrate:ボーレート
'''
def Repeater(mybaudrate):
    com = setSerial(mybaudrate)
    com.flushInput()
 
    signal.signal(signal.SIGINT, signal_handler)
 
    while True:
        text = ''
        com.flushInput()
        text = com.readline().strip()
        if text == '': continue
        texts = text.split(':')
        if len(texts) > 1:
            text = text.split(":")[1]
 
        com.write(b'TXDA ' + text + b'\r\n')
        com.flushOutput()
        com.readline()
 
if __name__ == '__main__':
    #ペアリング
    #Srid(19200,'5187')
 
    #削除
    #Erid(19200)
 
    #文字列送信
    Send(19200, 'Hello')
 
    #文字列受信
    #print Reception(19200)
 
    #中継機化
    #Repeater(19200)
 
    #固有ID
    Rdid(19200)
 
    #ボーレート設定
    #Sbrt(19200, '4')

