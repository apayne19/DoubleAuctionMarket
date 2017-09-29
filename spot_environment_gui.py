# universal imports
import tkinter as tk  # gui interface creator
import tkinter.filedialog
from tkinter import messagebox
import matplotlib  # graphing functions
matplotlib.use("TkAgg")
import time  # https://docs.python.org/3.6/library/time.html  # time functions
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# example of time module
'''start = time.gmtime(0)  # epoch = 1970, "start of time" for computers
seconds = time.time()  # time measured by seconds from epoch
print(time.localtime(seconds))  # gives time in present year, month, day, hour, min, sec, day of yr'''

# example of tkinter app build
'''class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Press my buttons\n;)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("oooooooh you're dirty...\nkiklu!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()'''

# local file imports
import os  # https://docs.python.org/3.6/library/os.html
import spot_environment_controller  # condensed modules/commands from spot_env_model

"""This class is using the control center commands from spot_market_controller (condensed methods 
from spot_market_model).... the HAND of the simulator"""

class SpotEnviornmentGui():
    def __init__(self, root, sec, name, debug=False):
        assert name != "", "Gui must have a name"

        self.root = root  # root builds tkinter app
        self.sec = sec  # will bring in spot_env_model and use debugger
        self.name = name  # name of gui
        self.debug = debug  # used as error checker...when false will return errors or warnings
        root.title(name)  # giving root a name

        self.num_buyers = 0  # setting number of buyers to 0
        self.num_sellers = 0  # setting number of sellers to 0

        self.num_units = 0  # setting number of units to 0
        # self.dem_units = 0
        # self.sup_units = 0  # TODO change to demand units and supply units
        #                       --> buyers could demand more units than suppliers have and vice versa...

        self.string_num_buyers = tk.StringVar()    # creates a tkinter variable
        self.string_num_sellers = tk.StringVar()   # StringVar() returns either an ASCII string or Unicode string

        self.string_num_units = tk.StringVar()     # can also be used to trace when changes made to variables
        # self.string_dem_units = tk.StringVar()
        # self.string_sup_units = tk.StringVar()  # TODO if ^todo is agreed then will need to reformat code
        #                                           --> could cause errors when calling other methods

        self.string_project_name = tk.StringVar()  # BooleanVar() will return 0 for false and 1 for true...
        self.string_eq = tk.StringVar()
        self.string_pl = tk.StringVar()
        self.string_ph = tk.StringVar()
        self.string_ms = tk.StringVar()
        self.current_row = 0  # setting current read row to 0... self.current_row+1 would read next row
        self.current_row_contents = []
        self.ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # is this limiting the amount to 10 buyers and 10 sellers?
        self.file_name = None  # none is a placeholder to be filled

        # have to build matrices for future tkinter display
        # self.buyer_values = self.build_array(self.num_buyers, self.num_units)  # matrix of buyers and number of units
        # self.seller_costs = self.build_array(self.num_sellers, self.num_units)  # matrix of sellers and number of units
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)  # matrix of buyers and number of units
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)  # matrix of sellers and number of units

        # have to set local file path for icon images and project data
        self.file_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\icons\\"
        self.project_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects\\"

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
        file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', accelerator='Alt+F4', command=self.on_quit_chosen)
        menu_bar.add_cascade(label='File', menu=file_menu)  # allows toolbar tab to drop down with multiple choices

        # create show action menu item
        show_menu = tk.Menu(menu_bar, tearoff=0)
        show_menu.add_command(label='Plot', command=self.on_plot_clicked)  # click = plot action
        show_menu.add_command(label='Show', command=self.on_show_clicked)  # click = show action
        show_menu.add_command(label='Calc EQ', command=self.on_calc_eq_clicked)  # click = calc action
        menu_bar.add_cascade(label='Actions', menu=show_menu)  # allows menu to drop down

        # create about/help menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='About', command=self.display_about_messagebox)  # click = display about message
        about_menu.add_command(label='Help', command=self.display_help_messagebox)  # click = display help message
        menu_bar.add_cascade(label='Misc', menu=about_menu)  # drop down menu
        root.config(menu=menu_bar)  # makes menu setup final

    def show_shortcut(self):
        shortcut_bar = tk.Frame(self.root)  # creates a frame within the tkinter object
        shortcut_bar.grid(row=0, column=0, columnspan=4, sticky='W')  # setting parameters of frame
        """WARNING: Never use grid and pack in same tkinter master window, will create error --> loop to solve
        ...according to stackoverflow"""

    def show_infobar(self):
        info_bar = tk.LabelFrame(self.root, height=15, text=str(self.name))  # creates a label frame for initial inputs
        info_bar.grid(row=1, column=0, columnspan=4, sticky='W', padx=5, pady=5)  # set parameters

        # create project name label
        tk.Label(info_bar, text="Project Name:").grid(row=0, column=0)
        tk.Entry(info_bar, width=15, justify=tk.LEFT, textvariable=self.string_project_name).grid(row=0, column=1, padx=5)

        # create number of buyers label
        tk.Label(info_bar, text="Number of Buyers: ").grid(row=0, column=2)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_buyers).grid(row=0, column=3, padx=5)
        self.string_num_buyers.set(str(self.num_buyers))  # sets initial display value at self.num_buyers = 0

        # create number of sellers label
        tk.Label(info_bar, text="Number of Sellers: ").grid(row=0, column=4, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_sellers).grid(row=0, column=5)
        self.string_num_sellers.set(str(self.num_sellers))  # sets initial display value at self.num_sellers = 0

        # create number of units label
        tk.Label(info_bar, text="Number of Units: ").grid(row=0, column=6, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_num_units).grid(row=0, column=7)
        self.string_num_units.set(str(self.num_units))  # sets initial display value at self.num_units = 0

        # create demand units label
        # tk.Label(info_bar, text="Demand Units: ").grid(row=0, column=6, padx=5)
        # tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_dem_units).grid(row=0, column=7)
        # self.string_dem_units.set(str(self.dem_units))  # sets initial display value at self.num_units = 0

        # create supply units label
        # tk.Label(info_bar, text="Supply Units: ").grid(row=0, column=8, padx=5)
        # tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_sup_units).grid(row=0, column=7)
        # self.string_sup_units.set(str(self.sup_units))  # sets initial display value at self.num_units = 0

        # create a button with action input (command = click)
        info_button = tk.Button(info_bar, text="Set", width=4,
                                command=self.on_set_parms_clicked)
        '''Click = calls on_set_parms_clicked 
                    --> calls show_player_frames() 
                        --> calls show_buyer_frames() and show_seller_frames()
                            --> builds a frame for each group'''
        info_button.grid(row=0, column=8, padx=10, pady=5)  # creates grids in both built frames

        # create Equilibrium Q label
        tk.Label(info_bar, text="Equilibrium Q: ").grid(row=1, column=2)  # create/grid location
        tk.Label(info_bar, width=4, justify=tk.CENTER,
                 textvariable=self.string_eq, relief='sunken').grid(row=1, column=3)  # relief='sunken' = visual depth
        self.string_eq.set("n/a")  # sets display in box to N/A and makes the box unchangeable

        # create EQ Price low label
        tk.Label(info_bar, text="EQ Price Low: ").grid(row=1, column=4)
        tk.Label(info_bar, width=4, justify=tk.CENTER,
                 textvariable=self.string_pl, relief='sunken').grid(row=1, column=5)
        self.string_pl.set("n/a")  # display to N/A and unchangeable

        # create EQ high price label
        tk.Label(info_bar, text="EQ Price High: ").grid(row=1, column=6)
        tk.Label(info_bar, width=4, justify=tk.CENTER,
                 textvariable=self.string_ph, relief='sunken').grid(row=1, column=7)
        self.string_ph.set("n/a")  # display n/a and unchangeable

        # create Max Surplus label
        tk.Label(info_bar, text="   Max Surplus: ").grid(row=1, column=8, pady=15)
        tk.Label(info_bar, width=4, justify=tk.CENTER,
                 textvariable=self.string_ms, relief='sunken').grid(row=1, column=9, padx=15)
        self.string_ms.set("n/a")  # display n/a and unchangeable

    def on_quit_chosen(self):
        # TODO create similar action for when x clicked in top right corner of window
        if tkinter.messagebox.askokcancel("Exit?", "Have you saved your work?"):
            root.destroy()  # closes window and destroys tkinter object

    def process_sd_string(self):
        if self.num_buyers == 0:
            return "Empty"
        else:
            s_d_list = self.sec.get_supply_demand_list()  # calls supply_demand_list from spot_env_model
            return s_d_list

    def on_calc_eq_clicked(self):
        qt, pl, ph, ms = sec.get_equilibrium()  # click = calls get_eq() from spot_env_model
        self.string_eq.set(str(qt))
        self.string_pl.set(str(pl))  # these change n/a displays to new calc values
        self.string_ph.set(str(ph))
        self.string_ms.set(str(ms))

    def on_show_clicked(self):
        if self.debug:  # if error trap not tripped and still set to False
            print("In GUI -> on_show_clicked -> begin")
        self.set_market()
        lfr_show = tk.LabelFrame(root, text="List of Supply and Demand")
        lfr_show.grid(row=2, rowspan=3, column=2, sticky=tk.W + tk.E + tk.N + tk.S, padx=15, pady=4)
        lbl_show = tk.Label(lfr_show, text=self.process_sd_string())
        lbl_show.grid(row=0, column=0)
        if self.debug:
            print("In GUI -> on_show_clicked -> end")

    def on_plot_clicked(self):
        """ Plot supply and demand in a frame with toolbar."""
        """Click = calls set_market()
                    --> which calls methods from spot_env_model to display values in GUI"""
        if self.debug:
            print("In Gui -> on_plot_clicked --> begin")
        self.set_market()

        # set up frame to plot in
        fr_plot = tk.LabelFrame(root, text="Plot of Supply and Demand")
        fr_plot.grid(row=2, rowspan=2, column=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=15, pady=4)

        # set up graph to plot in frame
        f = Figure(figsize=(7, 7), dpi=100)
        a = f.add_subplot(111)
        if self.num_buyers == 0:
            canvas = FigureCanvasTkAgg(f, fr_plot)
            canvas.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
            canvas.draw()
            if self.debug:
                print("In Gui -> on_plot_clicked --> early end")
            self.set_market()  # why is this called twice?
            return

        # get some model information here
        dunits, sunits, munits, demand_values, supply_costs, eq_price_high, eq_price_low = sec.get_supply_demand_plot_info()
        if self.debug:
            print("In Gui --> 0n_plot_clicked  --> info from model")
            print("demand = {}".format(demand_values))
            print("supply = {}".format(supply_costs))

        # do some plotting here
        if eq_price_high != eq_price_low:
            a.plot(munits, [eq_price_high for x in munits], label='Price High')  # High Price Line
            a.plot(munits, [eq_price_low for x in munits], label='Price Low')  # Low Price Line
        else:
            a.plot(munits, [eq_price_high for x in munits], label='EQ Price')  # Just one price

        a.step(dunits, demand_values, label='Demand')  # plots the demand step-wise curve
        a.step(sunits, supply_costs, label='Supply')  # plots the supply step-wise curve

        a.legend(bbox_to_anchor=(0.65, 0.98))  # places a legend on the plot
        a.set_title("Supply and Demand")  # add the title
        a.set_xlabel("Units")  # add the x axis label       -------> WORKS NOW!!
        a.set_ylabel("$")  # add the y axis label                    --> problem was set_ missing

        # finish setting up the canvas here
        canvas = FigureCanvasTkAgg(f, fr_plot)
        canvas.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
        canvas.draw()

        # Add navigation bar:  This adds a toolbar.  This is optional and does not work yet
        toolbar = NavigationToolbar2TkAgg(canvas, fr_plot)
        toolbar.pack()  # This is the other pack.  Both go into frame fr_plot
        toolbar.update()

        if self.debug:
            print("In Gui -> on_plot_clicked --> end")

    def set_market(self):
        """ Sends all values on screen to model"""
        # Start with name and all that
        if self.debug:
            print("In Gui -> set_market -> begin")
        self.sec.set_market_parms([self.string_project_name.get(), self.num_buyers, self.num_sellers,
                                   self.num_units])
        make_d = {}

        # Now Add Buyer Values and Seller Costs
        make_d["buyers"] = {}
        for k in range(self.num_buyers):
            make_d["buyers"][k] = []
            for j in range(self.num_units):
                make_d["buyers"][k].append(int(self.buyer_values[k][j].get()))

        make_d["sellers"] = {}
        for k in range(self.num_sellers):
            make_d["sellers"][k] = []
            for j in range(self.num_units):
                make_d["sellers"][k].append(int(self.seller_costs[k][j].get()))

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
        print("... num_buyers = {}".format(self.num_buyers))
        print("... num_sellers = {}".format(self.num_sellers))
        print("... num_units = {}".format(self.num_units))

        for k in range(self.num_buyers):
            print("... make_d[buyers][{}] = {}".format(k, make_d["buyers"][k]))
        for k in range(self.num_sellers):
            print("... make_d[sellers][{}] = {}".format(k, make_d["sellers"][k]))

        if self.debug:
            print("In Gui -> show_market -> end")


    def on_set_parms_clicked(self):
        """Set parameters from info_bar, initializes a new experiment. Message box will allow the user to opt out."""
        if not messagebox.askyesno("DESTROY WORK", "This will destroy your work \n Do you wish to continue?"):
            return

        self.num_buyers = int(self.string_num_buyers.get())
        self.num_sellers = int(self.string_num_sellers.get())
        self.num_units = int(self.string_num_units.get())
        self.root.title(self.string_project_name.get())

        if self.num_buyers > 0 and self.num_units > 0:  # Build array if useful
            self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        if self.num_sellers > 0 and self.num_units > 0:  # Build array if useful
            self.seller_costs = self.build_array(self.num_sellers, self.num_units)

        self.show_player_frames()  # calls show_player_frames --> builds frame
        self.sec.set_market_parms([self.string_project_name.get(), self.num_buyers, self.num_sellers, self.num_units])


    def on_button_clicked(self, row, col):
        def event_handler():
            self.process_button_clicked(row, col)

        return event_handler

    def process_button_clicked(self, row, col):
        self.target_row = row
        if self.debug == True:
            print("In GUI -> process button click row {} col {}".format(row, col))

        # implement copy button
        if col == 0:
            self.current_row_contents = [x for x in range(self.num_units)]
            if row < self.num_buyers:  # implement copy on buyers
                for k in range(self.num_units):
                    self.current_row_contents[k] = self.buyer_values[row][k].get()
            else:  # implement copy on sellers
                for k in range(self.num_units):
                    self.current_row_contents[k] = self.seller_costs[row-self.num_buyers][k].get()  # fix row to seller
        # implement replace buttons
        elif col == 1:
            if row < self.num_buyers:  # implement replace on buyers
                if len(self.current_row_contents) != self.num_units:
                    return
                for k in range(self.num_units):
                    self.buyer_values[row][k].set(self.current_row_contents[k])
            else:  # implement replace on sellers
                if len(self.current_row_contents) != self.num_units:
                    return
                for k in range(self.num_units):
                    self.seller_costs[row-self.num_buyers][k].set(self.current_row_contents[k])
        return

    def show_player_frames(self):
        self.show_buyers_frame()
        self.show_sellers_frame()

    def show_buyers_frame(self):
        bf = tk.LabelFrame(self.root, text="Buyer Entries")
        bf.grid(row=2, column=0, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_buyers == 0: return   # Notihing to show
        self.buttons = [[None for x in range(3)] for x in range(self.num_buyers + self.num_sellers)]

        buy_ids = [k for k in range(self.num_buyers)]
        tk.Label(bf, text="ID").grid(row=0, column=0)
        for unit in range(self.num_units):
            sunit = "Unit " + str(unit + 1)
            tk.Label(bf, text=sunit).grid(row=0, column=unit + 1)
        for buyer in range(self.num_buyers):
            buy_ids[buyer] = tk.StringVar()
            tk.Entry(bf, width=5, justify=tk.CENTER,
                     textvariable=buy_ids[buyer]).grid(row=buyer + 1, column=0)
            buy_ids[buyer].set(str(buyer + 1))
            for unit in range(self.num_units):
                self.buyer_values[buyer][unit] = tk.StringVar()
                tk.Entry(bf, width=5, justify=tk.RIGHT,
                         textvariable=self.buyer_values[buyer][unit]).grid(row=buyer + 1,
                                                                                                          column=unit + 1)
                self.buyer_values[buyer][unit].set("")
            self.buttons[buyer][0] = tk.Button(bf, width=2, text="C",
                                               command=self.on_button_clicked(buyer, 0))
            self.buttons[buyer][0].grid(row=buyer + 1, column=self.num_units + 2)
            self.buttons[buyer][1] = tk.Button(bf, width=2, text="R",
                                               command=self.on_button_clicked(buyer, 1))
            self.buttons[buyer][1].grid(row=buyer + 1, column=self.num_units + 3)

    def show_sellers_frame(self):
        sf = tk.LabelFrame(self.root, text="Seller Entries")
        sf.grid(row=2, column=1, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_sellers == 0: return  # Nothing to show
        sell_ids = [k for k in range(self.num_sellers)]
        tk.Label(sf, text="ID").grid(row=0, column=0)
        for unit in range(self.num_units):
            sunit = "Unit " + str(unit + 1)
            tk.Label(sf, text=sunit).grid(row=0, column=unit + 1)
        for seller in range(self.num_sellers):
            sell_ids[seller] = tk.StringVar()
            tk.Entry(sf, width=5, justify=tk.CENTER,
                     textvariable=sell_ids[seller]).grid(row=seller + 1, column=0)
            sell_ids[seller].set(str(seller + 1))
            for unit in range(self.num_units):
                self.seller_costs[seller][unit] = tk.StringVar()
                tk.Entry(sf, width=5, justify=tk.RIGHT,
                         textvariable=self.seller_costs[seller][unit]).grid(
                    row=seller + 1,
                    column=unit + 1)
                self.seller_costs[seller][unit].set("")
            row = self.num_buyers + seller
            self.buttons[row][0] = tk.Button(sf, width=2, text="C",
                                             command=self.on_button_clicked(row, 0))
            self.buttons[row][0].grid(row=seller + 1, column=self.num_units + 2)
            self.buttons[row][1] = tk.Button(sf, width=2, text="R",
                                             command=self.on_button_clicked(row, 1))
            self.buttons[row][1].grid(row=seller + 1, column=self.num_units + 3)

    def show_info_bar_parms(self):
        self.string_num_buyers.set(str(self.num_buyers))
        self.string_num_sellers.set(str(self.num_sellers))
        self.string_num_units.set(str(self.num_units))

    def process_new_project(self, event=None):
        if self.debug == True:
            print("In GUI -> process_new_project -> begin")
        self.root.title("Untitled")
        self.file_name = None
        self.string_project_name.set("Untitled")

        self.num_buyers = 0
        self.num_sellers = 0
        self.num_units = 0

        self.show_info_bar_parms()
        self.show_player_frames()

        self.on_show_clicked()
        self.on_plot_clicked()

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
            self.show_project()

    def write_to_file(self, file_name):  # creates ability to write directly in file  # can use when users put in info
        pass
        """
        try:
            content = content_text.get(1.0, 'end')
            with open(self.file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass  # in actual we will show a error message box.
            # we discuss message boxes in the next section so ignored here.
        """

    def save_as(self, event=None):  # TODO create ability to save work anywhere on the computer
        pass

    def save(self, event=None):  # saves file in it's path location
        # TODO:  Add existing file check
        self.set_market()
        self.project_path += self.string_project_name.get()
        self.sec.save_project(self.project_path)

    def display_about_messagebox(self, event=None):  # dispays about message
        tkinter.messagebox.showinfo("About", "{}{}".format(self.name,
                                                           "\n\nCenter for the Study of Neuroeconomics\n\nOctober, 2017"))

    def display_help_messagebox(self, event=None):  # displays help messages when message link clicked
        help_msg = "Quick Help: \n\n"
        help_msg += "   File Menu \n"
        help_msg += "      New  - Create New Project \n"
        help_msg += "      Load - Load Project \n"
        help_msg += "      Save - Save Project \n\n"
        help_msg += "   Getting Started \n"
        help_msg += "      1). Enter unique Project Name \n"
        help_msg += "      2). Enter Number of Buyers \n"
        help_msg += "      3). Enter Number of Sellers \n"
        help_msg += "      4). Enter Number of Units \n"
        help_msg += "      5). Click Set Button \n"
        help_msg += "          a). Say yes to message box \n"
        help_msg += "          b). Buyers and Sellers entries displayed \n"
        tkinter.messagebox.showinfo("Help", help_msg)

    def show_project(self):
        self.num_buyers = sec.get_num_buyers()
        self.num_sellers = sec.get_num_sellers()
        self.num_units = sec.get_num_units()
        self.string_project_name.set(self.name)
        self.string_num_buyers.set(str(self.num_buyers))
        self.string_num_sellers.set(str(self.num_sellers))
        self.string_num_units.set(str(self.num_units))
        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.seller_costs = self.build_array(self.num_sellers, self.num_units)

        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.show_buyers_frame()
        self.set_all_buyer_values()

        self.seller_costs = self.build_array(self.num_sellers, self.num_units)
        self.show_sellers_frame()
        self.set_all_seller_costs()

    def set_all_buyer_values(self):
        for buyer in range(self.num_buyers):
            values = sec.get_buyer_values(buyer)
            self.set_buyer_values(buyer, values)

    def set_all_seller_costs(self):
        for seller in range(self.num_sellers):
            costs = sec.get_seller_costs(seller)
            self.set_seller_costs(seller, costs)

    def set_buyer_values(self, buyer, values):
        assert buyer < self.num_buyers, "Buyer {} not in range".format(buyer)
        assert len(values) == self.num_units, "values {} shoud have {} value units".format(values, self.num_units)
        for unit in range(self.num_units):
            self.buyer_values[buyer][unit].set(str(values[unit]))

    def set_seller_costs(self, seller, costs):
        assert seller < self.num_sellers, "seller {} not in range".format(seller)
        assert len(costs) == self.num_units, "costs {} should have {} cost units".format(costs, self.num_units)
        for unit in range(self.num_units):
            self.seller_costs[seller][unit].set(str(costs[unit]))

    def blank_arrays(self):
        for j in range(self.num_buyers):
            for k in range(self.num_units):
                self.buyer_values[j][k].set("")
        for j in range(self.num_sellers):
            for k in range(self.num_units):
                self.seller_costs[j][k].set("")


if __name__ == "__main__":
    # setup gui
    root = tk.Tk()
    debug_test = True
    if debug_test:
        print("In Gui -> START")
    sec = spot_environment_controller.SpotEnvironmentController(debug_test)
    gui = SpotEnviornmentGui(root, sec, "Trading Platform", debug_test)
    root.mainloop()
    if debug_test:
        print("In Gui -> END")