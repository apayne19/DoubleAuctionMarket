import random
import math
alphas = []
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
                    bid = max(cur_value, standing_bid + 10)  # 10 is an arbitrary increment
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
                    ask = max(standing_ask - 10, cur_cost)  # 10 is an arbitrary decrement
                    return ["S", self.name, ask]
                else:
                    return []
            else:
                if cur_cost > 0:
                    ask = 999
                    return["B", self.name, ask]

class KaplanTrader(object):
    """Trader based on Kaplan's Sniping Trader, waits in background until certain threshold met then
    places last minute bid/ask to steal trade"""

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


class ZI_Ctrader(object):
    """ A trader that bids and asks based on random amount"""

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
                        return ["S", self.name, ask]
                else:
                    return []

            else:
                if cur_cost < 999:
                    ask = 999
                    return["S", self.name, ask]
                else:
                    return[]

class ZI_Utrader(object):
    """ A class always increases bid by 3, decreases ask by 3, does not take cur_value or cur_cost into account
    makes a trader that is subject to Winner's Curse"""

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
                bid = random.randint(standing_bid + 1, 999)  # random number between standing_bid and cur_value
                return ["B", self.name, bid]
            else:
                bid = 1
                return ["B", self.name, bid]
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
                ask = random.randint(1, standing_ask - 1)  # random number between cost and standing ask
                return ["S", self.name, ask]
            else:
                ask = 999
                return ["S", self.name, ask]

class PStrader(object):
    """Trader using learning rule to get target price to bid/ask"""

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
            # beta = 0.3  # learning rate... adjustment speed
            # gamma = 0.05  # momentum... damps oscillation
            r_1 = random.uniform(0, 0.2)  # random variable between 0 and 20
            r_2 = random.uniform(0, 0.2)
            if standing_ask > standing_bid:  # ask greater than bid
                if standing_bid == 0:
                    bid = random.randint(10, 40)
                    return ["B", self.name, bid]
                else:
                    sigma = r_1*standing_bid + r_2  # bidders price change
                    target = standing_bid + sigma  # target valuation
                    bid = round(target, 0)
                    if bid <= cur_value:
                        # bid = gamma*cur_value + (1-gamma)*beta*(target-cur_value)  # learning rule
                        return ["B", self.name, bid]
                    else:
                        return []
            elif standing_ask <= standing_bid:  # ask less than or equal to bid
                sigma = r_1*standing_ask + r_2  # bidders price change
                target = standing_ask - sigma  # target valuation
                bid = round(target, 0)
                if bid <= cur_value:
                    # bid = gamma*cur_value + (1-gamma)*beta*(target-cur_value)  # learning rule
                    return ["B", self.name, bid]
                else:
                    return []
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
            # beta = 0.3  # learning rate... adjustment speed
            # gamma = 0.05  # momentum... damps oscillation
            r_1 = random.uniform(0, 0.2)  # random variable between 0 and 20
            r_2 = random.uniform(0, 0.2)
            if standing_ask > standing_bid:  # ask greater than bid
                sigma = r_1*standing_ask + r_2  # sellers price change
                target = standing_ask - sigma  # sellers target valuation
                ask = round(target, 0)
                if ask >= cur_cost:
                    # ask = gamma*cur_cost + (1-gamma)*beta*(target-cur_cost)  # learning rule
                    return ["S", self.name, ask]
                else:
                    return []
            elif standing_ask <= standing_bid:  # ask less than or equal to bid
                sigma = r_1*standing_bid + r_2  # sellers price change
                target = standing_bid + sigma  # sellers target valuation
                ask = round(target, 0)
                if ask >= cur_cost:
                    # ask = gamma*cur_cost + (1-gamma)*beta*(target-cur_cost)  # learning rule
                    return ["S", self.name, ask]
                else:
                    return []
            else:
                return []


