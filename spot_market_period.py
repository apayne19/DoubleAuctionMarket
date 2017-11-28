import spot_system as sys
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os
import time
import math
'''This program is a condensed version of spot_system to build the periods of trading'''

'''1). import plotly
2). change input/ouput url paths to local computer'''

'''Problem with graphing multiple plotly graphs... trying to fix'''
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
        self.num_periods = num_periods
        self.num_buyers = 10  # number of buyers
        self.num_sellers = 10  # number of sellers
        self.limits = (999, 0)  # ceiling and floor for bidding
        self.num_market_periods = 100  # number of periods auction run
        self.trader_names = []
        self.traders = []
        self.trader_info = {}
        self.sys = sys.SpotSystem()  # calls SpotSystem() which prepares market and traders

    def init_spot_system(self, name, limits, rounds, input_path, input_file):
        self.sys.init_spot_system(name, limits, rounds, input_path, input_file)

    def init_traders(self, trader_names):
        self.sys.init_traders(trader_names)

    def run(self):
        self.sys.run()

    def eval(self):
        return self.sys.eval()  # runs eval method from spot_system

    '''Accessing contracts to obtain prices'''
    def get_contracts(self):
        self.prices = []  # temp dictionary for contract prices
        self.ends = []  # temp dictionary for end of period (end of contracts)
        for contract in self.sys.da.report_contracts():
            price = contract[0]  # pulls price from contracts
            self.prices.append(price)  # appends to temp dict
        try:
            avg = sum(self.prices)/len(self.prices)  # gets avg of all contract prices in period
        except ZeroDivisionError:  # if no contracts avg = 0
            avg = 0
        print("Transaction Avg: " + str(avg))
        avg_prices.append(avg)  # appends avg to global dict
        print("Transaction Avg List: " + str(avg_prices))
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
            if bool(self.endpoints) == False:
                self.endpoints.append(i)
            else:
                self.endpoints.append(i + self.endpoints[-1])

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

    '''Obtains Smith's Alpha of Convergence: shows converge level to eq price'''
    def get_alpha(self):
        eq_low = self.sys.trader_info['equilibrium'][1]
        eq_high = self.sys.trader_info['equilibrium'][2]
        if eq_low == eq_high:
            self.eq = eq_high
        elif eq_low != eq_high:
            self.eq = (eq_low + eq_high) / 2
        else:
            print("error")
        self.alpha = []
        for i in all_prices:
            p_i = i
            p_o = self.eq
            summation = (((p_i - p_o)**2)/len(all_prices))
            denom = math.sqrt(summation)
            sd = denom/p_o
            self.alpha.append(sd)
        return sum(self.alpha)

    '''Obtains Avg trade ratio for all periods: actual transactions/equilibrium quantity'''
    def get_avg_trade_ratio(self):
        trade_ratio_list = self.sys.trade_ratio_list
        trade_ratio_avg = sum(trade_ratio_list)/len(trade_ratio_list)
        print("Avg. Trade Ratio:" + str(trade_ratio_avg))

    '''Obtains Time, Trader, Ask/Bid, Offer Amt for table graph'''
    def get_table(self):
        self.table = []  # created to make info enter table plot as columns
        self.table.append(['Time', 'Trader', 'Bid/Ask', 'Offer'])
        for i in self.sys.da.report_orders():
            self.table.append(np.array(i))

    '''Graphs a table in plotly of Time, Trader, Ask/Bid, Offer Amt for all periods'''
    def graph_table(self):
        table_data = self.table  # calls data from table dictionary
        # Initialize a figure with ff.create_table(table_data)
        figure = ff.create_table(table_data)  # creates a table using plotly
        py.offline.plot(figure)  # plots into web browser

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

    def run_period(self, period, header):
        self.period = period
        self.run()

    def save_period(self, results):
        pass

'''This program iterates through the number of rounds'''
if __name__ == "__main__":
    num_periods = 6
    limits = (999, 0)
    rounds = 50
    name = "trial"
    period = 0
    session_name = "session_test"
    header = session_name
    smp = SpotMarketPeriod(session_name, num_periods)
    '''This will change when we create more programmed agents to add into the model'''
    # Put Trader Class Names Here - note traders strategy is named trader class name
    zic = "ZI_Ctrader"  # zero intelligence constrained
    #zip = "ZeroIntelligenceTraderPlus"
    ziu = "ZI_Utrader"  # zero intelligence unconstrained
    kp = "KaplanTrader"  # sniping strategy
    si = "SimpleTrader"
    # trader_names = [zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic]
    trader_names = [zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic, zic]
    # input - output and display options
    input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"
    input_file = "Das Data v3"  # data file plugged in SF = santa fe VS = vernon smith
    output_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\data\\"
    header = session_name
    smp.init_spot_system(name, limits, rounds, input_path, input_file)
    rnd_traders = trader_names    # because shuffle shuffles the list in place, returns none
    n = 0  # used in file creation
    file_check = os.path.isfile('./Experiment' + str(n) + '.csv')  # checks directory for existing file
    # TODO check for existing file before creating new one
    # TODO fix so that saves period/experiment data for each run
    output_file = open('Experiment' + str(n) + '.csv', 'w', newline='')  # creates a new file
    for k in range(num_periods):
        smp.get_contracts()  # gets transaction prices and period endpoints
        periods_list.append(k)
        random.shuffle(rnd_traders)  # reassign traders each period
        # print(rnd_traders)  # prints list of trader strategy
        smp.init_traders(rnd_traders)
        print("**** Running Period {}".format(k))
        smp.run_period(period, header)
        results = smp.eval()
        eff.append(results[8])  # appends the efficiencies per period
        act_surplus.append(results[7])  # appends actual surplus per period
        maxi_surplus.append(results[6])  # appends maximum surplus per period
        output_writer = csv.writer(output_file)  # prepares new csv file for writing
        output_writer.writerow(results)  # writes period info to csv row per period
        smp.get_table()  # see function doc_string
    output_file.close()  # closes the csv file
    print("Market Efficiencies:" + str(eff))  # print market efficiencies
    print("Avg. Efficiency:" + str(sum(eff)/num_periods))  # print avg efficiency
    print("Total Avg. Transaction Price:" + str(sum(avg_prices[1:])/(num_periods - 1)))
    print("Smith's Convergence Alpha:" + str(smp.get_alpha()))  # print smiths alpha
    print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
    print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
    smp.get_avg_trade_ratio()  # prints avg trade ratio for all periods
    smp.graph_trader_eff()  # plots individual efficiency
    time.sleep(0.5)  # program waits half second
    smp.graph_efficiency()  # plots period efficiency
    time.sleep(0.5)  # wait
    smp.get_endpoints()  # obtains endpoints of periods for graph
    smp.graph_contracts()  # graphs contract transactions and avg transaction per period
    time.sleep(0.5)  # wait
    smp.graph_surplus()  # graphs actual and max surplus
    time.sleep(0.5)  # wait
    smp.graph_table()  # graphs a table of Time, Trader, Bid/Ask, Offer