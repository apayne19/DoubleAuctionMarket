# DoubleAuctionMarket
## Experimental Market Simulations

### DISCLAIMER: THIS PROJECT IS NOT CURRENTLY BEING DEVELOPED
   * code is provided as-is, use at your own risk
   * some functionality may be limited
   * this project may start back up at a future time
 
### ------------------------------------------------------------------------------------------------------------
### Created by Dr. Kevin McCabe and Alexander Payne
### Please read license.txt and requirements.txt before proceeding

### Author Information
   * Dr. Kevin McCabe 
      * Full-time professor of Economics, Law, and Neuroscience at George Mason University
      * Director at The Center for the Study of Neuroeconomics
      * Website link: http://www.kevinmccabe.net/kevin/
   * Alexander Payne
      * Graduated from George Mason University with a BS in Economics
      * Currently a Data Scientist at Deloitte
      * Previous Data Science Analyst at Accenture
      * Previous Lead Python Developer at The Center for the Study of Neuroeconomics
      * LinkedIn link: https://www.linkedin.com/in/alex-david-payne/
      
### Work Cited
   * Dr. Dave Cliff
      * Trader_AA and Trader_ZIP strategies are based on code from his repository
   * Repository link: https://github.com/davecliff/BristolStockExchange
   * Website link: http://people.cs.bris.ac.uk/~dc/
### ------------------------------------------------------------------------------------------------------------

#### This project will allow the user to experiment with several tools to simulate markets and analyze trading strategies
   ##### Market Simulator GUI: a guided user interface application that will allow any user to run multiple quick simulations
      * create endless supply and demand schedules
      * change various market parameters
      * introduce market shocks into your model
      * discover volatility effects with dynamic shocks
   
   ##### For Developers Section: putting the next ultimate trading strategy at your fingertips
      * create new trading strategies 
      * create new market institutions 
      * create new auction types 
      
### ------------------------------------------------------------------------------------------------------------

### Market Simulator GUI
#### Simple GUI for easy use
  * This interface can be accessed by running market_gui.py
  * Excellent for users with no programming experience
  
#### Running the Script
   * After cloning or downloading this project, the user will need to open the code
   * PyCharm IDE is recommended and the Community Edition can be downloaded for free from: https://www.jetbrains.com/pycharm/
   * Run market_gui.py
   
#### Setting File Paths
   * Upon running market_gui.py, a window will appear for the user to set two file paths
   * Project Path: this is where you will access previously created supply/demand schedules or save newly created ones to
      * Example: C:/Users/Summer17/Desktop/Repos/DoubleAuctionMarket/Data/projects
   * Simulation Save Path: this is where all the market simulation data and graphs will be saved when using the gui
      * Example: C:/Users/Summer17/Desktop/Repos/DoubleAuctionMarket/Data/period data
   * After these are set you will need to click the submit button at the bottom of the window
### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/path_entry_1.JPG) ---> ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/path_entry_2.JPG)

