import random
import math
import AI_Testing as prd
import spot_market_period as smp
alphas = []

'''Changed init.traders in spot.system and spot.market.prd to include current_period'''

class Trader_Shaver(object):
    """ This trading strategy attempts to increase standing bid by 1 and decrease standing ask by -1...
    ... based on Dave Cliff's Shaver strategy"""

    def __init__(self):
        self.name = ""
        self.limits = (0, 0)
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
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
                    bid = standing_bid + 1  # 1 is an arbitrary increment
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
                if cur_cost < 2000:
                    ask = 2000
                    return["B", self.name, ask]

class Trader_Kaplan(object):
    """Trader using Kaplan strategy from Rust et al.(1992)
    ## trader waits until standing bid/standing ask get close enough then steals the deal
    --> shown to be best strategy when only one in heterogeneous population
    --> fails when many of the same in population"""
    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
        num_contracts = 0  # intialize number of contracts
        if pmax == None and pmin == None:  # if first period then infinity and -infinity
            pmax = 100000000
            pmin = -100000000
        if self.type == "buyer":
            # find out how many contracts you have
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                return []  # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on
            try:
                next_value = self.values[num_contracts+1]  # if multiple units demanded
            except IndexError:
                next_value = None
            spread = standing_ask - standing_bid  # distance between standing ask and standing bid
            profit = cur_value - standing_bid  # expected earnings
            expected_profit = profit/cur_value  # TODO discuss expected profit calculation
            profit_threshold = 0.02  # profit has to be greater than 2%
            spread_factor = 0.1 * standing_ask  # 10% of standing ask
            lurk_threshold = 0.2  # when 80% of trading period done
            time_conversion = round_num/total_rounds  # % of trading period done
            if standing_bid:
                if standing_ask:
                    if next_value == None:
                        most = min(standing_ask, cur_value - 1)
                        if most > standing_bid:
                            if standing_ask <= pmax and expected_profit > profit_threshold and spread < spread_factor:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif standing_ask <= pmin:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif float(1 - time_conversion) <= lurk_threshold:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            else:
                                return []

                        else:
                            return []

                    else:
                        most = min(standing_ask, next_value - 1)
                        if most > standing_bid:
                            if standing_ask <= pmax and expected_profit > profit_threshold and spread < spread_factor:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif standing_ask <= pmin:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif float(1 - time_conversion) <= lurk_threshold:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            else:
                                return []
                        else:
                            return []

                else:
                    if next_value == None:
                        most = cur_value - 1
                        if most > standing_bid:
                            if standing_ask <= pmax and expected_profit > profit_threshold and spread < spread_factor:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif standing_ask <= pmin:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif float(1 - time_conversion) <= lurk_threshold:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            else:
                                return []
                        else:
                            return []
                    else:
                        most = next_value - 1
                        if most > standing_bid:
                            if standing_ask <= pmax and expected_profit > profit_threshold and spread < spread_factor:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif standing_ask <= pmin:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            elif float(1 - time_conversion) <= lurk_threshold:
                                bid = min(standing_ask, most)
                                return ["B", self.name, bid]
                            else:
                                return []
                        else:
                            return []

            else:
                bid = 1
                return ["B", self.name, bid]

        else:
            return []
            # find out how many contracts you have
            # for contract in contracts:
            #     if contract[2] == self.name:  # third position is seller id
            #         num_contracts = num_contracts + 1
            # if num_contracts >= len(self.costs):
            #     return []  # You can't ask anymore
            # cur_cost = self.costs[num_contracts]  # this is the current value working on
            # next_cost = self.costs[num_contracts + 1]
            # spread = standing_ask - standing_bid
            # spread_factor = 0.1 * standing_bid
            # profit = standing_ask - cur_cost
            # expected_profit = profit / cur_value
            # profit_threshold = 0.02
            # lurk_threshold = 0.2
            # time_conversion = round / total_rounds
            # if standing_ask:
            #     if standing_bid:
            #         if next_cost == None:
            #             most = max(cur_cost - 1, standing_bid)
            #             if most < standing_ask:
            #                 if standing_ask <= pmax and ...... and spread < spread_factor:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif standing_ask <= pmin:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif float(1 - time_conversion) <= lurk_threshold:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 else:
            #                     return []
            #
            #             else:
            #                 return []
            #
            #         else:
            #             most = max(cur_cost +1 , standing_bid)
            #             if most > standing_bid:
            #                 if standing_ask <= pmax and ...... and spread < spread_factor:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif standing_ask <= pmin:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif float(1 - time_conversion) <= lurk_threshold:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 else:
            #                     return []
            #             else:
            #                 return []
            #
            #     else:
            #         if next_cost == None:
            #             most = cur_cost + 1
            #             if most > standing_bid:
            #                 if standing_ask <= pmax and ...... and spread < spread_factor:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif standing_ask <= pmin:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif float(1 - time_conversion) <= lurk_threshold:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 else:
            #                     return []
            #             else:
            #                 return []
            #         else:
            #             most = next_value - 1
            #             if most > standing_bid:
            #                 if standing_ask <= pmax and ...... and spread < spread_factor:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif standing_ask <= pmin:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 elif float(1 - time_conversion) <= lurk_threshold:
            #                     bid = min(standing_ask, most)
            #                     return ["B", self.name, bid]
            #                 else:
            #                     return []
            #             else:
            #                 return []
            #
            # else:
            #     bid = 1
            #     return ["B", self.name, bid]

