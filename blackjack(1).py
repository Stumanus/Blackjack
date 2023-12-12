import random
import os

class Deck:
    def __init__(self):
        self.cards = []
    @property
    def shuffle(self):
        if len(self.cards) < 5:
            self.cards.clear()
            ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
            suits = ['C','S','H','D']
            for s in suits:
                for c in ranks:
                    self.cards.append(c + s)
            print('Shuffling cards...')
            random.shuffle(self.cards)
    def deal(self, num_cards: int):
        dealt_cards = []
        for x in range(num_cards):
            dealt_cards.append(self.cards.pop())
        return dealt_cards
    
class Player:
    def __init__(self):
        self.hand_list = []
        self.money = 100

class Hand:
    def __init__(self, cards, bet):
        self.cards = cards
        self.bet = bet
        self.state = ''
    @property
    def score(self):
        aces = 0
        score = 0
        card_values = {'2':2, '3':3, '4':4, '5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':0}
        for x in self.cards:
            if x[0] == 'A':
                aces +=1
                score +=11
            else:
                score += card_values[x[:-1]]
        while score > 21 and aces != 0:
            score -= 10
            aces -= 1
        return score
        
    def hit(self):
        card = deck.deal(1)
        self.cards.append(card[0])

def display():
    os.system('cls')
    print('Dealer:')
    if player_turn == True:
        print(str([dealer.hand_list[0].cards[0], 'X']) + str(dealer.hand_list[0].state))
    else:
        [print(str(hand.cards) + str(hand.state)) for hand in dealer.hand_list]
    print('Player:')
    for hand in player.hand_list:
        print(str(hand.cards) + str(hand.state))

def bet_input():
    bet_amount = None
    while bet_amount == None:
        try:
            input_amount = int(input('How much would you like to bet?\n'))
            bet_amount = input_amount
        except:
            print(f'Your bet needs to be an amount between 1 and {player.money}' )
    return bet_amount

def move_input():
    move = None
    while move == None:
        move_input = str(input('h = hit\ns = stand\na = split\nd = double down\n'))
        if move_input in 'hsad':
            move = move_input
        else:
            print('That\'s not a valid move.')
    return move

#Gameplay
if __name__ == '__main__':
    print('Welcome to Blackjack!\n')
    deck = Deck()
    dealer = Player()
    player = Player()
    playing = True
    while playing == True: 
        
        # Initial round setup: Create deck, take bet, deal hands
        player_turn = True
        dealer.hand_list.clear()
        player.hand_list.clear()
        deck.shuffle
        print(f'Cards in Deck: {len(deck.cards)}')
        print('You have ' + str(int(player.money)) + ' chips.')
        bet = bet_input()
        print('Dealing cards...')
        dealer.hand_list.append(Hand(deck.deal(2),0))
        player.hand_list.append(Hand(deck.deal(2),bet))
        hand_in_play = player.hand_list[0]
        
        # Check for blackjacks before gameplay starts
        if dealer.hand_list[0].score == 21 and player.hand_list[0].score == 21:
            display()
            print('Push')
            player.money -= bet
            continue
        elif dealer.hand_list[0].score == 21:
            display()
            print('Dealer Blackjack!')
            player.money -= bet
            continue
        elif player.hand_list[0].score == 21:
            display()
            print('Blackjack!')
            player.money += bet * 1.5
            continue
        
        # Gameplay logic:
        i = 0
        while i < len(player.hand_list): 
            deck.shuffle
            hand_in_play = player.hand_list[i]
            hand_in_play.state = '<--playing'
            display()
            if hand_in_play.state == 'stand': 
                i+=1
                continue
            if hand_in_play.score > 21:
                hand_in_play.state = 'bust'
                i+=1
                continue
            move = input('Type h to hit, s to stand, a to split, d to double down')
            if  move == 'h':
                hand_in_play.hit()
                continue
            elif move == 'a':
                if len(hand_in_play.cards) == 2:
                #  and hand_in_play.cards[0][:-1] == hand_in_play.cards[1][:-1]:
                    new_hand = Hand([hand_in_play.cards.pop()],hand_in_play.bet)
                    player.hand_list.append(new_hand)
                    continue
                else:
                    print('You can\'t split this hand!')
                    continue
            elif move == 'd':
                if hand_in_play.state != 'doubled_down':
                    hand_in_play.hit()
                    hand_in_play.bet * 2
                    hand_in_play.state = 'doubled_down'
                    i+=1
                else:
                    print('You can only double down once on a hand!')
            elif move == 's':
                i+=1
                hand_in_play.state = 'stand'
                continue
        player_turn = False
        while dealer.hand_list[0].score < 17:
                dealer.hand_list[0].hit()
        
        # Scoring logic:
        dealer_score = dealer.hand_list[0].score
        if dealer_score > 21:
            dealer.hand_list[0].state = 'bust'
            dealer_score = 0
        for plyr in [dealer,player]:   
            for hand in plyr.hand_list:
                if hand.score > 21:
                    hand.state = 'bust'
                    player.money -= hand.bet
                    continue
                elif hand.score > dealer_score:
                    hand.state = 'win'
                    player.money += hand.bet
                    continue
                elif hand.score < dealer_score:
                    hand.state = 'lose'
                    player.money -= hand.bet
                    continue
                elif hand.score == dealer_score:
                    hand.state = 'push'
                    player.money -= hand.bet
        display()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
