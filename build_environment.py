import operator
import matplotlib.pyplot as plt  # import matplotlib
import numpy as np  # import numpy
import time
import random
import csv
#TEST
#testing Adam Choy BRANCH
class BuildMarketEnv(object):
    """ A class that makes a market"""
    env = {"demand": [], "dem": [], "supply": [], "sup": [], "buyers": {}, "sellers": {}, "eq": {}}

    def __init__(self, name, num_buyers, num_sellers, debug=False):
        self.name = name
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.debug = debug
        if debug:
            print(self.num_buyers, self.num_sellers)
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            self.env["buyers"][buyer_id] = []  # Add a list of values to buyers[buyer_id] as key
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            self.env["sellers"][seller_id] = []  # Add a list of costs to sellers[seller_id] as key

    def show(self):
        print("I am market {} with {} buyers and {} sellers.".format(self.name, self.num_buyers, self.num_sellers))
        print("")

    def show_participants(self):
        print("Market Participants")
        print("-------------------")
        print("BUYERS")
        print("------")
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            print("buyer {} has values {}".format(buyer_id, self.env["buyers"][buyer_id]))
        print("SELLERS")
        print("-------")
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            print("seller {} has costs {}".format(seller_id, self.env["sellers"][seller_id]))
        print("")

    def add_buyer(self, buyer_number, values):
        buyer_id = "buyer" + str(buyer_number)
        self.env["buyers"][buyer_id] = values

    def get_buyer_values(self, buyer_number):
        if buyer_number > self.num_buyers - 1:
            return [-1]
        else:
            return self.env["buyers"]["buyer" + str(buyer_number)]

    def add_seller(self, seller_number, costs):
        seller_id = "seller" + str(seller_number)
        self.env["sellers"][seller_id] = costs

    def get_seller_costs(self, seller_number):
        if seller_number > self.num_sellers - 1:
            return [-1]
        else:
            return self.env["sellers"]["seller" + str(seller_number)]

    def make_demand(self):
        dem = []
        for buyer in range(self.num_buyers):
            buyer_id = "buyer" + str(buyer)
            for value in self.env["buyers"][buyer_id]:
                dem.append((buyer_id, value))
        sdem = sorted(dem, key=operator.itemgetter(1), reverse=True)
        self.env["demand"] = sdem

    def make_supply(self):
        sup = []
        for seller in range(self.num_sellers):
            seller_id = "seller" + str(seller)
            for cost in self.env["sellers"][seller_id]:
                sup.append((seller_id, cost))
        ssup = sorted(sup, key=operator.itemgetter(1))
        self.env["supply"] = ssup

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

    def plot_supply_demand(self):
        """
        First define supply and demand curves
        """
        # make units
        dunits = [units for units in range(len(self.env["demand"]) + 2)]  # demand units list of numbers
        sunits = [units for units in range(len(self.env["supply"]) + 1)]  # supply units list of numbers
        munits = [units for units in range(max(len(dunits), len(sunits)))]  # maximum units list of numbers

        self.calc_equilibrium()

        """
        Then plot the curves
        """
        demand_values = self.env["dem"]
        supply_costs = self.env["sup"]

        plt.step(dunits, demand_values, label='Demand')  # generate the demand plot
        plt.step(sunits, supply_costs, label='Supply')  # generate the supply plot

        eq_price_high = self.env["eq"]["price_high"]
        eq_price_low = self.env["eq"]["price_low"]

        if eq_price_high != eq_price_low:
            plt.plot(munits, [eq_price_high for x in munits], label='Price High')  # High Price Line
            plt.plot(munits, [eq_price_low for x in munits], label='Price Low')  # Low Price Line
        else:
            plt.plot(munits, [eq_price_high for x in munits], label='Price')  # Just one price

        plt.legend(bbox_to_anchor=(0.65, 0.98))  # places a legend on the plot
        plt.title('Supply and Demand')  # add the title
        plt.xlabel('Units')  # add the x axis label
        plt.ylabel('$')  # add the y axis label
        plt.show()  # display the plot

    def calc_equilibrium(self):
        # make demand values
        max_value = 0
        for index in self.env["demand"]:
            if index[1] > max_value:  # find the maximum value
                max_value = index[1]
        demand_values = [max_value + 1]  # note first element is just used to create upper range in graph
        for index in self.env["demand"]:  # get demand tuples
            demand_values.append(index[1])  # and pull out second element to get value
        demand_values.append(0)  # put a zero value at the end to pull graph down to x axes

        # make suppl values the same way
        supply_costs = [0]  # note first elemnt is used to create lower range of supply values
        for index in self.env["supply"]:  # get supply tupples
            supply_costs.append(index[1])  # and pull out second element to get cost

        self.env["dem"] = demand_values
        self.env["sup"] = supply_costs

        # calculate equilibrium and maximum surplus

        # note supply and demand schedules can be different lengths
        min_length = min(len(self.env["demand"]), len(self.env["supply"])) + 1
        max_length = max(len(self.env["demand"]), len(self.env["supply"])) + 1

        # now make equilibrium calculations
        # TODO need to test for supply and dmeand not crossing
        #      this can happen at beginning or at end
        #
        max_surplus = 0  # max_surplus is the area under the supply and demand up to equilibrium
        eq_units = 0  # this is the maximum number of units that can sell
        for unit in range(1, min_length):  # only go as far as shortest schedule
            if demand_values[unit] >= supply_costs[unit]:  # As long as value is above or equal to cost
                eq_units = eq_units + 1  # unit should sell in equilibrium
                max_surplus = max_surplus + demand_values[unit] - supply_costs[unit]  # add surplus
                last_accepted_value = demand_values[unit]  # update last accepted value
                last_accepted_cost = supply_costs[unit]  # update first rejected
            else:  # now value is below cost
                first_rejected_value = demand_values[unit]  # calculate first rejected value
                first_rejected_cost = supply_costs[unit]  # calculate first rejected cost
                break  # exit loop we are done here

        # Now caluclate equilibrium price range
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
        pl = self.env["eq"]["price_low"]
        ph = self.env["eq"]["price_high"]
        qt = self.env["eq"]["quantity"]
        ms = self.env["eq"]["surplus"]
        return (pl, ph, qt, ms)

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
        print(s)
        output_writer.writerow(s)
        self.make_demand()
        s = []
        for element in self.env["demand"]:
            s.append(element[0])
            s.append(element[1])
        print(s)
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
        # Thats it for now
        output_file.close()

    def load_file(self, path):
        # load a .csv file
        try:
            input_file = open(path + '.csv')
            input_reader = csv.reader(input_file)
            env_data = list(input_reader)

            # Process num_buyers and num_sellers  (First)
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
            #
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

    def prepare_market(self, input_path, input_file):
        self.load_file(input_path + input_file)
        self.plot_supply_demand()
        self.show_participants()
        self.show_equilibrium()

if __name__ == "__main__":
    # This code shows some basic usage of BuildMarkeEnv
    mkt = BuildMarketEnv("test", 2, 3)
    mkt.show()
    mkt.add_buyer(0, [200, 100, 50])
    mkt.add_buyer(1, [150, 125, 75])
    mkt.add_seller(0, [50, 75, 125])
    mkt.add_seller(1, [25, 65, 100])
    mkt.add_seller(2, [60, 70, 150])
    mkt.show_participants()
    mkt.make_demand()
    mkt.make_supply()
    mkt.list_supply_demand()
    mkt.calc_equilibrium()
    mkt.show_equilibrium()
    print(mkt.get_buyer_values(0))
    print(mkt.get_seller_costs(0))
    mkt.plot_supply_demand()
    # methods not shown
    #      load_file(path)
    #      save_file(path)
    #      prepare market(input_path, input_file)