class Trader_ZIC(object):
    """Trader using Zero Intelligence Constrained strategy from Gode/Sunder(1993)
    ## submits random bids/asks between standing bid/standing ask and individual limit valuations
    --> supposedly represents human trading behavior
    --> Plott et al.(2002) show that ZIC does not display human behavior"""
    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
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
                        bid = random.randint(standing_bid, cur_value)  # random number between
                        return ["B", self.name, bid]
                else:
                    return []

            else:
                bid = 1
                return["B", self.name, bid]
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
                        ask = random.randint(cur_cost, standing_ask)  # random number between
                        return ["S", self.name, ask]
                else:
                    return []

            else:
                ask = 399
                return["S", self.name, ask]

class Trader_ZIU(object):
    """ A class always increases bid by 3, decreases ask by 3, does not take cur_value or cur_cost into account
    makes a trader that is subject to Winner's Curse"""
    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
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

class Trader_PS(object):
    """Trader using learning rule to get target price to bid/ask"""

    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
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
    '''Adaptive-Agressiveness trading strategy from Cliff et al.(2008)
    ## sellers and buyers given aggressiveness levels and use to alter profit margins for bids/asks
    --> more aggressive = trade off profit for higher chance of transaction
    --> less aggressive = trade off transaction chance for higher profit
    --> shown to beat GDX and ZIP trading strategies
    --> potential comparison to human traders in Smith(1962) +++ '''
    def __init__(self):
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
        self.active = False
        self.job = None
        self.limit = None

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

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
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
            self.limit = self.values[num_contracts]  # this is the current value working on
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
            self.limit = self.costs[num_contracts]  # this is the current value working on
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
            #self.updateEq(price)  #TODO allow equilibrium updating or no??
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

