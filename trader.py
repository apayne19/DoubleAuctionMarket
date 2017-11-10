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
            if standing_bid:
                if cur_value > standing_bid:
                    bid = standing_bid + 1  # 10 is an arbitrary increment
                    return ["B", self.name, bid]
                else:
                    return []
            else:
                if cur_value > 0:
                    bid = 1
                    return["B", self.name, bid]
                else:
                    return[]
        else:
            # find out how many contracts you have
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return  [] # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on

            # TODO Put in asking or selling strategy
            if standing_ask:
                if cur_cost < standing_ask:
                    ask = standing_ask - 1  # 10 is an arbitrary decrement
                    return ["S", self.name, ask]
                else:
                    return []
            else:
                if cur_cost > 0:
                    ask = 999
                    return["B", self.name, ask]

class KaplanTrader(object):
    """Kaplan Sniping Trader"""

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

            if standing_bid:
                if standing_ask:
                    if standing_bid/standing_ask >= 0.98 and cur_value > standing_bid:
                        bid = standing_ask - 1
                        return ["B", self.name, bid]
                    else:
                        return []
                else:
                    if cur_value > standing_bid:
                        bid = standing_bid + 1
                        return ["B", self.name, bid]
                    else:
                        return []
            else:
                if cur_value > 0:
                    bid = 1
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

            if standing_ask:
                if standing_bid:
                    if standing_bid/standing_ask >= 0.98 and cur_cost < standing_ask:
                        ask = standing_bid + 1  # random number between cost and standing ask
                        return ["S", self.name, ask]
                    else:
                        return []

                else:
                    if cur_cost < 999:
                        ask = standing_ask - 1
                        return ["S", self.name, ask]
                    else:
                        return []
            else:
                if cur_cost > 0:
                    ask = 999
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
            if standing_bid:
                if cur_value > standing_bid:
                    bid = random.randint(standing_bid + 1, cur_value)  # random number between
                    # standing_bid + 10 used to be cur_value
                    return ["B", self.name, bid]
                else:
                    return []
            else:
                if cur_value > 0:
                    bid = 1
                    return["B", self.name, bid]
                else:
                    return[]
        else:
            # find out how many contracts you have
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return []  # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on

            # TODO Put in asking or selling strategy
            if standing_ask:
                if cur_cost < standing_ask:
                    ask = random.randint(cur_cost, standing_ask - 1)  # random number between
                    # standing_ask - 10 used to be cur_cost
                    return ["S", self.name, ask]
                else:
                    return []
            else:
                if cur_cost < 999:
                    ask = 999
                    return["S", self.name, ask]
                else:
                    return[]

class HaveToWin(object):
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

            if standing_bid:
                bid = standing_bid + 3  # random number between standing_bid and cur_value
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

            if standing_ask:
                ask = standing_ask - 3  # random number between cost and standing ask
                return ["S", self.name, ask]
            else:
                return []

if __name__ == "__main__":
    zi = ZeroIntelligenceTrader()