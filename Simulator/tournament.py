from Trader.trader import Trader_Shaver, Trader_ZIU, Trader_ZIC, Trader_Kaplan, Trader_PS, Trader_AA, Trader_GD, Trader_ZIP
import Institution.double_auction_institution as ins
import random

class Tournament(object):
    """ A class that makes a trader"""

    def __init__(self, name, iterations, auction):
        self.name = name
        self.iterations = iterations
        self.traders = []
        self.auction = auction

    def show(self):
        print ("I am tournament {}.".format(self.name))

    def prepare_traders(self, tn, mkt, limits):
        d = {}
        t = {}
        if len(tn) != mkt.num_buyers + mkt.num_sellers:
            print ("tn = {} does not have the right length".format(tn))
        for k in range(mkt.num_buyers + mkt.num_sellers):
            t_id = "t" + str(k)  # make trader id
            t[t_id] = globals()[tn[k]]()  # create object
            t[t_id].name = t_id  # set objects name
            t[t_id].da = ins.Auction("da", limits[0], limits[1])
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

    def run(self, display):
        self.auction.open_board("tournament official")
        if display:
            print()
            print("Auction Open")
            print(self.auction.report_standing(), self.auction.report_contracts())
        length_old_contracts = 0
        for i in range(self.iterations):
            random.shuffle(self.traders)
            for trader in self.traders:
                trader.offer()
                contracts = self.auction.report_contracts()
                if len(contracts) > length_old_contracts:
                    length_old_contracts = len(contracts)
                    if display:
                        print (i, contracts[len(contracts) - 1])
        if display:
            print()

    def eval(self, display, d, result_header):
        # calculate market efficiency
        ep_low = d['equilibrium'][0]
        ep_high = d['equilibrium'][1]
        e_quantity = d['equilibrium'][2]
        maximum_surplus = d['equilibrium'][3]

        for trader in self.traders:
            trader_id = trader.name
            d[trader_id]['units'] = 0
            d[trader_id]['earn'] = 0

            # calculate actual surplus and earnings

        actual_surplus = 0
        for contract in self.auction.report_contracts():
            price = contract[0]
            buyer_id = contract[1]
            seller_id = contract[2]
            if d[buyer_id]['type'] == 'B':
                value = d[buyer_id]['values'][d[buyer_id]['units']]
                d[buyer_id]['earn'] += value - price
                d[buyer_id]['units'] += 1
            else:
                print ("error, buyer id = {}, buyer type = {}".format(buyer_id, d[buyer_id]['type']))
            if d[seller_id]['type'] == 'S':
                cost = d[seller_id]['costs'][d[seller_id]['units']]
                d[seller_id]['earn'] += price - cost
                d[seller_id]['units'] += 1
            else:
                print ("error in contract {}, seller id = {}, seller type = {}".format(contract, seller_id,
                                                                                       d[seller_id]['type']))
            actual_surplus += value - cost

        efficiency = int((actual_surplus / maximum_surplus) * 100)

        result_header.extend([ep_low, ep_high, e_quantity, maximum_surplus, actual_surplus, efficiency])
        if display:
            print ("actual surplus = {}, maximum surplus = {}.".format(actual_surplus, maximum_surplus))
            print ("market efficiency = {} percent.".format(efficiency))

        for k in range(len(self.traders)):
            t_id = "t" + str(k)
            t_strat = d[t_id]['strat']
            earn = d[t_id]['earn']
            if display:
                print ("Trader {}, using strategy {}, earned {}.".format(t_id, t_strat, earn))
            result_header.extend([t_id, t_strat, earn])
        if display:
            print()

        for k in d['strategies']:
            strat_earn = 0
            count = 0
            for l in range(len(self.traders)):
                t_id = "t" + str(l)
                if k == d[t_id]['strat']:
                    count = count + 1
                    strat_earn += d[t_id]['earn']
            if count > 0:
                avg_earn = int(strat_earn / count)
                result_header.extend([k, avg_earn])
            if display:
                print ("Strategy {} earned an average of {}.".format(k, avg_earn))

        return result_header

    def save_results(self, result_header, output_file):
        # write tournamnet results as .csv file
        output_file = open(output_file + '.csv', 'w', newline='')
        output_writer = csv.writer(output_file)

        # First write out result header record
        output_writer.writerow(result_header)

        # Second write out offers information
        orders = self.auction.report_orders()
        output_writer.writerow(["orders", "time, id, type, amt/null", len(orders)])
        for element in orders:
            s = []
            s.append(element[0])
            s.append(element[1])
            s.append(element[2])
            s.append(element[3])
            output_writer.writerow(s)

        # Third write out contract information
        contracts = self.auction.report_contracts()
        output_writer.writerow(["contracts", "price, buyer_id, seller_id", len(contracts)])
        for element in contracts:
            s = []
            s.append(element[0])
            s.append(element[1])
            s.append(element[2])
            output_writer.writerow(s)

        output_file.close()

    def sim(self, display, num_trials, d):

        # initialize sum variables

        total_earnings = [0] * len(d['strategies'])
        sum_squared = [0] * len(d['strategies'])

        for k in range(num_trials):
            result = []
            self.run(display)
            # TODO Put input and output files back in for blanks
            result_header = [" ", " ", len(self.traders)]
            result_header = self.eval(display, d, result_header)
            # result header = [input_file, output_file, num_traders, ep_low, ep_high, e_quantity,
            #                  max_surplus, actual_surplus, efficiency,
            #                  ** for all numtraders** trader id, trader strategy, trader earnings]
            # print(result_header)
            result.append(result_header[8])
            j = 9 + int(result_header[2]) * 3  # move to where strategy results are
            for k in d['strategies']:
                result.append(result_header[j + 1])
                j = j + 2

            if display:
                print("for run {} result {}".format(k, result))

            for j in range(len(d['strategies'])):
                earn = result[j + 1]
                total_earnings[j] += earn
                sum_squared[j] += earn * earn

        avg_earning = []
        var = []
        sdev = []
        for j in range(len(d['strategies'])):
            avg_earn = total_earnings[j] / num_trials
            variance = ((sum_squared[j] / num_trials) - (avg_earn * avg_earn))
            standard_deviation = variance ** 0.5
            avg_earning.append(avg_earn)
            var.append(variance)
            sdev.append(standard_deviation)
        print ()
        print ("Average Earnings for {} rounds".format(num_trials))
        print (d['strategies'])
        print(avg_earning)
        print(sdev)

if __name__ == "__main__":
    trn = Tournament ("Tournamnet Name", 10, "placeholder for double auction")