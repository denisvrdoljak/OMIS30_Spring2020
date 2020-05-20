from deckofcards import Deck,Card

class Boot(Deck):
    def __init__(self,numberofdecks=1):
        # make sure numberofdecks is valid 
        if type(numberofdecks) is not int or numberofdecks < 1:
            raise ValueError("numberofdecks argument must be a positive integer. The current value is: {}".format(numberofdecks))
        self.numberofdecks = numberofdecks
        self.loadnewboot()
        self.shuffledeck()

    def loadnewboot(self):
        self.loadnewdeck()
        self.deck  *= self.numberofdecks
        # use inherited loadnewdeck() method to load 1 deck
        # then increase number of decks in Boot to numberofdecks

class Player:
    def __init__(self,name=None,dealer=False):
        # argument error checking
        if type(dealer) is not bool:
            raise ValueError("dealer argument must be a boolean. The current value is: {}".format(dealer))
        if type(name) is not str and name is not None:
            raise ValueError("player name must be a string")
        
        # create attribute that is a dictionary of card point values
        self.cardpointvalues = {value:int(value) for value in Card.possiblecardvalues[:9]}
        self.cardpointvalues.update({value:10 for value in Card.possiblecardvalues[9:]})
        self.cardpointvalues.update({'A':11})
        
        # initialize variables
        self.showcards = False
        self.money = 1000 # starting amount
        self.dealer = dealer # dealer flag
        self.clear_hand() # creates and clears self.hand list
        self.betamount = 0

        # figure out names
        if name is None:
            name = "<unnamed>"
            if dealer:
                name = ""
        if dealer:
            name = "Dealer " + name
        self.name = name.strip()
                
    def set_showhand(self):
        self.showcards = True
        # make hand visible, used in __repr__ method

    def set_hidehand(self):
        self.showcards = False
        # make hand not visible, used in __repr__ method
    
    def get_handvalue(self):
        handvalue = sum([self.cardpointvalues[card.value] for card in self.hand])
        # get hand value (using 11 for all Aces)
        for card in self.hand:
            if handvalue > 21 and card.value == 'A':
                handvalue -=10
                # subract 10 for each Ace until under 21
        return handvalue
    
    def bet(self,betammount):
        if type(betammount) is not int:
            raise ValueError("betammount must be an int")
        if betammount > self.money:
            raise ValueError("cannot bet more than player has. Player has (), bet was ().".format(self.money,betammount))
        self.money -= betammount
        self.betamount = betammount
        # remove money from Player when placing a bet
    
    def win(self):
        self.money += 2*self.betamount
        # add winnings to player's money'
        # winnings  include original bet + profit, so 2 * self.betamount
        self.betamount = 0
        # clear bet
    
    def lose(self):
        self.betamount = 0
        # clear bet
    
    def isdealer(self):
        return self.dealer
    
    def get_moneyamount(self):
        return self.money
    
    def clear_hand(self):
        self.hand = []

    def take_card(self,card):
        if type(card) is not Card:
            raise ValueError("card must of of Card class")
        self.hand.append(card)
    
    def __repr__(self):
        # this method allows us to define what Player will look like
        # Also, we will be able to print(Player) once we define this
        # in this case, we can also control how the dealer shows/hides cards here
        
        if self.showcards:
            return self.name + ': ['+' '.join([card.__repr__() for card in self.hand])+']'
        elif self.dealer and len(self.hand)>1:
            return self.name + ': [** ' +' '.join([card.__repr__() for card in self.hand[1:]])+']'
        else:
            return self.name + ': ['+' '.join([' ** ' for card in self.hand])+']'

