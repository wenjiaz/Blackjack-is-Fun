# By Wenjia Zhao
#===========================================================#
# BLACKJACK
#-----------------------------------------------------------#
# You are playing as the Player.
#
# Instructions:
# 1. Game begins with a shuffled shoe (ie playing deck of cards).
# 2. Player puts down his bet (at least 1 chip).
# 3. Player and Dealer each receive 2 cards. Dealer shows 1 card and hides the other (hole card).
# 4. Aces can be interpreted two ways: Soft (11 pts) or Hard (1 pt)
# 5. If Player or Dealer gets a Blackjack (Ace & Face card or 10 card) in the first two, he reveals it and wins the game.
# 6. Otherwise, Player gets to choose if he wants to Hit, Stand, Surrender or Double Wager. Surrender is only possible as first decision of the round.
# 7. If Hit, Player receives another card. If Surrender, Player gives up half his bet and finishes the round. If Double, Player doubles his bet and picks up only one more card.
# 8. If Stand, Player ends his turn and lets Dealer take over.
# 9. Dealer now takes his turn. He reveals his hole card and hits until he reaches or exceeds 17 pts. Then he stands.
# 10. The person who exceeds 21 pts automatically loses. Otherwise the person who has the greater number of pts wins.
# 11. If both have the same number of pts, they tie and neither loses anything.
#===========================================================#


import random as rd 

# Class definitions for Card, Person
# Card has name, hard value and soft value.
class Card:
    def __init__(self, num_in_deck):
        if num_in_deck > 13 or num_in_deck < 1:
            raise ValueError("Cards go from 1 to 13. Ace is 1")

        if num_in_deck == 1:
            self.name = 'Ace'
            self.hard_value = 1
            self.soft_value = 11
        
        elif num_in_deck == 13:
            self.name = 'K'
            self.hard_value = 10
            self.soft_value = 10

        elif num_in_deck == 12:
            self.name = 'Q'
            self.hard_value = 10
            self.soft_value = 10

        elif num_in_deck == 11:
            self.name = 'J'
            self.hard_value = 10
            self.soft_value = 10

        else:
            self.name = str(num_in_deck)
            self.hard_value = num_in_deck
            self.soft_value = num_in_deck

# Attributes: Person has name, hand, points of hardened hand and points of softened hand. It also has a end_turn_flag to explain how they ended their turn. 
# Flags: -1 for Stand, 0/False for Not End, 1 for Blackjack (Ace & Face Card or 10), 2 for Bust (> 21 points), 3 for Surrender
# Methods: Person can hit or stand. There's also a new_round function to reset after each round.
class Person:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points_hard = 0
        self.points_soft = 0
        self.end_turn_flag = 0

    def __str__(self):
        return self.card_hand_str() 

    def __repr__(self):
        return self.card_hand_str()

    def card_hand_str(self):
        if len(self.hand) > 1:
            hand_names = ', '.join([x_card.name for x_card in self.hand[:-1]]) + " and " + self.hand[-1].name
        else:
            hand_names = self.hand[0].name
        return "%s shows %s." %(self.name, hand_names)

    def new_round(self):
        self.hand = []
        self.points_hard = 0
        self.points_soft = 0
        self.end_turn_flag = 0

    def calculate_points(self):

        self.points_hard = sum([x_Card.hard_value for x_Card in self.hand])
        self.points_soft = sum([x_Card.soft_value for x_Card in self.hand])

        hard_hand = [x_Card.hard_value for x_Card in self.hand]
                
        if len(self.hand) == 2:
            if 1 in hard_hand:
                if 10 in hard_hand:
                    self.end_turn_flag = 1

        else:
            if self.points_hard > 21:
                self.end_turn_flag = 2

    def hit(self, a_card):
        foo = self.card_hand_str()[:-1]
        self.hand.append(a_card)
        self.calculate_points()
        print "%s, and received %s. (%d points)" %(foo, a_card.name, self.points_hard)

    def stand(self):
        print "%s stands." %(self.name)
        self.end_turn_flag = -1


