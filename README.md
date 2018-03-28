# DoubleAuctionMarket

## Experimental Market Simulations

### ------------------------------------------------------------------------------------------------------------
### Created by Kevin McCabe and Alex Payne
### Please read license.txt and requirements.txt before proceeding
### ------------------------------------------------------------------------------------------------------------

#### This project will allow the user to access a gui application for running market simulations, testing multiple trading strategies, testing various market institutions, and researching the effect of shocks in the market 

#### Simple GUI for easy use
  * This interface can be accessed by running market_gui.py
  
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
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/Data Entry.JPG)
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
         ##### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/sd_info.JPG)
            
   * Step c). number of period shocks and number of round shocks can be set
      * these parameters are optional and can be left at 0 if no shocks desired
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
      * this is an optional setting and can be explained in detail by clicking the Explain button next to that parameter
         ##### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/instant_shocks.JPG)
         - using this parameter will be explained further below
   
   * Step i). once the parameters have been set the user can then click on the Set button to the right of the window
      * this will set the parameters in the system and move the user to the 2nd process of running simulations

   * Error Checks: will result if there are any errors in the user's parameters
      * these will make a window appear that explain the error to the user
      
#### Setting Secondary Parameters
   * After clicking the Set button the window will be populated with a few more frames
   #### ![](https://github.com/apayne19/DoubleAuctionMarket/blob/master/Data/icons/simple_set_1.JPG)
   * jljfo
   



