# PairsStatArb
Using the IBKR Python API, a pairs trade is opened when the log difference between two correlated stocks (pairs) is sufficiently large and closed once this difference is sufficiently small. The thresholds for entering and closing the trade may be determined by long run statistical analysis and these values are hardcoded. As a simple example, GOOGL and GOOG were chosen in the code (GOOGL are Class A shares which have voting rights and GOOG are Class C but the log difference between them fluctuates tightly around 0). The opportunity for statistical arbitrage often exists with more illiquid stocks (however finding pairs that are liquid enough to trade in these cases is difficult and should be automated). 

Lambda denotes the stock which is bought and S denotes the stock which is sold. This may be easily generalised. The socket port for paper trading is 7497 and the port for live trading is 7496.

You may not use the material for commercial purposes.
