# CouncilDB

This project is a grant council database desgined to store information about grant proposals, competitions, reviewers, and more. The databse is in BCNF, provides triggers to update the tables that hold specific constraints, and has indicies that optimize the performance of querys. 

The database is implemented in sqlite3. This program can was coded on Windows 10 and can run on Winddows 10 by downloading sqlite3 onto your pc. Then navigate te the file where you have downloaded this repository and use the command "sqlite3 council.db". Then you can check out the database using standard sqlite3 syntax. 

The front end is coded in python. It provides a command line interface and presents the user with some query/insertion options. The front end is highly scalabe. Each operation you want to conduct in the database can simply be added to the front end by creating a function for the operation within the python file. 

Thanks for reading, I hope you enjoy the project!











