import tkinter as tk  # gui interface creator
import tkinter.ttk as ttk
import tkinter.filedialog
from tkinter import messagebox
import matplotlib  # graphing functions
matplotlib.use("TkAgg")
import time  # https://docs.python.org/3.6/library/time.html  # time functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import random
import os  # https://docs.python.org/3.6/library/os.html
import Environment.spot_environment_controller  # condensed modules/commands from spot_env_model
import Simulator.spot_market_period

import Institution.spot_system as sys
import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from win32api import GetSystemMetrics  # gets your computer's resolution size
import time
import Trader.trader as tdr
from timeit import default_timer as timer
import scipy.stats as stats
import GUI.spot_environment_gui
import inspect
instant_shock_status = 0

# TODO IMPORTANT: need to clear contract list in spot system or double auction institution...
# --> causing problems with transactions graph when re-running the simulator in market_gui
# --> maybe clearing lists in run_sim() or spot_market_period?

# TODO IMPORTANT: need to fix Supply and Demand graph error in run_sim()...
# --> when re-running simulator in market_gui plots trader efficiency distribution in supply demand graph

# TODO IMPORTANT: add round and period shocks into run_sim()...
# --> pass r_shock_list (line 740 below) to spot_system's run_system() for round shocks
# --> p_shock_list (line 739 below) can be used within for loop (line 775 below)

# TODO IMPORTANT: fix tkinter error after sim run...
# --> getting "ttk:ThemeChanged... event destroyed" error after sim run --> don't know why

# TODO OPTIONAL: add ability for all info to be stored in json files...
# --> could then let user choose between using excel csv or json files

