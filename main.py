from fcoin import Fcoin
from buy import Buy
import datetime
import schedule
import time

fcoin = Fcoin()
fcoin.auth('你的key', '你的秘钥')
coin_buy = Buy('ethusdt',fcoin=fcoin,type='limit')


def buyTask():
    print("I'm working for buy and sell")
    coin_buy.buy()      

def run():
    schedule.every(1).seconds.do(buyTask)

    while True:
        schedule.run_pending()
        
  
if __name__ == '__main__':
    run()