# Player has additional Surrender and Double Wager methods. It also has the chips attribute and specifies amount to be bet. 
class Player(Person):
    def __init__(self):
        Person.__init__(self, "Player")
        self.chips = 100
        self.bets = 0

    def surrender(self):
        self.bets = int(round(self.bets/2))
        self.end_turn_flag = 3
        print "Player surrenders. Gives up half wager."

    def double_wager(self):
        if self.chips < 2*self.bets:
            print "Not enough chips to bet double wager! Try something else."
            return 0
        else:
            self.bets = 2*self.bets
            self.end_turn_flag = -1
            print "Player puts double wager. Hit a single card to end turn."
            return 1

# Dealer has an additional Hole Card attribute.
class Dealer(Person):
    def __init__(self):
        Person.__init__(self, "Dealer")
        self.hole_card = None



# Utility Functions -------------------------------

# Generator for user raw_input checking. This repeats the raw input function until a recognizable answer is received.
def user_input(question_str):
    while True:
        yield raw_input(question_str)

def ask_deck():
    for attempt in user_input('How many decks would you like to use? (1-10): '):
        try:
            num_of_decks = int(attempt.strip())
            if num_of_decks < 1 or num_of_decks > 10:
                raise ValueError
            return num_of_decks
        except ValueError:
            print "Please enter valid number of decks from 1 to 10."

# Ask for decision
def ask_decision(first_decision=False):
    if first_decision:
        question = "Would you like to stand (S), surrender (R), double wager (D) or hit (H)?: "
        decision_list = ['H', 'S', 'R', 'D']
    else:
        question = "Would you like to stand (S), double wager (D) or hit (H)?: "
        decision_list = ['H', 'S', 'D']

    for attempt in user_input(question):
        try:
            answer=attempt.strip().upper()[0] 
            if answer in decision_list:
                return answer
            else:
                raise ValueError
        except ValueError:
            print ("Invalid command, please retype?")


# Ask for user inputed bet
def ask_bets(round_num, max_bet):
    for attempt in user_input("Place bet for Round No. %d: " %round_num):       
        try:
            player_bet= int(attempt.strip())

            if player_bet < 1 or player_bet > max_bet:
                raise ValueError

            return player_bet

        except ValueError:
            print "Bet has to be between 1 to %d chips! (Player's max)" %max_bet


#-------------------------------------#

