import operator  # https://docs.python.org/2/library/operator.html
import matplotlib.pyplot as plt  # matplotlib #graphing
import numpy as np  # import numpy
import time  # time functions
import random  # random number generator
import csv  # reads csv files from excel

"""This class is where all the information is brought into and where the output information is
sent back.... the HEART of the simulator"""

class SpotEnvironmentModel(object):
    """ A class that makes a market"""

    def __init__(self, debug=False):
        self.env = {"demand": [], "dem": [], "supply": [], "sup": [],
                    "buyers": {}, "sellers": {}, "eq": {}}
        self.name = ""
        self.num_buyers = 0
        self.num_sellers = 0
        self.num_units = 0  # num_units is the number of units
        self.debug = debug
        if debug:
            print("...... In Model -> __init__")

        # This should never run for now
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)  # buyer_id = 'buyer0', 'buyer1', etc.
            self.env["buyers"][buyer_id] = []   # env['buyers'] is a dictionary
            # env['buyers'][buyer_id] is a list of values

        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)  # seller_id = 'seller0', 'seller1', etc.
            self.env["sellers"][seller_id] = []  # env['sellers'] is a dictionary
            #  env['sellers'][seller_id] is a list of costs

    def reset_market(self):  # clears all values and dictionaries
        self.name = ""  # resets market name
        self.num_buyers = 0  # resets number of buyers
        self.num_sellers = 0  # resets number of sellers
        self.num_units = 0  # resets number of units
        self.env["demand"] = []  # resets list of demand values
        self.env["dem"] = []  # resets list of ????
        self.env["supply"] = []  # resets list of supply values
        self.env["sup"] = []  # resets list of ????
        self.env["buyers"] = {}  # resets list of buyers
        self.env["sellers"] = {}  # resets list of sellers
        self.env["eq"] = {}  # resets list of equilibrium values
        if self.debug:
            print("...... In Model -> reset_market")
            self.show_environment()

    def make_market(self, make_d):

        if self.debug:  # Creates a log
            print ("...... In Model --> set_market_parms")
            print("...... params = {}".format([self.name, self.num_buyers, self.num_sellers, self.num_units]))

        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            self.env["buyers"][buyer_id] = make_d["buyers"][buyer]

        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            self.env["sellers"][seller_id] = make_d["sellers"][seller]

    def set_market_parms(self, parms):
        """Initialize Environment"""
        if self.debug:  # Creates a log
            print("...... In Model --> set_market_params --> begin")
        # test to make sure params will not kill model
        test_flag = False  # arms the error trap
        if parms[0] == "":  # if project name is blank
            test_flag = True  # triggers project name trap
        if parms[1] <= 0:  # if buyers <= 0
            test_flag = True  # triggers buyer trap
        if parms[2] <= 0:  # if sellers <= 0
            test_flag = True  # triggers seller trap
        if parms[3] <= 0:  # if units <= 0
            test_flag = True  # triggers unit trap
        if test_flag == True:  # error trap if any above = false then passes test
            if self.debug:  # Creates a log
                print("...... In Model --> set_market_params --> early exit on params warning")
            print("WARNING: Project parameters not set")
            self.name = "Untitled"  # name of environment
            self.num_buyers = 0  # number of buyers
            self.num_sellers = 0  # number of sellers
            self.num_units = 0  # number of units
            return

        self.name = parms[0]         # name of environment
        self.num_buyers = parms[1]   # number of buyers
        self.num_sellers = parms[2]  # number of sellers
        self.num_units = parms[3]    # number of units

        # Initialize buyers and sellers dictionaries

        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            self.env["buyers"][buyer_id] = []  # env['buyers'] is a dictionary
            # env['buyers'][buyer_id] is a list of values
            # buyer_id = 'buyer0', 'buyer1', etc.

        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            self.env["sellers"][seller_id] = []  # env['sellers'] is a dictionary
            # env['sellers'][seller_id] is a list of costs
            # seller_id = 'seller0', 'seller1', etc.

        if self.debug:  # Creates a log
            self.show_environment()
            print("...,... In Model --> set_market_parms --> end")

        return

    def show_environment(self):  # displays all data to user

        print("...... In Model -> show_environment")
        print("......... name = {}".format(self.name))  # printing dictionary with values
        print("......... num_buyers = {}".format(self.num_buyers))
        print("......... num_sellers = {}".format(self.num_sellers))
        print("......... num_units = {}\n".format(self.num_units))

        print("......... demand = {}".format(self.env["demand"]))
        print("......... dem = {}".format(self.env["dem"]))
        print("......... supply = {}".format(self.env["supply"]))
        print("......... sup = {}\n".format(self.env["sup"]))

        for k in range(self.num_buyers):
            id = "buyer" + str(k)
            print("............ buyer {} values {}".format(k, self.env["buyers"][id]))
        for k in range(self.num_sellers):
            id = "seller" + str(k)
            print("............ seller {} costs {}".format(k, self.env["sellers"][id]))

        print("\n")

    def get_num_buyers(self):
        return self.num_buyers

    def get_num_sellers(self):
        return self.num_sellers

    def get_num_units(self):
        return len(self.get_seller_costs(0))

    def show(self):
        """Prints basic information about environment --> used in stand alone mode without gui."""
        print("I am environment {} with {} buyers and {} sellers.".format(self.name,
                                                                          self.num_buyers,
                                                                          self.num_sellers))
        print("")

    def show_participants(self):
        """ Prints buyers/values and sellers/costs --> used in stand alone mode without gui."""
        print("Market Participants")
        print("-------------------")
        print("BUYERS")
        print("------")
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            print("buyer {} values {}".format(buyer_id, self.env["buyers"][buyer_id]))
        print("SELLERS")
        print("-------")
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            print("seller {} costs {}".format(seller_id, self.env["sellers"][seller_id]))
        print("")

    def add_buyer(self, buyer_number, values):
        """Add buyer and buyer values to environment"""
        if self.debug:
            print("...... In Model -> add_buyer -> on entry")
            print("...... Buyer {} Values {}".format(buyer_number, values))

        if buyer_number >= self.num_buyers:
            return
        if len(values) != self.num_units:
            return

        buyer_id = "buyer" + str(buyer_number)
        self.env["buyers"][buyer_id] = values

        if self.debug:
            print("...... In Model -> add_buyer -> upon good exit")
            print("...... buyer_id = {} env/buyers/buyer_id = {}"
                  .format(buyer_id, self.env["buyers"][buyer_id]))
            self.show_env_buyers()
            print("\n")

    def get_buyer_values(self, buyer_number):
        if buyer_number > self.num_buyers - 1:
            return [-1]
        else:
            return self.env["buyers"]["buyer" + str(buyer_number)]

    def add_seller(self, seller_number, costs):
        if self.debug:
            print("...,... In Model -> add_seller")
            print("...,... Seller {} Costs {}".format(seller_number, costs))
            self.show_env_buyers()

        if seller_number >= self.num_sellers:
            return
        if len(costs) != self.num_units:
            return

        seller_id = "seller" + str(seller_number)
        self.env["sellers"][seller_id] = costs

        if self.debug:
            print("...... In Model -> add_seller -> upon good exit")
            print("...... seller_id = {} env/sellers/costs = {}"
                  .format(seller_id, self.env["sellers"][seller_id]))
            self.show_env_buyers()
            print("\n")

    def get_seller_costs(self, seller_number):
        if seller_number > self.num_sellers - 1:
            return [-1]
        else:
            return self.env["sellers"]["seller" + str(seller_number)]

    def show_env_buyers(self):
        if self.debug:
            print("...... In Model -> show_env_buyers")
            print('...... env[buyers] = {}'.format(self.env["buyers"]))

    def make_demand(self):

        if self.debug:
            print("...... In Model ->  make_demand -> starting")
            print('......... env[buyers] = {}'.format(self.env["buyers"]))

        dem = []
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            for value in self.env["buyers"][buyer_id]:
                dem.append((buyer_id, value))
        sdem = sorted(dem, key=operator.itemgetter(1), reverse=True)
        self.env["demand"] = sdem
        if self.debug:
            print("...... In Model -> make_demand -> ending")
            print('......... dem = {}'.format(dem))
            print("......... sdem = {}".format(sdem))

    def make_supply(self):

        if self.debug:
            print("...... In Model ->  make_supply -> starting")
            print('......... env[sellers] = {}'.format(self.env["sellers"]))

        sup = []
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            for cost in self.env["sellers"][seller_id]:
                sup.append((seller_id, cost))
        ssup = sorted(sup, key=operator.itemgetter(1))
        self.env["supply"] = ssup
        if self.debug:
            print("...... In Model -> make_supply -> ending")
            print('......... sup = {}'.format(sup))
            print("......... ssup = {}".format(ssup))

    def get_supply_demand_list(self):

        if self.debug:
            print("...... In Model -> get_supply_demand_list -> beginning")

        dem = self.env["demand"]
        sup = self.env["supply"]
        dem_list = sorted(dem, key=operator.itemgetter(1), reverse=True)
        sup_list = sorted(sup, key=operator.itemgetter(1))
        max_list = len(dem_list)
        if max_list < len(sup_list): max_list = len(sup_list)
        s_d_string = "Unit  ID    Value | Cost      ID \n"
        s_d_string += "---------------------------------- \n"
        eq_flag = False  # set to True when equilibrium found

        if self.debug: print(" ...... In get_supply_demand_list -> max_list = {}".format(max_list))
        if self.debug: print(" ...... In get_supply_demand_list -> len(dem_list) = {}".format(len(dem_list)))
        if self.debug: print(" ...... In get_supply_demand_list -> len(sup_list) = {}".format(len(sup_list)))

        for x in range(max_list):
            if x < len(dem_list) and x < len(sup_list):
                if dem_list[x][1] < sup_list[x][1]:
                    if eq_flag == False:
                        eq_flag = True
                        s_d_string += "---------------------------------- \n"
            s_d_string += "  {:^2}  ".format(x+1)
            if x < len(dem_list):
                s_d_string += "{:^3}  {:^3} | ".format(dem_list[x][0], dem_list[x][1])
            else:
                s_d_string += " "*10
            if x < len(sup_list):
                s_d_string += "{:^3}  {:^3} \n ".format(sup_list[x][1], sup_list[x][0])
            else:
                s_d_string += "\n"

        if self.debug:
            print("...... In Model -> get_supply_demand_list -> ending")
            print(s_d_string)

        return s_d_string


    def list_supply_demand(self):
        dem = self.env["demand"]
        sup = self.env["supply"]
        sd = sup + dem
        s_and_d = sorted(sd, key=operator.itemgetter(1), reverse=True)
        print("Unit    ID     Cost | Value     ID")
        print("----------------------------------")
        for unit in s_and_d:
            if unit[0][0] == "b":
                print(" " * 20 + "| {:^3}    {:^3}".format(unit[1], unit[0]))
            if unit[0][0] == "s":
                print(" " * 5 + "{:^3}   {:^3}  |".format(unit[0], unit[1]))
        print("")

    def get_supply_demand_plot_info(self):
        """First define supply and demand curves"""
        # make dunits = list of deman units, sunits = list of supply units
        dunits = [units for units in range(len(self.env["demand"]) + 2)]
        sunits = [units for units in range(len(self.env["supply"]) + 1)]
        munits = [units for units in range(max(len(dunits), len(sunits)))]

        self.calc_equilibrium()  # this is where env["dem"] and env["sup"] created

        # Then plot the curves

        demand_values = self.env["dem"]
        supply_costs = self.env["sup"]

        eq_price_high = self.env["eq"]["price_high"]
        eq_price_low = self.env["eq"]["price_low"]

        if self.debug:
            print("...... In Model --> get_supply_demand_plot_info")
            print("...... demand = {}".format(demand_values))
            print("...... supply = {}".format(supply_costs))

        return dunits, sunits, munits, demand_values, supply_costs, eq_price_high, eq_price_low

    def plot_supply_demand(self, output_path, session_name, fig_name):
        """First define supply and demand curves"""
        with plt.style.context('seaborn'):
            # make dunits = list of deman units, sunits = list of supply units
            dunits = [units for units in range(len(self.env["demand"]) + 2)]
            sunits = [units for units in range(len(self.env["supply"]) + 1)]
            munits = [units for units in range(max(len(dunits), len(sunits)))]

            self.calc_equilibrium()  # this is where env["dem"] and env["sup"] created

            # Then plot the curves

            demand_values = self.env["dem"]
            supply_costs = self.env["sup"]

            plt.step(dunits, demand_values, label='Demand', color='orangered')  # generate demand plot
            plt.step(sunits, supply_costs, label='Supply', color='darkorange')  # generate supply plot

            eq_price_high = self.env["eq"]["price_high"]
            eq_price_low = self.env["eq"]["price_low"]

            if eq_price_high != eq_price_low:
                plt.plot(munits, [eq_price_high for x in munits], linestyle='--', color='darkslategray', label='Eq. Price High')
                plt.plot(munits, [eq_price_low for x in munits], linestyle='--', color='darkslategray', label='Eq. Price Low')
            else:
                plt.plot(munits, [eq_price_high for x in munits], linestyle='--', color='darkslategray', label='Eq. Price') # one price

            plt.legend(bbox_to_anchor=(0.65, 0.98))  # places a legend on the plot
            plt.title('Simulation Market Supply and Demand')  # add the title
            plt.xlabel('Units')  # add the x axis label
            plt.ylabel('Value ($)')  # add the y axis label
            plt.savefig(output_path + session_name + "\\" + fig_name)  # display the plot
            plt.close()


    def calc_equilibrium(self):
        # make demand values
        max_value = 0
        for index in self.env["demand"]:
            if index[1] > max_value:  # find the maximum value
                max_value = index[1]
        demand_values = [max_value + 1]  # first element used for upper range in graph
        for index in self.env["demand"]:  # get demand tuples
            demand_values.append(index[1])  # and pull out second element to get value
        demand_values.append(0)  # put a zero value at the end to pull graph down to x axes

        # make suppl values the same way
        supply_costs = [0]  # first element used to create lower range of supply values
        for index in self.env["supply"]:  # get supply tupples
            supply_costs.append(index[1])  # and pull out second element to get cost

        # make demand and supply curves without id's and added elements for plotting
        self.env["dem"] = demand_values
        self.env["sup"] = supply_costs

        # get length of supply and demand schedules
        min_length = min(len(self.env["demand"]), len(self.env["supply"])) + 1
        max_length = max(len(self.env["demand"]), len(self.env["supply"])) + 1

        # now make equilibrium and surplus calculations
        # TODO need to test for supply and demand not crossing
        # this can happen at beginning or at end

        max_surplus = 0  # max_surplus is the area up to equilibrium units
        eq_units = 0  # this is the maximum number of units that can sell
        for unit in range(1, min_length):  # only go as far as shortest schedule
            if demand_values[unit] >= supply_costs[unit]:  # As long as value is above or equal to cost
                eq_units = eq_units + 1  # unit should sell in equilibrium
                max_surplus = max_surplus + demand_values[unit] - supply_costs[unit]  # add surplus
                last_accepted_value = demand_values[unit]  # update last accepted value
                last_accepted_cost = supply_costs[unit]  # update last accepted cost
            else:  # now value is below cost
                first_rejected_value = demand_values[unit]  # calculate first rejected value
                first_rejected_cost = supply_costs[unit]  # calculate first rejected cost
                break  # exit loop we are done here

        # Now calculate equilibrium price range
        eq_price_high = min(last_accepted_value, first_rejected_cost)
        eq_price_low = max(last_accepted_cost, first_rejected_value)

        self.env["eq"]["price_high"] = eq_price_high
        self.env["eq"]["price_low"] = eq_price_low
        self.env["eq"]["quantity"] = eq_units
        self.env["eq"]["surplus"] = max_surplus

    def show_equilibrium(self):
        #  Print out market equilibrium numbers
        print()
        print("----- Equilibrium -----")
        print("When market {} is in equilibrium we have:".format(self.name))
        print("equilibrium price    = {} - {}".format(self.env["eq"]["price_low"], self.env["eq"]["price_high"]))
        print("equilibrium quantity = {}".format(self.env["eq"]["quantity"]))
        print("maximum surplus      = {}".format(self.env["eq"]["surplus"]))
        print(" ")

    def get_equilibrium(self):
        self.calc_equilibrium()
        # get equilibrium information and return as tuple
        pl = self.env["eq"]["price_low"]
        ph = self.env["eq"]["price_high"]
        qt = self.env["eq"]["quantity"]
        ms = self.env["eq"]["surplus"]
        return qt, pl, ph, ms

    def save_file(self, path):
        # write out "env" as .csv file
        output_file = open(path + '.csv', 'w', newline='')
        output_writer = csv.writer(output_file)

        # First write out number of buyers and number of sellers
        output_writer.writerow([self.num_buyers, self.num_sellers])

        # Second write out buyer information
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            output_writer.writerow(self.env["buyers"][buyer_id])

        # Third write out seller information
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            output_writer.writerow(self.env["sellers"][seller_id])

        # Fourth write out supply and demand curves with id's
        # Write as two lists
        self.make_supply()
        s = []
        for element in self.env["supply"]:
            s.append(element[0])
            s.append(element[1])
        output_writer.writerow(s)
        self.make_demand()
        s = []
        for element in self.env["demand"]:
            s.append(element[0])
            s.append(element[1])
        output_writer.writerow(s)

        # Make equilibrium calculations
        self.calc_equilibrium()

        # Fifth write out supply and demand without id's
        output_writer.writerow(self.env["sup"])
        output_writer.writerow(self.env["dem"])

        # Sixth write out equilibrium values
        output_writer.writerow([self.env["eq"]["price_high"],
                                self.env["eq"]["price_low"],
                                self.env["eq"]["quantity"],
                                self.env["eq"]["surplus"]])
        # That's it for now
        output_file.close()

    def load_file(self, path):
        # load a .csv file
        try:
            input_file = open(path)
            input_reader = csv.reader(input_file)
            env_data = list(input_reader)
            if self.debug:
                print("...,... In Model -> load_file -> first read")
                print('...,... data = {}'.format(env_data))


            # Process num_buyers and num_sellers(First)
            line = 0
            self.num_buyers = int(env_data[line][0])
            self.num_sellers = int(env_data[line][1])

            # Process buyer values (Second)
            for buyer in range(self.num_buyers):
                line = 1 + buyer
                values = [int(x) for x in env_data[line]]  # have to convert back to integers
                buyer_id = "buyer" + str(buyer)
                self.env["buyers"][buyer_id] = values

            # Process seller costs  (Third)
            for seller in range(self.num_sellers):
                line = 1 + self.num_buyers + seller
                costs = [int(x) for x in env_data[line]]  # have to convert back to integers
                seller_id = "seller" + str(seller)
                self.env["sellers"][seller_id] = costs

            # Process supply and demand curves with id's  (Fourth)
            line = 1 + self.num_buyers + self.num_sellers
            remake = []
            for i in range(0, len(env_data[line]), 2):
                e1 = env_data[line][i]
                e2 = int(env_data[line][i + 1])
                remake.append((e1, e2))
            self.env["supply"] = remake

            remake = []
            for i in range(0, len(env_data[line + 1]), 2):
                e1 = env_data[line + 1][i]
                e2 = int(env_data[line + 1][i + 1])
                remake.append((e1, e2))
            self.env["demand"] = remake

            # Process supply and demand curves without id's (Fifth)
            self.env["sup"] = [int(x) for x in env_data[line + 2]]
            self.env["dem"] = [int(x) for x in env_data[line + 3]]

            # Process equilibrium values
            self.env["eq"]["price_high"] = int(env_data[line + 4][0])
            self.env["eq"]["price_low"] = int(env_data[line + 4][1])
            self.env["eq"]["quantity"] = int(env_data[line + 4][2])
            self.env["eq"]["surplus"] = int(env_data[line + 4][3])
        except OSError as err:
            print("File {} does not exist".format(path))

    def prepare_market(self, input_path, input_file, output_path, session_name, fig_name):
        self.load_file(input_path + input_file + ".csv")
        self.plot_supply_demand(output_path, session_name, fig_name)
        self.show_participants()
        self.show_equilibrium()

if __name__ == "__main__":
    mkt = SpotEnvironmentModel()  # allows access when called in build_environment