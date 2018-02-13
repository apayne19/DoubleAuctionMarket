from trader import Trader_Shaver, Trader_ZIU, Trader_ZIC, Trader_Kaplan, Trader_PS, Trader_AA, Trader_GD, Trader_ZIP, Trader_AI
#import build_environment as env
import spot_environment_model as env
import double_auction_institution as ins
import tournament as trna  # imported but unused??
import trader as t  # imported but unused??
import random  # allows things to be generated randomly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import math

# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
class SpotSystem(object):
    def __init__(self):
        self.name = ""  # place holder for session name
        self.display = True  # calls function to display board
        self.limits = (0, 0)  # creates limits that can be changed
        self.num_market_rounds = 0  # sets number of market rounds to 0
        self.trader_names = []  # dictionary for trader names to be logged
        self.traders = []  # dictionary of trader strategies
        self.eff_list = []  # trader efficiency list
        self.t_list = []  # trader number list
        self.alphas = []  # holds smith's convergence alphas, proximities to equilibrium
        self.trade_ratio_list = []  # holds period trade ratios
        self.trader_info = {}  # dictionary of keys:values
        self.mkt = None  # function called from spot_environment_model
        self.da = None  # function called from double_auction_institution
        self.current_period = 0  # place holder for period number
        self.current_round = 0  # place holder for round number
        self.number_bids = 0  # running count of bid offers made previously
        self.number_asks = 0  # running count of asks offers made previously
        self.AA_earn = []
        self.GD_earn = []
        self.PS_earn = []  # these hold strategy total earns
        self.AI_earn = []
        self.ZIP_earn = []
        self.ZIC_earn = []
        self.SI_earn = []
        self.KP_earn = []
        self.ZIP_watch = []
        self.deal_status = None
        self.t = None
        self.d = None

    def init_spot_system(self, name, limits, rounds, input_path, input_file, output_path, session_name):
        self.name = name  # session name
        self.limits = limits  # price ceiling and floor
        self.num_market_rounds = rounds  # total number of rounds to run
        self.mkt = env.SpotEnvironmentModel()  # instantiate environment object
        self.da = ins.Auction('da', self.limits[0], self.limits[1])  # instantiate auction
        self.load_market(input_path, input_file, output_path, session_name)  # loads market file from gui inputs

    def init_spot_system_crash(self, name, limits, rounds, input_path, input_file_market_shock, output_path,
                               session_name):
        self.name = name
        self.limits = limits
        self.num_market_rounds = rounds
        self.mkt = env.SpotEnvironmentModel()  # instantiate environment object
        self.da = ins.Auction('da', self.limits[0], self.limits[1])  # instantiate auction
        self.load_market(input_path, input_file_market_shock, output_path, session_name)

    def init_traders(self, trader_names, period):
        self.current_period = period  # trading period
        self.trader_names = trader_names  # trader strategies
        self.trader_info = self.prepare_traders(self.trader_names, self.mkt, self.limits)  # instantiate traders

    def load_market(self, input_path, input_file, output_path, session_name):
        self.mkt.prepare_market(input_path, input_file, output_path, session_name)  # set and show market

    def run(self):
        self.run_system()  # starts market by calling method below

    def run_system(self):
        self.da.open_board("tournament official")
        num_contracts = 1  # shouldnt this be 0??
        if self.display:  # if display = true (if tournament still running)
            print()
            print("Auction Open")
        length_old_contracts = 0  # number of previous contracts
        temp_traders = self.traders  # trader ids
        for i in range(self.num_market_rounds):  # iterates through each round
            random.shuffle(temp_traders)  # generates random order of traders each round
            self.current_round = i
            # TODO add in market shocks here
            for trader in temp_traders:  # iterates through each trader

                self.number_bids = 0  # starting bid offers = 0
                self.number_asks = 0  # starting ask offers = 0
                self.trader_handler(trader)  # calls next function, executes trader's offer based on strategy

                print("Standing Bid, Standing Ask:" + str(self.da.report_standing()))  # prints bid,ask in real time
                contracts = self.da.report_contracts()  # list of contracts as they happen
                '''need to put ZIP respond() here'''
                if len(contracts) > length_old_contracts:  # if len(contracts)>0
                    length_old_contracts = len(contracts)  # update previous contracts
                    if self.display:  # if display still true (tournament still running)
                        '''need to put ZIP respond() here'''
                        self.deal_status = True
                        # TODO fix ZIP response to not be hard coded... need values and type
                        # print("DEAL")
                        # print("ZIP Before: " + str(self.ZIP_watch))
                        # self.ZIP_watch = Trader_ZIP().respond(self.t['t3'].values, self.t['t3'].type, contracts, self.deal_status, self.da.report_standing()[0],
                        #                                       self.da.report_standing()[1], self.ZIP_watch)
                        # print("ZIP After: " + str(self.ZIP_watch))
                        print("--> Contract #" + str(num_contracts), "|", "Round #" + str(self.current_round), "|",
                              contracts[len(contracts) - 1], "|", self.da.time_index())
                        print("#bids: " + str(self.number_bids))
                        print("#asks: " + str(self.number_asks))
                        # prints info for each trader
                        num_contracts = num_contracts + 1  # add 1 to contracts number
                else:
                    self.deal_status = False
                    # print("NO DEAL")
                    # print("ZIP Before: " + str(self.ZIP_watch))
                    # self.ZIP_watch = Trader_ZIP().respond(self.t['t3'].values, self.t['t3'].type, contracts, self.deal_status, self.da.report_standing()[0], self.da.report_standing()[1], self.ZIP_watch)
                    # #self.ZIP_watch = random.randint(0, 100)
                    # print("ZIP After: " + str(self.ZIP_watch))

        if self.display:
            print()

    def trader_handler(self, trader):
        last_period_prices = []
        for order in self.da.report_orders():  # iterates through orders
            last_period_prices.append(order[0])
            if order[2] == 'bid':
                self.number_bids = self.number_bids + 1  # if bid add 1 to bid count
            elif order[2] == 'ask':
                self.number_asks = self.number_asks + 1  # if ask add 1 to ask count
        try:
            last_period_min = min(last_period_prices)
        except ValueError:
            last_period_min = None
        try:
            last_period_max = max(last_period_prices)
        except ValueError:
            last_period_max = None
        '''below the trader generates an offer based on strategy function called in trader.py'''
        try:
            offer = trader.offer(self.da.report_contracts(), self.da.report_standing()[0], self.da.report_standing()[1],
                                 self.current_period, self.number_bids, self.number_asks, last_period_max, last_period_min,
                                 self.current_round, self.num_market_rounds, self.ZIP_watch[1])  # added periods, # bids, # asks
        except IndexError:
            offer = trader.offer(self.da.report_contracts(), self.da.report_standing()[0], self.da.report_standing()[1],
                                 self.current_period, self.number_bids, self.number_asks, last_period_max, last_period_min,
                                 self.current_round, self.num_market_rounds, self.ZIP_watch)  # added periods, # bids, # asks

        if len(offer) == 0:
            return  # if no offer then return nothing
        '''below the bid and ask functions are called from double_auction_institution...
        ... takes information from trader offer and submits bid or ask to market'''
        if offer[0] == "B":  # identifies the buyers and bids
            self.da.bid(offer[1], offer[2], self.trader_info, self.current_period, self.current_round)
        else:  # identifies the sellers and asks
            self.da.ask(offer[1], offer[2], self.trader_info, self.current_period, self.current_round)

    def eval(self):
        # calculate market efficiency
        result_header = [" ", " ", len(self.traders)]
        ep_low = self.trader_info['equilibrium'][1]  # equilibrium price low
        ep_high = self.trader_info['equilibrium'][2]  # equilibrium price high
        e_quantity = self.trader_info['equilibrium'][0]  # equilibrium quantity
        maximum_surplus = self.trader_info['equilibrium'][3]  # max surplus that can be obtained

        for trader in self.traders:
            trader_id = trader.name
            self.trader_info[trader_id]['units'] = 0  # sets units to 0 at every round
            self.trader_info[trader_id]['earn'] = 0  # sets earned to 0 at every round

            # calculate actual surplus and earnings

        actual_surplus = 0  # will change as updated
        count = 0
        act_p = []  # actual transactions

        if ep_low == ep_high:
            theor_p = ep_high
        else:
            theor_p = (ep_low + ep_high)/2  # if equilibrium high and low prices then take avg

        for contract in self.da.report_contracts():  # going through list of contracts
            count = count + 1  # counts contracts
            price = contract[0]  # pulls transaction price from board
            act_p.append(price)  # appends transaction price to global dictionary
            buyer_id = contract[1]  # pulls buyer id from board
            seller_id = contract[2]  # pulls seller id from board
            if self.trader_info[buyer_id]['type'] == 'B':  # if bidding
                value = self.trader_info[buyer_id]['values'][self.trader_info[buyer_id]['units']]  # max valuation
                self.trader_info[buyer_id]['earn'] += value - price  # profit
                self.trader_info[buyer_id]['units'] += 1  # trader's units gained
            else:
                print("error, buyer id = {}, buyer type = {}".format(buyer_id, self.trader_info[buyer_id]['type']))
            if self.trader_info[seller_id]['type'] == 'S':  # if selling
                cost = self.trader_info[seller_id]['costs'][self.trader_info[seller_id]['units']]  # lowest cost
                self.trader_info[seller_id]['earn'] += price - cost  # profit
                self.trader_info[seller_id]['units'] += 1  # trader's units sold
            else:
                print("error in contract {}, seller id = {}, seller type = {}".format(contract, seller_id,
                                                                                       self.trader_info[seller_id]['type']))
            # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
            actual_surplus += value - cost
        summation = []  # dictionary for holding the summation calculations for Smith's Alpha
        for i in act_p:  # iterate through transaction prices
            s_step = (i-theor_p)**2  # (transaction price - equilibrium price)squared
            summation.append(s_step)  # appends each calculation
        if len(act_p) != 0:
            smith_alpha = (math.sqrt(sum(summation)/len(act_p))/theor_p)*100
            '''the above calculation comes from Vernon Smith (1967)'''
        else:
            smith_alpha = 0  # TODO this needs to be changed to None etc.
        self.alphas.append(smith_alpha)  # appends each period's convergence alpha
        efficiency = int((actual_surplus / maximum_surplus) * 100)  # periods trading efficiency
        trade_ratio = count/e_quantity
        self.trade_ratio_list.append(trade_ratio)  # appends period's trade ratio
        result_header.extend([ep_low, ep_high, e_quantity, maximum_surplus, actual_surplus, efficiency])
        if self.display:
            # print("actP:" + str(act_p) + "length:" + str(len(act_p)) + "theorP:" + str(theor_p))
            # print("summations:" + str(summation))
            # print("Smith_alpha:" + str(smith_alpha))
            print("actual surplus = {}, maximum surplus = {}.".format(actual_surplus, maximum_surplus))
            print("market efficiency = {} percent.".format(efficiency))
            print("trade ratio = {}.".format(trade_ratio))
            # print("#bids: " + str(self.number_bids))
            # print("#asks: " + str(self.number_asks))

        for k in range(len(self.traders)):
            t_id = "t" + str(k)  # trader id
            t_strat = self.trader_info[t_id]['strat']  # trading strategy
            earn = self.trader_info[t_id]['earn']  # trader earnings
            if ep_high == ep_low:  # if high and low eqs the same
                t_eff = (earn/ep_high)*100  # trader's efficiency in %
            elif ep_high != ep_low:  # if eqs different
                avg_eq = (ep_high + ep_low)/2  # take avg of eqs
                t_eff = (earn/avg_eq)*100  # trader's efficiency in %
            else:
                t_eff = "error"
            if self.display:
                print("Trader {}, using strategy {}, earned {}, had efficiency {} %.".format(t_id, t_strat, earn, round(t_eff, 1)))
            result_header.extend([t_id, t_strat, earn])
            self.eff_list.append(round(t_eff, 1))  # appends trader's period efficiency and rounds
            self.t_list.append(k)  # appends trader number to list
        if self.display:
            print()

        for k in self.trader_info['strategies']:
            strat_earn = 0  # place holder for strategy earnings
            count = 0
            for l in range(len(self.traders)):
                t_id = "t" + str(l)
                if k == self.trader_info[t_id]['strat']:
                    count = count + 1  # count times strategy used
                    strat_earn += self.trader_info[t_id]['earn']
            if k == 'Trader_AA':
                self.AA_earn.append(strat_earn)  # these append trader earnings to their unique dicts
            elif k == 'Trader_GD':
                self.GD_earn.append(strat_earn)
            elif k == 'Trader_PS':
                self.PS_earn.append(strat_earn)
            elif k == 'Trader_AI':
                self.AI_earn.append(strat_earn)
            elif k == 'Trader_ZIP':
                self.ZIP_earn.append(strat_earn)
            elif k == 'Trader_ZIC':
                self.ZIC_earn.append(strat_earn)
            elif k == 'Trader_Shaver':
                self.SI_earn.append(strat_earn)
            elif k == 'Trader_Kaplan':
                self.KP_earn.append(strat_earn)
            else:
                print("Trader not listed!")  # lets the user know if trader dicts not updated
            if count > 0:
                avg_earn = int(strat_earn / count)  # calculates strategies avg earning
                result_header.extend([k, avg_earn])
            if self.display:
                # noinspection PyUnboundLocalVariable
                print("Strategy {} earned {} with a trader average of {}.".format(k, strat_earn, avg_earn))

        return result_header

    def prepare_traders(self, tn, mkt, limits):
        d = {}
        t = {}
        if len(tn) != mkt.num_buyers + mkt.num_sellers:
            print("tn = {} does not have the right length".format(tn))
        print("Buyers = {}, Sellers = {}, Total = {}".format(mkt.num_buyers, mkt.num_sellers, len(tn)))
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
        self.t = t
        self.d = d
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
    spot_system.run()
    results = spot_system.eval()
