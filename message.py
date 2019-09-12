#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#IM920のデバッグ用プログラム
import IM920

#文字列受信
self.imbool = False

if IM920.Reception(19200):
    self.imbool = True
print(IM920.Reception(19200))


#文字列送信
IM920.Send(19200, "Hallo")



