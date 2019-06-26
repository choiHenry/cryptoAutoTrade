# ABOUT THIS REPO

This repo contains project files for automated crypto-currency trading program. It is only a prototype and needs to be improved.

# HOW TO USE
It is recoomended not to use this program right now. If you want to test the program, open a bithumb account and get bithumb aip key pair of (connect key, secret key). Once ready, open index.py and insert the connect key to var 'con_key' and the secret key to 'sec_key'.

# ABOUT PROGRAM

1. Shows the current price(Price), moving average for 5 days(MA5), whether the channel for crpyto-currency is ascending or descending(A/D), and the balance of your account, for each cryptos. 
2. Renews every data for every second.
3. Buy automatically according to the overly simplified VRB(volatility range breakout) strategy.

        Target price for VRB strategy is renewed every midnight(GMT +9).
        
4. Sell all the cryptos at midnight.
