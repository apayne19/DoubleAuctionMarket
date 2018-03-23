from Institution import spot_system as sys
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from timeit import default_timer as timer
import scipy.stats as stats

'''Input_path, input_file, output_path, and session_name need to be set before running this program...

... input_path pulls data file containing supply/demand, equilibrium price/quantity, etc.
    --> will need to create data file by running spot_environment_gui.py and saving
    
... input_file is the data set you are experimenting with

... output_path is the path location that session data folders will be saved to

... session_name is the unique identifier for each session run
    --> ex. "filename-tradestrategy-#buyers-#sellers-$limit-version" '''

input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMarket\\Data\\projects\\"
input_file = "TestVS"
output_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMarket\\Data\\period data\\"
session_name = "Market Test 17"
input_file_market_shock = "MarketShockTest"
'''Below are global dictionaries that will contain information needed to execute several functions'''
all_prices = []
theoretical_transactions = []
all_ends = []
avg_prices = []
endpoints = []
eff = []
periods_list = []
act_surplus = []
maxi_surplus = []



class SpotMarketPeriod(object):

    def __init__(self, session_name, num_periods, limits):  # creates name and number of periods for market
        self.display = True
        self.session_name = session_name
        self.period = 0

        # self.period_number = None
        self.num_periods = num_periods
        self.num_buyers = 0  # number of buyers
        self.num_sellers = 0  # number of sellers
        self.limits = limits  # ceiling and floor for bidding
        self.num_market_periods = num_periods  # number of periods auction run
        self.trader_names = []
        self.traders = []
        self.trader_info = {}  # dictionary of all trader info
        self.sys = sys.SpotSystem()  # calls SpotSystem() which prepares market and traders

    def init_spot_system(self, name, limits, rounds, input_path, input_file, output_path, session_name):
        self.sys.init_spot_system(name, limits, rounds, input_path, input_file, output_path, session_name)
        # initializes spot system and passes key market information

    # added for gui
    def init_spot_system_gui(self, name, limits, rounds, input_path, input_file, output_path, session_name):
        self.sys.init_spot_system_gui(name, limits, rounds, input_path, input_file, output_path, session_name)

    def init_shock(self, name, limits, rounds, input_path, input_file_market_shock, output_path, session_name):
        self.sys.init_shock(name, limits, rounds, input_path, input_file_market_shock, output_path, session_name)

    def init_traders(self, traders, period_k):
        self.sys.init_traders(traders, period_k)
        # initializes trader building in spot system, passes strategies and period number

    def run(self):
        self.sys.run()  # runs spot system run_period() --> starts double auction

    def eval(self):
        return self.sys.eval()  # runs eval method from spot_system returns results

    '''Accessing contracts to obtain prices'''
    def get_contracts(self):
        self.prices = []  # temp dictionary for contract prices
        self.ends = []  # temp dictionary for end of period (end of contracts)
        # print(self.sys.da.report_contracts())
        for contract in self.sys.da.report_contracts():
            price = contract[0]  # pulls price from contracts
            self.prices.append(price)  # appends to temp dict
        try:
            avg = sum(self.prices)/len(self.prices)  # gets avg of all contract prices in period
        except ZeroDivisionError:  # if no contracts avg = 0
            avg = 0
        print("Transaction Avg: " + str(avg))  # print to editor
        avg_prices.append(avg)  # appends avg to global dict
        print("Transaction Avg List: " + str(avg_prices))  # print to editor
        end = len(self.prices)  # finds end of contracts for period
        self.ends.append(end)  # appends end int to temp dict
        for p in self.prices:
            all_prices.append(p)  # appends all prices in temp dict to global dict
        for e in self.ends:
            all_ends.append(e)  # appends all ends in temp dict to global dict

    '''Obtains end of period for plot'''
    def get_endpoints(self):
        self.endpoints = []  # dictionary of period ends, will be used in plotting
        for i in all_ends:
            if bool(self.endpoints) == False:  # if list is empty
                self.endpoints.append(i)  # starts list
            else:
                self.endpoints.append(i + self.endpoints[-1])  # appends to end of list

    '''Graphs avg and max surpluses by period.. use matplotlib until plot error fixed...
    ... generates same graph as period efficiency'''
    # def graph_surplus(self):
    #     trace1 = go.Scatter(
    #         x=np.array(periods_list),
    #         y=np.array(act_surplus), name='Actual Surplus')
    #     trace2 = go.Scatter(
    #         x=np.array(periods_list),
    #         y=np.array(maxi_surplus), name='Max Surplus')
    #     data = [trace1, trace2]
    #     layout = go.Layout(title='Market Surpluses by Period',
    #                         xaxis=dict(title='Periods',
    #                                    titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
    #                         yaxis=dict(title='Surplus (units)',
    #                                    titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
    #     fig = go.Figure(data=data, layout=layout)
    #     py.offline.plot(fig)

    '''Graphs market efficiencies by period.. use matplotlib until plot error fixed'''
    def graph_efficiency(self, output, session):
        with plt.style.context('seaborn'):
            x = periods_list  # list of period numbers
            y = eff  # list of period efficiency calculations
            plt.plot(x, y, marker='o', markersize=4, color='mediumslateblue')
            plt.grid(True)  # creates a grid in the graph
            plt.xlabel("Period")  # x-axis = items
            plt.ylabel("Efficiency (%)")  # y-axis = U(x) = utility
            plt.title("Simulation Market Efficiencies by Period")
            plt.savefig(output + session + "\\" + "Period Efficiencies.png")
            # plt.show()
            plt.close()

    def graph_efficiency_gui(self, output, session, eff_gui, periods_list_gui):
        with plt.style.context('seaborn'):
            x = periods_list_gui  # list of period numbers
            y = eff_gui  # list of period efficiency calculations
            plt.plot(x, y, marker='o', markersize=4, color='mediumslateblue')
            plt.grid(True)  # creates a grid in the graph
            plt.xlabel("Period")  # x-axis = items
            plt.ylabel("Efficiency (%)")  # y-axis = U(x) = utility
            plt.title("Simulation Market Efficiencies by Period")
            plt.savefig(output + session + "\\" + "Period Efficiencies.png")
            # plt.show()
            plt.close()

    '''Graphs the contracts from all periods'''
    def graph_contracts(self, output, session):
        with plt.style.context('seaborn'):
            eq_low = self.sys.trader_info['equilibrium'][1]
            eq_high = self.sys.trader_info['equilibrium'][2]
            if eq_low == eq_high:
                self.eq = eq_high
            elif eq_low != eq_high:
                self.eq = (eq_low + eq_high)/2
            else:
                print("error")

            x_1 = range(len(all_prices))
            y_1 = all_prices
            plt.plot(x_1, y_1, marker='o', markersize=5, color='royalblue', label='Contract Price')
            x_2 = self.endpoints
            y_2 = avg_prices
            x_2_adjust = []
            for i in x_2:
                x_2_adjust.append(i+.30)
            plt.plot(x_2_adjust, y_2, marker='o', markersize=5, color='deepskyblue', label='Avg. Price')
            eq_line = []
            for i in x_1:
                eq_line.append(self.eq)
            plt.plot(x_1, eq_line, linewidth=2, linestyle='--', color='darkslategray', label='Eq. Price')
            for i in self.endpoints:
                plt.axvline(x=i+.30, linewidth=2, linestyle=':', color='dimgrey')
            plt.grid(True)  # creates a grid in the graph
            plt.legend(bbox_to_anchor=(0.90, 0.98))  # places a legend on the plot
            plt.xlabel("Contract Number")  # x-axis = items
            plt.ylabel("Transaction Price")  # y-axis = U(x) = utility
            plt.title("Simulation Market Contract Prices")
            plt.savefig(output + session + "\\" + "Transactions.png")
            # plt.show()
            plt.close()


    def graph_alphas(self, output, session, periods):
        with plt.style.context('seaborn'):
            alphas = self.sys.alphas
            x = periods
            y = alphas
            plt.plot(x, y, marker='o', markersize=4, color='mediumorchid')
            plt.grid(True)  # creates a grid in the graph
            plt.xlabel("Period")  # x-axis = items
            plt.ylabel("Smith's Alpha")  # y-axis = U(x) = utility
            plt.title("Simulation Market Equilibrium Convergence")
            plt.savefig(output + session + "\\" + "Convergence Alphas.png")
            #plt.show()
            plt.close()

    '''Obtains Avg trade ratio for all periods: actual transactions/equilibrium quantity'''
    def get_avg_trade_ratio(self):
        trade_ratio_list = self.sys.trade_ratio_list  # list of trade ratios
        trade_ratio_avg = sum(trade_ratio_list)/len(trade_ratio_list)  # average trade ratio
        print("Avg. Trade Ratio:" + str(trade_ratio_avg))  # print to editor

    '''Obtains Time, Trader, Ask/Bid, Offer Amt for experiment run, writes to csv file'''
    def record_session_data(self, session_folder):  # session_folder is new output path
        with open(session_folder + "Market_History.csv", "w") as file_1:  # creates csv file
            output_1 = csv.writer(file_1)
            output_1.writerow(['Time', 'Trader', 'Unit', 'Max', 'Earns', 'Bid/Ask', 'Offer', 'Strategy', 'Period',
                               'Round'])  # header
            file_1.close()
        with open(session_folder + "Market_History.csv", "a") as file_1:  # creates csv file
            output_1 = csv.writer(file_1)
            orders = self.sys.da.report_orders()
            contracts = self.sys.da.report_contracts()
            for o in orders:
                for c in contracts:
                    if o[0] == c[3] or o[0] == c[3] - 0.00001 or o[0] == c[3] + 0.00001:  # TODO can it be +-?
                        orders[orders.index(o)].append("Contract:" + str(c))
                    else:
                        pass
            print(orders)
            print(contracts)
            output_1.writerows(orders)  # saves bid/ask history in excel csv
            file_1.close()  # closes file

    '''Graph individual trader efficiencies'''
    def graph_trader_eff(self, output, session):
        with plt.style.context('seaborn'):
            t_i_eff = self.sys.eff_list
            t_i = self.sys.t_list
            x = t_i
            y = t_i_eff
            plt.scatter(x, y, color='mediumseagreen')
            plt.grid(True)  # creates a grid in the graph
            plt.xlabel("Trader Number")  # x-axis = items
            plt.ylabel("Efficiency (%)")  # y-axis = U(x) = utility
            plt.title("Simulation Efficiencies by Trader")
            plt.savefig(output + session + "\\" + "Trader Efficiencies.png")
            #plt.show()
            plt.close()

    def graph_distribution(self, output, session):
        with plt.style.context('seaborn'):
            t_effs = sorted(self.sys.eff_list)  # list of trader efficiencies
            plt.subplot(2, 1, 1)
            mean = np.mean(t_effs)  # numpy function to get average
            std_dev = np.std(t_effs)  # numpy function to get standard deviation
            median = np.median(t_effs)  # numpy function to get median
            max = np.max(t_effs)  # numpy function to get maximum value
            min = np.min(t_effs)  # numpy function to get minimum value
            fit = stats.norm.pdf(t_effs, mean, std_dev)
            plt.plot(t_effs, fit, '-o', linewidth=2, color='coral')
            plt.annotate("n_samples = " + str(len(t_effs)), xy=(0, 0.0075))
            plt.annotate("out of market: " + str(t_effs.count(0)), xy=(0, 0.0050))
            plt.axvline(x=mean, linewidth=2, linestyle='--', color='darkslategray', label='µ')
            plt.axvline(x=mean + std_dev, linewidth=2, linestyle=':', color='dimgrey', label='µ + σ')
            plt.axvline(x=mean + (std_dev * 2), linewidth=2, linestyle=':', color='dimgrey', label='µ + 2σ')
            plt.xlabel('Trader Efficiency (%)')
            plt.title('Simulation Market Trader Efficiency Distribution')
            plt.legend(bbox_to_anchor=(0.85, 0.98))  # places a legend on the plot
            plt.subplot(2, 1, 2)
            print(t_effs)
            for i in range(t_effs.count(0)):
                t_effs.remove(0)
            print(t_effs)
            mean2 = np.mean(t_effs)  # numpy function to get average
            std_dev2 = np.std(t_effs)  # numpy function to get standard deviation
            median2 = np.median(t_effs)  # numpy function to get median
            max2 = np.max(t_effs)  # numpy function to get maximum value
            min2 = np.min(t_effs)  # numpy function to get minimum value
            fit2 = stats.norm.pdf(t_effs, mean2, std_dev2)
            plt.plot(t_effs, fit2, '-o', linewidth=2, color='coral')
            plt.annotate("n_samples = " + str(len(t_effs)), xy=(0, 0.0075))
            plt.annotate("out of market: " + str(t_effs.count(0)), xy=(0, 0.0050))
            plt.axvline(x=mean2 - std_dev2, linewidth=2, linestyle=':', color='dimgrey', label='µ - σ')
            plt.axvline(x=mean2, linewidth=2, linestyle='--', color='darkslategray', label='µ')
            plt.axvline(x=mean2 + std_dev2, linewidth=2, linestyle=':', color='dimgrey', label='µ + σ')
            plt.axvline(x=mean2 + (std_dev2 * 2), linewidth=2, linestyle=':', color='dimgrey', label='µ + 2σ')
            plt.xlabel('Trader Efficiency (%)')
            plt.title('Traders Out of Market Removed')
            plt.legend(bbox_to_anchor=(0.85, 0.98))  # places a legend on the plot
            plt.savefig(output + session + "\\" + "Efficiency Distribution.png")
            #plt.show()
        '''Print statements below '''
        print()
        print("All Trader Efficiencies")
        print("Trader Efficiency Mean:" + str(mean))
        print("Trader Efficiency Std. Deviation:" + str(std_dev))
        print("Trader Efficiency Median:" + str(median))
        print("Trader Efficiency Max:" + str(max))
        print("Trader Efficiency Min:" + str(min))
        print("---------------------------------------------------")
        print("Out of Market Traders Removed")
        print("Trader Efficiency Mean:" + str(mean2))
        print("Trader Efficiency Std. Deviation:" + str(std_dev2))
        print("Trader Efficiency Median:" + str(median2))
        print("Trader Efficiency Max:" + str(max2))
        print("Trader Efficiency Min:" + str(min2))
        print()

    def trader_eff_gui(self):
        return sorted(self.sys.eff_list)



    def run_period(self, period, header):
        self.period = period
        self.run()

    def save_period(self, results):
        pass

    def total_avg_earns(self, trader, total_count):  # ADDED: function to call total avg earns from spot system
        # TODO way to condense into one line?
        if total_count == 0:
            return "NONE"
        else:
            if trader == 'AA':
                return sum(self.sys.AA_earn)/total_count
            elif trader == 'GD':
                return sum(self.sys.GD_earn)/total_count
            elif trader == 'PS':
                return sum(self.sys.PS_earn)/total_count
            elif trader == 'AI':
                return sum(self.sys.AI_earn)/total_count
            elif trader == 'ZIP':
                return sum(self.sys.ZIP_earn)/total_count
            elif trader == 'ZIC':
                return sum(self.sys.ZIC_earn)/total_count
            elif trader == 'KP':
                return sum(self.sys.KP_earn)/total_count
            elif trader == 'SI':
                return sum(self.sys.SI_earn)/total_count
            else:
                return "Trader not listed!"

    def total_earns(self, trader):  # ADDED: function to call total avg earns from spot system
        # TODO way to condense into one line?
        if trader == 'AA':
            return self.sys.AA_earn
        elif trader == 'GD':
            return self.sys.GD_earn
        elif trader == 'PS':
            return self.sys.PS_earn
        elif trader == 'AI':
            return self.sys.AI_earn
        elif trader == 'ZIP':
            return self.sys.ZIP_earn
        elif trader == 'ZIC':
            return self.sys.ZIC_earn
        elif trader == 'KP':
            return self.sys.KP_earn
        elif trader == 'SI':
            return self.sys.SI_earn
        else:
            return "Trader not listed!"





