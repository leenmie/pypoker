'''
Created on Apr 15, 2014

@author: leen
'''
import copy
#from helper.utils import get_card_value

HIGH_CARD = 0x01
ONE_PAIR = 0x02
TWO_PAIR = 0x03
THREE_OF_A_KIND = 0x04
STRAIGHT = 0x05
FLUSH = 0x06
FULL_HOUSE = 0x07
FOUR_OF_A_KIND = 0x08
STRAIGHT_FLUSH = 0x09

def count_key(my_dict, key):
    if key in my_dict:
        my_dict[key] += 1
    else:
        my_dict[key] = 1

class PokerHand():
    """get a list of cards, return some values in poker
        number of cards should be <=7"""
    def __init__(self, cards):
        if not cards:
            raise Exception("Null poker hand")
        if len(cards) > 7:
            raise Exception("This implementation is not support a have have more than 7 cards")        
        self._cards = sorted(cards)
        self.hand = HIGH_CARD
        self.mean_cards = []
        """process cards"""
        self._process()
    
    def _process(self):
        self._calculate_hand_and_count_suit_kind()
        self._get_mean_cards_and_correct_hand_type()
        
    def _calculate_hand_and_count_suit_kind(self):
        kind_list = {}
        suit_list = {}
        cards = self._cards
        hand = self.hand
        seq = 1
        has_pair = False
        has_3ofakind = False
        #has_low_straight = False
        last_kind = cards[0].kind        
        _index = 0
        length = len(cards)
        while _index < length:
            _card = cards[_index]
            kind, suit = _card.kind, _card.suit
            count_key(kind_list, kind)
            count_key(suit_list, suit)            
            #print last_kind, kind_list[last_kind], hand
            if (last_kind != kind) or (_index == length-1):                
                if (kind_list[last_kind] == 2):
                    """
                    if we have a pair, we may have ONE PAIR
                    or TWO PAIR or FULL HOUSE
                    """
                    hand = ONE_PAIR
                    if has_3ofakind:
                        hand = max(hand, FULL_HOUSE)
                    else:
                        if has_pair:
                            hand = max(hand, TWO_PAIR)
                    has_pair = True                
                if (kind_list[last_kind] == 3):
                    """
                    if we have a 3 of a kind, we may have THREE of A KIND
                    or FULL HOUSE
                    """
                    if not has_pair:
                        hand = max(hand, THREE_OF_A_KIND)
                    else:
                        hand = max(hand, FULL_HOUSE)
                    has_pair = True
                    has_3ofakind = True
                if (kind_list[last_kind] >= 4):
                    hand = max(hand, FOUR_OF_A_KIND)                
                if (kind - last_kind == 1):
                    """if we have a sequence"""
                    seq+=1
                    if seq >= 5:
                        hand = max(hand, STRAIGHT)                        
                else:
                    seq = 1
                last_kind = kind
            _index+=1        
        self._kind_list = kind_list
        self._suit_list = suit_list
        self.hand = hand
        
    def _get_mean_cards_and_correct_hand_type(self):
        cards = self._cards
        hand = self.hand
        mean_cards = []
        kind_list = self._kind_list
        suit_list = self._suit_list
        """mean cards number are <= 5"""        
        remaining_cards = min(5, len(cards))
        
        if hand == HIGH_CARD:
            """get highest cards in value"""
            for _index in range(len(cards)-1, -1, -1):
                mean_cards.append(cards[_index])
                remaining_cards-=1
                if remaining_cards == 0:
                    break
        elif hand == ONE_PAIR:
            """get highest pair, then highest cards"""
            remaining_pairs = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_pairs:
                    if remaining_cards > 2:
                        """we have to leave available slots for a pair"""
                        if kind_list[kind] == 1:
                            mean_cards.append(cards[_index])
                            remaining_cards -= 1
                    if kind_list[kind] == 2:
                        """we found highest pair, add them to our mean cards"""
                        mean_cards.append(cards[_index])
                        mean_cards.append(cards[_index-1])
                        _index -= 2
                        remaining_cards-=2
                        remaining_pairs-=1
                        continue
                else:
                    """add remaining cards from high to low"""
                    mean_cards.append(cards[_index])
                    remaining_cards -= 1
                _index -= 1
        elif hand == TWO_PAIR:
            remaining_pairs = 2
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_pairs:
                    if remaining_cards > remaining_pairs*2:
                        if kind_list[kind] == 1:
                            mean_cards.append(cards[_index])
                            remaining_cards -= 1
                    if kind_list[kind] == 2:
                        mean_cards.append(cards[_index])
                        mean_cards.append(cards[_index-1])
                        _index -= 2
                        remaining_cards-=2
                        remaining_pairs-=1
                        continue
                else:
                    mean_cards.append(cards[_index])
                    remaining_cards -= 1
                _index -= 1
        elif hand == THREE_OF_A_KIND:
            remaining_three = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                kind = cards[_index].kind
                if remaining_three:
                    if remaining_cards > 3:
                        if kind_list[kind] == 1:
                            mean_cards.append(cards[_index])
                            remaining_cards -= 1
                    if kind_list[kind] == 3:
                        mean_cards.append(cards[_index])
                        mean_cards.append(cards[_index-1])
                        mean_cards.append(cards[_index-2])
                        _index -= 3
                        remaining_cards-=3
                        remaining_three-=1
                        continue
                else:
                    mean_cards.append(cards[_index])
                    remaining_cards -= 1
                _index -= 1
        elif hand == FOUR_OF_A_KIND:
            remaining_four = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                #print cards[_index]
                kind = cards[_index].kind
                if remaining_four:
                    if remaining_cards > 4:
                        if kind_list[kind] < 4:
                            mean_cards.append(cards[_index])
                            remaining_cards -= 1
                    if kind_list[kind] >= 4:
                        mean_cards.append(cards[_index])
                        mean_cards.append(cards[_index-1])
                        mean_cards.append(cards[_index-2])
                        mean_cards.append(cards[_index-3])
                        _index -= 4
                        remaining_cards-=4
                        remaining_four-=1
                        continue
                else:
                    mean_cards.append(cards[_index])
                    remaining_cards -= 1
                _index -= 1
        elif hand == FULL_HOUSE:
            remaining_three = 1
            remaining_pair = 1
            _index = len(cards) - 1
            while remaining_cards > 0 and _index>=0:
                #print cards[_index]
                kind = cards[_index].kind
                if remaining_three:
                    if kind_list[kind] == 3:
                        mean_cards.append(cards[_index])
                        mean_cards.append(cards[_index-1])
                        mean_cards.append(cards[_index-2])
                        _index-=3
                        remaining_cards-=3
                        remaining_three-=1
                        continue
                    elif kind_list[kind] == 2:
                        if remaining_pair:
                            mean_cards.append(cards[_index])
                            mean_cards.append(cards[_index-1])
                            _index-=2
                            remaining_cards-=2
                            remaining_pair-=1
                            continue
                else:
                    if remaining_pair:
                        if kind_list[kind] >=2:
                            mean_cards.append(cards[_index])
                            mean_cards.append(cards[_index-1])
                            _index-=2
                            remaining_cards-=2
                            remaining_pair-=1
                            continue
                _index -= 1
        #was_straight = (hand == STRAIGHT)
        #flush_suit = None
        may_flush = False                        
        for suit in suit_list.keys():
            if suit_list[suit] >= 5:
                may_flush = True
                if hand < FLUSH:
                    hand = FLUSH
                    #mean_cards = []
                #flush_suit = suit
        if may_flush:
            """high chance of straight flush here"""
            flush_cards = []
            for _index in range(len(cards)):
                suit = cards[_index].suit
                if suit_list[suit] >= 5:
                    flush_cards.append(cards[_index])
            last_kind = flush_cards[-1].kind
            has_ace_in_flush = (last_kind == 14)
            seq = 1
            for _index in range(len(flush_cards)-2,-1,-1):
                kind = flush_cards[_index].kind
                if last_kind - kind == 1:
                    seq +=1
                else:
                    seq = 1
                if seq == 5:
                    hand = STRAIGHT_FLUSH
                    mean_cards =[]
                    for k in range(_index, _index+5):
                        mean_cards.insert(0,flush_cards[k])
                    break
                if seq == 4:
                    if kind == 2 and has_ace_in_flush:
                        hand = STRAIGHT_FLUSH
                        mean_cards = []
                        mean_cards.append(flush_cards[-1])
                        for k in range(_index, _index+4):
                            mean_cards.insert(0,flush_cards[k])
                        break
                last_kind = kind
        if hand == STRAIGHT:
            mean_cards = []
            seq = 1
            last_kind = cards[-1].kind
            for _index in range(len(cards)-2,-1,-1):                
                kind = cards[_index].kind
                if last_kind - kind == 1:
                    seq +=1
                elif last_kind - kind >1:
                    seq = 1
                if seq == 5:
                    mean_cards.insert(0,cards[_index])
                    k = _index+1
                    count_forward = 4
                    prev_kind = kind
                    while count_forward >0:
                        kind2 = cards[k].kind
                        if kind2 - prev_kind == 1:                            
                            mean_cards.insert(0,cards[k])
                            count_forward -=1
                        k+=1
                        prev_kind = kind2
                    break
                last_kind = kind                
        elif hand == FLUSH:
            mean_cards = []
            remaining_cards = 5
            for _index in range(len(cards)-1,-1,-1):
                suit = cards[_index].suit
                if suit_list[suit] >= 5:
                    mean_cards.append(cards[_index])
                    remaining_cards-=1
                if remaining_cards == 0:
                    break

        self.hand = hand
        mean_cards.sort()
        self.mean_cards = mean_cards
        
    
    def __cmp__(self, other):
        """compare other hand"""
        if self.hand != other.hand:
            return self.hand - other.hand
        else:
            """
            same hand, so sort first, then compare from highest to lowest
            sorting priority: number of a kind, then value
            """                                
            def get_this_cmp_value(card):
                kind = card.kind
                return card.compare_value + (self._kind_list[kind] - 1) * 100

            def get_other_cmp_value(card):
                kind = card.kind
                return card.compare_value + (other._kind_list[kind] - 1) * 100                
            
            this_mean_cards = copy.copy(self.mean_cards)
            other_mean_cards = copy.copy(other.mean_cards)
            this_mean_cards.sort(key=get_this_cmp_value)
            other_mean_cards.sort(key=get_other_cmp_value)
            
            result = 0
            for j in range(len(this_mean_cards)-1,-1,-1):
                thiskind = this_mean_cards[j].kind
                otherkind = other_mean_cards[j].kind
                result = thiskind - otherkind
                if result != 0:
                    break
            return result
