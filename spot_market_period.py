import spot_system as sys
import AI_Testing as prd
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os
import time
import trader as tdr
import math

'''Input_path, input_file, output_path, and session_name need to be set before running this program...

... input_path pulls data file containing supply/demand, equilibrium price/quantity, etc.
    --> will need to create data file by running spot_environment_gui.py and saving
    
... input_file is the data set you are experimenting with

... output_path is the path location that session data folders will be saved to

... session_name is the unique identifier for each session run
    --> ex. "filename-tradestrategy-#buyers-#sellers-$limit-version" '''

input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"
input_file = "TestVS"
output_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\period data\\"
session_name = "AI_trader Run 1"

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

    def __init__(self, session_name, num_periods):  # creates name and number of periods for market
        self.display = True
        self.session_name = session_name
        self.period = 0

        # self.period_number = None
        self.num_periods = num_periods
        self.num_buyers = 11  # number of buyers
        self.num_sellers = 11  # number of sellers
        self.limits = (400, 0)  # ceiling and floor for bidding
        self.num_market_periods = 5  # number of periods auction run
        self.trader_names = []
        self.traders = []
        self.trader_info = {}
        self.sys = sys.SpotSystem()  # calls SpotSystem() which prepares market and traders
        self.prd = prd.SpotMarketPrediction()

    def init_spot_system(self, name, limits, rounds, input_path, input_file):
        self.sys.init_spot_system(name, limits, rounds, input_path, input_file)

    def init_traders(self, trader_names, period_k):
        print(trader_names)
        print(period_k)
        self.sys.init_traders(trader_names, period_k)

    def run(self):
        self.sys.run()

    def eval(self):
        return self.sys.eval()  # runs eval method from spot_system

    '''Accessing contracts to obtain prices'''
    def get_contracts(self):
        self.prices = []  # temp dictionary for contract prices
        self.ends = []  # temp dictionary for end of period (end of contracts)
        print(self.sys.da.report_contracts())
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
        self.endpoints = []
        for i in all_ends:
            if bool(self.endpoints) == False:  # if list is empty
                self.endpoints.append(i)  # starts list
            else:
                self.endpoints.append(i + self.endpoints[-1])  # appends to end of list

    '''Graphs avg and max surpluses by period.. use matplotlib until plot error fixed'''
    def graph_surplus(self):
        trace1 = go.Scatter(
            x=np.array(periods_list),
            y=np.array(act_surplus), name='Actual Surplus')
        trace2 = go.Scatter(
            x=np.array(periods_list),
            y=np.array(maxi_surplus), name='Max Surplus')
        data = [trace1, trace2]
        layout = go.Layout(title='Market Surpluses by Period',
                            xaxis=dict(title='Periods',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                            yaxis=dict(title='Surplus (units)',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    '''Graphs market efficiencies by period.. use matplotlib until plot error fixed'''
    def graph_efficiency(self):
        trace = go.Scatter(
            x=np.array(periods_list),
            y=np.array(eff), name='Efficiency',
            mode='lines+markers',
            line=dict(color='rgb(131, 90, 241)', width=4),
            marker=dict(size=10, color='rgb(143, 19, 131)')
        )
        data = [trace]
        layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
                           paper_bgcolor='rgb(255,255,255)',
                           title='Market Efficiency by Period',
                           xaxis=dict(title='Period #',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                           yaxis=dict(title='Efficiency (%)',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    '''Graphs the contracts from all periods'''
    def graph_contracts(self):
        eq_low = self.sys.trader_info['equilibrium'][1]
        eq_high = self.sys.trader_info['equilibrium'][2]
        if eq_low == eq_high:
            self.eq = eq_high
        elif eq_low != eq_high:
            self.eq = (eq_low + eq_high)/2
        else:
            print("error")
        # graph all transactions per period
        trace1 = go.Scatter(
            x=np.array(range(len(all_prices))),
            y=np.array(all_prices), name='All Transactions',
            mode='lines+markers',
            line=dict(color='rgba(152, 0, 0, .8)', width=4),
            marker=dict(size=10, color='rgba(152, 0, 0, .8)'))
        # graph avg transaction per period
        trace2 = go.Scatter(
            x=np.array(self.endpoints),
            y=np.array(avg_prices), name='Avg Transaction',
            mode='lines+markers',
            line=dict(color='rgba(200, 150, 150, .9)', width=4),
            marker=dict(size=10, color='rgba(200, 150, 150, .9)'))
        data = [trace1, trace2]
        shapes = list()
        # graph period cutoff lines
        for i in self.endpoints:
            # create period lines
            shapes.append({'type': 'line',
                           'xref': 'x',
                           'yref': 'grid',
                           'x0': i - .10,
                           'y0': 0,
                           'x1': i - .10,
                           'y1': max(all_prices)})
        # create equilibrium line
        shapes.append({'type': 'line',
                       'line': {'color': 'rgb(0,176,246)', 'width': 5, 'dash': 'dot'},
                           'xref': 'grid',
                           'yref': 'y',
                           'x0': 0,
                           'y0': self.eq,
                           'x1': max(self.endpoints),
                           'y1': self.eq})
        layout = go.Layout(shapes=shapes,
                            plot_bgcolor='rgb(229,229,229)',
                           paper_bgcolor='rgb(255,255,255)',
                           title='Market Transactions by Period',
                           xaxis=dict(title='Contract #',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                           yaxis=dict(title='Price ($)',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    def graph_alphas(self):
        alphas = self.sys.alphas
        trace = go.Scatter(
            x=np.array(periods_list),
            y=np.array(alphas), name='Convergence Alpha',
            mode='lines+markers',
            line=dict(color='rgb(131, 90, 241)', width=4),
            marker=dict(size=10, color='rgb(143, 19, 131)')
        )
        data = [trace]
        layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
                           paper_bgcolor='rgb(255,255,255)',
                           title='Smith Alphas by Period',
                           xaxis=dict(title='Period #',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                           yaxis=dict(title='Convergence Alpha',
                                      gridcolor='rgb(255,255,255)',
                                      showgrid=True,
                                      showline=False,
                                      showticklabels=True,
                                      tickcolor='rgb(127,127,127)',
                                      ticks='outside',
                                      zeroline=False,
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    '''Obtains Avg trade ratio for all periods: actual transactions/equilibrium quantity'''
    def get_avg_trade_ratio(self):
        trade_ratio_list = self.sys.trade_ratio_list  # list of trade ratios
        trade_ratio_avg = sum(trade_ratio_list)/len(trade_ratio_list)  # average trade ratio
        print("Avg. Trade Ratio:" + str(trade_ratio_avg))  # print to editor

    '''Obtains Time, Trader, Ask/Bid, Offer Amt for experiment run, writes to csv file'''
    def record_session_data(self, session_folder, period):  # session_folder is new output path
        with open(session_folder + "Bid_Ask_History.csv", "a") as file_1:  # creates csv file
            output_1 = csv.writer(file_1)
            #output_1.writerow(['Time', 'Trader', 'Bid/Ask', 'Offer'])  # header
            output_1.writerows(self.sys.da.report_orders())  # saves bid/ask history in excel csv
            file_1.close()  # closes file
        with open(session_folder + "Contract_History.csv", "a") as file_2:  # creates csv file
            output_2 = csv.writer(file_2)
            #output_2.writerow(['Price', 'Buyer', 'Seller', "Prd. " + str(period)])  # header
            output_2.writerows(self.sys.da.report_contracts())  # saves contracts in excel csv
            file_2.close()  # closes file

    '''Graph individual trader efficiencies'''
    def graph_trader_eff(self):
        t_i_eff = self.sys.eff_list
        t_i = self.sys.t_list
        trace = go.Scatter(
            x=np.array(t_i),
            y=np.array(t_i_eff),
            mode='markers',
            marker=dict(
                size=10,
                color='rgb(0,176,246)',
                line=dict(width=2,)))
        data = [trace]
        layout = go.Layout(plot_bgcolor='rgb(229,229,229)',
                           paper_bgcolor='rgb(255,255,255)',
                           title='Individual Efficiency by Trader',
                            xaxis=dict(title='Trader #',
                                       gridcolor='rgb(255,255,255)',
                                       showgrid=True,
                                       showline=False,
                                       showticklabels=True,
                                       tickcolor='rgb(127,127,127)',
                                       ticks='outside',
                                       zeroline=False,
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                            yaxis=dict(title='Efficiency (%)',
                                       gridcolor='rgb(255,255,255)',
                                       showgrid=True,
                                       showline=False,
                                       showticklabels=True,
                                       tickcolor='rgb(127,127,127)',
                                       ticks='outside',
                                       zeroline=False,
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    # TODO create normal distribution graph of trader efficiencies
    def graph_distribution(self):
        t_effs = self.sys.eff_list  # list of trader efficiencies
        mean = np.mean(t_effs)  # numpy function to get average
        std_dev = np.std(t_effs)  # numpy function to get standard deviation
        median = np.median(t_effs)  # numpy function to get median
        max = np.max(t_effs)  # numpy function to get maximum value
        min = np.min(t_effs)  # numpy function to get minimum value
        '''Print statements below '''
        print("Trader Efficiency Mean:" + str(mean))
        print("Trader Efficiency Std. Deviation:" + str(std_dev))
        print("Trader Efficiency Median:" + str(median))
        print("Trader Efficiency Max:" + str(max))
        print("Trader Efficiency Min:" + str(min))
        y = t_effs
        '''Graph boxplot of trader efficiency'''
        trace = go.Box(
            y=y,
            name='Trader Efficiency',
            boxpoints='all',
            jitter=0.3,
            marker=dict(
                color='rgb(214,12,140)',
            ),
        )
        layout = go.Layout(
            width=1000,
            yaxis=dict(
                title='Trader Efficiency Boxplot',
                zeroline=False
            ),
        )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        py.offline.plot(fig)

    def run_period(self, period, header):
        self.period = period
        self.run()

    def save_period(self, results):
        pass

    def total_avg_earns(self, trader):  # ADDED: function to call total avg earns from spot system
        if trader == 'AA':
            return sum(self.sys.AA_earn)/len(self.sys.AA_earn)
        elif trader == 'GD':
            return sum(self.sys.GD_earn)/len(self.sys.GD_earn)
        elif trader == 'PS':
            return sum(self.sys.PS_earn)/len(self.sys.PS_earn)
        elif trader == 'AI':
            return sum(self.sys.AI_earn)/len(self.sys.AI_earn)
        elif trader == 'ZIP':
            return sum(self.sys.ZIP_earn)/len(self.sys.ZIP_earn)
        elif trader == 'ZIC':
            return sum(self.sys.ZIC_earn)/len(self.sys.ZIC_earn)
        else:
            return "Trader not listed!"





'''This program iterates through the number of rounds'''
if __name__ == "__main__":
    num_periods = 5  # periods or trading days
    limits = (400, 0)  # price ceiling, price floor
    rounds = 20  # rounds in each period (can substitute time clock)
    name = "trial"
    period = 0  # ...??
    try:
        os.makedirs(output_path + session_name)  # creates folder for session data
    except FileExistsError:
        print("ERROR: File Exists... must rename or delete previous session data")
        raise  # raises error if folder already exists
    header = session_name
    smp = SpotMarketPeriod(session_name, num_periods)
    '''Below trader classes are abbreviated'''
    zic = "Trader_ZIC"  # zero intelligence constrained
    ziu = "Trader_ZIU"  # zero intelligence unconstrained trader.. not used
    kp = "Trader_Kaplan"  # sniping trader based on Santa Fe paper
    si = "Trader_Simple"  # simple trader.. not used
    ps = "Trader_PS"  # PS trader based on Priest and Tol paper
    aa = "Trader_AA"  # aggressiveness trader based on Cliff and Vytelingum paper
    gd = "Trader_GD"  # GD trader based on Gjerstadt and Dickhaut paper
    zip = "Trader_ZIP"  # zero intelligence plus trader
    ai = "Trader_AI"
    '''The lists below establish the number and order of traders and trading strategy'''
    # TODO create way to automate input of trader # and strategies
    # trader_names = [zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip, zip]
    # trader_names = [gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd, gd]
    trader_names = [aa, aa, aa, aa, zip, zip, zip, zip, gd, gd, gd, gd, ps, ps, ps, ps, zic, zic, zic, zic, aa, ai]
    # trader_names = [ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps, ps]
    # trader_names = [zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic]
    header = session_name
    smp.init_spot_system(name, limits, rounds, input_path, input_file)
    rnd_traders = trader_names    # because shuffle shuffles the list in place, returns none
    #smp.get_predictions()
    for k in range(num_periods):  # iterates through number of periods or "trading days"

        periods_list.append(k)
        random.shuffle(rnd_traders)  # shuffles trader order per round
        # print(rnd_traders)  # prints list of trader strategy
        smp.init_traders(rnd_traders, k)
        print("**** Running Period {}".format(k))  # provides visual effect in editor
        smp.run_period(period, header)
        results = smp.eval()
        '''the below data is appended into global dictionaries'''
        eff.append(results[8])  # appends the efficiencies per period
        act_surplus.append(results[7])  # appends actual surplus per period
        maxi_surplus.append(results[6])  # appends maximum surplus per period
        smp.get_contracts()  # gets transaction prices and period endpoints
        session_folder = output_path + session_name + "\\"  # establishes file path for session data folder
        smp.record_session_data(session_folder, k)  # records session data in excel csv

    print("Market Efficiencies:" + str(eff))  # print market efficiencies
    print("Avg. Efficiency:" + str(sum(eff)/num_periods))  # print avg efficiency
    print("Total Avg. Transaction Price:" + str(sum(avg_prices[1:])/(num_periods - 1)))
    print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
    print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
    print()
    print("Strategy Total Avg. Earnings")
    print("Trader_AA: " + str(smp.total_avg_earns('AA')))   #
    print("Trader_GD: " + str(smp.total_avg_earns('GD')))   #
    print("Trader_PS: " + str(smp.total_avg_earns('PS')))   # ADDED: section to list total avg earns
    print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
    print("Trader_ZIP: " + str(smp.total_avg_earns('ZIP'))) #
    print("Trader_ZIC: " + str(smp.total_avg_earns('ZIC'))) #
    '''time.sleep() is called several times below to allow data aggregation in graphing functions...
    ... if not used, graphing functions have inheritance issues'''
    smp.get_avg_trade_ratio()  # prints avg trade ratio for all periods
    time.sleep(0.75)  # program waits 0.75 seconds before continuing
    smp.graph_trader_eff()  # plots individual efficiency
    time.sleep(0.75)
    smp.graph_efficiency()  # plots period efficiency
    time.sleep(0.75)
    smp.get_endpoints()  # obtains endpoints of periods for graph
    time.sleep(0.75)
    smp.graph_contracts()  # graphs contract transactions and avg transaction per period
    time.sleep(0.75)
    smp.graph_surplus()  # graphs actual and max surplus
    time.sleep(0.75)
    smp.graph_alphas()  # graphs Smith's Alpha of convergence
    time.sleep(0.75)
    smp.graph_distribution()  # graphs normal distribution of trader efficiencies
    '''graphs will open in browser of your choosing...
    ... can download images of graphs by clicking camera icon in browser
    ... or can create a free online plotly account which allows you to save and edit graphs'''