class Trader_GD(object):
    '''Trader using strategy from Gjerstadt/Dickhaut(1998)
    ## uses market history to calculate belief function to estimate prob of bid/ask being accepted at price p
    --> suffers from excessive volatility when rejected orders = 0
    --> volatility can be fixed using MGD strategy from Das(2001) +++
    --> not performing as expected... potential errors in code +++ '''
    def __init__(self):
            self.name = ""
            self.type = ""
            self.bidbestprice = None
            self.askbestprice = None
            self.values = []
            self.costs = []
            self.blotter = []
            self.orders = []
            # this is the transaction history recorded by this trader
            # only trading price will be recorded for each transaction
            # most recent trading price will be inserted at the begining
            # of the list
            self.history_transac = []

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
            # Get the acceptance possibility of a price existing
            # in the transaction history.
            # Params. price: target price
            self.bidbestprice = standing_bid
            self.askbestprice = standing_ask
            num_contracts = 0
            if self.type == "buyer":
                for contract in contracts:
                    if contract[1] == self.name:  # second position is buyer_id
                        num_contracts = num_contracts + 1
            else:
                for contract in contracts:
                    if contract[2] == self.name:  # third position is seller id
                        num_contracts = num_contracts + 1

            def getP(price):
                # History limitation is set to 100
                m = 100
                # if the length of history is lower than 100
                # then set history limitation to the length
                # of history until the length is greater than
                # 100
                if len(self.history_transac) < 100:
                    m = len(self.history_transac)
                if self.type == 'buyer':
                    success = 0.0
                    for i in range(0, m):
                        value = self.history_transac[i]
                        if value <= price:
                            success += 1
                    if m == 0.0:
                        return 0.0
                    else:
                        return success / m

                else:
                    success = 0.0
                    for i in range(0, m):
                        value = self.history_transac[i]
                        if value >= price:
                            success += 1

                    if m == 0.0:
                        return 0.0
                    else:
                        return success / m

            # Calculate expectation of a price
            # Params. price: target price
            #         profit: the profit gains by target price
            #         profit_rate: the profit rate (profit/limit price) of a target price
            def getE(price, profit, profit_rate):
                possibility = getP(price)
                return possibility ** 3 * profit * profit_rate

            # Calculate the best-guess price based on known expectation
            # of each price in transaction history
            # Params. knownlist: a list of [expectation,price] for each target price
            #                    i.e. [[e1,p1],[e2,p2]...]
            #         knownbest: the highest expectation with its price in knownlist
            #                    i.e. [e,p]
            def getbgprice(knownlist, knownbest):
                knownlist.sort(key=lambda x: x[1])  # sort by price
                position = knownlist.index(knownbest)  # position of known best price
                #                        print 'kb position',position,'list len',len(knownlist)
                kbprice = knownbest[1]  # get price of know best E-price item
                kbE = knownbest[0]  # get E of know best E-price item
                bgprice = kbprice  # initialize the hidden best price to known best price
                if position != 0 and position != len(
                        knownlist) - 1:  # if known-best price is not at first and last position in list
                    left = knownlist[position - 1]  # get E-price item by shifting left of 1
                    right = knownlist[position + 1]  # get E-price item by shifting right of 1
                    leftprice = left[1]  # get price of left E-price item
                    leftE = left[0]  # get E of left E-price item
                    rightprice = right[1]  # get price of right E-price item
                    rightE = right[0]  # get E of right E-price item

                    # now calculate the best guess price (bgprice)
                    part1 = (kbE - rightE) * (leftprice ** 2 - kbprice ** 2) - (leftE - kbE) * (
                    kbprice ** 2 - rightprice ** 2)
                    part2 = 2.0 * ((leftE - kbE) * (rightprice - kbprice) - (kbE - rightE) * (kbprice - leftprice))

                    if part2 != 0:
                        bgprice = part1 / part2
                        # according to assumption, bgprice should be between leftprice and rightprice
                        if not (bgprice > leftprice and bgprice < rightprice):
                            raise ValueError

                return bgprice

            # Calculate the quote price using geometric mean method
            # a gmprice will be returned if there was a best price
            # in LOB, otherwise the quote price will remain the same
            # Params. price: the quote price we have got so far
            def getgmprice(price):
                # limit price of the order
                # quote price calculated by gemotric mean method
                gmprice = 0
                if self.type == 'buyer':
                    # best bid price in LOB at present
                    if standing_bid != None:
                        if standing_bid < cur_value:
                            gmprice = (standing_bid * price) ** (0.5)
                        if standing_bid > cur_value:
                            gmprice = (cur_value * price) ** (0.5)
                        return gmprice
                    else:
                        return price
                else:
                    # best ask price in LOB at present
                    if standing_ask != None:
                        if standing_ask > cur_cost:
                            gmprice = (standing_ask * price) ** (0.5)
                        if standing_ask < cur_cost:
                            gmprice = (cur_cost * price) ** (0.5)
                        return gmprice
                    else:
                        return price

            # Calculate the quote price
            def getquoteprice():
                # if the type of oder is to bid..
                if self.type == 'buyer':
                    profit_price = []  # structure: a list of [expectation,price]
                    temp = []  # temp list to avoid adding expectation of same price to profit_price list
                    # get each target price from transaction history
                    for price in self.history_transac:
                        # ensure a target price produces profit and its expection
                        # has not been calculated yet
                        if price < cur_value and price not in temp:
                            temp.append(price)
                            profit = cur_value - price  # profit made by target price
                            profit_rate = float(profit) / float(cur_value)  # profit rate of the target price
                            E = getE(price, profit, profit_rate)  # expectation of the target price
                            if E != 0:
                                profit_price.append([E, price])  # add [E,price] to the list
                    profit_price.sort(reverse=True)  # sort list from higher E to lower E

                    # if profit_price contains elements, which means there existing some
                    #  price in history that can make profit
                    if len(profit_price) != 0:
                        # get the first element in the list, which contains the highest E
                        # and corresponding price
                        knownbest = profit_price[0]
                        # price with the highest E we have got so far, if best-guess
                        # method not applied
                        kbprice = knownbest[1]

                        # calculate the best-guess price
                        bgprice = getbgprice(profit_price, knownbest)

                        # calculate the geometric mean price
                        gmprice = getgmprice(bgprice)
                        return gmprice

                    # if there was nothing in the list, that means none of existing price
                    # can make profit, then we quote same price as limit price
                    else:
                        return cur_value

                # if the type of order is to ask, similar as 'Bid' above
                else:
                    profit_price = []  # [profit expectation,price]
                    temp = []
                    for price in self.history_transac:
                        if price > cur_cost and price not in temp:
                            temp.append(price)
                            profit = price - cur_cost
                            profit_rate = float(profit) / float(cur_cost)
                            E = getE(price, profit, profit_rate)
                            if E != 0:
                                profit_price.append([E, price])
                    profit_price.sort(reverse=True)
                    if len(profit_price) != 0:
                        knownbest = profit_price[0]
                        kbprice = knownbest[1]

                        # calculate the best-guess price
                        bgprice = getbgprice(profit_price, knownbest)

                        # calculate the geometric mean price
                        gmprice = getgmprice(bgprice)
                        return gmprice
                    else:
                        return cur_cost

            if self.type == "buyer":
                if num_contracts >= len(self.values):
                    return []  # You can't bid anymore
                else:
                    cur_value = self.values[num_contracts]
                    bid = getquoteprice()
                    return["B", self.name, round(bid, 0)]
            else:
                if num_contracts >= len(self.costs):
                    return []  # You can't ask anymore
                else:
                    cur_cost = self.costs[num_contracts]
                    ask = getquoteprice()
                    return["S", self.name, ask]

        # Every time a new order was placed in LOB, market_session() will invoke
        # respond() function of each trader. Therefore our trader will update
        # transaction history here using the LOB passed by market_session()
        # This methond is rewrite from Trader class

    def respond(self, time, lob, trade, verbose):

            # update transaction history
            def updatehistory():
                # trading price
                price = trade['price']
                # trading quantity
                count = trade['qty']
                # each transaction will be recored multiple times
                # if the quantity > 0. However in BSE, the quantity
                # of transaction will always be 1
                while count != 0:
                    # most recent transaction will be inserted at the beginning
                    self.history_transac.insert(0, price)
                    count -= 1

            # if there was a transaction occurred in the market, then
            # we update transaction history
            if trade != None:
                updatehistory()