#### Setting Market Parameters
   * After clicking submit on the file path window, a new window will appear for the user to enter market parameters
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/data_entry.JPG)
   * Step a). the user will need to name the session
      * a unique name is recommended
      * this name must change with every use of the gui, or will result in file errors
      
      
   * Step b). the user will need to choose a starting data file (supply and demand schedule)
      * these can be accessed through the dropdown menu
      * if there are no files to choose from the user can create a new data file
      * this can be done by clicking on the Create button to the right of the window
         - this process will be explained below      
      * after selecting a file, the user can click the Show button to the right of the parameter
      * clicking this button will show the supply/demand graph and the buyer/seller info in that file
         ##### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/sd_info.JPG) ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/sd_show.JPG)
            
   * Step c). number of period shocks and number of round shocks can be set
      * optional setting
      * these are advanced settings and can be left at 0 if no shocks desired
      * the user can also choose to set period shocks and have no round shocks or vice versa
         - period shocks and round shocks will be explained further below
                 
   * Step d). the user will need to set the number of periods to allow trading
      * these can be viewed as "trading days" in the market
         
   * Step e). the user will need to set the number of trading rounds to allow during each period/trading day
      * during each round a trader will be randomly selected to place a bid or ask
      * this will continue until either a contract is made or the round times out
         
   * Step f). the user will need to set the price floor and price ceiling
      * the price floor is the minimum price that can be bid while trading, this can be left at 0 or changed
      * the price ceiling is the maximum price that can be bid while trading
      * price ceiling is usually set with respect to the max values in the supply and demand schedule
         
   * Step g). the user will set the market institution to be used while trading
      * these are the rules that the market follows regarding how bidding behavior and buying/selling units is regulated
      * for now the default is DoubleAuction until further institutions are added to the code base
      * these various institutions can be explained in detail by clicking the Explain button next to that parameter
      ##### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/institutions.JPG)
        
   * Step h). the user can choose to enable instantaneous market shocks
      * optional setting
      * this is an advanced setting and can be explained in detail by clicking the Explain button next to that parameter
         ##### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/instant_shocks.JPG)
         - using this parameter will be explained further below
   
   * Step i). once the parameters have been set the user can then click on the Set button to the right of the window
      * this will set the parameters in the system and move the user to the 2nd process of running simulations

   * Error Checks: will result if there are any errors in the user's parameters
      * these will make a window appear that explain the error to the user
      
#### Setting Instantaneous Market Shocks
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/instant_shocks_ex.JPG)
   * If the user wishes to use these shocks they will need to check the box at that parameter
   * This will enable these shocks to occur in the simulation
   * Even after clicking the Set button a user can check the box and click the Set button again to implement these shocks
   * The user will need to set the shift direction of the incoming buyer/seller and shift strategies
      
#### Setting Secondary Parameters (No Shocks)
   * After clicking the Set button the window will be populated with a few more frames
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/simple_set_1.JPG)
   * The user will need to set each trader's strategy used in the trader frame
   * This can be done by clicking on each drop down menu
   * The user can obtain a detailed description of trading strategies by clicking the Strategy Description button
      * this is currently being worked on
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/strategy.JPG)
   * After all of the trading strategies have been set the user can click the Run button in the window
   * Error checks: if any trading strategies are left blank a new window with an error message will appear to the user
   
#### Setting Secondary Parameters (With Period and Round Shocks)
   * If period shocks or round shocks have been set then clicking the Set button will generate frames to set these shocks
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/simple_shocks.JPG)
   * The user will want to enter the period numbers to shock and data file to shock to
   * The user will want to enter the round number to shock and data file to shock to
   * After all of the entries for these shocks have been completed the user can click the Run button in the window
   * Error checks: if any entries are missing a new window with an error message will appear to the user
   
#### Running a Market Simulation
   * After clicking the Run button in the window a new window will appear to the user
   * This window will contain the results from the simulation run
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/run_sim_1.JPG)
   * After this the user can enter the Data Entry window and change parameters, run again, or create new data files
   * All of the data and graphs from this simulation will be saved to the Simulation Save Path that you set earlier
      * to access this data see the next section
      
#### Accessing Saved Simulation Data
   * Whenever the user wishes to access past simulation run data they can do so by opening their file explorer and navigating to the folder they set as their Simulation Save Path earlier
   * After navigating to this folder the user will notice several things contained in the folder
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/period_data_folder.JPG)
   * The user can open any of the graphs that were generated from the simulation run
   * The user can also access all bidding behavior and contract history stored in an excel csv file
   * An example of this excel csv file is displayed below
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/excel_file.JPG)
   
### In Progress Section
#### Graphing Errors
   * supply/demand graphing error and transactions graphing error in run_sim window
   * occurs when re-running the market simulation in market_gui.py
   * can be avoided by re-running the market_gui.py script for each simulation
   
#### Round/Period Shocks Coming
   * work being done on market_gui.py and spot_system.py
   * period shocks and round shocks are not currently available in the market simulator
   
#### Json Data Extensions Coming
   * ability to save in json data files coming
   * user will then be able to choose between saving data in excel csv files or json data files
   
   
   
   



