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
import spot_environment_controller  # condensed modules/commands from spot_env_model
import spot_market_period
import subprocess
class MarketGui():
    def __init__(self, root, sec, name, debug=False):
        assert name != "", "Gui must have a name"

        self.root = root  # root builds tkinter app
        '''Can maybe add an os function for resolutions to adapt'''
        self.root.geometry("1600x1200")
        self.sec = sec  # will bring in spot_env_model and use debugger
        self.name = name  # name of gui
        self.debug = debug  # used as error checker...when false will return errors or warnings
        self.root.title(name)  # giving root a name
        '''Added a messagebox for when escape button pressed... calls on_escape_chosen()'''
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit_chosen)
        self.num_periods = 0  # setting number of buyers to 0
        self.num_p_shocks = 0  # setting number of sellers to 0
        self.num_r_shocks = 0  # setting number of units to 0

        self.string_periods = tk.StringVar()    # creates a tkinter variable
        self.string_round_shocks = tk.StringVar()   # StringVar() returns either an ASCII string or Unicode string
        self.string_period_shocks = tk.StringVar()     # can also be used to trace when changes made to variables

        self.string_session_name = tk.StringVar()  # BooleanVar() will return 0 for false and 1 for true...
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

        # have to set local file path for icon images and project data
        #  TODO change these to your file path
        self.file_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\icons\\"
        self.project_path = "C:\\Users\\Summer17\\Desktop\\Repos\\DoubleAuctionMisc\\projects"

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

    # def on_plot_clicked(self):
    #     """ Plot supply and demand in a frame with toolbar."""
    #     """Click = calls set_market()
    #                 --> which calls methods from spot_env_model to display values in GUI"""
    #     if self.debug:
    #         print("In Gui -> on_plot_clicked --> begin")
    #     self.set_market()
    #
    #     # set up frame to plot in
    #     fr_plot = tk.LabelFrame(self.root, text="Plot of Supply and Demand")
    #     fr_plot.grid(row=2, rowspan=1, column=2, sticky=tk.W + tk.E + tk.N + tk.S, padx=15, pady=4)
    #     c_plot = tk.LabelFrame(self.root, text="Plot of Contracts")
    #     c_plot.grid(row=3, rowspan=1, column=2, sticky=tk.W + tk.E + tk.N + tk.S, padx=15, pady=4)
    #     # set up graph to plot in frame
    #     f = Figure(figsize=(4, 4), dpi=100)
    #     a = f.add_subplot(111)
    #     if self.num_buyers == 0:
    #         canvas1 = FigureCanvasTkAgg(f, fr_plot)
    #         canvas1.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
    #         canvas1.draw()
    #         canvas2 = FigureCanvasTkAgg(f, c_plot)
    #         canvas2.get_tk_widget().pack()  # Have to use pack here to work with toolbar.  Not sure why.
    #         canvas2.draw()
    #         if self.debug:
    #             print("In Gui -> on_plot_clicked --> early end")
    #         self.set_market()  # why is this called twice?
    #         return

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
        # show_menu = tk.Menu(menu_bar, tearoff=0)
        # show_menu.add_command(label='Show Supply & Demand', command=self.on_show_clicked)  # click = show action
        # show_menu.add_command(label='Calculate Equilibrium', command=self.on_calc_eq_clicked)  # click = calc action
        # menu_bar.add_cascade(label='Actions', menu=show_menu)  # allows menu to drop down

        # created a plot menu item
        # plot_menu = tk.Menu(menu_bar, tearoff=0)
        # plot_menu.add_command(label='Plot Supply & Demand', command=self.on_plot_clicked)  # click = plot action
        # plot_menu.add_command(label='Plot Contracts', command=self.on_plot_clicked)
        # menu_bar.add_cascade(label='Plot', menu=plot_menu)  # allows menu to drop down

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
        tk.Entry(info_bar, width=15, justify=tk.LEFT, textvariable=self.string_session_name).grid(row=0, column=1, padx=5)

        # create number of buyers label
        tk.Label(info_bar, text="Number of Period Shocks: ").grid(row=0, column=2)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_period_shocks).grid(row=0, column=3, padx=5)
        self.string_period_shocks.set(str(self.num_p_shocks))  # sets initial display value at self.num_buyers = 0

        # create number of sellers label
        tk.Label(info_bar, text="Number of Round Shocks: ").grid(row=0, column=4, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_round_shocks).grid(row=0, column=5)
        self.string_round_shocks.set(str(self.num_r_shocks))  # sets initial display value at self.num_sellers = 0

        # create number of units label
        tk.Label(info_bar, text="Number of Periods: ").grid(row=0, column=6, padx=5)
        tk.Entry(info_bar, width=3, justify=tk.CENTER, textvariable=self.string_periods).grid(row=0, column=7)
        self.string_periods.set(str(self.num_periods))  # sets initial display value at self.num_units = 0


        # create a button with action input (command = click)
        info_button = tk.Button(info_bar, text="Set", width=4,
                                command=self.on_set_parms_clicked)
        '''Click = calls on_set_parms_clicked 
                    --> calls show_player_frames() 
                        --> calls show_buyer_frames() and show_seller_frames()
                            --> builds a frame for each group'''
        info_button.grid(row=0, column=8, padx=10, pady=5)  # creates grids in both built frames
        # create Equilibrium Q label
        tk.Label(info_bar, text="Starting Data File: ").grid(row=1, column=0)  # create/grid location
        ttk.Combobox(info_bar, values=os.listdir(self.project_path)).grid(row=1, column=1)
        plot_button = tk.Button(info_bar, text="Plot", width=4, command=None)
        plot_button.grid(row=1, column=2, padx=10, pady=5)

        run_frame = tk.LabelFrame(self.root, height=15, text="RUN SIMULATION")
        run_frame.grid(row=1, column=9, columnspan=2, sticky='E', padx=15, pady=5)
        run_button = tk.Button(run_frame, text="RUN", width=4, command=self.callback())
        run_button.grid(row=0, column=1)
        # # create EQ Price low label
        # tk.Label(info_bar, text="EQ Price Low: ").grid(row=1, column=4)
        # tk.Label(info_bar, width=4, justify=tk.CENTER,
        #          textvariable=self.string_pl, relief='sunken').grid(row=1, column=5)
        # self.string_pl.set("n/a")  # display to N/A and unchangeable
        #
        # # create EQ high price label
        # tk.Label(info_bar, text="EQ Price High: ").grid(row=1, column=6)
        # tk.Label(info_bar, width=4, justify=tk.CENTER,
        #          textvariable=self.string_ph, relief='sunken').grid(row=1, column=7)
        # self.string_ph.set("n/a")  # display n/a and unchangeable
        #
        # # create Max Surplus label
        # tk.Label(info_bar, text="   Max Surplus: ").grid(row=1, column=8, pady=15)
        # tk.Label(info_bar, width=4, justify=tk.CENTER,
        #          textvariable=self.string_ms, relief='sunken').grid(row=1, column=9, padx=15)
        # self.string_ms.set("n/a")  # display n/a and unchangeable

    def on_quit_chosen(self):
        """This gives a messagebox when either quit or escape is chosen"""
        if tkinter.messagebox.askokcancel("Exit?", "Have you saved your work?"):
            self.root.destroy()  # closes window and destroys tkinter object

    def callback(self):
        # TODO add in process to run spot_market_period
        pass

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


    def on_set_parms_clicked(self):
        """Set parameters from info_bar, initializes a new experiment. Message box will allow the user to opt out."""
        if not messagebox.askyesno("DESTROY WORK", "This will destroy your work \n Do you wish to continue?"):
            return

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
        pf.grid(row=2, column=0, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_p_shocks == 0: return   # Notihing to show
        self.buttons = [[None for x in range(3)] for x in range(self.num_p_shocks + self.num_r_shocks)]

        pshock_ids = [k for k in range(self.num_p_shocks)]
        tk.Label(pf, text="ID").grid(row=0, column=0)
        for i in range(self.num_p_shocks):
            pshock_num = "P Shock #" + str(i + 1)
            tk.Label(pf, text=pshock_num).grid(row=i+1, column=0)
        for i in range(self.num_p_shocks):
            pshock_ids[i] = tk.StringVar()
            tk.Entry(pf, width=5, justify=tk.CENTER,
                     textvariable=pshock_ids[i]).grid(row=i + 1, column=1)
            pshock_ids[i].set("")
        for i in range(self.num_p_shocks):
            ttk.Combobox(pf, values=os.listdir(self.project_path)).grid(row=i + 1, column=2)

    #
    def show_rshock_frame(self):
        rf = tk.LabelFrame(self.root, text="Round Shock Entries")
        rf.grid(row=3, column=0, sticky=tk.W +
                                        tk.E + tk.N + tk.S, padx=15, pady=4)
        if self.num_r_shocks == 0: return  # Nothing to show
        rshock_ids = [k for k in range(self.num_r_shocks)]
        tk.Label(rf, text="ID").grid(row=0, column=0)
        tk.Label(rf, text="Shock Data File").grid(row=0, column=3)
        for i in range(self.num_r_shocks):
            rshock_num = "R Shock #" + str(i + 1)
            tk.Label(rf, text=rshock_num).grid(row=i + 1, column=0)
        for i in range(self.num_r_shocks):
            rshock_ids[i] = tk.StringVar()
            tk.Entry(rf, width=5, justify=tk.CENTER,
                     textvariable=rshock_ids[i]).grid(row=i + 1, column=1)
            rshock_ids[i].set("")
        for i in range(self.num_r_shocks):
            ttk.Combobox(rf, values=os.listdir(self.project_path)).grid(row=i + 1, column=2)
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

    '''Created tkinter frame for save_as for file naming and creating'''
    def save_as(self, event=None):  # TODO create ability to save work anywhere on the computer
        """We want to create a dialog box that will accept a file name, then create that file, then save to that file"""
        top = tk.Toplevel(self.root)
        top.geometry("100x100")
        frm = tk.Frame(top, borderwidth=4, relief='ridge')
        frm.pack(fill='both', expand=True)
        label = tk.Label(frm, text="Name your file")
        label.pack()
        self.entry = tk.Entry(frm)
        self.entry.pack(pady=4)
        b_submit = tk.Button(frm, label='Save As', command=self.save_as_file())
        '''opening the file before the button is pressed...how to fix??'''
        b_submit.pack()

    def save_as_file(self):
        open(self.project_path + self.entry.get() + '.csv', 'w', newline='')

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

    def show_project(self):
        self.num_buyers = self.sec.get_num_buyers()
        self.num_sellers = self.sec.get_num_sellers()
        self.num_units = self.sec.get_num_units()
        self.string_session_name.set(self.name)
        self.string_period_shocks.set(str(self.num_p_shocks))
        self.string_round_shocks.set(str(self.num_r_shocks))
        self.string_periods.set(str(self.num_periods))
        self.periodshock_values = self.build_array(self.num_p_shocks, self.num_p_shocks)
        self.roundshock_values = self.build_array(self.num_r_shocks, self.num_r_shocks)

        self.buyer_values = self.build_array(self.num_buyers, self.num_units)
        self.show_pshock_frame()
        #self.set_all_buyer_values()

        # self.seller_costs = self.build_array(self.num_sellers, self.num_units)
        # self.show_sellers_frame()
        # self.set_all_seller_costs()




if __name__ == "__main__":
    # setup gui
    root = tk.Tk()
    debug_test = True
    if debug_test:
        print("In Gui -> START")
    sec = spot_environment_controller.SpotEnvironmentController(debug_test)
    gui = MarketGui(root, sec, "Data Entry", debug_test)
    root.mainloop()
    if debug_test:
        print("In Gui -> END")