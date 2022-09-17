# Author: Vitaliy Tsupriyan
# Github username: Vitaliy2283
# Date: 06/01/2022
# Description: This is a project for Real Estate Game that allows two or more people to play a simplified version of the game Monopoly.
# Players start at the "GO" space on the board. Players take turns rolling a single die (values 1-6), and moving around the board spaces.
# The spaces are arranged in a circle, and players will pass each space repeatedly. Each player receives a certain amount of money at the start, and also every time they
# land on or pass the "GO" space. Each space on the board may be purchased except for "GO". Once purchased, the player owner charges rent
# to other players who land on the space. When a player runs out of money, that player becomes inactive, and cannot move or own spaces.
# The game continues until all players, but one, have run out of money. The last player with money is declared the winner.
# This code has three classes: Player, Space and RealEstateGame which the game admin class. All data members is private.

class Player:
    """Represent a player of the game and using the class RealEstateGame.
    It includes a private data members and stores the player info"""

    def __init__(self, name, account_balance):
        """ Constructor for a Player class. Takes two parameters name -> str and account balance -> int.
         And initialize current player position -> int and properties -> list """
        self._player_name = name
        self._account_balance = account_balance
        self._current_position = 0
        self._properties = []

    def get_account_balance(self):
        """ Returns players account balance -> int """
        return self._account_balance

    def set_account_balance(self, amount):
        """ Takes amount ->int as parameter and sets players account balance amount -> int """
        self._account_balance = amount

    def update_account_balance(self, amount):
        """ Takes amount ->int as parameter and updates players account balance -> int. """
        self._account_balance += amount

    def decrease_account_balance(self, amount):
        """ Takes amount ->int as parameter and decreases players account balance -> int. """
        self._account_balance -= amount

    def get_current_position(self):
        """Returns players current position -> int """
        return self._current_position

    def get_player_name(self):
        """Returns player current name -> str """
        return self._player_name

    def get_properties(self):
        """ Returns properties list of the player ->list """
        return self._properties

    def buy_space(self, space):
        """Takes as a parameter object of a space class. Checks if the player account balance is greater
        than the purchase price, and if the space doesn't have an owner and if the space is not a "GO" space.
        Deducts space purchase from the player's account. Sets the player as the owner of the current space and returns True,
        otherwise return False """
        if self._account_balance >= space.get_purchase_price():
            if space.get_space_owner() is None and space.get_name() != "GO":
                self._account_balance = self._account_balance - space.get_purchase_price()
                space.set_space_owner(self._player_name)
                self._properties.append(space)
                return True
            else:
                return False
        else:
            return

    def move_player(self, spaces_to_move):
        """ Takes as a parameter the number of spaces to move. Checks if current position becomes 0 after move,
        if it is it will update player account balance with a "GO" amount and will set the current position to 0.
        Otherwise checks if player completes 24 moves and updates account balance and player current position for the new round"""
        if self._current_position + spaces_to_move == 25:
            self._account_balance += Space.go_amount
            self._current_position = 0

        elif self._current_position + spaces_to_move > 24:
            self._account_balance += Space.go_amount
            self._current_position = (self._current_position + spaces_to_move -1) - 24

        else:
            self._current_position += spaces_to_move


class Space:
    """Represents a single game cell space and using class RealEstateGame
    It includes a private data members to store the space info"""

    go_amount = 0 # initial amount of the GO space

    def __init__(self, name, rent):
        """ Constructor for a Space class. Takes two parameters name -> str and rent -> int.
         Initialize purchase price -> int that equal to 5 times the rent amount and initialize current space owner"""
        self._name = name
        self._rent = rent
        self._purchase_price = rent * 5
        self._space_owner = None

    def get_name(self):
        """Returns space name -> str"""
        return self._name

    def get_purchase_price(self):
        """Returns space purchase price -> int"""
        return self._purchase_price

    def get_space_owner(self):
        """Returns owner of the space -> str"""
        return self._space_owner

    def set_space_owner(self, player_name):
        """ Takes player name -> str as a parameter and  sets space owners name -> str"""
        self._space_owner = player_name

    def get_rent(self):
        """Returns the rent of the space -> int """
        return self._rent


