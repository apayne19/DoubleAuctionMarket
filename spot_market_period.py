import spot_system as sys
import random

class SpotMarketPeriod(object):
    def __init__(self, session_name, num_periods):

        self.display = True
        self.session_name = session_name

        self.period = 0
        self.num_periods = num_periods
        self.num_buyers = 4  # number of buyers
        self.num_sellers = 4  # number of sellers
        self.limits = (999, 0)  # ceiling and floor for bidding
        self.num_market_periods = 100  # number of periods auction run
        self.trader_names = []
        self.traders = []
        self.trader_info = {}
        self.sys = sys.SpotSystem()

    def init_spot_system(self, name, limits, rounds, input_path, input_file):
        self.sys.init_spot_system(name, limits, rounds, input_path, input_file)

    def init_traders(self, trader_names):
        self.sys.init_traders(trader_names)

    def run(self):
        self.sys.run()

    def eval(self):
        return self.sys.eval()

    def run_period(self, period, header):
        self.period = period
        self.run()

    def save_period(self):
        # TODO:  Save period data file
        pass



if __name__ == "__main__":
    num_periods = 10
    limits = (999, 0)
    rounds = 100
    name = "trial"
    period = 1
    session_name = "session_test"
    header = session_name

    smp = SpotMarketPeriod(session_name, num_periods)

    # Put Trader Class Names Here - note traders strategy is named trader class name
    zi = "ZeroIntelligenceTrader"
    si = "SimpleTrader"
    trader_names = [zi, si, zi, si, zi, si, zi, si]  # Order of trader strategies in generic trader array
    # input - output and display options
    #input_path = "C:\\Users\\kevin\\Desktop\\spot_market_working\\projects\\"
    input_path = "C:\\Users\\Admin\\Desktop\\spot_market_working\\projects\\"
    input_file = "env_0616_4x4w3_sym"

    ouput_path = "C:\\Users\\Admin\\Desktop\\spot_market_working\\data\\"
    header = session_name

    smp.init_spot_system(name, limits, rounds, input_path, input_file)
    rnd_traders = trader_names    # because shuffle shuffels the list in place, returns none
    for k in range(num_periods):
        random.shuffle(rnd_traders)  #  reassign traders each period
        print(rnd_traders)
        smp.init_traders(rnd_traders)
        print("**** Running Period {}".format(k))
        smp.run_period(period, header)
        results = smp.eval()
        print(results)