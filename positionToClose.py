import ibapi

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time
import math

import os

# Class to establish IB Connection
class IBApi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)
    # Listen for live data
    def realtimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)
        
class Bot:
    ib = None
    def __init__(self):
        # IB conncetion on init
        self.ib = IBApi()
        self.ib.connect("127.0.0.1",7497,1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        
        time.sleep(1)
        contract0 = Contract() 
        contract0.symbol = "GOOGL"
        contract0.secType = "STK"
        contract0.exchange = "SMART"
        contract0.currency = "USD"

        contract1 = Contract()
        contract1.symbol = "GOOG"
        contract1.secType = "STK"
        contract1.exchange = "SMART"
        contract1.currency = "USD"
        
        # Request live data
        self.ib.reqRealTimeBars(0, contract0, 5, "BID", True, [])
        self.ib.reqRealTimeBars(1, contract1, 5, "ASK", True, [])
        #self.ib.cancelRealTimeBars(0)

    #Listen to socket in distinct thread
    def run_loop(self):
        self.ib.run()

    #Pass live data back to bot object
    def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
        global STime, LTime, S, Lambda
        if reqId == 1:
            S = close
            STime = time
        else:
            Lambda = close
            LTime = time
        if STime == LTime:
            ratio = math.log(S)-math.log(Lambda)
            if ratio <= 0.003:
                self.ib.cancelRealTimeBars(0)
                self.ib.cancelRealTimeBars(1)

                self.ib.done = True
                self.ib.disconnect()
                    
                # Execuate order
                os.system('sellLambdaBuyS.py & positionToOpen.py')
                #& positionToOpen.py in system command

            # Print ratio
            print("At", time, "the ratio is", ratio)

STime = 0
LTime = 0
S = 0
Lambda = 0

#position = False

bot = Bot()

#Execute Buy 1 Lambda_t and Sell 1500 S_t
#os.system('buyLambdaSellS.py')
#time.sleep(60)

#Execute Sell 1 Lambda_t and Buy 1500 S_t
#os.system('sellLambdaBuyS.py')

