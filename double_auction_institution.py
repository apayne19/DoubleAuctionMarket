from timeit import default_timer as timer
import spot_system
class Auction(object):
    """ A class that makes a market"""
    board = {"is_open": False, "orders": [], "contracts": [], "standing": {}}

    def __init__(self, name, ceiling, floor):
        self.name = name
        self.ceiling = ceiling
        self.floor = floor
        self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid # buyers want low
        self.board["standing"]["bidder"] = self.name  # displays bidder
        self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask # sellers want high
        self.board["standing"]["asker"] = self.name  # displays seller
        self.srt = timer()
        self.strategy = None
        self.player_id = None
        self.sys = spot_system.SpotSystem()
    def show(self):
        print("I am auction {}, with ceiling {} and floor {}.".format(self.name, self.ceiling, self.floor))

    def report_standing(self):
        return (self.board["standing"]["bid"], self.board["standing"]["ask"])

    def report_contracts(self):
        return self.board["contracts"]

    def report_orders(self):
        return self.board["orders"]

    def time_index(self):
        stp = timer()
        t = (round(stp - self.srt, 5))
        return t

    def bid(self, player_id, amt, strategies, period, round):
        self.strategy = strategies[player_id]['strat']
        current_unit = strategies[player_id]['units']
        if len(strategies[player_id]['values']) == 1:
            current_value = strategies[player_id]['values'][0]  # TODO is trader's max value still the 1st if no trade?
        else:
            current_value = strategies[player_id]['values'][current_unit]
        current_earns = strategies[player_id]['earn']
        self.player_id = player_id
        if self.board["is_open"]:
            self.board["orders"].append([self.time_index(), self.player_id, current_unit, current_value, current_earns, "bid", amt, self.strategy, period, round])
        else:
            return "closed"

        if amt > self.board["standing"]["bid"] and amt < self.ceiling:  # check for valid amount
            if amt > self.board["standing"]["ask"]:
                status = "contract"  # contract = (price, buyer, seller) price = standing ask
                contract = (self.board["standing"]["ask"], player_id, self.board["standing"]["asker"], self.time_index())
                # TODO contract price should be random between bid and ask...??
                self.board["contracts"].append(contract)
                # reinitalize standing bid and ask
                self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid
                self.board["standing"]["bidder"] = self.name
                self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask
                self.board["standing"]["asker"] = self.name
            else:
                status = "stand"
                self.board["standing"]["bid"] = amt
                self.board["standing"]["bidder"] = player_id
        else:
            status = "reject"
        return status

    def ask(self, player_id, amt, strategies, period, round):
        self.strategy = strategies[player_id]['strat']
        current_unit = strategies[player_id]['units']
        if len(strategies[player_id]['costs']) == 1:
            current_cost = strategies[player_id]['costs'][0]
        else:
            current_cost = strategies[player_id]['costs'][current_unit]
        current_earns = strategies[player_id]['earn']
        self.player_id = player_id
        if self.board["is_open"]:
            self.board["orders"].append([self.time_index(), self.player_id, current_unit, current_cost, current_earns, "ask", amt, self.strategy, period, round])
        else:
            return "closed"
        if amt < self.board["standing"]["ask"] and amt > self.floor:  # check for valid ask
            if amt < self.board["standing"]["bid"]:  # check for contract
                status = "contract"  # contract = (price, buyer, seller) price = standing bid
                contract = (self.board["standing"]["bid"], self.board["standing"]["bidder"], player_id, self.time_index())
                self.board["contracts"].append(contract)
                # reinitalize standing bid and ask
                self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid
                self.board["standing"]["bidder"] = self.name
                self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask
                self.board["standing"]["asker"] = self.name
            else:
                status = "stand"
                self.board["standing"]["ask"] = amt
                self.board["standing"]["asker"] = player_id
        else:
            status = "reject"
        return status

    def buy(self, player_id):
        if self.board["is_open"]:
            self.board["orders"].append((self.time_index(), player_id, "buy", "null"))
        else:
            return "closed"
        if self.board["standing"]["asker"] != self.name:  # Buying from  true seller
            status = "contract"  # contract = (price, buyer, seller) price = standing ask
            contract = (self.board["standing"]["ask"], player_id, self.board["standing"]["asker"])
            self.board["contracts"].append(contract)
            # reinitalize standing bid and ask
            self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid
            self.board["standing"]["bidder"] = self.name
            self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask
            self.board["standing"]["asker"] = self.name
        else:
            status = "reject"
        return status

    def sell(self, player_id):
        if self.board["is_open"]:
            self.board["orders"].append((self.time_index(), player_id, "sell", "null"))
        else:
            return "closed"
        if self.board["standing"]["bidder"] != self.name:  # Buying from  true seller
            status = "contract"  # contract = (price, buyer, seller) price = standing ask
            contract = (self.board["standing"]["bid"], self.board["standing"]["bidder"], player_id)
            self.board["contracts"].append(contract)
            # reinitalize standing bid and ask
            self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid
            self.board["standing"]["bidder"] = self.name
            self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask
            self.board["standing"]["asker"] = self.name
        else:
            status = "reject"
        return status

    def open_board(self, player_id):
        if player_id == "tournament official":
            self.board["is_open"] = True
            self.board["contracts"] = []
            self.board["offers"] = []
            self.board["standing"]["bid"] = self.floor  # Start at smallest possible bid
            self.board["standing"]["bidder"] = self.name
            self.board["standing"]["ask"] = self.ceiling  # Starts at largest possible ask
            self.board["standing"]["asker"] = self.name

    def close_board(self, player_id):
        if player_id == "tournament official":
            self.board["is_open"] = False

if __name__ == "__main__":
    da = Auction('da', 0, 400)