'''This program iterates through the number of rounds'''
if __name__ == "__main__":
    num_periods = 6  # periods or trading days
    limits = (400, 0)  # price ceiling, price floor
    rounds = 25  # rounds in each period (can substitute time clock)

    name = "trial"
    period = 1  # ...??
    '''The code below creates a file for your session name for market run info to be dumped into...
    ... will raise file error if session name not changed --> prevents overwriting previous runs'''
    try:
        os.makedirs(output_path + session_name)  # creates folder for session data
    except FileExistsError:
        print("ERROR: File Exists... must rename or delete previous session data")
        raise  # raises error if folder already exists
    header = session_name
    smp = SpotMarketPeriod(session_name, num_periods, limits)
    '''Below trader classes are abbreviated'''
    zic = "Trader_ZIC"  # zero intelligence constrained
    ziu = "Trader_ZIU"  # zero intelligence unconstrained trader.. not used
    kp = "Trader_Kaplan"  # sniping trader based on Santa Fe paper
    si = "Trader_Shaver"  # simple trader.. not used
    ps = "Trader_PS"  # PS trader based on Priest and Tol paper
    aa = "Trader_AA"  # aggressiveness trader based on Cliff and Vytelingum paper
    gd = "Trader_GD"  # GD trader based on Gjerstadt and Dickhaut paper
    zip = "Trader_ZIP"  # zero intelligence plus trader
    ai = "Trader_AI"
    '''The lists below establish the number and order of traders and trading strategy'''
    trader_names = [aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa]
    header = session_name
    smp.init_spot_system(name, limits, rounds, input_path, input_file, output_path, session_name)
    rnd_traders = trader_names    # because shuffle shuffles the list in place, returns none
    times = []
    for k in range(num_periods):  # iterates through number of periods or "trading days"
        if k == 3:  # if round = 3 then shock or change traders
            # TODO trader shocks happen below
            # rnd_traders.append(zic)
            # rnd_traders.append(gd)
            # smp.num_buyers = 12
            # smp.num_sellers = 12
            # print(rnd_traders)
            # TODO period shocks happen below
            #smp.init_shock(name, limits, rounds, input_path, input_file_market_shock, output_path, session_name)
            pass

        else:
            pass
        timer_start = timer()
        periods_list.append(k)
        # random.shuffle(rnd_traders)  # shuffles trader order per period
        # print(rnd_traders)  # prints list of trader strategy
        smp.init_traders(rnd_traders, k)
        print("**** Running Period {}".format(k))  # provides visual effect in editor
        smp.run_period(period, header)
        timer_stop = timer()
        results = smp.eval()
        '''the below data is appended into global dictionaries'''
        eff.append(results[8])  # appends the efficiencies per period
        act_surplus.append(results[7])  # appends actual surplus per period
        maxi_surplus.append(results[6])  # appends maximum surplus per period
        smp.get_contracts()  # gets transaction prices and period endpoints
        session_folder = output_path + session_name + "\\"  # establishes file path for session data folder
        smp.record_session_data(session_folder)  # records session data in excel csv
        time = timer_start - timer_stop
        times.append(time)

    print("Period Times: " + str(times))
    print("Market Efficiencies:" + str(eff))  # print market efficiencies
    print("Avg. Efficiency:" + str(sum(eff)/num_periods))  # print avg efficiency
    #print("Total Avg. Transaction Price:" + str(sum(avg_prices[1:])/(num_periods - 1)))
    print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
    print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
    print()
    # TODO trader info below can be funtionalized further
    print("Strategy Total Earnings")
    print("Trader_AA: " + str(smp.total_earns('AA')))
    #print("Trader_AI: " + str(smp.total_earns('AI')))
    print("Trader_GD: " + str(smp.total_earns('GD')))  #
    print("Trader_PS: " + str(smp.total_earns('PS')))  # ADDED: section to list total avg earns
    # print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
    print("Trader_ZIP: " + str(smp.total_earns('ZIP')))  #
    print("Trader_ZIC: " + str(smp.total_earns('ZIC')))  #
    print("Trader_Kaplan: " + str(smp.total_earns('KP')))
    print("Trader_Shaver: " + str(smp.total_earns('SI')))
    print()
    print("Strategy Total Avg. Earnings (per trader)")
    print("Trader_AA: " + str(smp.total_avg_earns('AA', trader_names.count(aa)*num_periods)))   #
    print("Trader_GD: " + str(smp.total_avg_earns('GD', trader_names.count(gd)*num_periods)))   #
    print("Trader_PS: " + str(smp.total_avg_earns('PS', trader_names.count(ps)*num_periods)))   # ADDED: section to list total avg earns
    #print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
    print("Trader_ZIP: " + str(smp.total_avg_earns('ZIP', trader_names.count(zip)*num_periods))) #
    print("Trader_ZIC: " + str(smp.total_avg_earns('ZIC', trader_names.count(zic)*num_periods))) #
    print("Trader_Kaplan: " + str(smp.total_avg_earns('KP', trader_names.count(kp)*num_periods)))
    print("Trader_Shaver: " + str(smp.total_avg_earns('SI', trader_names.count(si)*num_periods)))
    smp.get_avg_trade_ratio()  # prints avg trade ratio for all periods
    smp.graph_trader_eff(output_path, session_name)  # plots individual efficiency
    smp.graph_efficiency(output_path, session_name)  # plots period efficiency
    smp.get_endpoints()  # obtains endpoints of periods for graph
    smp.graph_contracts(output_path, session_name)  # graphs contract transactions and avg transaction per period
    # smp.graph_surplus()  # graphs actual and max surplus
    smp.graph_alphas(output_path, session_name, periods_list)  # graphs Smith's Alpha of convergence
    smp.graph_distribution(output_path, session_name)  # graphs normal distribution of trader efficiencies