class Trader_AA(object):
    def __init__(self):
        '''Trading strategy that uses aggressiveness levels, adjusts bids and asks according to target'''
        '''Refer to Vytelingum, Cliff, Jennings 2008'''
        '''Code contained within was created by Ash Booth and accessed on Github, his code adds functions to use
        Newton's method to obtain theta estimates...'''
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []
        # External parameters (you must choose [optimise] values yourselves)
        self.spin_up_time = 20  # same as rounds..?
        self.eta = 3.0
        self.theta_max = 2.0
        self.theta_min = -8.0
        self.lambda_a = 0.01
        self.lambda_r = 0.02
        self.beta_1 = 0.4
        self.beta_2 = 0.4
        self.gamma = 2.0
        self.nLastTrades = 5  # N in AIJ08
        self.ema_param = 2 / float(self.nLastTrades + 1)
        self.maxNewtonItter = 10
        self.maxNewtonError = 0.0001

        # The order we're trying to trade
        self.orders = []
        self.limit = None
        self.active = False
        self.job = None

        # Parameters describing what the market looks like and it's contstraints
        self.marketMax = 400  # hardcoded
        self.prev_best_bid_p = None
        self.prev_best_bid_q = None  # hardcoded
        self.prev_best_ask_p = None
        self.prev_best_ask_q = None  # hardcoded

        # Internal parameters (spin up time need to get values for some of these)
        self.eqlbm = 200
        self.theta = -1.0 * (5.0 * random.random())
        self.smithsAlpha = None
        self.lastTrades = []
        self.smithsAlphaMin = None
        self.smithsAlphaMax = None

        self.aggressiveness_buy = -1.0 * (0.3 * random.random())
        self.aggressiveness_sell = -1.0 * (0.3 * random.random())
        self.target_buy = None
        self.target_sell = None

    def updateEq(self, price):
        # Updates the equilibrium price estimate using EMA
        if self.eqlbm == None:
            self.eqlbm = price
        else:
            self.eqlbm = self.ema_param * price + (1 - self.ema_param) * self.eqlbm

    def newton4Buying(self):
        # runs Newton-Raphson to find theta_est (the value of theta that makes the 1st
        # derivative of eqn(3) continuous)
        theta_est = self.theta
        rightHside = ((self.theta * (self.limit - self.eqlbm)) / float(math.exp(self.theta) - 1));
        i = 0
        while i <= self.maxNewtonItter:
            eX = math.exp(theta_est)
            eXminOne = eX - 1
            fofX = (((theta_est * self.eqlbm) / float(eXminOne)) - rightHside)
            if abs(fofX) <= self.maxNewtonError:
                break
            dfofX = ((self.eqlbm / eXminOne) - ((eX * self.eqlbm * theta_est) / float(eXminOne * eXminOne)))
            theta_est = (theta_est - (fofX / float(dfofX)));
            i += 1
        if theta_est == 0.0: theta_est += 0.000001
        return theta_est

    def newton4Selling(self):
        # runs Newton-Raphson to find theta_est (the value of theta that makes the 1st
        # derivative of eqn(4) continuous)
        theta_est = self.theta
        rightHside = ((self.theta * (self.eqlbm - self.limit)) / float(math.exp(self.theta) - 1))
        i = 0
        while i <= self.maxNewtonItter:
            eX = math.exp(theta_est)
            eXminOne = eX - 1
            fofX = (((theta_est * (self.marketMax - self.eqlbm)) / float(eXminOne)) - rightHside)
            if abs(fofX) <= self.maxNewtonError:
                break
            dfofX = (((self.marketMax - self.eqlbm) / eXminOne) - (
            (eX * (self.marketMax - self.eqlbm) * theta_est) / float(eXminOne * eXminOne)))
            theta_est = (theta_est - (fofX / float(dfofX)))
            i += 1
        if theta_est == 0.0: theta_est += 0.000001
        return theta_est

    def updateTarget(self):
        # relates to eqns (3),(4),(5) and (6)
        # For buying
        if self.limit < self.eqlbm:
            # Extra-marginal buyer
            if self.aggressiveness_buy >= 0:
                target = self.limit
            else:
                target = self.limit * (
                1 - (math.exp(-self.aggressiveness_buy * self.theta) - 1) / float(math.exp(self.theta) - 1))
            self.target_buy = target
        else:
            # Intra-marginal buyer
            if self.aggressiveness_buy >= 0:
                target = (self.eqlbm + (self.limit - self.eqlbm) * (
                (math.exp(self.aggressiveness_buy * self.theta) - 1) / float(math.exp(self.theta) - 1)))
            else:
                theta_est = self.newton4Buying()
                target = self.eqlbm * (
                1 - (math.exp(-self.aggressiveness_buy * theta_est) - 1) / float(math.exp(theta_est) - 1))
            self.target_buy = target
        # For selling
        if self.limit > self.eqlbm:
            # Extra-marginal seller
            if self.aggressiveness_sell >= 0:
                target = self.limit
            else:
                target = self.limit + (self.marketMax - self.limit) * (
                (math.exp(-self.aggressiveness_sell * self.theta) - 1) / float(math.exp(self.theta) - 1))
            self.target_sell = target
        else:
            # Intra-marginal seller
            if self.aggressiveness_sell >= 0:
                target = self.limit + (self.eqlbm - self.limit) * (
                1 - (math.exp(self.aggressiveness_sell * self.theta) - 1) / float(math.exp(self.theta) - 1))
            else:
                theta_est = self.newton4Selling()
                target = self.eqlbm + (self.marketMax - self.eqlbm) * (
                (math.exp(-self.aggressiveness_sell * theta_est) - 1) / (math.exp(theta_est) - 1))
            self.target_sell = target

    def calcRshout(self, target, buying):
        if buying:
            # Are we extramarginal?
            if self.eqlbm >= self.limit:
                r_shout = 0.0
            else:  # Intra-marginal
                if target > self.eqlbm:
                    if target > self.limit: target = self.limit
                    r_shout = math.log((((target - self.eqlbm) * (math.exp(self.theta) - 1)) / (
                    self.limit - self.eqlbm)) + 1) / self.theta
                else:  # other formula for intra buyer
                    r_shout = math.log(
                        (1 - (target / self.eqlbm)) * (math.exp(self.newton4Buying()) - 1) + 1) / -self.newton4Buying()
        else:  # Selling
            # Are we extra-marginal?
            if self.limit >= self.eqlbm:
                r_shout = 0.0
            else:  # Intra-marginal
                if target > self.eqlbm:
                    r_shout = math.log(((target - self.eqlbm) * (math.exp(self.newton4Selling()) - 1)) / (
                    self.marketMax - self.eqlbm) + 1) / -self.newton4Selling()
                else:  # other intra seller formula
                    if target < self.limit: target = self.limit
                    r_shout = math.log((1 - (target - self.limit) / (self.eqlbm - self.limit)) * (
                    math.exp(self.theta) - 1) + 1) / self.theta
        return r_shout

    def updateAgg(self, up, buying, target):
        if buying:
            old_agg = self.aggressiveness_buy
        else:
            old_agg = self.aggressiveness_sell
        if up:
            delta = (1 + self.lambda_r) * self.calcRshout(target, buying) + self.lambda_a
        else:
            delta = (1 - self.lambda_r) * self.calcRshout(target, buying) - self.lambda_a
        new_agg = old_agg + self.beta_1 * (delta - old_agg)
        if new_agg > 1.0:
            new_agg = 1.0
        elif new_agg < 0.0:
            new_agg = 0.000001
        return new_agg

    def updateSmithsAlpha(self, price):
        self.lastTrades.append(price)
        if not (len(self.lastTrades) <= self.nLastTrades): self.lastTrades.pop(0)
        self.smithsAlpha = math.sqrt(
            sum(((p - self.eqlbm) ** 2) for p in self.lastTrades) * (1 / float(len(self.lastTrades)))) / self.eqlbm
        if self.smithsAlphaMin == None:
            self.smithsAlphaMin = self.smithsAlpha
            self.smithsAlphaMax = self.smithsAlphaMax
        else:
            if self.smithsAlpha < self.smithsAlphaMin: self.smithsAlphaMin = self.smithsAlpha
            if self.smithsAlpha > self.smithsAlphaMax: self.smithsAlphaMax = self.smithsAlpha
        alphas.append(self.smithsAlpha)

    def updateTheta(self):
        alphaBar = (self.smithsAlpha - self.smithsAlphaMin) / (self.smithsAlphaMax - self.smithsAlphaMin)
        desiredTheta = (self.theta_max - self.theta_min) * (
        1 - (alphaBar * math.exp(self.gamma * (alphaBar - 1)))) + self.theta_min
        theta = self.theta + self.beta_2 * (desiredTheta - self.theta)
        if theta == 0: theta += 0.0000001
        self.theta = theta

    def offer(self, contracts, standing_bid, standing_ask):
        self.prev_best_bid_p = standing_bid
        self.prev_best_ask_p = standing_ask
        num_contracts = 0
        if self.type == "buyer":
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                self.active = False
                return []  # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on
            self.limit = self.values[0]
            self.job = self.type
            self.active = True
            self.updateTarget()
            # currently a buyer (working a bid order)
            if self.spin_up_time > 0:
                ask_plus = (1 + self.lambda_r) * self.prev_best_ask_p + self.lambda_a
                bid = self.prev_best_bid_p + (min(self.limit, ask_plus) - self.prev_best_bid_p) / self.eta
                return ["B", self.name, round(bid, 0)]
            else:
                bid = self.prev_best_bid_p + (self.target_buy - self.prev_best_bid_p) / self.eta
                return ["B", self.name, round(bid, 0)]
        else:
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return []  # You can't ask anymore
            cur_cost = self.costs[num_contracts]  # this is the current value working on
            self.limit = self.costs[0]
            self.job = self.type
            self.active = True
            self.updateTarget()
            # currently a seller (working a sell order)
            if self.spin_up_time > 0:
                bid_minus = (1 - self.lambda_r) * self.prev_best_bid_p - self.lambda_a
                ask = self.prev_best_ask_p - (self.prev_best_ask_p - max(self.limit, bid_minus)) / self.eta
                return ["S", self.name, round(ask, 0)]
            else:
                ask = (self.prev_best_ask_p - (self.prev_best_ask_p - self.target_sell) / self.eta)
                return ["S", self.name, round(ask, 0)]

    def respond(self, time, lob, trade, verbose):
        # what, if anything, has happened on the bid LOB?
        bid_improved = False
        bid_hit = False
        lob_best_bid_p = lob['bids']['best']
        lob_best_bid_q = None
        if lob_best_bid_p != None:
            # non-empty bid LOB
            lob_best_bid_q = lob['bids']['lob'][-1][1]
            if self.prev_best_bid_p < lob_best_bid_p:
                # best bid has improved
                # NB doesn't check if the improvement was by self
                bid_improved = True
            elif trade != None and ((self.prev_best_bid_p > lob_best_bid_p) or (
                (self.prev_best_bid_p == lob_best_bid_p) and (self.prev_best_bid_q > lob_best_bid_q))):
                # previous best bid was hit
                bid_hit = True
        elif self.prev_best_bid_p != None:
            # the bid LOB has been emptied by a hit
            bid_hit = True

        # what, if anything, has happened on the ask LOB?
        ask_improved = False
        ask_lifted = False
        lob_best_ask_p = lob['asks']['best']
        lob_best_ask_q = None
        if lob_best_ask_p != None:
            # non-empty ask LOB
            lob_best_ask_q = lob['asks']['lob'][0][1]
            if self.prev_best_ask_p > lob_best_ask_p:
                # best ask has improved -- NB doesn't check if the improvement was by self
                ask_improved = True
            elif trade != None and ((self.prev_best_ask_p < lob_best_ask_p) or (
                (self.prev_best_ask_p == lob_best_ask_p) and (self.prev_best_ask_q > lob_best_ask_q))):
                # trade happened and best ask price has got worse, or stayed same but quantity reduced -- assume previous best ask was lifted
                ask_lifted = True
        elif self.prev_best_ask_p != None:
            # the bid LOB is empty now but was not previously, so must have been hit
            ask_lifted = True

        if verbose and (bid_improved or bid_hit or ask_improved or ask_lifted):
            print('B_improved', bid_improved, 'B_hit', bid_hit, 'A_improved', ask_improved, 'A_lifted', ask_lifted)

        deal = bid_hit or ask_lifted
        self.prev_best_bid_p = lob_best_bid_p
        self.prev_best_ask_p = lob_best_ask_p

        if self.spin_up_time > 0: self.spin_up_time -= 1
        if deal:
            price = trade['price']
            #self.updateEq(price)
            self.updateSmithsAlpha(price)
            self.updateTheta()

        # The lines below represent the rules in fig(7) in AIJ08. The if statements have not
        # been merged for the sake of clarity.

        # For buying
        if deal:
            price = trade['price']
            if self.target_buy >= price:
                self.aggressiveness_buy = self.updateAgg(False, True, price)
            else:
                self.aggressiveness_buy = self.updateAgg(True, True, price)
        elif bid_improved and self.target_buy <= trade['price']:
            self.aggressiveness_buy = self.updateAgg(True, True, self.prev_best_bid_p)
        # For selling
        if deal:
            price = trade['price']
            if self.target_sell <= price:
                self.aggressiveness_sell = self.updateAgg(False, False, price)
            else:
                self.aggressiveness_sell = self.updateAgg(True, False, price)
        elif ask_improved and (self.target_sell >= trade['price']):
            self.aggressiveness_sell = self.updateAgg(True, False, self.prev_best_ask_p)

        self.updateTarget()

if __name__ == "__main__":
    zi = ZeroIntelligenceTrader()