class RealEstateGame:
    """This is a game admin class. It uses Players and Space classes to play the game.
    It includes a private data members and keeps tracks of the players and spaces"""

    def __init__(self):
        """Constructor for a RealEstateGame class. Initialize lists of the players ->list and spaces ->list """
        self._players = []
        self._spaces = []

    def find_player(self, players_name):
        """"Helper method to find players during the implementation of the class while using different classes
        and returns player name -> str"""
        for player in self._players:
            if player.get_player_name() == players_name:
                return player

    def get_players(self):
        """Returns the list of all players -> list """
        return self._players

    def create_spaces(self, given_amount, rent_amount_list):
        """ Takes two parameters given_amount ->int and rents ->int.
        Creates space "GO" by using Space class and given_amount.
        Creates all 24 spaces with unique names and setting rents using given rents list parameter. """
        space_go = Space("GO", given_amount)
        Space.go_amount = given_amount
        self._spaces.append(space_go)
        s_num = 1
        for rent in rent_amount_list:
            space = Space(f"Space {s_num}", rent)
            self._spaces.append(space)
            s_num += 1

    def create_player(self, player_name, account_balance):
        """Takes two parameters player name and initial account balance. Creates player with unique name using Player class
        constructor method and adds player to the players list. Method checks if any player's name is duplicated """
        new_player = self.find_player(player_name)
        if new_player not in self._players:
            player = Player(player_name, account_balance)
            self._players.append(player)
        else:
            # print("Error: Player name is duplicated")
            return

    def get_player_account_balance(self, player_name):
        """ Takes player's same as the parameter and returns the players account balance -> int
        using Player class get_account_balance method"""
        player = self.find_player(player_name)
        return player.get_account_balance()

    def get_player_current_position(self, player_name):
        """ Takes player's name as the parameter and returns the players current position -> int
        using Player class get_current_position method"""
        player = self.find_player(player_name)
        return player.get_current_position()

    def buy_space(self, player_name):
        """Takes player's name as the parameter, finds the player object of the given name and
        buys space for the player using Player class buy_space method """
        player = self.find_player(player_name)
        current_space = self._spaces[player.get_current_position()]
        return player.buy_space(current_space)

    def move_player(self, player_name, number_of_spaces):
        """ Takes two parameters player name and number of spaces. Finds the player object of the given name.
         If the player's account balance is 0, the method will do nothing.
         Making a move by using move method of the player class.
         After the move is complete the player will pay rent for the new space occupied, if necessary.
         If the player is occupying the "GO" space, or if the space has no owner, or if the owner is the player no rent will be paid.
         Otherwise: The player pay's the rent for the current space.
         If current rent less than the player's account balance the space can be purchased.
         The amount paid will be deducted from the players account and added to the current space owner's account.
         If the player's new account balance is 0, the player has lost the game, and will be removed as the owner of any spaces"""
        player = self.find_player(player_name)
        if player.get_account_balance() == 0:
            return
        else:
            player.move_player(number_of_spaces)
            players_position = player.get_current_position()
            space_owner = self._spaces[players_position].get_space_owner()
            player_balance = player.get_account_balance()
            if players_position != 0 and space_owner is not None and space_owner != player.get_player_name():
                current_rent = self._spaces[players_position].get_rent()
                if current_rent <= player_balance:
                    owner = self.find_player(space_owner)
                    player.decrease_account_balance(current_rent)
                    if owner is not None:
                        owner.update_account_balance(current_rent)
                    if player.get_account_balance() == 0:
                        player.get_properties().clear()

    def check_game_over(self):
        """This method returns the name of the winner,if all players but one have an account balance of 0,
        otherwise returns empty string"""
        player_with_bal_zero = 0
        winner = "No winner"
        for player in self._players:
            if player.get_account_balance() == 0:
                player_with_bal_zero += 1
            else:
                winner = player.get_player_name()
        if player_with_bal_zero == len(self._players)-1:
            return winner
        else:
            winner = ""
            return winner


#main function to execute the game
def main():
    game = RealEstateGame()

    rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
             350, 350]
    game.create_spaces(50, rents)

    game.create_player("Player 1", 1000)
    game.create_player("Player 2", 1000)
    game.create_player("Player 3", 1000)
    game.create_player("Player 4", 1000)


    # while loop to play the game until the game is over and if all players but one have an account balance of 0
    while [player.get_account_balance() for player in game.get_players()].count(0) != len(game.get_players()) -1:

        game.move_player("Player 1", 4)
        game.buy_space("Player 1")
        game.move_player("Player 2", 6)
        game.buy_space("Player 2")
        game.move_player("Player 3", 1)
        game.buy_space("Player 3")
        game.move_player("Player 4", 3)
        game.buy_space("Player 4")

        print("P1", game.get_player_account_balance("Player 1"))
        print("P2", game.get_player_account_balance("Player 2"))
        print("P3", game.get_player_account_balance("Player 3"))
        print("P4", game.get_player_account_balance("Player 4"))


    print(game.check_game_over(), "is the winner")

if __name__ == "__main__":
    main()