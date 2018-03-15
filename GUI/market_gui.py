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
class MarketGui():
    def __init__(self, root, sec, name, debug=False):
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

        self.current_row = 0  # setting current read row to 0... self.current_row+1 would read next row
        self.current_row_contents = []
        self.ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # is this limiting the amount to 10 buyers and 10 sellers?
        self.file_name = None  # none is a placeholder to be filled

        # have to build matrices for future tkinter display
        self.pshock_values = self.build_array(self.num_r_shocks, self.num_r_shocks)  # matrix of buyers and number of units
        self.rshock_values = self.build_array(self.num_p_shocks, self.num_p_shocks)  # matrix of sellers and number of units
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)  # matrix of buyers and number of units
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)  # matrix of sellers and number of units

        # have to set local file path for icon images and project data
        #  TODO change these to your file path
        self.file_path = "C:\\Users\\alexd\\Desktop\\Repos\\DoubleAuctionMarket\\Data\\icons\\"
        self.project_path = "C:\\Users\\alexd\\Desktop\\Repos\\DoubleAuctionMarket\\Data\\projects"
        self.output_path = "C:\\Users\\alexd\\Desktop\\Repos\\DoubleAuctionMarket\\Data\\period data\\"
        self.data_files = os.listdir(self.project_path)

        # have to create small images for tkinter display... open file, save, etc.
        self.new_file_icon = tk.PhotoImage(file=self.file_path + 'new.png')
        self.open_file_icon = tk.PhotoImage(file=self.file_path + 'open.png')
        self.save_file_icon = tk.PhotoImage(file=self.file_path + 'save.png')  # calling images from icons folder
        self.cut_icon = tk.PhotoImage(file=self.file_path + 'cut.png')         # --> pulled from internet images
        self.copy_icon = tk.PhotoImage(file=self.file_path + 'copy.png')       # --> images edited/shrunk to meet scale
        self.paste_icon = tk.PhotoImage(file=self.file_path + 'paste.png')
        self.undo_icon = tk.PhotoImage(file=self.file_path + 'undo.png')
        self.redo_icon = tk.PhotoImage(file=self.file_path + 'redo.png')

        # have to build menu and start the project
        self.show_menu()  # executes menu build with toolbar and help/action messages
        self.show_shortcut()  # executes frame build in tkinter
        self.show_infobar()  # executes sub-frame for user entering number buyers, number sellers, units
        self.process_new_project()

        self.trigger = False  # safety feature when rerunning in gui: if same parameters used = True


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
                              compound='left', image=self.new_file_icon, underline=0, command=self.process_new_project)
        file_menu.add_command(label='Open', accelerator='Ctrl+O',
                              compound='left', image=self.open_file_icon, underline=0, command=self.open_file)
        file_menu.add_command(label='Save', accelerator='Ctrl+S',
                              compound='left', image=self.save_file_icon, underline=0, command=self.save)
        #file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', accelerator='Alt+F4', command=self.on_quit_chosen)
        menu_bar.add_cascade(label='File', menu=file_menu)  # allows toolbar tab to drop down with multiple choices

        # create about/help menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='About', command=self.display_about_messagebox)  # click = display about message
        about_menu.add_command(label='Help', command=self.display_help_messagebox)  # click = display help message
        menu_bar.add_cascade(label='Misc', menu=about_menu)  # drop down menu
        self.root.config(menu=menu_bar)  # makes menu setup final

    def show_shortcut(self):
        shortcut_bar = tk.Frame(self.root)  # creates a frame within the tkinter object
        shortcut_bar.grid(row=0, column=0, columnspan=4, sticky='W')  # setting parameters of frame

    def show_infobar(self):
        info_bar = tk.LabelFrame(self.root, height=15, text=str(self.name))  # creates a label frame for initial inputs
        info_bar.grid(row=1, column=0, columnspan=4, sticky='W', padx=5, pady=5)  # set parameters

        # create project name label
        tk.Label(info_bar, text="Session Name:").grid(row=0, column=0)
        tk.Entry(info_bar, width=15, justify=tk.LEFT, textvariable=self.string_session_name).grid(row=0, column=1)

        # create number of buyers label
        tk.Label(info_bar, text="Period Shocks:").grid(row=0, column=2)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_period_shocks).grid(row=0, column=3)
        self.string_period_shocks.set(str(self.num_p_shocks))  # sets initial display value at self.num_buyers = 0

        # create number of sellers label
        tk.Label(info_bar, text="Round Shocks:").grid(row=0, column=4)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_round_shocks).grid(row=0, column=5)
        self.string_round_shocks.set(str(self.num_r_shocks))  # sets initial display value at self.num_sellers = 0

        # create number of units label
        tk.Label(info_bar, text="Periods:").grid(row=0, column=6)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_periods).grid(row=0, column=7)
        self.string_periods.set(str(self.num_periods))  # sets initial display value at self.num_units = 0

        tk.Label(info_bar, text="Rounds:").grid(row=0, column=8)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_rounds).grid(row=0, column=9)
        self.string_rounds.set(str(self.num_rounds))  # sets initial display value at self.num_units = 0

        tk.Label(info_bar, text="Starting Data File:").grid(row=1, column=0)  # create/grid location
        ttk.Combobox(info_bar, values=os.listdir(self.project_path), textvariable=self.string_data).grid(row=1, column=1)
        self.string_data.set("Select")

        plot_button = tk.Button(info_bar, text="Show", width=4, command=self.on_show_clicked)
        plot_button.grid(row=1, column=2)

        tk.Label(info_bar, text="Price Floor:").grid(row=1, column=3)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.price_floor).grid(row=1, column=4)
        self.price_floor.set(str(self.floor))

        tk.Label(info_bar, text="Price Ceiling:").grid(row=1, column=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.price_ceiling).grid(row=1, column=6)
        self.price_ceiling.set(str(self.ceiling))

        # create a button with action input (command = click)
        info_button = tk.Button(info_bar, text="Set", width=4,
                                command=self.on_set_parms_clicked)
        info_button.grid(row=1, column=7, padx=10, pady=5)  # creates grids in both built frames
        # create Equilibrium Q label

        run_frame = tk.LabelFrame(self.root, height=15, text="RUN SIMULATION")
        run_frame.grid(row=1, column=11, columnspan=2, sticky='E', padx=15, pady=5)
        run_button = tk.Button(run_frame, text="RUN", width=4, command=self.run_sim)
        run_button.grid(row=0, column=1, padx=30)

        create_frame = tk.LabelFrame(self.root, height=15, text="New Supply Demand")
        create_frame.grid(row=1, column=9, columnspan=2, sticky='E', padx=15, pady=5)
        create_button = tk.Button(create_frame, text="CREATE", width=6, command=self.on_create_clicked)
        create_button.grid(row=0, column=1, padx=30)
        mini_root = tk.Toplevel()
        mini_root.geometry("200x200")
        path_frame = tk.LabelFrame(mini_root, text="SET FILE PATHS")
        path_frame.grid(row=0, column=0)
        tk.Label(path_frame, text="Project Path: ").grid(row=1, column=0)
        tk.Button(path_frame, text="SET", command=self.project_set_button).grid(row=1, column=1)
        tk.Label(path_frame, text="Simulation Save Path: ").grid(row=2, column=0)
        tk.Button(path_frame, text="SET", command=self.sim_path_set_button).grid(row=2, column=2)
        mini_root.mainloop()

    def project_set_button(self):
        chosen_file = tk.filedialog.askdirectory()
        self.project_path = chosen_file
        print(self.project_path)

    def sim_path_set_button(self):
        sim_save_file = tk.filedialog.askdirectory()
        self.output_path = sim_save_file
        print(self.output_path)

    def refresh_files(self):
        self.data_files = os.listdir(self.project_path)

    def on_create_clicked(self):
        '''Added ability to run spot_environment_gui in market_gui... allows new SD creation'''
        create_root = tk.Toplevel()
        create_debug_test = True
        if create_debug_test:
            print("In Gui -> START")
        create_sec = Environment.spot_environment_controller.SpotEnvironmentController(create_debug_test)
        create_gui = GUI.spot_environment_gui.SpotEnvironmentGui(create_root, create_sec, "File Creation", create_debug_test)
        create_root.mainloop()
        if debug_test:
            print("In Gui -> END")

    def on_quit_chosen(self):
        """This gives a messagebox when either quit or escape is chosen"""
        if tkinter.messagebox.askokcancel("Exit?", "Have you saved your work?"):
            self.root.destroy()  # closes window and destroys tkinter object

    def set_market(self):
        """ Sends all values on screen to model"""
        # Start with name and all that
        if self.debug:
            print("In Gui -> set_market -> begin")
        self.sec.set_market_parms([self.string_session_name.get(), self.num_p_shocks, self.num_r_shocks,
                                   self.num_periods])
        make_d = {}

        # Now Add Buyer Values and Seller Costs
        make_d["buyers"] = {}
        for k in range(self.num_p_shocks):
            make_d["buyers"][k] = []
            for j in range(self.num_periods):
                make_d["buyers"][k].append(int(self.pshock_values[k][j].get()))

        # make_d["sellers"] = {}
        # for k in range(self.num_sellers):
        #     make_d["sellers"][k] = []
        #     for j in range(self.num_units):
        #         make_d["sellers"][k].append(int(self.seller_costs[k][j].get()))

        # now make supply and demand
        if self.debug:
            print("In Gui -> set_market -> make_d")
            self.show_market(make_d)

        self.sec.make_market(make_d)
        self.sec.make_supply()
        self.sec.make_demand()
        if self.debug:
            print("In Gui -> set_market -> end")

    def show_market(self, make_d):

        if self.debug:
            print("In Gui -> show_market -> begin")
        print("... name = {}".format(self.name))
        print("... num_period_shocks = {}".format(self.num_p_shocks))
        print("... num_round_shocks = {}".format(self.num_r_shocks))
        print("... num_periods = {}".format(self.num_periods))

        # for k in range(self.num_buyers):
        #     print("... make_d[buyers][{}] = {}".format(k, make_d["buyers"][k]))
        # for k in range(self.num_sellers):
        #     print("... make_d[sellers][{}] = {}".format(k, make_d["sellers"][k]))

        if self.debug:
            print("In Gui -> show_market -> end")

    def on_show_clicked(self):
        '''When clicked will show the supply/demand graph and seller/buyer values of chosen data file'''
        self.sec.load_file(self.project_path + "\\" + str(self.string_data.get()))
        data_frame = tk.LabelFrame(self.root, text="Data File Information")
        data_frame.grid(row=2, column=0)
        tk.Label(data_frame, text="Buyers: " + str(self.sec.get_num_buyers())).grid(row=0, column=0)
        tk.Label(data_frame, text="Sellers: " + str(self.sec.get_num_sellers())).grid(row=0, column=1)
        tk.Label(data_frame, text="Units: " + str(self.sec.get_num_units())).grid(row=0, column=2)
        tk.Label(data_frame, text=str(self.sec.get_supply_demand_list())).grid(row=1, column=0, columnspan=4)
        self.num_buyers = self.sec.get_num_buyers()
        self.num_sellers = self.sec.get_num_sellers()
        self.num_units = self.sec.get_num_units()
        #tk.Label(data_frame, text="Buyer Values: " + str(self.sec.get_buyer_values())).grid(row=1, column=0)
        #tk.Label(data_frame, text="Seller Costs: " + str(self.sec.get_seller_costs())).grid(row=2, column=0)
        self.sec.plot_gui(self.string_data.get())



    def on_set_parms_clicked(self):
        """The below message boxes will appear to the user if the parameters are not set"""

        print(self.string_data.get())
        # check if session name file exists
        try:
            os.makedirs(self.output_path + self.string_session_name.get())  # creates folder for session data
        except FileExistsError:
            messagebox.askokcancel("FILE ERROR", "Session file name already exists... \n Please rename session \n OR \n Please delete previous file in project_path")
            raise  # raises error if folder already exists

        # check that starting data file has been set
        if self.string_data.get() == "Select":
            messagebox.askokcancel("DATA ERROR", "A starting data file was not selected \n Please choose one or create one")

        # check that number of periods has been set
        elif self.string_periods.get() == '0':
            messagebox.askokcancel("PERIOD ERROR", "Periods have not been set \n Please set the number of trading periods to run")

        # check that number of rounds are set
        elif self.string_rounds.get() == '0':
            messagebox.askokcancel("ROUND ERROR", "Rounds have not been set \n Please set the number of rounds to run in each period")

        # check that maximum price ceiling has been set
        elif self.price_ceiling.get() == '0':
            messagebox.askokcancel("MAX PRICE ERROR", "Price ceiling has not been set \n Please set a maximum price for the market")

        # lastly ask user to make sure all parameters have been set correctly
        else:
            messagebox.askyesno("PROCEED?", "Please make sure all parameters are set correctly \n Do you wish to continue?")
            return

        # this will be used when user presses run after already running... will need to recheck session file
        self.trigger = True  # TODO implement in def run_sim()

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



    def show_shock_frames(self):
        self.show_pshock_frame()
        self.show_rshock_frame()

    def show_pshock_frame(self):
        pf = tk.LabelFrame(self.root, text="Period Shock Entries")
        pf.grid(row=2, column=1, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_p_shocks == 0: return   # Notihing to show
        self.buttons = [[None for x in range(3)] for x in range(self.num_p_shocks + self.num_r_shocks)]

        pshock_ids = [k for k in range(self.num_p_shocks)]
        tk.Label(pf, text="ID").grid(row=0, column=0)
        tk.Label(pf, text="Shock Data File").grid(row=0, column=2)
        tk.Label(pf, text="Period").grid(row=0, column=1)
        for i in range(self.num_p_shocks):
            pshock_num = "P Shock #" + str(i + 1)
            tk.Label(pf, text=pshock_num).grid(row=i+1, column=0)
        for i in range(self.num_p_shocks):
            pshock_ids[i] = tk.StringVar()
            tk.Entry(pf, width=5, justify=tk.CENTER,
                     textvariable=pshock_ids[i]).grid(row=i + 1, column=1)
            pshock_ids[i].set("")
        for i in range(self.num_p_shocks):
            ttk.Combobox(pf, values=os.listdir(self.project_path), textvariable=self.new_string_data).grid(row=i + 1, column=2)
            plot_button = tk.Button(pf, text="Show", width=4, command=self.on_show_clicked)
            plot_button.grid(row=i + 1, column=3)

    #
    def show_rshock_frame(self):
        rf = tk.LabelFrame(self.root, text="Round Shock Entries")
        rf.grid(row=2, column=2, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_r_shocks == 0: return  # Nothing to show
        rshock_ids = [k for k in range(self.num_r_shocks)]
        tk.Label(rf, text="ID").grid(row=0, column=0)
        tk.Label(rf, text="Shock Data File").grid(row=0, column=2)
        tk.Label(rf, text="Round").grid(row=0, column=1)
        for i in range(self.num_r_shocks):
            rshock_num = "R Shock #" + str(i + 1)
            tk.Label(rf, text=rshock_num).grid(row=i + 1, column=0)
        for i in range(self.num_r_shocks):
            rshock_ids[i] = tk.StringVar()
            tk.Entry(rf, width=5, justify=tk.CENTER,
                     textvariable=rshock_ids[i]).grid(row=i + 1, column=1)
            rshock_ids[i].set("")
        for i in range(self.num_r_shocks):
            ttk.Combobox(rf, values=os.listdir(self.project_path), textvariable=self.new_string_data).grid(row=i + 1, column=2)
            plot_button = tk.Button(rf, text="Show", width=4, command=self.on_show_clicked)
            plot_button.grid(row=i+1, column=3)
    #
    def show_info_bar_parms(self):
        self.string_period_shocks.set(str(self.num_p_shocks))
        self.string_round_shocks.set(str(self.num_r_shocks))
        self.string_periods.set(str(self.num_periods))

    def process_new_project(self, event=None):
        if self.debug == True:
            print("In GUI -> process_new_project -> begin")
        self.root.title("Untitled")
        self.file_name = None
        self.string_session_name.set("Untitled")

        self.num_p_shocks = 0
        self.num_r_shocks = 0
        self.num_periods = 0

        self.show_info_bar_parms()
        self.show_shock_frames()


        #self.set_market()
        #self.sec.reset_market()
        self.sec.show_environment()

        if self.debug == True:
            print("In GUI -> process_new_project -> end")

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
        self.set_market()
        self.project_path += self.string_session_name.get()
        self.sec.save_project(self.project_path)

    def display_about_messagebox(self, event=None):
        # displays about message
        tkinter.messagebox.showinfo("About", "{}{}".format(self.name,
                                                           "\n\nCenter for the Study of Neuroeconomics\n\nOctober, 2017"))

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

    def run_sim(self):
        '''Adding in a new window to run simulations in market_gui'''
        if not messagebox.askyesno("PROGRESS CHECK", "Have all the parameters been set? \n If not please set parameters"):
            return
        run_root = tk.Toplevel()
        run_root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))

        # TODO keep working on this root window!


        all_prices = []
        theoretical_transactions = []
        all_ends = []
        avg_prices = []
        endpoints = []
        eff = []
        periods_list = []
        act_surplus = []
        maxi_surplus = []
        session = self.string_session_name.get()

        num_periods = int(self.string_periods.get())  # periods or trading days
        limits = (int(self.price_ceiling.get()), int(self.price_floor.get()))  # price ceiling, price floor
        rounds = int(self.string_rounds.get())  # rounds in each period (can substitute time clock)
        name = "trial"
        period = 0  # ...??
        '''The code below creates a file for your session name for market run info to be dumped into...
        ... will raise file error if session name not changed --> prevents overwriting previous runs'''

        smp = Simulator.spot_market_period.SpotMarketPeriod(session, num_periods, limits)

        #smp = spot_market_period.SpotMarketPeriod(self.string_session_name, self.num_periods)
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
        # TODO create way to automate input of trader # and strategies
        trader_names = [aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa, aa]
        #tk.Label(run_frame, text="Traders: " + str(trader_names)).grid(row=2, column=0)
        smp.init_spot_system_gui(name, limits, rounds, self.project_path, self.string_data.get(), self.output_path,
                                session)
        rnd_traders = trader_names  # because shuffle shuffles the list in place, returns none
        times = []
        for k in range(int(self.string_periods.get())):  # iterates through number of periods or "trading days"
            if k == 3:  # if round = 3 then shock or change traders
                # TODO trader shocks happen below
                # rnd_traders.append(zic)
                # rnd_traders.append(gd)
                # smp.num_buyers = 12
                # smp.num_sellers = 12
                # print(rnd_traders)
                # TODO period shocks happen below
                # smp.init_spot_system_crash(name, limits, rounds, input_path, input_file_market_shock, output_path, session_name)
                pass
            else:
                pass
            timer_start = timer()
            periods_list.append(k)
            # random.shuffle(rnd_traders)  # shuffles trader order per period
            # print(rnd_traders)  # prints list of trader strategy
            smp.init_traders(rnd_traders, k)
            print("**** Running Period {}".format(k))  # provides visual effect in editor
            smp.run_period(period, session)
            timer_stop = timer()
            results = smp.eval()
            '''the below data is appended into global dictionaries'''
            eff.append(results[8])  # appends the efficiencies per period
            act_surplus.append(results[7])  # appends actual surplus per period
            maxi_surplus.append(results[6])  # appends maximum surplus per period
            smp.get_contracts()  # gets transaction prices and period endpoints
            session_folder = self.output_path + session + "\\"  # establishes file path for session data folder
            smp.record_session_data(session_folder)  # records session data in excel csv
            time = timer_start - timer_stop
            times.append(time)

        # creates a frame for simulation results
        run_frame = tk.LabelFrame(run_root, text="Simulation Results")
        run_frame.grid(row=1, column=0)  # set parameters
        tk.Label(run_frame, text="Session Name: " + str(self.string_session_name.get())).grid(row=0, column=0)
        tk.Label(run_frame, text="Data Used: " + str(self.string_data.get())).grid(row=1, column=0)
        tk.Label(run_frame, text="Market Efficiencies:" + str(eff)).grid(row=3, column=0)
        tk.Label(run_frame, text="Avg. Efficiency:" + str(sum(eff) / num_periods)).grid(row=4, column=0)
        tk.Label(run_frame, text="Actual Surpluses:" + str(act_surplus)).grid(row=5, column=0)
        tk.Label(run_frame, text="Maximum Surpluses:" + str(maxi_surplus)).grid(row=3, column=0)

        print("Period Times: " + str(times))
        print("Market Efficiencies:" + str(eff))  # print market efficiencies
        print("Avg. Efficiency:" + str(sum(eff) / num_periods))  # print avg efficiency
        # print("Total Avg. Transaction Price:" + str(sum(avg_prices[1:])/(num_periods - 1)))
        print("Actual Surpluses:" + str(act_surplus))  # print actual surpluses
        print("Maximum Surpluses:" + str(maxi_surplus))  # print max surpluses
        print()

        # TODO trader info below can be functionalized further
        # builds frame for trader total earnings
        trader_frame1 = tk.LabelFrame(run_root, text="Strategy Total Earnings (per period)")
        trader_frame1.grid(row=1, column=1)  # set parameters
        tk.Label(trader_frame1, text="Trader_AA: " + str(smp.total_earns('AA'))).grid(row=0, column=0)
        tk.Label(trader_frame1, text="Trader_GD: " + str(smp.total_earns('GD'))).grid(row=1, column=0)
        tk.Label(trader_frame1, text="Trader_PS: " + str(smp.total_earns('PS'))).grid(row=2, column=0)
        tk.Label(trader_frame1, text="Trader_ZIP: " + str(smp.total_earns('ZIP'))).grid(row=3, column=0)
        tk.Label(trader_frame1, text="Trader_Kaplan: " + str(smp.total_earns('KP'))).grid(row=4, column=0)
        tk.Label(trader_frame1, text="Trader_Shaver: " + str(smp.total_earns('SI'))).grid(row=5, column=0)
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
        trader_frame2 = tk.LabelFrame(run_root, text="Strategy Total Avg. Earnings (per trader)")
        trader_frame2.grid(row=1, column=2)  # set parameters
        tk.Label(trader_frame2, text="Trader_AA: " + str(smp.total_avg_earns('AA', trader_names.count(aa) * num_periods))).grid(row=0, column=0)
        tk.Label(trader_frame2, text="Trader_GD: " + str(smp.total_avg_earns('GD', trader_names.count(gd) * num_periods))).grid(row=1, column=0)
        tk.Label(trader_frame2, text="Trader_PS: " + str(
            smp.total_avg_earns('PS', trader_names.count(ps) * num_periods))).grid(row=2, column=0)
        tk.Label(trader_frame2, text="Trader_ZIP: " + str(smp.total_avg_earns('ZIP', trader_names.count(zip) * num_periods))).grid(row=3, column=0)
        tk.Label(trader_frame2, text="Trader_Kaplan: " + str(smp.total_avg_earns('KP', trader_names.count(kp) * num_periods))).grid(row=4, column=0)
        tk.Label(trader_frame2, text="Trader_Shaver: " + str(smp.total_avg_earns('SI', trader_names.count(si) * num_periods))).grid(row=5, column=0)

        print("Strategy Total Avg. Earnings (per trader)")
        print("Trader_AA: " + str(smp.total_avg_earns('AA', trader_names.count(aa) * num_periods)))  #
        print("Trader_GD: " + str(smp.total_avg_earns('GD', trader_names.count(gd) * num_periods)))  #
        print("Trader_PS: " + str(
            smp.total_avg_earns('PS', trader_names.count(ps) * num_periods)))  # ADDED: section to list total avg earns
        # print("Trader_AI: " + str(smp.total_avg_earns('AI')))   #
        print("Trader_ZIP: " + str(smp.total_avg_earns('ZIP', trader_names.count(zip) * num_periods)))  #
        print("Trader_ZIC: " + str(smp.total_avg_earns('ZIC', trader_names.count(zic) * num_periods)))  #
        print("Trader_Kaplan: " + str(smp.total_avg_earns('KP', trader_names.count(kp) * num_periods)))
        print("Trader_Shaver: " + str(smp.total_avg_earns('SI', trader_names.count(si) * num_periods)))

        """The below function calls create graphs from the simulation results and save in project path"""
        smp.get_avg_trade_ratio()  # prints avg trade ratio for all periods
        smp.graph_trader_eff(self.output_path, session)  # plots individual efficiency
        smp.graph_efficiency_gui(self.output_path, session, eff, periods_list)  # plots period efficiency
        smp.get_endpoints()  # obtains endpoints of periods for graph
        smp.graph_contracts(self.output_path, session)  # graphs contract transactions and avg transaction per period
        # smp.graph_surplus()  # graphs actual and max surplus
        #smp.graph_alphas(self.output_path, session)  # graphs Smith's Alpha of convergence
        smp.graph_distribution(self.output_path, session)  # graphs normal distribution of trader efficiencies

        from PIL import Image  # import python image library
        new_size = 400, 225  # makes original image smaller

        # below builds a frame to display the smaller transactions graph
        graph_frame1 = tk.LabelFrame(run_root, text="Transactions")  # frame created in run root
        graph_frame1.grid(row=2, column=1)
        edit = Image.open(self.output_path + session + '\\' + "Transactions.png")  # accesses original image
        edit.thumbnail(new_size, Image.ANTIALIAS)  # turns the image into a thumbnail size
        edit.save(self.output_path + session + '\\' + "Transactions Mini.png")  # saves new file
        photo = tk.PhotoImage(file=self.output_path + session + '\\' + "Transactions Mini.png")  # accesses new image
        label = tk.Label(graph_frame1, image=photo)  # turns into tk label and packs into frame
        label.pack()

        # below builds a frame to display the smaller SD graph
        sd_frame = tk.LabelFrame(run_root, text="Supply and Demand")  # new frame in run root
        sd_frame.grid(row=2, column=0)
        edit2 = Image.open(self.output_path + session + '\\' + "SD Before.png") # old image accessed
        edit2.thumbnail(new_size, Image.ANTIALIAS)  # old image turned into thumbnail
        edit2.save(self.output_path + session + '\\' + "SD Mini.png")  # new image saved
        photo2 = tk.PhotoImage(file=self.output_path + session + '\\' + "SD Mini.png")  # new image accessed
        label2 = tk.Label(sd_frame, image=photo2)  # turned into label and packed into frame
        label2.pack()

        stat_frame = tk.LabelFrame(run_root, text="Trader Efficiency Distribution")  # new frame in run root
        stat_frame.grid(row=2, column=2)
        edit3 = Image.open(self.output_path + session + '\\' + "Efficiency Distribution.png")  # old image accessed
        edit3.thumbnail(new_size, Image.ANTIALIAS)  # old image turned into thumbnail
        edit3.save(self.output_path + session + '\\' + "Eff Dist Mini.png")  # new image saved
        photo3 = tk.PhotoImage(file=self.output_path + session + '\\' + "Eff Dist Mini.png")  # new image accessed
        label3 = tk.Label(stat_frame, image=photo3)  # turned into label and packed into frame
        label3.pack()

        run_root.mainloop()  # continues running run root
        # TODO ttk error needs to be discovered and fixed
        # TODO graphing error when rerunning inside the gui .. plots trader eff dist into SD graph..

if __name__ == "__main__":
    # setup gui
    root = tk.Tk()
    # TODO add file path set as first root window then have everything display
    #root2 = tk.Tk()
    debug_test = True
    if debug_test:
        print("In Gui -> START")
    sec = Environment.spot_environment_controller.SpotEnvironmentController(debug_test)
    gui = MarketGui(root, sec, "Data Entry", debug_test)
    root.mainloop()
    if debug_test:
        print("In Gui -> END")