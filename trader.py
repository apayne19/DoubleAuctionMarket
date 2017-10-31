import random
class SimpleTrader(object):
    """ A class that makes a trader"""

    def __init__(self):
        self.name = ""
        self.limits = (0, 0)
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask):
        num_contracts = 0  # intialize number of contracts

        if self.type == "buyer":
            # find out how many contracts you have
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                return [] # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on

            # TODO Put in bidding or buying strategy

            if cur_value > standing_bid:
                bid = min(cur_value, standing_bid + 10)  # 10 is an arbitrary increment
                return ["B", self.name, bid]
            else:
                return []
        else:
            # find out how many contracts you have
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return  [] # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on

            # TODO Put in asking or selling strategy

            if cur_cost < standing_ask:
                ask = max(cur_cost, standing_ask - 10)  # 10 is an arbitrary decrement
                return ["S", self.name, ask]
            else:
                return []


class ZeroIntelligenceTrader(object):
    """ A class that makes a trader"""

    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask):
        num_contracts = 0  # intialize number of contracts

        if self.type == "buyer":
            # find out how many contracts you have
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                return []  # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on

            # TODO Put in bidding or buying strategy

            if cur_value > standing_bid:
                bid = random.randint(standing_bid + 1, cur_value)  # random number between standing_bid and cur_value
                return ["B", self.name, bid]
            else:
                return []
        else:
            # find out how many contracts you have
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return []  # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on

            # TODO Put in asking or selling strategy

            if cur_cost < standing_ask:
                ask = random.randint(cur_cost, standing_ask - 1)  # random number between cost and standing ask
                return ["S", self.name, ask]
            else:
                return []

class ZIPTrader(object):
    """ A class that makes a trader"""

    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask):
        num_contracts = 0  # intialize number of contracts

        if self.type == "buyer":
            # find out how many contracts you have
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                return []  # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on

            # TODO Put in bidding or buying strategy

            if cur_value > standing_bid:
                bid = random.randint(standing_bid + 1, cur_value)  # random number between standing_bid and cur_value
                return ["B", self.name, bid]
            else:
                return []
        else:
            # find out how many contracts you have
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return []  # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on

            # TODO Put in asking or selling strategy

            if cur_cost < standing_ask:
                ask = random.randint(cur_cost, standing_ask - 1)  # random number between cost and standing ask
                return ["S", self.name, ask]
            else:
                return []




if __name__ == "__main__":
    zi = ZeroIntelligenceTrader()