class BlackJackTable:
    def __init__(self):
        self.table = []
        self.dealer = None
        self.boot = None
    
    def sit_at_table(self,player):
        if type(player) is not Player:
            raise ValueError("player must be an instance of the Player class")
        if player.isdealer():
            raise ValueError("player cannot be a dealer")
        self.table.append(player)
    
    def assigndealer(self,dealer):
        if type(dealer) is not Player:
            raise ValueError("player must be an instance of the Player class")
        if not dealer.isdealer():
            raise ValueError("dealer must be a dealer")
        self.dealer = dealer
    
    def loadboot(self,boot):
        if type(boot) is not Boot:
            raise ValueError("must must be an instance of the Boot class")
        self.boot = boot
    
    def isready(self):
        if self.dealer is not None and len(self.table)>0 and self.boot is not None:
            return True
        else:
            return False
    
    def clear_table(self):
        if not self.isready():
            raise ValueError("Table is not ready.")
        self.dealer.clear_hand()
        for player in self.table:
            player.clear_hand()
    
    def deal_cards(self):
        if not self.isready():
            raise ValueError("Table is not ready.")
        self.clear_table()
        
        if self.boot.cardsleftindeck() < 2* (1 + len(self.table)):
            print("Boot empty. Loading another deck.")
            self.boot.loadnewdeck()
            self.boot.shuffledeck()
        
        # deal to players
        for player in self.table:
            self.deal_one(player)
            self.deal_one(player)
            #player.take_card(self.boot.dealcard())
            #player.take_card(self.boot.dealcard())
        # deal to dealer
        self.deal_one(self.dealer)
        self.deal_one(self.dealer)
        #self.dealer.take_card(self.boot.dealcard())
        #self.dealer.take_card(self.boot.dealcard())
    
    def __repr__(self):
        table_repr = []
        table_repr.append("\n")
        table_repr.append("\n")
        table_repr.append("========== BLACKJACK TABLE ==========")
        table_repr.append("\n")
        table_repr.append("Dealer")
        table_repr.append(self.dealer.__repr__())
        table_repr.append("\n")
        table_repr.append("Player(s)")
        for player in self.table:
            table_repr.append(player.__repr__())
        table_repr.append("\n")
        return "\n".join(table_repr)
    
    def userplay(self,player):
        while True:
            print()
            print(self.__repr__())
            print("Hello {}!".format(player.name))
            print("you have {}. Would you like to hit?".format(player.get_handvalue()))
            play = input("[Enter] to stay, any other entry to hit: ")
            if play == '':
                print("You chose to stay.")
                break
            else:
                player.take_card(self.boot.dealcard())
    
    def get_besthand(self):
        best = -1
        for player in self.table:
            if player.get_handvalue() > 21:
                continue
            elif player.get_handvalue() > best:
                best = player.get_handvalue()
        return best
    
    def user_bet(self,player):
        while True:
            bet = input("Please enter a bet amount (dollars as an int, [Enter] for default of 100)\nYou have ${}: ".format(player.get_moneyamount()))
            if bet == '':
                bet = 100
                break
            elif not bet.isdigit():
                print("That's not a valid bet.\n\nPlease try again.")
                continue
            elif int(bet) > player.get_moneyamount():
                print("You do not have that much money. Please try again.")
                continue
            else:
                bet = int(bet)
                break
        print("You bet ${}".format(bet))
        player.bet(bet)
        print("(You have ${} left.".format(player.get_moneyamount()))
    
    def deal_one(self,player):
        if not self.boot.cardsleftindeck():
            print("Boot empty. Loading another deck.")
            self.boot.loadnewdeck()
            self.boot.shuffledeck()
        player.take_card(self.boot.dealcard())
    
    def dealerplay(self):
        dealer = self.dealer #so I don't have to keep writing self.dealer
        dealer.set_showhand()
        # show dealer hand when dealer starts to play

        # old dealer logic, changing to simpler, "hit until 17"
        # this is the dealer gameplay, hit until over 17 AND over player's value, unless player already busted
        #while dealer.get_handvalue() < 21 and dealer.get_handvalue() < self.get_besthand() and dealer.get_handvalue() <17:
        
        # dealer hits until getting 17 or more
        if dealer.get_handvalue() >=17:
            print("Dealer will STAY")
        while dealer.get_handvalue() <17:
        
            print("Dealer HITS")
            #dealer.take_card(self.boot.dealcard())
            self.deal_one(dealer)
            print(dealer)
            if dealer.get_handvalue() > 21:
                print("Dealer BUSTS, with {}!".format(dealer.get_handvalue()))   
            else:
                print("Dealer STAYS, with {}.".format(dealer.get_handvalue()))
    
    def evaluate(self):
        print("Dealer has {}".format(self.dealer.get_handvalue()))
        bestplayerhand = self.get_besthand() if self.get_besthand() != -1 else "BUST"
        print("Best player has {}".format(bestplayerhand))
        if self.dealer.get_handvalue() <= 21 and self.dealer.get_handvalue() > self.get_besthand():
            print("Dealer wins!")
            for player in self.table:
                player.lose()
                print("Player {} now has ${}.".format(player.name,player.get_moneyamount()))
        else:
            print("Player wins!")
            for player in self.table:
                player.win()
            print("Player {} now has ${}.".format(player.name,player.get_moneyamount()))
    