class Trader_ZIP(object):
    '''Trader using Zero Intelligence Plus strategy from Cliff(1997)
    ## uses prior trading information and limit values to alter profit margin up or down
    --> potential error at bottom of class when calling def respond() traders need memory +++
    --> currently trades are not generating eq quantity +++ '''

    # ZIP init key param-values are those used in Cliff's 1997 original HP Labs tech report
    # NB this implementation keeps separate margin values for buying & sellling,
    #    so a single trader can both buy AND sell
    #    -- in the original, traders were either buyers OR sellers
    def __init__(self):

        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []
        # got rid of self.balance = balance
        self.blotter = []
        self.orders = []
        # got rid of self.job for self.type
        self.active = False  # gets switched to True while actively working an order
        self.prev_change = 0  # this was called last_d in Cliff'97
        self.beta = 0.1 + 0.4 * random.random()
        self.momntm = 0.1 * random.random()
        self.ca = 0.05  # self.ca & .cr were hard-coded in '97 but parameterised later
        self.cr = 0.05
        self.margin = None  # this was called profit in Cliff'97
        self.margin_buy = -1.0 * (0.05 + 0.3 * random.random())
        self.margin_sell = 0.05 + 0.3 * random.random()
        self.price = None
        self.cur_value = None
        self.cur_cost = None
        # memory of best price & quantity of best bid and ask, on LOB on previous update
        self.prev_best_bid_p = None
        self.prev_best_bid_q = None
        self.prev_best_ask_p = None
        self.prev_best_ask_q = None

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
        num_contracts = 0
        self.prev_best_bid_p = standing_bid
        self.prev_best_ask_p = standing_ask
        if self.type == "buyer":
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                self.active = False
                return []  # You can't bid anymore
            self.cur_value = self.values[num_contracts]  # this is the current value working on
            self.active = True
            self.margin = self.margin_buy
            bid = int(self.cur_value * (1 + self.margin))
            self.price = bid
            return["B", self.name, bid]

        else:
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                self.active = False
                return []  # You can't bid anymore
            self.cur_cost = self.costs[num_contracts]  # this is the current value working on
            self.active = True
            self.margin = self.margin_sell
            ask = int(self.cur_cost * (1 + self.margin))
            self.price = ask
            return["S", self.name, ask]

    # update margin on basis of what happened in market
    def respond(self, time, lob, trade, verbose):
        # ZIP trader responds to market events, altering its margin
        # does this whether it currently has an order to work or not
        def target_up(price):
            # generate a higher target price by randomly perturbing given price
            ptrb_abs = self.ca * random.random()  # absolute shift
            ptrb_rel = price * (1.0 + (self.cr * random.random()))  # relative shift
            target = int(round(ptrb_rel + ptrb_abs, 0))
            # #                        print('TargetUp: %d %d\n' % (price,target))

            return target

        def target_down(price):
            # generate a lower target price by randomly perturbing given price
            ptrb_abs = self.ca * random.random()  # absolute shift
            ptrb_rel = price * (1.0 - (self.cr * random.random()))  # relative shift
            target = int(round(ptrb_rel - ptrb_abs, 0))
            # #                        print('TargetDn: %d %d\n' % (price,target))

            return target

        def willing_to_trade(price):
            # am I willing to trade at this price?
            willing = False
            if self.type == 'buyer' and self.active and self.price >= price:
                willing = True

            if self.type == 'seller' and self.active and self.price <= price:
                willing = True

            return willing

        def profit_alter(price):
            oldprice = self.price
            diff = price - oldprice
            change = ((1.0 - self.momntm) * (self.beta * diff)) + (self.momntm * self.prev_change)
            self.prev_change = change
            if self.type == 'buyer':
                newmargin = ((self.price + change) / self.cur_value) - 1.0
                if newmargin < 0.0:
                    self.margin_buy = newmargin
                    self.margin = newmargin
                self.price = int(round(self.cur_value * (1.0 + self.margin), 0))

            else:
                newmargin = ((self.price + change) / self.cur_cost) - 1.0
                if newmargin > 0.0:
                    self.margin_sell = newmargin
                    self.margin = newmargin
                # set the price from limit and profit-margin
                self.price = int(round(self.cur_cost * (1.0 + self.margin), 0))

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

        if self.type == 'seller':
            # seller
            if deal:
                tradeprice = trade['price']
                if self.price <= tradeprice:
                    # could sell for more? raise margin
                    target_price = target_up(tradeprice)
                    profit_alter(target_price)

                elif ask_lifted and self.active and not willing_to_trade(tradeprice):
                    # wouldnt have got this deal, still working order, so reduce margin
                    target_price = target_down(tradeprice)
                    profit_alter(target_price)

            else:
                # no deal: aim for a target price higher than best bid
                if ask_improved and self.price > lob_best_ask_p:
                    if lob_best_bid_p != None:
                        target_price = target_up(lob_best_bid_p)

                    else:
                        target_price = lob['asks']['worst']  # stub quote
                    profit_alter(target_price)

        if self.type == 'buyer':
            # buyer
            if deal:
                tradeprice = trade['price']
                if self.price >= tradeprice:
                    # could buy for less? raise margin (i.e. cut the price)
                    target_price = target_down(tradeprice)
                    profit_alter(target_price)

                elif bid_hit and self.active and not willing_to_trade(tradeprice):
                    # wouldnt have got this deal, still working order, so reduce margin
                    target_price = target_up(tradeprice)
                    profit_alter(target_price)

            else:
                # no deal: aim for target price lower than best ask
                if bid_improved and self.price < lob_best_bid_p:
                    if lob_best_ask_p != None:
                        target_price = target_down(lob_best_ask_p)

                    else:
                        target_price = lob['bids']['worst']  # stub quote
                    profit_alter(target_price)

        # remember the best LOB data ready for next response
        # TODO fix spot_system or d_a_institution to allow ZIP memory
        # LOb = limit order book (display ledger)... lob(bid) = standing bid...??? # TODO fix this
        self.prev_best_bid_p = lob_best_bid_p
        self.prev_best_bid_q = lob_best_bid_q
        self.prev_best_ask_p = lob_best_ask_p
        self.prev_best_ask_q = lob_best_ask_q

