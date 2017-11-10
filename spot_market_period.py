import spot_system as sys
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os
'''This program is a condensed version of spot_system to build the periods of trading'''

'''There could be a problem in counting traders... when running this program shows 10 traders 
when the input file only has 8'''
all_prices = []
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
        self.num_buyers = 8  # number of buyers
        self.num_sellers = 5  # number of sellers
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

    '''Graphs avg and max surpluses by period'''
    def graph_surplus(self):
        trace3 = go.Scatter(
            x=np.array(periods_list),
            y=np.array(act_surplus), name='Actual Surplus')
        trace4 = go.Scatter(
            x=np.array(periods_list),
            y=np.array(maxi_surplus), name='Max Surplus')
        data2 = [trace3, trace4]
        layout2 = go.Layout(title='Market Surpluses by Period',
                            xaxis=dict(title='Periods',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                            yaxis=dict(title='Surplus (units)',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig2 = go.Figure(data=data2, layout=layout2)
        py.offline.plot(fig2)

    '''Graphs market efficiencies by period'''
    def graph_efficiency(self):
        trace5 = go.Scatter(
            x=np.array(periods_list),
            y=np.array(eff), name='Efficiency')
        data3 = [trace5]
        layout3 = go.Layout(title='Market Efficiencies by Period',
                            xaxis=dict(title='Periods',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                            yaxis=dict(title='Efficiency (%)',
                                       titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig3 = go.Figure(data=data3, layout=layout3)

        py.offline.plot(fig3)

    '''Graphs the contracts from all periods'''
    def graph_contracts(self):
        # graph all transactions per period
        trace1 = go.Scatter(
            x=np.array(range(len(all_prices))),
            y=np.array(all_prices), name='All Transactions')
        # graph avg transaction per period
        trace2 = go.Scatter(
            x=np.array(self.endpoints),
            y=np.array(avg_prices), name='Avg Transaction'
        )
        data1 = [trace1, trace2]
        shapes = list()
        # graph period cutoff lines
        for i in self.endpoints:
            shapes.append({'type': 'line',
                           'xref': 'x',
                           'yref': 'paper',
                           'x0': i,
                           'y0': 0,
                           'x1': i,
                           'y1': 20})

        layout1 = go.Layout(shapes=shapes, title='Market Contracts by Period',
                           xaxis=dict(title='Contract #',
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')),
                           yaxis=dict(title='Prices ($)',
                                      titlefont=dict(family='Courier New, monospace', size=18, color='#7f7f7f')))
        fig1 = go.Figure(data=data1, layout=layout1)

        py.offline.plot(fig1)

    def get_table(self):
        '''Graph tables of Time, Trader, Ask/Bid, Offer Amt in real time per period'''
        self.table = []  # created to make info enter table plot as columns
        for i in self.sys.da.report_orders():
            self.table.append(np.array(i))

    def graph_table(self):
        table_data = self.table  # calls data from table dictionary
        # Initialize a figure with ff.create_table(table_data)
        figure = ff.create_table(table_data)  # creates a table using plotly
        py.offline.plot(figure)  # plots into web browser

        '''Will use in spot_environment_gui'''
        # with plt.style.context('seaborn-dark-palette'):
        #     xv = np.array(range(len(all_prices)))
        #     yv = np.array(all_prices)
        #     plt.scatter(xv, yv, marker='s')
        #     plt.title("Contracts per Period")
        #     plt.xlabel("Contract #")
        #     plt.ylabel("Price ($)")
        #     plt.grid(True)
        #     plt.show()

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
    period = 1
    session_name = "session_test"
    header = session_name

    smp = SpotMarketPeriod(session_name, num_periods)

    '''This will change when we create more programmed agents to add into the model'''

    # Put Trader Class Names Here - note traders strategy is named trader class name
    zi = "ZeroIntelligenceTrader"
    #zip = "ZeroIntelligenceTraderPlus"
    win = "HaveToWin"
    kp = "KaplanTrader"
    si = "SimpleTrader"

    '''Vernon Smith data traders'''
    #trader_names = [zi, zi, zi, zi, zi, zi]  # Order of trader strategies in generic trader array
    #trader_names = [zi, zi, zi, zi, zi, kp]
    #trader_names = [kp, zi, kp, zi, kp, zi]
    #trader_names = [kp, si, si, si, si, si]
    trader_names = [kp, zi, zi, zi, zi, zi]

    '''Santa Fe data traders'''
    #trader_names = [zi, zi, zi, zi, zi, zi, zi, zi]  # Order of trader strategies in generic trader array
    #trader_names = [kp, zi, zi, zi, zi, zi, zi, zi]
    #trader_names = [kp, zi, kp, zi, kp, zi, kp, zi]
    #trader_names = [kp, si, si, si, si, si, si, si]

    # input - output and display options
    input_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"
    input_file = "TestVS"
    output_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\data\\"
    header = session_name
    smp.init_spot_system(name, limits, rounds, input_path, input_file)
    rnd_traders = trader_names    # because shuffle shuffels the list in place, returns none
    n = 0  # used in file creation
    file_check = os.path.isfile('./Experiment' + str(n) + '.csv')  # checks directory for existing file
    # TODO check for existing file before creating new one
    output_file = open('Experiment' + str(n) + '.csv', 'w', newline='')  # creates a new file
    for k in range(num_periods):
        smp.get_contracts()
        periods_list.append(k)
        #random.shuffle(rnd_traders)  # reassign traders each period
        print(rnd_traders)
        smp.init_traders(rnd_traders)
        print("**** Running Period {}".format(k))
        smp.run_period(period, header)
        results = smp.eval()
        eff.append(results[8])  # appends the efficiencies per period
        act_surplus.append(results[7])  # appends actual surplus per period
        maxi_surplus.append(results[6])  # appends maximum surplus per period
        output_writer = csv.writer(output_file)  # prepares new csv file for writing
        output_writer.writerow(results)  # writes period info to csv row per period
        print(results)
        #smp.get_table()  # builds table of bids/asks etc
    output_file.close()  # closes the csv file
    print("Market Efficiencies:" + str(eff))  # print market efficiencies
    print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
    print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
    #smp.graph_table()  # graphs table in plotly
    '''Plot surpluses using matplotlib'''
    with plt.style.context('seaborn-dark-palette'):  # added a plot of the market efficiencies
        x = np.array(periods_list)
        y1 = np.array(act_surplus)
        y2 = np.array(maxi_surplus)
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.title("Market Surpluses")
        plt.xlabel("Period")
        plt.ylabel("Surplus")
        plt.grid(True)
        plt.show()
        pass  # trying to make the graph a background task
    '''Plot efficiencies using matplotlib'''
    with plt.style.context('seaborn-dark-palette'):
        x = np.array(periods_list)
        y = np.array(eff)
        plt.plot(x, y, marker='s')
        plt.title("Market Efficiencies")
        plt.xlabel("Period")
        plt.ylabel("Efficiency (%)")
        plt.grid(True)
        plt.show()
        pass  # trying to make the graph a background task

    #smp.graph_surplus()  # graphs surplus
    #smp.graph_efficiency()  # uses plot
    smp.get_endpoints()  # obtains endpoints of periods for graph
    smp.graph_contracts()  # graphs contracts per period



    # TODO create graphs of average earnings per period