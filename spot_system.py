from trader import SimpleTrader, ZeroIntelligenceTrader, UnconstrainedZITrader
#import build_environment as env
import spot_environment_model as env
import double_auction_institution as ins
import tournament as trna  # imported but unused??
import trader as t  # imported but unused??
import random  # allows things to be generated randomly

class SpotSystem(object):
    def __init__(self):
        self.name = ""
        self.display = True  # calls function to display board
        self.limits = (0, 0)  # creates limits that can be changed
        self.num_market_rounds = 0  # sets number of market rounds to 0
        self.trader_names = []  # dictionary for trader names to be logged
        self.traders = []  # dictionary of trader ids?
        self.trader_info = {}  # dictionary of keys:values
        self.mkt = None  # function called from spot_environment_model
        self.da = None  # function called from double_auction_institution

    def init_spot_system(self, name, limits, rounds, input_path, input_file):
        self.name = name
        self.limits = limits
        self.num_market_rounds = rounds
        self.mkt = env.SpotEnvironmentModel()  # instantiate environment object
        self.da = ins.Auction('da', self.limits[0], self.limits[1]) # instantiate auction
        self.load_market(input_path, input_file)  # loads market file from gui inputs

    def init_traders(self, trader_names):
        self.trader_names = trader_names
        self.trader_info = self.prepare_traders(self.trader_names, self.mkt, self.limits)  # instantiate traders

    def load_market(self, input_path, input_file):
        self.mkt.prepare_market(input_path, input_file)  # set and show market

    def run(self):
        self.run_system()  # starts market by calling method below

    def run_system(self):
        self.da.open_board("tournament official")
        num_contracts = 1
        if self.display:  # if display = true
            print()
            print("Auction Open")
            print(self.da.report_standing(), self.da.report_contracts())
        length_old_contracts = 0
        temp_traders = self.traders
        for i in range(self.num_market_rounds):
            random.shuffle(temp_traders)  # generates random order of traders each round
            for trader in temp_traders:
                self.trader_handler(trader)
                contracts = self.da.report_contracts()  # list of contracts as they happen
                if len(contracts) > length_old_contracts:  # if len(contracts)>0
                    length_old_contracts = len(contracts)
                    if self.display:  # if display still true
                        print(num_contracts, i, contracts[len(contracts) - 1])  # prints info for each trader
                        num_contracts = num_contracts + 1
        if self.display:
            print()

    def trader_handler(self, trader):
        offer = trader.offer(self.da.report_contracts(), self.da.report_standing()[0],self.da.report_standing()[1])
        if len(offer) == 0:
            return
        if offer[0] == "B":  # identifies the bidders and bids
            self.da.bid(offer[1], offer[2])
        else:
            self.da.ask(offer[1], offer[2])  # else identified as sellers and asks

    def eval(self):
        # calculate market efficiency
        result_header = [" ", " ", len(self.traders)]
        ep_low = self.trader_info['equilibrium'][0]
        ep_high = self.trader_info['equilibrium'][1]
        e_quantity = self.trader_info['equilibrium'][2]
        maximum_surplus = self.trader_info['equilibrium'][3]

        for trader in self.traders:
            trader_id = trader.name
            self.trader_info[trader_id]['units'] = 0  # sets units to 0 at every round
            self.trader_info[trader_id]['earn'] = 0  # sets earned to 0 at every round

            # calculate actual surplus and earnings

        actual_surplus = 0  # will change as updated
        for contract in self.da.report_contracts():  # going through list of contracts

            price = contract[0]  # pulls price from board
            buyer_id = contract[1]  # pulls buyer id from board
            seller_id = contract[2]  # pulls seller id from board
            if self.trader_info[buyer_id]['type'] == 'B':  # type is bid?
                value = self.trader_info[buyer_id]['values'][self.trader_info[buyer_id]['units']]
                '''the line above is indexing values and units from trader_info?'''
                self.trader_info[buyer_id]['earn'] += value - price
                self.trader_info[buyer_id]['units'] += 1
            else:
                print("error, buyer id = {}, buyer type = {}".format(buyer_id, self.trader_info[buyer_id]['type']))
            if self.trader_info[seller_id]['type'] == 'S':
                cost = self.trader_info[seller_id]['costs'][self.trader_info[seller_id]['units']]
                self.trader_info[seller_id]['earn'] += price - cost
                self.trader_info[seller_id]['units'] += 1
            else:
                print("error in contract {}, seller id = {}, seller type = {}".format(contract, seller_id,
                                                                                       self.trader_info[seller_id]['type']))
            actual_surplus += value - cost

        efficiency = int((actual_surplus / maximum_surplus) * 100)

        result_header.extend([ep_low, ep_high, e_quantity, maximum_surplus, actual_surplus, efficiency])
        if self.display:
            print("actual surplus = {}, maximum surplus = {}.".format(actual_surplus, maximum_surplus))
            print("market efficiency = {} percent.".format(efficiency))

        for k in range(len(self.traders)):
            t_id = "t" + str(k)
            t_strat = self.trader_info[t_id]['strat']
            earn = self.trader_info[t_id]['earn']
            if self.display:
                print("Trader {}, using strategy {}, earned {}.".format(t_id, t_strat, earn))
            result_header.extend([t_id, t_strat, earn])
        if self.display:
            print()

        for k in self.trader_info['strategies']:
            strat_earn = 0
            count = 0
            for l in range(len(self.traders)):
                t_id = "t" + str(l)
                if k == self.trader_info[t_id]['strat']:
                    count = count + 1
                    strat_earn += self.trader_info[t_id]['earn']
            if count > 0:
                avg_earn = int(strat_earn / count)
                result_header.extend([k, avg_earn])
            if self.display:
                print("Strategy {} earned an average of {}.".format(k, avg_earn))

        return result_header


    def prepare_traders(self, tn, mkt, limits):
        d = {}
        t = {}
        if len(tn) != mkt.num_buyers + mkt.num_sellers:
            print ("tn = {} does not have the right length".format(tn))
        print ("Number = {}, {}, {}".format(mkt.num_buyers, mkt.num_sellers, len(tn)))
        for k in range(mkt.num_buyers + mkt.num_sellers):
            t_id = "t" + str(k)  # make trader id
            t[t_id] = globals()[tn[k]]()  # create object
            t[t_id].name = t_id  # set objects name
            d[t_id] = {}
            d[t_id]['units'] = 0  # keep track of units used
            d[t_id]['earn'] = 0  # keep track of earnings
            d[t_id]['strat'] = tn[k]  # traders strategy

            if k < mkt.num_buyers:
                t[t_id].type = "buyer"  # set objects type
                t[t_id].values = mkt.get_buyer_values(k)  # set objects values
                d[t_id]['type'] = "B"  # traders type
                d[t_id]['values'] = mkt.get_buyer_values(k)  # trader's values
            else:  # note seller index is trader_index - num_buyers
                t[t_id].type = "seller"  # set objects type
                t[t_id].costs = mkt.get_seller_costs(k - mkt.num_buyers)  # set objects values
                d[t_id]['type'] = "S"  # traders type
                d[t_id]['costs'] = mkt.get_seller_costs(k - mkt.num_buyers)  # trader's values

        d["strategies"] = [k for k in set(tn)]
        # get market efficiency
        eqv = mkt.get_equilibrium()  # (Price low, Price High Quantity, Maximum Surplus)
        ep_low = eqv[0]
        ep_high = eqv[1]
        e_quantity = eqv[2]
        maximum_surplus = eqv[3]
        d["equilibrium"] = (ep_low, ep_high, e_quantity, maximum_surplus)
        traders = [t[t_id] for t_id in t.keys()]
        self.traders = [t[t_id] for t_id in t.keys()]
        return d


if __name__ == "__main__":
    # Put Trader Class Names Here - note traders strategy is named trader class name
    #zi = "ZeroIntelligenceTrader"
    zi = "UnconstrainedZITrader"
    si = "SimpleTrader"
    trader_names = [zi, si, zi, si, zi, si, zi, si]  # Order of trader strategies in generic trader array
    # trader_names = [zi, zi, zi, zi, zi, zi, zi, zi, zi, zi]  # Order of trader strategies in generic trader array
    # input - output and display options
    input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"
    input_file = "TEST"

    name = "Trial"
    limits = (999, 0)
    rounds = 100

    spot_system = SpotSystem()
    spot_system.init_spot_system(name, limits, rounds, input_path, input_file)
    spot_system.init_traders(trader_names)
    print(spot_system.trader_info)
    spot_system.run()
    results = spot_system.eval()
    print(results)