def play_blackjack():
    print ("\n~---Let's play Blackjack!---~\n\n")
    one_deck = 4*[Card(x) for x in range(1,13)] 

    num_of_decks = ask_deck()
    shoe = one_deck * num_of_decks
    rd.shuffle(shoe)

    a_player = Player()
    a_dealer = Dealer()

    round_num = 0
    next_round = True



    # Function to handle end-of-turn exit flags at end of each round

    def end_of_round():

        if a_player.end_turn_flag > 0:
            if a_player.end_turn_flag == 1:
                if a_dealer.end_turn_flag == 1:
                    print "Player and Dealer both have a Blackjack. What are the odds? Tie."
                else:
                    print "Player has a Blackjack! Player wins %d chips" %a_player.bets
                    a_player.chips += a_player.bets

            if a_player.end_turn_flag == 2:
                print "Player busts! Player loses %d chips." %a_player.bets
                a_player.chips -= a_player.bets

            if a_player.end_turn_flag == 3:
                print "Player loses %d chips." %a_player.bets
                a_player.chips -= a_player.bets

        # Dealer triggered end of round
        elif a_dealer.end_turn_flag > 0:
            if a_dealer.end_turn_flag == 1:
                print a_dealer,
                print "Dealer has a Blackjack! Player loses %d chips" %a_player.bets
                a_player.chips -= a_player.bets
            if a_dealer.end_turn_flag == 2:
                print "Dealer busts! Player wins %d chips." %a_player.bets
                a_player.chips += a_player.bets
        
        # Both stand
        else: 
            a_dealer.calculate_points()
            a_player.calculate_points()

            if a_dealer.end_turn_flag > 0:
                end_of_round()
            
            else:
                dealer_pts = max([x for x in (a_dealer.points_hard, a_dealer.points_soft) if x <=21])
                player_pts =  max([x for x in (a_player.points_hard, a_player.points_soft) if x <=21])

                print "Player has %d points. Dealer has %d points." %(player_pts, dealer_pts)
                if dealer_pts == player_pts:
                    print "Dealer and Player tie."
                elif dealer_pts < player_pts:
                    print "Player has more points than Dealer. Player wins %d chips." %a_player.bets
                    a_player.chips += a_player.bets
                else:
                    print "Dealer has more points than Player. Player loses %d chips." %a_player.bets
                    a_player.chips -= a_player.bets


    # While loop to continuously run the game
    while next_round:
        round_num += 1
        a_player.new_round()
        a_dealer.new_round()

        print "\nStarting Round %d" %round_num

    # Player has to make a bet
        a_player.bets = ask_bets(round_num, a_player.chips)

    # Initialise with 2 cards each. Dealer has a hole card.     
        a_player.hand.append(shoe.pop())
        a_player.hand.append(shoe.pop())

        a_dealer.hand.append(shoe.pop())
        a_dealer.hole_card=shoe.pop()

    # Reveals the initial 2 cards
        print a_player,
        print a_dealer

        # Player looks at his hand and calculates.
        a_player.calculate_points()

        # Dealer peeks at his hole card and finds out if he has a blackjack.
        a_dealer.hand.append(a_dealer.hole_card)
        a_dealer.calculate_points()

        
        # If Player is lucky, he has a Blackjack:
        if a_player.end_turn_flag == 1:
            end_of_round()

        # If Dealer's hole card makes it blackjack, he should call it:
        elif a_dealer.end_turn_flag == 1:
            end_of_round()

    # Otherwise:
        else:
            # Dealer hides his hole card again.
            a_dealer.hand.pop()
            a_dealer.end_turn_flag = 0

            # Player start by hitting.
            first_decision = True
            while a_player.end_turn_flag ==0:
                if len(shoe) < 2:
                    shoe.extend(one_deck)
                    rd.shuffle(shoe)

                player_decision = ask_decision(first_decision)

                if player_decision == 'H':
                    a_player.hit(shoe.pop())
                if player_decision == 'R':
                    a_player.surrender()    
                if player_decision == 'D':
                    if a_player.double_wager():
                        a_player.hit(shoe.pop())
                    else:
                        continue
                if player_decision =='S':
                    a_player.stand()

                first_decision = False

            # Player ends round if he busts or surrenders
            if a_player.end_turn_flag > 0:
                end_of_round()

            else:
                # Dealer reveals hole card
                print "Dealer's hole card is %s." %a_dealer.hole_card.name
                a_dealer.hand.append(a_dealer.hole_card)
                a_dealer.calculate_points()

                # Dealer runs through his turn. Hits until he reaches or exceeds 17 points.
                while a_dealer.end_turn_flag == 0:
                    if len(shoe) < 2:
                        shoe.extend(one_deck)
                        rd.shuffle(shoe)

                    if a_dealer.points_hard < 17:
                        a_dealer.hit(shoe.pop())
                    else:
                        a_dealer.stand()

                end_of_round()

    #End of everybody's turn.

    
    # Decide if want run another round
        if a_player.chips < 1:
            print "Player has no more chips!"
            next_round = False
        
        else:
            foo = raw_input("\nPlayer has %d chips. Another round? Y/N (by default Y): " %a_player.chips).strip().upper()
            if foo:
                if foo[0] == "N":
                    print "Ending Blackjack Game."
                    next_round = False


if __name__== "__main__":
    play_blackjack()
