from fcoin import Fcoin
import datetime
import schedule
import threading
import time

'''
多线程定时器买和卖

'''

class Buy():
    def __init__(self,trade_pair = 'ftusdt',fcoin = None,type = 'market'):
        self._trade_pair = trade_pair
        self._fcoin = fcoin
        self._type = type
    
    '''
      不敢操作ft，波动太大，以后研究，只买卖eth_usdt对
    '''
    def trunc(self,f, n):
        
        if not str(f):
           return '0'   
        sarr = str(f).split('.')    
        if len(sarr) == 2:
            s1, s2 = str(f).split('.')
        else:
            s1 = str(f)
            s2 = '0'    
        if n == 0:
            return s1
        if n <= len(s2):
            return s1 + '.' + s2[:n]
        return s1 + '.' + s2 + '0' * (n - len(s2))

    def buy(self):
        if not self._fcoin:
            return
        '''
        账户中的钱
        '''    
        eth_num  = float(self._fcoin.get_coin_balance('ft')) * 0.5
        usdt_num  = float(self._fcoin.get_coin_balance('usdt')) * 0.8

        '''
         一个eth能买多少个usdt
        '''

        max_price = float(self._fcoin.get_coin_price_max(self._trade_pair))
        min_price = float(self._fcoin.get_coin_price_min(self._trade_pair))

        print('usdt num:')
        print(usdt_num)
        print('eth num:')
        print(eth_num)

        print('usdt price:')
        print(max_price)
      
        print('eth price')
        print(min_price)

        self._fcoin.sell(self._trade_pair,price = self.trunc(max_price,2),amount = self.trunc(eth_num,1) , type = self._type) 

        if min_price == 0 :
            buy_amount = 0
        else:
            buy_amount = eth_num / min_price

        self._fcoin.buy(self._trade_pair,price = self.trunc(min_price,2),amount = self.trunc(buy_amount,2) , type = self._type) 
       
        '''
        if  float(usdt_num) > 1:
            self._fcoin.buy(self._trade_pair,price = usdt_price,amount = usdt_num, type = self._type) 
        else:
            self._fcoin.sell(self._trade_pair,price = usdt_price,amount = eth_num, type = self._type)     
             
        '''    
 
        
            
           
                     


