from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from threading import Timer
import time

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):  # Store initial next order ID sent back on connection
        self.nextValidOrderId = orderId
        self.start()

    def nextOrderId(self):  # There must be a larger ID for each new order
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print("OrderStatus. Id: ", orderId, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining,
              ", LastFillPrice: ", lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrder. ID:", orderId, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action,
              order.orderType, order.totalQuantity, orderState.status)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails. ", reqId, contract.symbol, contract.secType, contract.currency, execution.execId,
              execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        lambdaStock = USStock("GOOGL")
        lambdaOrder = RelativePeggedToPrimary("BUY", 2000, 0, 0.01)
        lambdaOrder.transmit = False
        lambdaOrderId = self.nextOrderId()
        self.placeOrder(lambdaOrderId, lambdaStock, lambdaOrder)
        time.sleep(0.2) #planned to be no longer necessary in future

        # Pair trading documentation: http://interactivebrokers.github.io/tws-api/hedging.html
        sStock = USStock("GOOG")
        # Size is 0 for hedge orders because it is calculated using the ratio
        sOrder = RelativePeggedToPrimary("SELL", 0, 0, 0)
        sOrder.parentId = lambdaOrderId  # parent ID links child to parent order
        sOrder.hedgeType = "P"  # "P" stands for Pair Trade
        sOrder.hedgeParam = "1"  # the hedging ratio

        self.placeOrder(self.nextOrderId(), sStock, sOrder)

    def stop(self):
        self.done = True
        self.disconnect()

# The REL order type is adjusted by the system automatically with the bid (for Buy) or ask (for Sell ) orders
def RelativePeggedToPrimary(action: str, quantity: float, priceCap: float, offsetAmount: float):
    order = Order()
    order.action = action
    order.orderType = "REL"
    order.totalQuantity = quantity
    order.lmtPrice = priceCap
    order.auxPrice = offsetAmount
    return order

# API contract definition documentation: http://interactivebrokers.github.io/tws-api/basic_contracts.html#stk
def USStock(ticker: str):
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NYSE"  # Should be native exchange of stock
    return contract

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, 1)

    Timer(5, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()
