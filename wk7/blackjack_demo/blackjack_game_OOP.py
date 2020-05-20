from blackjack import Player,BlackJackTable,Boot
import os

if __name__ == "__main__":
    # setup
    table = BlackJackTable()
    boot = Boot(6)
    table.loadboot(boot)
    dealer = Player('Janet',dealer=True)
    table.assigndealer(dealer)

    # Clear stdout
    os.system('cls' if os.name == 'nt' else 'clear')

    # Get player name
    name = input("Welcome to the BlackJack table! Please enter a name to play: ")
    if name == '':
        name = 'Bob'
        print("Ok, we'll just call you 'Bob' for now.")
    player = Player(name)
    player.set_showhand() # single player mode, so show hand
    table.sit_at_table(player)
    
    # Game Begins
    while True:
        playagain = input("Would you like to play the next hand?\n[Enter] to play, 'q' to quit: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if (playagain+' ')[0].lower() == 'q':
            print("Thank you for playing.\nYou left with ${}.\nQuitting...".format(player.get_moneyamount()))
            break
        elif player.get_moneyamount() <= 0:
            print("You are out of money.\nQuitting...")
            break

        table.user_bet(player)
        
        table.deal_cards()
        table.userplay(player)

        table.dealer.set_showhand()
        table.dealerplay()

        print(table)

        table.evaluate()
        table.dealer.set_hidehand()
    

