
import random
import os

class Deck:
    def __init__(self):
        self.cards = []
        ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        suits = ['C','S','H','D']
        for s in suits:
            for c in ranks:
                self.cards.append(c + s)
    def shuffle(self):
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
    def show1(self):
        print([self.hand_list[0].cards[0], 'X'])
    def show_all(self):
        [print(hand.cards) for hand in self.hand_list]

class Hand:
    def __init__(self, cards, bet):
        self.cards = cards
        self.doubled_down = False
        self.stand = False
        self.bet = bet
       
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

def print_dealers_turn():
    os.system('cls')
    print('Dealer:')
    dealer.show_all()
    print('Player:')
    player.show_all()

def print_players_turn():
    os.system('cls')
    print('Dealer')
    dealer.show1()
    print('Player')
    player.show_all()

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

# Start gameplay:
print('Welcome to Blackjack!\n')
deck = Deck()
deck.shuffle()
dealer = Player()
player = Player()
playing = True
while playing == True: 
    
    # Initial round setup: Create deck, take bet, deal hands
    dealer.hand_list.clear()
    player.hand_list.clear()
    if len(deck.cards) < 10:
        print('Shuffling deck...')
        deck.shuffe()
    print(f'Cards in Deck: {len(deck.cards)}')
    deck.shuffle()
    print('You have ' + str(player.money) + ' chips.')
    bet = bet_input()
    print('Dealing cards...')
    dealer.hand_list.append(Hand(deck.deal(2),0))
    player.hand_list.append(Hand(deck.deal(2),bet))
    print_players_turn()
    
    # Check for blackjacks before gameplay starts
    if dealer.hand_list[0].score == 21 and player.hand_list[0].score == 21:
        print_dealers_turn()
        print('Push')
        continue
    elif dealer.hand_list[0].score == 21:
        print_dealers_turn()
        print('Dealer Blackjack!')
        player.money -= bet
        continue
    elif player.hand_list[0].score == 21:
        print_dealers_turn()
        print('Blackjack!')
        player.money += bet * 1.5
        continue
    
    # Gameplay logic:
    i = 0
    while i < len(player.hand_list): 
        hand_in_play = player.hand_list[i]
        if hand_in_play.score >= 21 or hand_in_play.stand == True:
            i+=1
            continue
        move = input('Type h to hit, s to stand, a to split, d to double down')
        if  move == 'h':
            hand_in_play.hit()
            print_players_turn()
            continue
        elif move == 'a':
            if len(hand_in_play.cards) == 2 :
                # and hand_in_play.cards[0][:-1] == hand_in_play.cards[1][:-1]: '''other half of split logic check'''
                new_hand = Hand([hand_in_play.cards.pop()],hand_in_play.bet)
                player.hand_list.append(new_hand)
                print_players_turn()
                continue
            else:
                print('You can\'t split this hand!')
                continue
        elif move == 'd':
            if hand_in_play.doubled_down == False:
                hand_in_play.hit()
                hand_in_play.bet * 2
                hand_in_play.doubled_down == True
                print_players_turn()
                i+=1
            else:
                print('You can only double down once on a hand!')
        elif move == 's':
            i+=1
            hand_in_play.stand = True
            print_players_turn()
            continue
    
    # Scoring logic:
    if hand_in_play.score > 21:
        print_dealers_turn()
        print('Player bust')
        player.money -= bet
        continue
    while dealer.hand_list[0].score < 17:
        dealer.hand_list[0].hit()
    if dealer.hand_list[0].score > 21:
        print_dealers_turn()
        print('Dealer bust!')
        player.money += bet
        continue
    elif dealer.hand_list[0].score > hand_in_play.score:
        print_dealers_turn()
        print('Dealer wins!')
        player.money -= bet
    elif dealer.hand_list[0].score < hand_in_play.score:
        print_dealers_turn()
        print('Player wins!')
        player.money += bet
    else:
        print_dealers_turn()
        print('Push')