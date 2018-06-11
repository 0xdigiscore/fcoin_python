from fcoin import Fcoin
from buy import Buy
import datetime
import schedule
import time

fcoin = Fcoin()
fcoin.auth('', '')
coin_buy = Buy('ftusdt',fcoin=fcoin,type='limit')

def buyTask():
    print("I'm working for buy and sell")
    coin_buy.buy()      

def run():
    schedule.every(1).seconds.do(buyTask)
    while True:
        schedule.run_pending()
        
  
if __name__ == '__main__':
    run()