class MarketGui():
    def __init__(self, root, sec, project_path, output_path, name, debug=False):
        assert name != "", "Gui must have a name"

        self.root = root  # root builds tkinter app
        '''Can maybe add an os function for resolutions to adapt'''
        self.root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))
        self.sec = sec  # will bring in spot_env_model and use debugger
        self.name = name  # name of gui
        self.debug = debug  # used as error checker...when false will return errors or warnings
        self.root.title(name)  # giving root a name
        '''Added a messagebox for when escape button pressed... calls on_escape_chosen()'''
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit_chosen)

        self.num_periods = 0  # setting number of buyers to 0
        self.num_rounds = 0
        self.num_p_shocks = 0  # setting number of sellers to 0
        self.num_r_shocks = 0  # setting number of units to 0
        self.num_buyers = 0  # setting number of buyers to 0
        self.num_sellers = 0  # setting number of sellers to 0
        self.num_units = 0  # setting number of units to 0
        self.floor = 0
        self.ceiling = 0
        self.session = None
        self.traders = []
        self.strategies = []

        self.strategy_string = tk.StringVar()
        self.string_institution = tk.StringVar()
        self.string_periods = tk.StringVar()    # creates a tkinter variable
        self.string_rounds = tk.StringVar()
        self.string_round_shocks = tk.StringVar()   # StringVar() returns either an ASCII string or Unicode string
        self.string_period_shocks = tk.StringVar()     # can also be used to trace when changes made to variables
        self.price_floor = tk.StringVar()
        self.price_ceiling = tk.StringVar()
        self.string_session_name = tk.StringVar()  # BooleanVar() will return 0 for false and 1 for true...
        self.string_data = tk.StringVar()
        self.new_string_data = tk.StringVar()
        self.string_num_buyers = tk.StringVar()  # creates a tkinter variable
        self.string_num_sellers = tk.StringVar()  # StringVar() returns either an ASCII string or Unicode string
        self.string_num_units = tk.StringVar()
        self.string_eq = tk.StringVar()
        self.string_pl = tk.StringVar()
        self.string_ph = tk.StringVar()
        self.string_ms = tk.StringVar()

        self.buyer_ids = None
        self.seller_ids = None
        self.p_shock_ids = None
        self.p_shock_files = None
        self.r_shock_ids = None
        self.r_shock_files = None
        self.buyer_shift = tk.StringVar()
        self.seller_shift = tk.StringVar()
        self.buyer_replace_strategy = tk.StringVar()
        self.seller_replace_strategy = tk.StringVar()

        self.trader_replace = tk.IntVar()

        self.current_row = 0  # setting current read row to 0... self.current_row+1 would read next row
        self.current_row_contents = []
        self.ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # is this limiting the amount to 10 buyers and 10 sellers?
        self.file_name = None  # none is a placeholder to be filled

        # have to build matrices for future tkinter display
        self.pshock_values = self.build_array(self.num_r_shocks, self.num_r_shocks)  # matrix of buyers and number of units
        self.rshock_values = self.build_array(self.num_p_shocks, self.num_p_shocks)  # matrix of sellers and number of units
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)  # matrix of buyers and number of units
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)  # matrix of sellers and number of units

        self.project_path = project_path
        self.output_path = output_path + '/'

        self.autofill_strat = tk.StringVar()

        # have to build menu and start the project
        self.show_menu()  # executes menu build with toolbar and help/action messages
        self.show_shortcut()  # executes frame build in tkinter
        self.show_infobar()  # executes sub-frame for user entering number buyers, number sellers, units
        #self.process_new_project()

        self.parameters_trigger = False
        self.save_file_trigger = False
        self.strategy_trigger = False  # safety feature when rerunning in gui: if same parameters used = True
        self.r_shock_trigger = False
        self.p_shock_trigger = False
        self.replace_trader_trigger = False
        self.display_sd_info = False

    def build_array(self, num_1, num_2):  # builds an array for buyers:values and sellers:costs
        x = []
        for j in range(num_1):
            a_row = []
            for k in range(num_2):
                a_row.append(k)
            x.append(a_row)
        return x

    def show_menu(self):
        # getting icons ready for compound menu
        menu_bar = tk.Menu(self.root)  # menu begins

        # create file menu item
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', accelerator='Ctrl+N',
                              compound='left', underline=0, command=None)
        file_menu.add_command(label='Open', accelerator='Ctrl+O',
                              compound='left', underline=0, command=self.open_file)
        file_menu.add_command(label='Save', accelerator='Ctrl+S',
                              compound='left', underline=0, command=self.save)
        #file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', accelerator='Alt+F4', command=self.on_quit_chosen)
        menu_bar.add_cascade(label='File', menu=file_menu)  # allows toolbar tab to drop down with multiple choices

        # create about/help menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='About', command=self.display_about_messagebox)  # click = display about message
        about_menu.add_command(label='Help', command=self.display_help_messagebox)  # click = display help message
        # TODO add link to github readme in display_help_messagebox
        menu_bar.add_cascade(label='Misc', menu=about_menu)  # drop down menu
        self.root.config(menu=menu_bar)  # makes menu setup final

    def show_shortcut(self):
        shortcut_bar = tk.Frame(self.root)  # creates a frame within the tkinter object
        shortcut_bar.grid(row=0, column=0, columnspan=4, sticky='W')  # setting parameters of frame

    def show_infobar(self):
        for name, obj in inspect.getmembers(tdr):  # obtains all trader strategies from Trader.trader
            if inspect.isclass(obj):
                self.strategies.append(obj.__name__)  # appends to list
        # creates a frame in gui to set project paths

        # creates a frame in gui to enter in new session data for simulator run
        info_bar = tk.LabelFrame(self.root, height=15, text=str(self.name))  # creates a label frame for initial inputs
        info_bar.grid(row=1, column=0, columnspan=3, sticky='W', padx=5, pady=5)  # set parameters

        # create project name label and entry
        tk.Label(info_bar, text="Session Name").grid(row=0, column=0, padx=10)
        tk.Entry(info_bar, width=15, justify=tk.LEFT, textvariable=self.string_session_name).grid(row=1, column=0)

        # create number of buyers label and entry
        tk.Label(info_bar, text="Period Shocks").grid(row=0, column=1, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.string_period_shocks).grid(row=1, column=1)
        self.string_period_shocks.set(str(self.num_p_shocks))

        # create number of sellers label and entry
        tk.Label(info_bar, text="Round Shocks").grid(row=0, column=2, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.string_round_shocks).grid(row=1, column=2)
        self.string_round_shocks.set(str(self.num_r_shocks))

        # create number of units label and entry
        tk.Label(info_bar, text="Periods").grid(row=0, column=3, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.string_periods).grid(row=1, column=3)
        self.string_periods.set(str(self.num_periods))

        # create number of rounds label and entry
        tk.Label(info_bar, text="Rounds").grid(row=0, column=4, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.string_rounds).grid(row=1, column=4)
        self.string_rounds.set(str(self.num_rounds))

        # create price floor label and entry
        tk.Label(info_bar, text="Price Floor").grid(row=0, column=5, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.price_floor).grid(row=1, column=5)
        self.price_floor.set(str(self.floor))

        # create price ceiling label and entry
        tk.Label(info_bar, text="Price Ceiling").grid(row=0, column=6, padx=10)
        tk.Entry(info_bar, width=5, justify=tk.CENTER, textvariable=self.price_ceiling).grid(row=1, column=6)
        self.price_ceiling.set(str(self.ceiling))

        # create data file label and drop down menu to choose from
        tk.Label(info_bar, text="Starting Data File: ").grid(row=2, column=0, pady=10)  # create/grid location
        ttk.Combobox(info_bar, values=os.listdir(self.project_path), textvariable=self.string_data, state='readonly').grid(row=2, column=1)

        # create drop down menu for choosing institution to use
        tk.Label(info_bar, text="Market Institution: ").grid(row=3, column=0, pady=10)
        ttk.Combobox(info_bar, values=["DoubleAuction", "SealedBid", "Vickrey"], textvariable=self.string_institution, state='readonly').grid(row=3, column=1)
        self.string_institution.set("DoubleAuction")

        # creates button to explain institution settings
        explain1_button = tk.Button(info_bar, text="Explain", width=7, command=self.explain1_clicked)
        explain1_button.grid(row=3, column=2)

        # creates a button to show the chosen file's supply/demand graph
        plot_button = tk.Button(info_bar, text="Show", width=4, command=self.on_show_clicked)
        plot_button.grid(row=2, column=2)

        # creates frame for set parameters button
        set_frame = tk.LabelFrame(info_bar, text="Set Parameters")
        set_frame.grid(row=0, column=7, padx=5, pady=5)
        set_button = tk.Button(set_frame, text="Set", width=4, command=self.on_set_parms_clicked)
        set_button.grid(row=0, column=0, padx=30)  # creates grids in both built frames

        # creates a frame in gui to create a new supply/demand data file by pressing a button
        file_frame = tk.LabelFrame(info_bar, height=15, text="New Data File")
        file_frame.grid(row=1, column=7, padx=5, pady=5)
        # create a button with action input (command = click)
        create_button = tk.Button(file_frame, text="Create", width=6, command=self.on_create_clicked)
        create_button.grid(row=0, column=0, padx=30)

        # creates a frame within the infobar to set instant shocks
        '''If this feature is enabled will execute code in spot_system.py ---> run_system() --> line 133'''
        trader_replace_frame = tk.LabelFrame(info_bar, text="Trader Replacement")
        trader_replace_frame.grid(row=3, column=3, columnspan=5)

        # creates a check box for enabling instantaneous market shocks
        enable_button = tk.Checkbutton(trader_replace_frame, text="Enabled", variable=self.trader_replace)
        enable_button.grid(row=0, column=0)

        # button that displays info about instantaneous market shocks
        explain2_button = tk.Button(trader_replace_frame, text="Explain", width=7, command=self.explain2_clicked)
        explain2_button.grid(row=0, column=1)

        # creates button to explain the different trading strategies that the user can use
        strat_info_button = tk.Button(trader_replace_frame, text="Strategy Descriptions", width=16,
                                      command=self.strategy_message)
        strat_info_button.grid(row=0, column=2)

        tk.Label(trader_replace_frame, text="Strategy").grid(row=1, column=1, pady=5)
        tk.Label(trader_replace_frame, text="New Buyer: ").grid(row=2, column=0)
        ttk.Combobox(trader_replace_frame, values=self.strategies, textvariable=self.buyer_replace_strategy, state='readonly').grid(row=2, column=1)
        tk.Label(trader_replace_frame, text="New Seller: ").grid(row=3, column=0)
        ttk.Combobox(trader_replace_frame, values=self.strategies, textvariable=self.seller_replace_strategy, state='readonly').grid(row=3, column=1)

    '''The comand below generates a tk messagebox to explain the different institutions that can be used'''
    def explain1_clicked(self):
        explain1_message = "\nChanging this variable will change the institution that is used," \
                           " which will set the rules of trading in the market simulation." \
                           "\n \nA Double Auction is when multiple sellers and buyers can trade" \
                           " a single unit or multiple units. The bidding will continue until a" \
                           " seller's and bidder's bid converge, at which point a contract will be made." \
                           "\n \nA Sealed Bid Auction is when there are either one seller and multiple buyers" \
                           " OR one buyer and multiple sellers. The group of multiple traders each submit" \
                           " a sealed bid, at which point the single seller or buyer accepts one of the bids " \
                           " and a contract is made." \
                           "\n \nA Vickrey Auction is a type of sealed bid auction where the highest bidder wins," \
                           " but the price paid is that of the second highest bid." \
                           "\n \nMore institutions can be added"
        tk.messagebox.askokcancel("MARKET INSTITUTIONS", explain1_message)

    '''The command below generates a tk messagebox to explain the use of instantaneous market shocks'''
    def explain2_clicked(self):
        explain2_message = "\nEnabling this feature will disable period and round shocks" \
                          "\n \nTrader replacement will occur when a contract is made" \
                          " between a seller and a buyer." \
                          "\n \nThis will result in those buyer's and seller's private values" \
                          " being recycled to the new buyer and new seller entering the market." \
                          "\n \nThis will result in keeping the supply and demand constant."
        tk.messagebox.askokcancel("TRADER REPLACEMENT", explain2_message)

    '''The command below generates a tk messagebox to explain the use of strategies that the user can use'''
    def strategy_message(self):
        # TODO fill in with descriptions of each strategy.. maybe include link or ref to paper?
        strat_explain = "\nTrader_AA: ..... \n \n Trader_AI: .... \n \n Trader_GD: .... \n \n Trader_Kaplan: ..." \
                        "\n \n Trader_PS: ... \n \n Trader ZIP: ... \n \n Trader_ZIC: ..."
        tk.messagebox.askokcancel("STRATEGY DESCRIPTIONS", strat_explain)


    def on_create_clicked(self):
        '''Added ability to run spot_environment_gui in market_gui... allows new SD creation'''
        create_root = tk.Toplevel()
        create_debug_test = True
        if create_debug_test:
            print("In Gui -> START")
        create_sec = Environment.spot_environment_controller.SpotEnvironmentController(create_debug_test)
        GUI.spot_environment_gui.SpotEnvironmentGui(create_root, create_sec, self.project_path, "File Creation", create_debug_test)
        create_root.mainloop()
        if debug_test:
            print("In Gui -> END")

    def on_quit_chosen(self):
        """This gives a messagebox when either quit or escape is chosen"""
        if tkinter.messagebox.askokcancel("Exit?", "Have you saved your work?"):
            self.root.destroy()  # closes window and destroys tkinter object

    def on_show_clicked(self):
        '''When clicked will show the supply/demand graph and seller/buyer values of chosen data file'''
        self.sec.load_file(self.project_path + "/" + str(self.string_data.get()))
        data_frame = tk.LabelFrame(self.root, text="Data File Information")
        data_frame.grid(row=2, column=0)
        tk.Label(data_frame, text="Buyers: " + str(self.sec.get_num_buyers())).grid(row=0, column=0)
        tk.Label(data_frame, text="Sellers: " + str(self.sec.get_num_sellers())).grid(row=0, column=1)
        tk.Label(data_frame, text="Units: " + str(self.sec.get_num_units())).grid(row=0, column=2)
        tk.Label(data_frame, text=str(self.sec.get_supply_demand_list())).grid(row=1, column=0, columnspan=4)
        self.num_buyers = self.sec.get_num_buyers()
        self.num_sellers = self.sec.get_num_sellers()
        self.num_units = self.sec.get_num_units()
        self.sec.plot_gui(self.string_data.get())
        self.display_sd_info = True

    '''The function below checks to make sure that each variable is an integer'''
    def check_integer(self, check_var):
        try:
            int(check_var)  # check if integer
        except ValueError:  # value error raised if not
            self.parameters_trigger = True  # triggers parameter alarm
            messagebox.askokcancel("INTEGER ERRORS", "A parameter requiring a number is not a number \n --> Please check")
        else:
            pass  # else pass to next variable check

    '''The function below checks all parameters are set correctly, if not will throw error message boxes to user'''
    def on_set_parms_clicked(self):
        if self.display_sd_info == False:  # if show was not clicked will still display supply/demand information
            self.sec.load_file(self.project_path + "/" + str(self.string_data.get()))
            data_frame = tk.LabelFrame(self.root, text="Data File Information")
            data_frame.grid(row=2, column=0)
            tk.Label(data_frame, text="Buyers: " + str(self.sec.get_num_buyers())).grid(row=0, column=0)
            tk.Label(data_frame, text="Sellers: " + str(self.sec.get_num_sellers())).grid(row=0, column=1)
            tk.Label(data_frame, text="Units: " + str(self.sec.get_num_units())).grid(row=0, column=2)
            tk.Label(data_frame, text=str(self.sec.get_supply_demand_list())).grid(row=1, column=0, columnspan=4)
            self.num_buyers = self.sec.get_num_buyers()
            self.num_sellers = self.sec.get_num_sellers()
            self.num_units = self.sec.get_num_units()
        else:
            pass

        """The below message boxes will appear to the user if the parameters are not set"""
        self.parameters_trigger = False  # sets alarm to catch parameter errors
        # check that session name is not blank
        if self.string_session_name.get() == "":  # if blank
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("SESSION ERROR", "Session name has not been set \n --> Please type a session name")

        # check that starting data file has been set
        elif self.string_data.get() == "":  # if blank
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("DATA ERROR", "A starting data file was not selected \n --> Please choose one or create one")

        # check that period shocks are not blank
        elif self.string_period_shocks.get() == "":  # if blank
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("PERIOD SHOCK ERROR", "This entry is blank \n Please set to 0 if no shocks desired or enter the number of shocks")

        # check that round shocks are not blank
        elif self.string_round_shocks.get() == "":  # if blank
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("ROUND SHOCK ERROR", "This entry is blank \n Please set to 0 if no shocks desired or enter the number of shocks")

        # check that number of periods has been set
        elif self.string_periods.get() == "" or self.string_periods.get() == '0':  # if blank or 0
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("PERIOD ERROR", "Periods have not been set \n --> Please set the number of trading periods to run")

        # check that number of rounds are set
        elif self.string_rounds.get() == "" or self.string_rounds.get() == '0':
            self.parameters_trigger = True
            messagebox.askokcancel("ROUND ERROR", "Rounds have not been set \n --> Please set the number of rounds to run in each period")

        # check that minimum price floor has been set
        elif self.price_floor.get() == "":  # ok if price floor = 0 but if blank
            self.parameters_trigger = True  # trigger alarm
            messagebox.askokcancel("MIN PRICE ERROR", "Price floor does not have an entry \n --> Please set a minimum price for the market")

        # check that maximum price ceiling has been set
        elif self.price_ceiling.get() == "" or self.price_ceiling.get() == '0':
            self.parameters_trigger = True
            messagebox.askokcancel("MAX PRICE ERROR", "Price ceiling has not been set \n --> Please set a maximum price for the market")

        elif self.trader_replace.get() == 1:  # if instant shocks enabled
            if self.buyer_replace_strategy.get() == "":
                self.parameters_trigger = True
                tk.messagebox.askokcancel("TRADER REPLACEMENT ERROR", "New Buyer Strategy is not set \n --> Please set buyer shift strategy")
            elif self.seller_replace_strategy.get() == "":
                self.parameters_trigger = True
                tk.messagebox.askokcancel("TRADER REPLACEMENT ERROR", "New Seller Strategy is not set \n --> Please set seller shift strategy")
            else:
                parameters = [self.string_period_shocks.get(), self.string_round_shocks.get(), self.string_periods.get(),
                              self.string_rounds.get(), self.price_floor.get(), self.price_ceiling.get()]
                for i in parameters:
                    self.check_integer(i)
        else:  # check each parameter = integer
            parameters = [self.string_period_shocks.get(), self.string_round_shocks.get(), self.string_periods.get(), self.string_rounds.get(), self.price_floor.get(), self.price_ceiling.get()]
            for i in parameters:
                self.check_integer(i)

        if self.parameters_trigger == False:  # last error check is if price ceiling is greater than price floor
            if int(self.price_floor.get()) >= int(self.price_ceiling.get()):
                self.parameters_trigger = True
                messagebox.askokcancel("MAX/MIN ERROR", "Minimum price floor exceeds or equals maximum price ceiling \n --> Please correct this")

        # lastly ask user to make sure all parameters have been set correctly
        if self.parameters_trigger == False:  # if all error checks clean
            # if instant shocks enabled ask user to do parameter check
            if self.trader_replace.get() == 1:
                box = messagebox.askyesno("PROCEED?",
                                          "Check that parameters are set correctly \n Do you wish to continue?")
            # if round shocks and period shocks not set and instant shocks disabled...
            # ... let user know that no market shocks specified
            elif self.string_round_shocks.get() == "" or self.string_period_shocks.get() == "":
                box = messagebox.askyesno("PROCEED?", "No market shocks have been set \n Do you wish to continue?")
            # if instant shocks disabled but p shocks and r shocks set ask user to check params
            else:
                box = messagebox.askyesno("PROCEED?",
                                          "Check that parameters are set correctly \n Do you wish to continue?")
            if box == True:  # if user clicked "OK" on proceed message
                self.num_periods = int(self.string_periods.get())
                self.num_r_shocks = int(self.string_round_shocks.get())
                self.num_p_shocks = int(self.string_period_shocks.get())
                self.root.title(self.string_session_name.get())

                if self.num_p_shocks > 0:  # Build array if useful
                    self.pshock_values = self.build_array(self.num_p_shocks, self.num_p_shocks)
                if self.num_r_shocks > 0:  # Build array if useful
                    self.rshock_values = self.build_array(self.num_r_shocks, self.num_r_shocks)

                self.show_shock_frames()  # calls show_player_frames --> builds frame
                self.sec.set_market_parms([self.string_session_name.get(), self.num_buyers, self.num_sellers, self.num_units])
                run_frame = tk.LabelFrame(self.root, text="Run Simulation")
                run_frame.grid(row=1, column=3)
                run_button = tk.Button(run_frame, text="Run", width=4, command=self.check_sim)
                run_button.grid(row=0, column=0, padx=30)

            else:  # if user clicked "Cancel" on proceed message
                print("Continuing")
        else:
            pass  # hold for user to fix parameter errors

    def show_shock_frames(self):
        self.show_pshock_frame()  # show round shocks frame for entries
        self.show_rshock_frame()  # show period shocks frame for entries
        self.show_trader_strategies()  # show trader strategy frame for entries

    '''The function below creates ability for user to auto fill strategies in gui'''
    def auto_fill_strategies(self):
        for i in range(len(self.buyer_ids)):
            self.buyer_ids[i].set(self.autofill_strat.get())

        for i in range(len(self.seller_ids)):
            self.seller_ids[i].set(self.autofill_strat.get())

    '''The function below builds a frame within the gui so that the user can set strategies for the traders'''
    def show_trader_strategies(self):
        trader_frame = tk.LabelFrame(self.root, text="Trader Strategies")
        trader_frame.grid(row=2, column=3, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        # creates a button to explain strategies to user
        strat_info_button = tk.Button(trader_frame, text="Strategy Descriptions", width=16, command=self.strategy_message)
        strat_info_button.grid(row=0, column=0)

        self.buyer_ids = [k for k in range(self.num_buyers)]  # will become list of tk.stringvar()
        self.seller_ids = [k for k in range(self.num_sellers)]  # will become list of tk.stringvar()

        # create labels to identify entries
        tk.Label(trader_frame, text="ID").grid(row=1, column=0)
        tk.Label(trader_frame, text="Strategy").grid(row=1, column=1)
        tk.Label(trader_frame, text="ID").grid(row=1, column=2)
        tk.Label(trader_frame, text="Strategy").grid(row=1, column=3)

        autofill_button = tk.Button(trader_frame, text="Auto-fill Strategies", width=16, command=self.auto_fill_strategies)
        autofill_button.grid(row=0, column=2)
        autofill_strategy = ttk.Combobox(trader_frame, values=self.strategies, textvariable=self.autofill_strat, state='readonly')
        autofill_strategy.grid(row=0, column=3)
        self.autofill_strat.set(self.strategies[0])
        # these create cascading entries for the user to pick trader strategies
        for i in range(self.num_buyers):
            buyer_num = "Buyer" + str(i)
            tk.Label(trader_frame, text=buyer_num).grid(row=i + 2, column=0)

        for i in range(self.num_buyers):
            self.buyer_ids[i] = tk.StringVar()
            ttk.Combobox(trader_frame, values=self.strategies, textvariable=self.buyer_ids[i], state='readonly').grid(row=i + 2, column=1)

            # creates a drop down menu to choose strategies

        for i in range(self.num_sellers):
            seller_num = "Seller" + str(i)
            tk.Label(trader_frame, text=seller_num).grid(row=i + 2, column=2)

        for i in range(self.num_sellers):
            self.seller_ids[i] = tk.StringVar()
            ttk.Combobox(trader_frame, values=self.strategies, textvariable=self.seller_ids[i], state='readonly').grid(row=i + 2, column=3)

            # creates a drop down menu to choose strategies

    '''The function below creates a frame within the gui so that the user can set period shocks'''
    def show_pshock_frame(self):
        # TODO add these shocks to rum_sim()
        pf = tk.LabelFrame(self.root, text="Period Shock Entries")
        pf.grid(row=2, column=1, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)

        if self.num_p_shocks == 0: return   # Nothing to show

        self.p_shock_ids = [k for k in range(self.num_p_shocks)]  # will become list of tk.stringvar()
        self.p_shock_files = [k for k in range(self.num_p_shocks)]  # will become list of tk.stringvar()

        tk.Label(pf, text="ID").grid(row=0, column=0)
        tk.Label(pf, text="Shock Data File").grid(row=0, column=2)
        tk.Label(pf, text="Period").grid(row=0, column=1)
        for i in range(self.num_p_shocks):
            pshock_num = "P Shock #" + str(i + 1)
            tk.Label(pf, text=pshock_num).grid(row=i+1, column=0)
        for i in range(self.num_p_shocks):
            self.p_shock_ids[i] = tk.StringVar()
            tk.Entry(pf, width=5, justify=tk.CENTER,
                     textvariable=self.p_shock_ids[i]).grid(row=i + 1, column=1)

        for i in range(self.num_p_shocks):
            self.p_shock_files[i] = tk.StringVar()
            # TODO needs to be a way to refresh combobox values if user creates new file in market_gui
            ttk.Combobox(pf, values=os.listdir(self.project_path), textvariable=self.p_shock_files[i], state='readonly').grid(row=i + 1, column=2)
            plot_button = tk.Button(pf, text="Show", width=4, command=self.on_show_clicked)
            plot_button.grid(row=i + 1, column=3)

    '''The function below creates a frame within the gui so that the user can set round shocks'''
    def show_rshock_frame(self):
        # TODO add these shocks to run_sim()
        rf = tk.LabelFrame(self.root, text="Round Shock Entries")
        rf.grid(row=2, column=2, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_r_shocks == 0: return  # Nothing to show

        self.r_shock_ids = [k for k in range(self.num_r_shocks)]
        self.r_shock_files = [k for k in range(self.num_r_shocks)]

        tk.Label(rf, text="ID").grid(row=0, column=0)
        tk.Label(rf, text="Shock Data File").grid(row=0, column=2)
        tk.Label(rf, text="Round").grid(row=0, column=1)
        for i in range(self.num_r_shocks):
            rshock_num = "R Shock #" + str(i + 1)
            tk.Label(rf, text=rshock_num).grid(row=i + 1, column=0)
        for i in range(self.num_r_shocks):
            self.r_shock_ids[i] = tk.StringVar()
            tk.Entry(rf, width=5, justify=tk.CENTER,
                     textvariable=self.r_shock_ids[i]).grid(row=i + 1, column=1)

        for i in range(self.num_r_shocks):
            self.r_shock_files[i] = tk.StringVar()
            ttk.Combobox(rf, values=os.listdir(self.project_path), textvariable=self.r_shock_files[i], state='readonly').grid(row=i + 1, column=2)
            plot_button = tk.Button(rf, text="Show", width=4, command=self.on_show_clicked)
            plot_button.grid(row=i+1, column=3)


    def show_info_bar_parms(self):
        self.string_period_shocks.set(str(self.num_p_shocks))
        self.string_round_shocks.set(str(self.num_r_shocks))
        self.string_periods.set(str(self.num_periods))

    def open_file(self, event=None):
        input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".csv",
                                                             filetypes=[("All Files", "*.*"),
                                                                        ("Text Documents", "*.txt")])  # accepts chosen file
        if input_file_name:
            # global file_name
            self.file_name = input_file_name
            self.name = os.path.basename(self.file_name)
            index = self.name.find(".")   # look for start of .csv
            self.name = self.name[:index]  # pulls file from directory/file path
            self.root.title('{}'.format(self.name))
            self.sec.load_file(self.file_name)
            #self.show_project()

    def save(self, event=None):  # saves file in it's path location
        """We want to create a messagebox that asks if the user wants to overwrite the current file"""
        # TODO:  Add existing file check
        self.project_path += self.string_session_name.get()
        self.sec.save_project(self.project_path)

    def display_about_messagebox(self, event=None):
        # displays about message
        tkinter.messagebox.showinfo("About", "{}{}".format(self.name,
                                                           "\n\nCenter for the Study of Neuroeconomics\n\n Created by Alex Payne"))

    def display_help_messagebox(self, event=None):  # displays help messages when message link clicked
        help_msg = "Quick Help: \n\n"
        help_msg += "   Getting Started \n"
        help_msg += "      1). Enter unique session name \n"
        help_msg += "      2). Enter number of period shocks \n"
        help_msg += "      3). Enter number of round shocks \n"
        help_msg += "      4). Enter starting data set \n"
        help_msg += "      5). Click Set Button \n"
        help_msg += "          a). Say yes to message box \n"
        help_msg += "          b). Period and round shock entries displayed \n"
        tkinter.messagebox.showinfo("Help", help_msg)

    '''The function below activates when the user clicks the Run button within the gui...
    ... it checks for errors in the secondary parameters such as trader strategies, round shocks, and period shocks
    ... also creates data folder for all simulation results to be stored in'''
    def check_sim(self):
        # code below checks that the user has set all trading strategies
        self.strategy_trigger = False  # alarm off
        for i in range(self.num_buyers):
            if self.buyer_ids[i].get() == "":
                self.strategy_trigger = True  # alarm triggered

        for i in range(self.num_sellers):
            if self.seller_ids[i].get() == "":
                self.strategy_trigger = True  # alarm triggered

        if self.strategy_trigger == False:
            # the error checks below will look to see if trader replace is enabled...
            # ... if they are: will check to make sure shift strategy is set
            # ... if not: will check to make sure period and round shocks ids and files are set
            self.r_shock_trigger = False  # sets alarms for p shocks and r shocks
            for i in range(self.num_r_shocks):  # look through round shock entries
                if self.r_shock_ids[i].get() == "":  # if any entries blank
                    self.r_shock_trigger = True  # trigger alarm

                elif self.r_shock_files[i].get() == "":  # if blank
                    self.r_shock_trigger = True  # trigger alarm

                else:
                    try:
                        int(self.r_shock_ids[i].get())  # check if integer
                        if int(self.r_shock_ids[i].get()) > int(self.string_rounds.get()):  # round to shock <= rounds
                            self.r_shock_trigger = True
                    except ValueError:  # value error raised if not
                        self.r_shock_trigger = True  # triggers parameter alarm
                        raise
                    else:
                        pass  # else pass to next variable check

            if self.r_shock_trigger == False:
                self.p_shock_trigger = False
                for i in range(self.num_p_shocks):
                    if self.p_shock_ids[i].get() == "":
                        self.p_shock_trigger = True

                    elif self.p_shock_files[i].get() == "":
                        self.p_shock_trigger = True

                    else:
                        try:
                            int(self.r_shock_ids[i].get())  # check if integer
                            if self.p_shock_ids[i].get() > self.string_periods.get():
                                self.p_shock_trigger = True
                        except ValueError:  # value error raised if not
                            self.p_shock_trigger = True  # triggers parameter alarm
                            raise
                        else:
                            pass  # else pass to next variable check

                if self.p_shock_trigger == False:
                    self.replace_trader_trigger = False  # set alarm
                    if self.trader_replace.get() == 1:  # if trader replacement enabled after clicking the Set button
                        if self.buyer_replace_strategy.get() == "":  # if blank
                            self.replace_trader_trigger = True  # trigger trader replace error
                            tk.messagebox.askokcancel("TRADER REPLACE ERROR",
                                                      "New Buyer Strategy has not been set \n --> Please check")
                        elif self.seller_replace_strategy.get() == "":  # if blank
                            self.replace_trader_trigger = True  # trigger trader replace error
                            tk.messagebox.askokcancel("TRADER REPLACE ERROR",
                                                      "New Seller Strategy has not been set \n --> Please check")
                        else:
                            pass  # else no errors found

                    else:
                        pass

                    if self.replace_trader_trigger == False:  # if no blanks in trader strategies
                        time_stamp = time.strftime("_h%Im%Ms%S", time.localtime())
                        session_name = self.string_session_name.get() + str(time_stamp)
                        os.makedirs(self.output_path + session_name)
                        self.run_sim(session_name)
                    else:
                        pass  # else hold for trader replacement fixes or cancellation from user
                else:
                    tk.messagebox.askokcancel("PERIOD SHOCK ERROR",
                                              "Error found in period shocks, please check the below requirements: \n"
                                              "--> period to shock is set \n"
                                              "--> period to shock is a whole number \n"
                                              "--> period shock data file is set \n"
                                              "To cancel these shocks, set Period Shocks to 0 and re-click the Set button")
                    pass  # else hold for period shock fixes or cancellation from user
            else:
                tk.messagebox.askokcancel("ROUND SHOCK ERROR",
                                          "Error found in round shocks, please check the below requirements: \n"
                                          "--> round to shock is set \n"
                                          "--> round to shock is a whole number \n"
                                          "--> round shock data file is set \n"
                                          "To cancel these shocks, set Round Shocks to 0 and re-click the Set button")
                pass  # else hold for round shock fixes or cancellation from user
        else:
            tk.messagebox.askokcancel("TRADER STRATEGIES ERROR",
                                      "Error found in trader strategies, please check the below requirements: \n"
                                      "--> each buyer has a strategy set \n"
                                      "--> each seller has a strategy set \n")
            pass  # else hold for trader strategy fixes from user

    '''This function will execute if no errors found in check_sim()...
    ... will create a new window to display simulation results to the user
    ... will also save all simulation results to a data folder'''
    def run_sim(self, session_name):
        '''Adding in a new window to run simulations in market_gui'''

        run_root = tk.Toplevel()  # creates top level root on main root
        # finds the dimension of user's computer screen and sizes root to fit
        run_root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))

        # This obtains the strategies that the user sets in market_gui
        # returns a list of the trader's strategies
        strat_list = []
        for i in range(len(self.buyer_ids)):
            trader = self.buyer_ids[i].get()
            strat_list.append(trader)
        for i in range(len(self.seller_ids)):
            trader = self.seller_ids[i].get()
            strat_list.append(trader)

        p_shock_list = []
        r_shock_list = []
        for i in range(len(self.p_shock_ids)):
            p_shock_list.append([int(self.p_shock_ids[i].get()), self.p_shock_files[i].get()])
        for i in range(len(self.r_shock_ids)):
            r_shock_list.append([int(self.r_shock_ids[i].get()), self.r_shock_files[i].get()])

        print("Trader Strategies: " + str(strat_list))
        print("Length: " + str(len(strat_list)))
        print("\n")
        print("Period Shocks: " + str(p_shock_list))
        print("Round Shocks: " + str(r_shock_list))
        print("\n")
        eff = []
        periods_list = []
        act_surplus = []
        maxi_surplus = []
        session = session_name

        num_periods = int(self.string_periods.get())  # periods or trading days
        limits = (int(self.price_ceiling.get()), int(self.price_floor.get()))  # price ceiling, price floor
        rounds = int(self.string_rounds.get())  # rounds in each period (can substitute time clock)
        name = "trial"
        period = 0  # ...??
        '''The code below creates a file for your session name for market run info to be dumped into...
        ... will raise file error if session name not changed --> prevents overwriting previous runs'''

        smp = Simulator.spot_market_period.SpotMarketPeriod(session, num_periods, limits)

        # --> could put this in json data file
        trader_names = strat_list

        smp.init_spot_system_gui(name, limits, rounds, self.project_path, self.string_data.get(), self.output_path,
                                session)
        rnd_traders = trader_names  # because shuffle shuffles the list in place, returns none
        times = []
        for k in range(int(self.string_periods.get())):  # iterates through number of periods or "trading days"
            timer_start = timer()
            periods_list.append(k)
            # random.shuffle(rnd_traders)  # shuffles trader order per period  # TODO random shuffle or no?
            smp.init_traders(rnd_traders, k)
            print("**** Running Period {}".format(k))  # provides visual effect in editor
            smp.run_period(period, session, self.trader_replace.get(),
                           self.buyer_replace_strategy.get(), self.seller_replace_strategy.get(),
                           self.num_buyers, self.num_sellers)  # runs period
            timer_stop = timer()  # ends period timer
            results = smp.eval()  # evaluation function called --> returns data
            '''the below data is appended into global dictionaries'''
            eff.append(results[8])  # appends the efficiencies per period
            act_surplus.append(results[7])  # appends actual surplus per period
            maxi_surplus.append(results[6])  # appends maximum surplus per period
            smp.get_contracts()  # gets transaction prices and period endpoints
            session_folder = self.output_path + session + "\\"  # establishes file path for session data folder
            smp.record_session_data(session_folder)  # records session data in excel csv
            time = timer_stop - timer_start  # period execution time
            times.append(time)  # list of execution times --> sum=total execution time

        # TODO add the tk.label information below to a json file so information can be saved to period data

        # creates frame to display parameters that were set before running the simulation
        info_frame = tk.LabelFrame(run_root, text="Parameters", font='bold')
        info_frame.grid(row=1, column=0)
        tk.Label(info_frame, text="Session Name: " + str(session)).grid(row=0, column=0)
        tk.Label(info_frame, text="Data Used: " + str(self.string_data.get())).grid(row=1, column=0)
        tk.Label(info_frame, text="Execution Time: " + str(sum(times))).grid(row=2, column=0)
        tk.Label(info_frame, text="Buyers: " + str(self.num_buyers) + "   " + "Sellers: " + str(self.num_sellers)).grid(row=3, column=0)
        tk.Label(info_frame, text="Periods: " + str(self.num_periods) + "   " + "Rounds: " + str(self.num_rounds)).grid(row=4, column=0)
        tk.Label(info_frame, text="Units: " + str(self.num_units)).grid(row=5, column=0)


        # creates a frame to display instant shocks if enabled
        if self.trader_replace.get() == 1:
            move_column = 2  # will change column position of next tk.labelframe
            trader_replace_frame = tk.LabelFrame(run_root, text="Trader Replacement", font='bold')
            trader_replace_frame.grid(row=1, column=1)
            tk.Label(trader_replace_frame, text="New Buyer Strategy: " + str(self.buyer_replace_strategy.get())).grid(row=1, column=0)
            tk.Label(trader_replace_frame, text="New Seller Strategy: " + str(self.seller_replace_strategy.get())).grid(row=3, column=0)
        else:
            move_column = 1  # if no instant shocks then next tk.labelframe column =1
            pass

        # creates a frame for simulation results
        run_frame = tk.LabelFrame(run_root, text="Simulation Results", font='bold')
        run_frame.grid(row=1, column=move_column)  # set parameters
        tk.Label(run_frame, text="Maximum Surpluses: " + str(maxi_surplus)).grid(row=0, column=0)
        tk.Label(run_frame, text="Actual Surpluses: " + str(act_surplus)).grid(row=1, column=0)
        tk.Label(run_frame, text="Avg. Market Surplus: " + str(sum(act_surplus)/len(act_surplus))).grid(row=2, column=0)
        tk.Label(run_frame, text="\nMarket Efficiencies: " + str(eff)).grid(row=3, column=0)
        tk.Label(run_frame, text="Avg. Efficiency: " + str(sum(eff) / num_periods)).grid(row=4, column=0)

        # prints to editor
        print("Period Times: " + str(times))
        print("Market Efficiencies:" + str(eff))  # print market efficiencies
        print("Avg. Efficiency:" + str(sum(eff) / num_periods))  # print avg efficiency
        # print("Total Avg. Transaction Price:" + str(sum(avg_prices[1:])/(num_periods - 1)))
        print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
        print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
        print()

        # TODO trader info below can be functionalized further
        # builds frame for trader total earnings
        trader_frame1 = tk.LabelFrame(run_root, text="Strategy Total Earnings (per period)", font='bold')
        trader_frame1.grid(row=1, column=2)  # set parameters
        tk.Label(trader_frame1, text="Trader_AA: " + str(smp.total_earns('AA'))).grid(row=0, column=0)
        tk.Label(trader_frame1, text="Trader_GD: " + str(smp.total_earns('GD'))).grid(row=1, column=0)
        tk.Label(trader_frame1, text="Trader_PS: " + str(smp.total_earns('PS'))).grid(row=2, column=0)
        tk.Label(trader_frame1, text="Trader_ZIP: " + str(smp.total_earns('ZIP'))).grid(row=3, column=0)
        tk.Label(trader_frame1, text="Trader_Kaplan: " + str(smp.total_earns('KP'))).grid(row=4, column=0)
        tk.Label(trader_frame1, text="Trader_Shaver: " + str(smp.total_earns('SI'))).grid(row=5, column=0)
        tk.Label(trader_frame1, text="Trader_ZIC: " + str(smp.total_earns('ZIC'))).grid(row=6, column=0)

        # print to editor
        print("Strategy Total Earnings")
        print("Trader_AA: " + str(smp.total_earns('AA')))
        # print("Trader_AI: " + str(smp.total_earns('AI')))
        print("Trader_GD: " + str(smp.total_earns('GD')))  #
        print("Trader_PS: " + str(smp.total_earns('PS')))  # ADDED: section to list total avg earns
        # print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
        print("Trader_ZIP: " + str(smp.total_earns('ZIP')))  #
        print("Trader_ZIC: " + str(smp.total_earns('ZIC')))  #
        print("Trader_Kaplan: " + str(smp.total_earns('KP')))
        print("Trader_Shaver: " + str(smp.total_earns('SI')))
        print()

        # builds frame for trader avg earnings
        trader_frame2 = tk.LabelFrame(run_root, text="Strategy Total Avg. Earnings (per trader)", font='bold')
        trader_frame2.grid(row=1, column=3)  # set parameters
        tk.Label(trader_frame2, text="Trader_AA: " + str(smp.total_avg_earns('AA', trader_names.count('Trader_AA') * num_periods))).grid(row=0, column=0)
        tk.Label(trader_frame2, text="Trader_GD: " + str(smp.total_avg_earns('GD', trader_names.count('Trader_GD') * num_periods))).grid(row=1, column=0)
        tk.Label(trader_frame2, text="Trader_PS: " + str(
            smp.total_avg_earns('PS', trader_names.count('Trader_PS') * num_periods))).grid(row=2, column=0)
        tk.Label(trader_frame2, text="Trader_ZIP: " + str(smp.total_avg_earns('ZIP', trader_names.count('Trader_ZIP') * num_periods))).grid(row=3, column=0)
        tk.Label(trader_frame2, text="Trader_Kaplan: " + str(smp.total_avg_earns('KP', trader_names.count('Trader_Kaplan') * num_periods))).grid(row=4, column=0)
        tk.Label(trader_frame2, text="Trader_Shaver: " + str(smp.total_avg_earns('SI', trader_names.count('Trader_Shaver') * num_periods))).grid(row=5, column=0)
        tk.Label(trader_frame2, text="Trader_ZIC: " + str(smp.total_avg_earns('ZIC', trader_names.count('Trader_ZIC') * num_periods))).grid(row=6, column=0)

        # prints to editor
        print("Strategy Total Avg. Earnings (per trader)")
        print("Trader_AA: " + str(smp.total_avg_earns('AA', trader_names.count('Trader_AA') * num_periods)))  #
        print("Trader_GD: " + str(smp.total_avg_earns('GD', trader_names.count('Trader_GD') * num_periods)))  #
        print("Trader_PS: " + str(
            smp.total_avg_earns('PS', trader_names.count('Trader_PS') * num_periods)))  # ADDED: section to list total avg earns
        # print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
        print("Trader_ZIP: " + str(smp.total_avg_earns('ZIP', trader_names.count('Trader_ZIP') * num_periods)))  #
        print("Trader_ZIC: " + str(smp.total_avg_earns('ZIC', trader_names.count('Trader_ZIC') * num_periods)))  #
        print("Trader_Kaplan: " + str(smp.total_avg_earns('KP', trader_names.count('Trader_Kaplan') * num_periods)))
        print("Trader_Shaver: " + str(smp.total_avg_earns('SI', trader_names.count('Trader_Shaver') * num_periods)))

        """The below function calls create graphs from the simulation results and save in project path"""
        smp.get_avg_trade_ratio()  # prints avg trade ratio for all periods
        smp.graph_trader_eff(self.output_path, session)  # plots individual efficiency
        smp.graph_efficiency_gui(self.output_path, session, eff, periods_list)  # plots period efficiency
        smp.get_endpoints()  # obtains endpoints of periods for graph
        smp.graph_contracts(self.output_path, session)  # graphs contract transactions and avg transaction per period
        # smp.graph_surplus()  # graphs actual and max surplus
        smp.graph_alphas(self.output_path, session, periods_list)  # graphs Smith's Alpha of convergence
        smp.graph_distribution(self.output_path, session)  # graphs normal distribution of trader efficiencies

        from PIL import Image  # import python image library
        new_size = 400, 225  # makes original image smaller
        temp_folder = self.output_path + session + "\\" + "Mini Images"
        os.makedirs(temp_folder)  # makes a temp folder to store mini images

        # below builds a frame to display the smaller transactions graph
        graph_frame1 = tk.LabelFrame(run_root, text="Transactions", font='bold')  # frame created in run root
        graph_frame1.grid(row=2, column=1)
        edit = Image.open(self.output_path + session + '\\' + "Transactions.png")  # accesses original image
        edit.thumbnail(new_size, Image.ANTIALIAS)  # turns the image into a thumbnail size
        edit.save(temp_folder + '\\' + "Transactions Mini.png")  # saves new file
        photo = tk.PhotoImage(file=temp_folder + '\\' + "Transactions Mini.png")  # accesses new image
        label = tk.Label(graph_frame1, image=photo)  # turns into tk label and packs into frame
        label.pack()

        # below builds a frame to display the smaller SD graph
        sd_frame = tk.LabelFrame(run_root, text="Supply and Demand", font='bold')  # new frame in run root
        sd_frame.grid(row=2, column=0)
        edit2 = Image.open(self.output_path + session + '\\' + "SD Before.png") # old image accessed
        edit2.thumbnail(new_size, Image.ANTIALIAS)  # old image turned into thumbnail
        edit2.save(temp_folder + '\\' + "SD Mini.png")  # new image saved
        photo2 = tk.PhotoImage(file=temp_folder + '\\' + "SD Mini.png")  # new image accessed
        label2 = tk.Label(sd_frame, image=photo2)  # turned into label and packed into frame
        label2.pack()

        # below builds a frame to display the distribution of trader efficiencies
        stat_frame = tk.LabelFrame(run_root, text="Trader Efficiency Distribution", font='bold')  # new frame in run root
        stat_frame.grid(row=2, column=2)
        edit3 = Image.open(self.output_path + session + '\\' + "Efficiency Distribution.png")  # old image accessed
        edit3.thumbnail(new_size, Image.ANTIALIAS)  # old image turned into thumbnail
        edit3.save(temp_folder + '\\' + "Eff Dist Mini.png")  # new image saved
        photo3 = tk.PhotoImage(file=temp_folder + '\\' + "Eff Dist Mini.png")  # new image accessed
        label3 = tk.Label(stat_frame, image=photo3)  # turned into label and packed into frame
        label3.pack()

        t_eff_frame = tk.LabelFrame(run_root, text="Efficiency by Trader", font='bold')
        t_eff_frame.grid(row=3, column=2)
        edit4 = Image.open(self.output_path + session + "\\" + "Trader Efficiencies.png")
        edit4.thumbnail(new_size, Image.ANTIALIAS)
        edit4.save(temp_folder + "\\" + "T Eff Mini.png")
        photo4 = tk.PhotoImage(file=temp_folder + "\\" + "T Eff Mini.png")
        label4 = tk.Label(t_eff_frame, image=photo4)
        label4.pack()

        p_eff_frame = tk.LabelFrame(run_root, text="Efficiency by Period", font='bold')
        p_eff_frame.grid(row=3, column=1)
        edit5 = Image.open(self.output_path + session + "\\" + "Period Efficiencies.png")
        edit5.thumbnail(new_size, Image.ANTIALIAS)
        edit5.save(temp_folder + "\\" + "P Eff Mini.png")
        photo5 = tk.PhotoImage(file=temp_folder + "\\" + "P Eff Mini.png")
        label5 = tk.Label(p_eff_frame, image=photo5)
        label5.pack()

        alpha_frame = tk.LabelFrame(run_root, text="Convergence Alphas", font='bold')
        alpha_frame.grid(row=3, column=0)
        edit6 = Image.open(self.output_path + session + "\\" + "Convergence Alphas.png")
        edit6.thumbnail(new_size, Image.ANTIALIAS)
        edit6.save(temp_folder + "\\" + "Alphas Mini.png")
        photo6 = tk.PhotoImage(file=temp_folder + "\\" + "Alphas Mini.png")
        label6 = tk.Label(alpha_frame, image=photo6)
        label6.pack()

        import shutil  # allows removal of non-empty directory
        shutil.rmtree(temp_folder)  # remove temp folder of resized images... no longer needed
        # below creates a statistics frame to display next to trader efficiency distribution graph
        stat_frame = tk.LabelFrame(run_root, text="Trader Efficiency Statistics")
        stat_frame.grid(row=2, column=3)

        t_effs = smp.trader_eff_gui()  # list of trader efficiencies
        mean = np.mean(t_effs)  # numpy function to get average
        std_dev = np.std(t_effs)  # numpy function to get standard deviation
        median = np.median(t_effs)  # numpy function to get median
        max = np.max(t_effs)  # numpy function to get maximum value
        min = np.min(t_effs)  # numpy function to get minimum value

        for i in range(t_effs.count(0)):  # removes traders with 0 efficiency
            t_effs.remove(0)
        mean2 = np.mean(t_effs)  # numpy function to get average
        std_dev2 = np.std(t_effs)  # numpy function to get standard deviation
        median2 = np.median(t_effs)  # numpy function to get median
        max2 = np.max(t_effs)  # numpy function to get maximum value
        min2 = np.min(t_effs)  # numpy function to get minimum value

        tk.Label(stat_frame, text="All Traders", font='bold').grid(row=0, column=0)
        tk.Label(stat_frame, text="Mean: {}   Std Dev: {}".format(mean, std_dev)).grid(row=1, column=0)
        tk.Label(stat_frame, text="Median: {}   Max: {}   Min: {}".format(median, max, min)).grid(row=2, column=0)
        tk.Label(stat_frame, text="").grid(row=3, column=0)
        tk.Label(stat_frame, text="Out of Market Traders Removed", font='bold').grid(row=4, column=0)
        tk.Label(stat_frame, text="Mean: {}   Std Dev: {}".format(mean2, std_dev2)).grid(row=5, column=0)
        tk.Label(stat_frame, text="Median: {}   Max: {}   Min: {}".format(median2, max2, min2)).grid(row=6, column=0)

        eff.clear()
        strat_list.clear()
        periods_list.clear()  # not sure if clearing all these does anything...
        maxi_surplus.clear()
        act_surplus.clear()

        run_root.mainloop()  # continues running run root

