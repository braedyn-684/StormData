How do I get data from this code?
1. Go to https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
2. Download the StormEvents details files from 1996 to 2024
   a. (https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d1950_c20210803.csv.gz)
   b. thats what it looks like
   c. I put mine in the /StormEvents/ folder
   d. Extract each file into this so that you are just working with csvs and not .gz
3. Run aa_getstormdata.py
   a. Make sure to specify the folder that you put your files in
   b. This is where you can filter the data by state, event type, etc. 
   INPUTS: all those files from step 2
   OUTPUT: Storm Data.csv
4. Run bb_stormdata_cpi.py to get the CPI adjusted values 
   INPUTS: CPI adjustments (retrieved from https://www.bls.gov/cpi/regional-resources.htm)
            - click on southern region
            - specify 1996 to 2024
            - checkmark include annual averages
            - click Download
           Storm Data.csv (from step 3)
   OUTPUT: Storm Data CPI.csv
-----------------STOP HERE IF YOU JUST WANT STORM DATA--------------------------------------
5. Run cc_groupbycounty.py
   INPUT: Storm Data CPI.csv
   OUTPUT: Storm Data by County.csv
6. 
5. Run ice_df.py to get master CSV

