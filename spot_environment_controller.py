import spot_environment_model

"""This is basically the control center. All actions here are being condensed and brought in from
 spot_market_model...... the BRAIN of the simulator"""

class SpotEnvironmentController():
    def __init__(self, debug=False):  # debug builds an error trap
        self.debug = debug
        if self.debug == True:
            print("... In Controller -> __init__")
        self.sem = spot_environment_model.SpotEnvironmentModel(self.debug)

    def load_file(self, path):
        self.sem.load_file(path)  # loads file by pulling from file path

    def save_project(self, path):
        self.sem.save_file(path)

    def reset_market(self):
        pass
        self.sem.reset_market()

    def make_market(self, make_d):
        if self.debug == True:
            print("... In Controller -> make_market")
        self.sem.make_market(make_d)

    def set_market_parms(self, parms):
        if self.debug == True:
            print("... In Controller -> set_market_params")
        self.sem.set_market_parms(parms)

    def add_buyer(self, bn, values):
        if self.debug == True:
            print("... In Controller -> add_buyer")
            print ("... Buyer {}, values {}".format(bn, values))

        self.sem.add_buyer(bn, values)

    def add_seller(self, sn, costs):
        if self.debug == True:
            print("... In Controller -> add_seller")
            print ("... Seller {}, costs {}".format(sn, costs))
        self.sem.add_seller(sn, costs)

    def get_num_buyers(self):
        return self.sem.get_num_buyers()

    def get_num_sellers(self):
        return self.sem.get_num_sellers()

    def get_num_units(self):
        return self.sem.get_num_units()

    def get_seller_costs(self, seller):
        return self.sem.get_seller_costs(seller)

    def get_buyer_values(self, buyer):
        return self.sem.get_buyer_values(buyer)

    def make_demand(self):
        self.sem.make_demand()

    def make_supply(self):
        self.sem.make_supply()

    def show_env_buyers(self):
        self.sem.show_env_buyers()

    def show_environment(self):
        self.sem.show_environment()

    def get_supply_demand_plot_info(self):
        return self.sem.get_supply_demand_plot_info()

    def get_supply_demand_list(self):
        return self.sem.get_supply_demand_list()

    def get_equilibrium(self):
        return self.sem.get_equilibrium()

    def show(self):
        self.sem.show()

    def plot(self):
        self.sem.make_demand()
        self.sem.make_supply()
        self.sem.plot_supply_demand()

    def plot_gui(self, name):
        self.sem.make_demand()
        self.sem.make_supply()
        self.sem.plot_supply_demand_gui(name)