if __name__ == "__main__":
    # setup gui
    # TODO can add this into mkt_root somehow...
    class file_path():
        def __init__(self, path_root):
            self.path_root = path_root
            self.project_path = None
            self.output_path = None
            self.path_frame = tk.LabelFrame(self.path_root, text="SET FILE PATHS")
            self.path_frame.grid(row=1, column=0, columnspan=3)
            tk.Label(self.path_frame, text="Project Path: ").grid(row=1, column=0)
            tk.Button(self.path_frame, text="Link Path", command=self.project_set_button).grid(row=1, column=2)

            tk.Label(self.path_frame, text="Simulation Save Path: ").grid(row=2, column=0)
            tk.Button(self.path_frame, text="Link Path", command=self.sim_path_set_button).grid(row=2, column=2)

            tk.Button(self.path_frame, text="Submit", command=self.submit_button).grid(row=3, column=0)
            self.path_root.mainloop()

        def project_set_button(self):
            chosen_file = tk.filedialog.askdirectory()
            self.project_path = chosen_file
            tk.Label(self.path_frame, text=self.project_path).grid(row=1, column=1)

        def sim_path_set_button(self):
            sim_save_file = tk.filedialog.askdirectory()
            self.output_path = sim_save_file
            tk.Label(self.path_frame, text=self.output_path).grid(row=2, column=1)

        def submit_button(self):
            if self.project_path == None:
                tk.messagebox.askokcancel("ERROR", "Project path has not been set \n Please set this file path")
            elif self.output_path == None:
                tk.messagebox.askokcancel("ERROR", "Sim Save Path has not been set \n Please set this file path")
            else:
                box = tk.messagebox.askyesno("File Check", "Have you set the right file paths?")
                if box == True:
                    self.path_root.destroy()
                else:
                    print("Continuing")

        def return_paths(self):
            return self.project_path, self.output_path

    path_root = tk.Tk()
    results = file_path(path_root)
    final_project_path = results.return_paths()[0]
    final_output_path = results.return_paths()[1]
    mkt_root = tk.Tk()
    debug_test = True
    if debug_test:
        print("In Gui -> START")
        print("---> Project Path: " + str(final_project_path))
        print("---> Output Path: " + str(final_output_path))
        sec = Environment.spot_environment_controller.SpotEnvironmentController(debug_test)
        gui = MarketGui(mkt_root, sec, final_project_path, final_output_path, "Data Entry", debug_test)
        mkt_root.mainloop()
    if debug_test:
        print("In Gui -> END")