class Trader_AI(object):
    """ A class that makes a trader"""

    def __init__(self):
        self.name = ""
        self.type = ""
        self.values = []
        self.costs = []
        self.prd = prd.SpotMarketPrediction()
        self.prd.__init__()
        self.prd.get_data()
        self.prd.predict_market()
        self.market_bids = self.prd.give_trader_info('bid')
        self.market_asks = self.prd.give_trader_info('ask')
        self.current_period = 0
        self.current_number_bids = 0
        self.current_number_asks = 0
        self.standing_bid = None
        self.standing_ask = None

    def offer(self, contracts, standing_bid, standing_ask, period, number_bids, number_asks, pmax, pmin, round_num, total_rounds):
        self.current_period = period
        self.current_number_bids = number_bids  # will update with every offer
        self.current_number_asks = number_asks  # will update with every offer
        standing_ask = standing_ask
        standing_bid = standing_bid
        num_contracts = 0
        if self.type == "buyer":
            for contract in contracts:
                if contract[1] == self.name:  # second position is buyer_id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.values):
                return []  # You can't bid anymore
            cur_value = self.values[num_contracts]  # this is the current value working on
            if standing_bid:
                # for i in range(len(self.market_bids)):
                #     if standing_bid/self.market_bids[i] >= 0.95 and standing_bid/self.market_bids[i] < 1.00:
                #         if self.market_bids[i] <= cur_value:
                #             bid = self.market_bids[i]
                #             return ["B", self.name, bid]
                #         return []
                #
                #     elif standing_bid/self.market_bids[i] >= 0.90 and standing_bid/self.market_bids[i] < 1.00:
                #         if self.market_bids[i] <= cur_value:
                #             bid = self.market_bids[i]
                #             return ["B", self.name, bid]
                #         else:
                #             return []
                #
                #     else:
                #         pass
                # return []
                if standing_bid < self.market_bids[self.current_number_bids]:
                    if self.market_bids[self.current_number_bids] <= cur_value:
                                bid = self.market_bids[self.current_number_bids]
                                return ["B", self.name, bid]
                    else:
                        return []

                elif standing_bid == self.market_bids[self.current_number_bids]:
                    if self.market_bids[self.current_number_bids] + 1 <= cur_value:
                        bid = self.market_bids[self.current_number_bids] + 1
                        return ["B", self.name, bid]
                    else:
                        return []

                elif self.market_bids[self.current_number_bids] < standing_bid < self.market_bids[self.current_number_bids + 1]:
                    if self.market_bids[self.current_number_bids + 1] <= cur_value:
                        bid = self.market_bids[self.current_number_bids + 1]
                        return ["B", self.name, bid]
                    else:
                        return []

                else:
                    return []

            else:
                if self.market_bids[0] <= cur_value:
                    bid = self.market_bids[0]
                    return["B", self.name, bid]
                else:
                    return []

        else:
            for contract in contracts:
                if contract[2] == self.name:  # third position is seller id
                    num_contracts = num_contracts + 1
            if num_contracts >= len(self.costs):
                return [] # You can't ask anymore
            cur_cost = self.costs[num_contracts]
            if standing_ask:
                # for i in range(len(self.market_asks)):
                #     if self.market_asks[i]/standing_ask >= 0.95 and self.market_asks[i]/standing_ask < 1.0:
                #         if self.market_asks[i] >= cur_cost:
                #             ask = self.market_asks[i]
                #             return ["S", self.name, ask]
                #         else:
                #             return []
                #
                #     elif self.market_asks[i]/standing_ask >= 0.90 and self.market_asks[i]/standing_ask < 1.0:
                #         if self.market_asks[i] >= cur_cost:
                #             ask = self.market_asks[i]
                #             return ["S", self.name, ask]
                #         else:
                #             return []
                #
                #     else:
                #         pass
                # return []
                if standing_ask > self.market_asks[self.current_number_asks]:
                    if self.market_asks[self.current_number_asks] >= cur_cost:
                        ask = self.market_asks[self.current_number_asks]
                        return ["S", self.name, ask]
                    else:
                        return []

                elif standing_ask == self.market_asks[self.current_number_asks]:
                    if self.market_asks[self.current_number_asks] + 1 >= cur_cost:
                        ask = self.market_asks[self.current_number_asks] + 1
                        return ["S", self.name, ask]
                    else:
                        return []

                elif self.market_asks[self.current_number_asks + 1] < standing_ask < self.market_asks[self.current_number_asks]:
                    if self.market_asks[self.current_number_asks + 1] >= cur_cost:
                        ask = self.market_asks[self.current_number_asks + 1]
                        return ["S", self.name, ask]
                    else:
                        return []

                else:
                    return []

            else:
                if self.market_asks[0] >= cur_cost:
                    ask = self.market_asks[0]
                    return["S", self.name, ask]
                else:
                    return []


if __name__ == "__main__":
    zi = ZeroIntelligenceTrader()