'''
Created on Apr 15, 2014

@author: leen
'''
from helper.utils import get_card_value

class PokerCard():
    def __init__(self, value):
        """value should be from 0 to 51"""
        if value < 0 or value > 51:
            raise Exception("Invalid Poker Value")
        self.value = value        
        self.kind, self.suit = get_card_value(value)
        self.compare_value = value
        if self.is_ace():
            self.compare_value += 52        
    
    def is_ace(self):
        return (self.value < 4)
    
    def __cmp__(self, other):
        return self.compare_value - other.compare_value
    