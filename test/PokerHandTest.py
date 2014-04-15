'''
Created on Apr 16, 2014

@author: leen
'''
import unittest
import random
from PokerCard import PokerCard
import PokerHand as Hand
from PokerHand import PokerHand

class PokerHandTest(unittest.TestCase):
            
    def testPokerHand5CardsGeneric(self):
        for _count in xrange(1000):
            cards1 = [PokerCard(random.randint(0,51)) for _ in range(5)]
            cards2 = [PokerCard(random.randint(0,51)) for _ in range(5)]
            hand1 = PokerHand(cards1)
            hand2 = PokerHand(cards2)
            if hand1 < hand2:
                self.assertLessEqual(hand1.hand, hand2.hand)
            elif hand1 > hand2:
                self.assertGreaterEqual(hand1.hand, hand2.hand)
            elif hand1 == hand2:
                self.assertEqual(hand1.hand, hand2.hand)
    
    def testPokerHand7CardsGeneric(self):
        for _count in xrange(1000):
            cards1 = [PokerCard(random.randint(0,51)) for _ in range(7)]
            cards2 = [PokerCard(random.randint(0,51)) for _ in range(7)]
            hand1 = PokerHand(cards1)
            hand2 = PokerHand(cards2)
            if hand1 < hand2:
                self.assertLessEqual(hand1.hand, hand2.hand)
            elif hand1 > hand2:
                self.assertGreaterEqual(hand1.hand, hand2.hand)
            elif hand1 == hand2:
                self.assertEqual(hand1.hand, hand2.hand)    
                
    def testPokerHandHighCard(self):
        cards1 = [PokerCard(c) for c in [1, 9, 18, 25, 35]]
        cards2 = [PokerCard(c) for c in [2, 10, 19, 26, 34]]
        hand1 = PokerHand(cards1)
        hand2 = PokerHand(cards2)
        self.assertEqual(hand1.hand, Hand.HIGH_CARD)
        self.assertEqual(hand2.hand, Hand.HIGH_CARD)        
        self.assertEqual(hand1, hand2)
        
        cards1 = [PokerCard(c) for c in [1, 9, 18, 25, 35]]
        cards2 = [PokerCard(c) for c in [10, 19, 26, 34, 50]]
        hand1 = PokerHand(cards1)
        hand2 = PokerHand(cards2)        
        self.assertEqual(hand1.hand, Hand.HIGH_CARD)
        self.assertEqual(hand2.hand, Hand.HIGH_CARD)
        self.assertGreater(hand1, hand2)
        
    def testPokerHandOnePair(self):
        pass
    
    def testPokerHandTwoPair(self):
        pass
    
    def testPokerHandStraight(self):
        pass
    
    def testPokerHandFlush(self):
        pass
    
    def testPokerHandFullHouse(self):
        pass

    def testPokerHandFourOfAKind(self):
        pass

    def testPokerHandRoyalFlush(self):
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()