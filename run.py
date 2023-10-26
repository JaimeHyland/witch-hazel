import gspread
from google.oauth2.service_account import Credentials
import sys

help_text = "\n#############################################################################################################################################################\
    \n\n                                                       W I T C H - H A Z E L\
    \nTo run witch-hazel, call the script file that contains its code ('run.py') by simply typing the name of the file on the command line (``run.py``)\
    \nOn opening, the app will show you a list of the options available to you and ask which of them you would like to perform.\
    \n\n0. Help\
    \n1. Close out current year\
    \n\n2. Plan this year's cutting campaign\
    \n3. Record cuttings taken\
    \n4. Record rooted cuttings potted up\
    \n\n5. Plan grafts for this year\
    \n6. Record grafts taken\
    \n\n7. Record plant losses\
    \n8. Record plant gains\
    \n9. Hold over plants for one year\
    \n10. Bring plants forward one year\
    \n\n11. Check plant stock\
    \n\nYou should then type in the number of the operation you wish to perform.\
    \nThe app will then guide you through the operation you have chosen to perform.\
    \nYou will need to restart the app each time you wish to run an operation.\
    \n\nPlease see the README.md file for further details on each of these options.\
    \n\nAt some points it may be necessary to ask you a yes or no question. Where this happens\
    \nyou should answer in the affirmative by typing a 'y' or 'Y' on the command line.\
    \nTyping in any other symbol will be interpreted as a 'No', which will result in the app closing.\
    \n\nIn other cases you will be asked to enter a number. Sometimes the range of valid numbers\
    \nwill indicated. Negative numbers are always interpreted as invalid. Any time you enter an\
    \ninvalid number, the app will give you another opportunity to enter a valid one.\
    \n\n\nPlease look at the relevant section of the README.md file to find out which numbers\
    \n\nare valid in each individual user interaction.\
    \n\n#############################################################################################################################################################\
    \n"

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


SHEET = GSPREAD_CLIENT.open('hamamelis')
rootstock = SHEET.worksheet('rootstock')
grafts_year_zero = SHEET.worksheet('grafts-year-zero')
plants = SHEET.worksheet('plants')

cuttings_taken = int(rootstock.acell('c1').value)
rootstocks_potted = int(rootstock.acell('d1').value)
mature_rootstocks = int(rootstock.acell('e1').value)

rootstock_data = rootstock.get_all_values()
grafts_data = grafts_year_zero.get_all_values()
Plants_data = plants.get_all_values()


def Get_survival_rate(start_num, end_num):
    if int(start_num) == 0:
        return 'The starting number is not recorded.'
    elif int(end_num) > int(start_num):
        return 'You ended up with more units than you started with.'
    else:
        return int(end_num) / int(start_num)

def Is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
        
cutting_success = Get_survival_rate(cuttings_taken, rootstocks_potted) 
potting_success = Get_survival_rate(rootstocks_potted, mature_rootstocks)


"""
The program's main menu on startup
"""
def Startup_instructions():
    print("Welcome to witch-hazel, your simple app for planning your production of grafted Hamamelis plants!\
    \nWhat would you like to do?\
    \nChoose from among the following functions:\
    \n\n0. Help\
    \n\n1. Create new year/Close out current year\
    \n\n2. Plan this year's cutting campaign\
    \n3. Record cuttings taken\
    \n4. Record rooted cuttings potted up\
    \n\n5. Plan grafts for this year\
    \n6. Record grafts taken\
    \n\n7. Record plant losses\
    \n8. Record plant gains\
    \n9. Hold over plants for one year\
    \n10. Bring plants forward one year\
    \n\n11. Check plant stock\
    \nFor full list of the program's functions and instructions on how to call them, enter '0' on the\
    \ncommand line. This will show you the help text for the app.
    \n\nYou must restart the app for each operation you would like to perform.\
    \n\n    
    \n\n")
    
    lower_bound = 0
    upper_bound = 11

    while True:
        user_entry = input(f"Please indicate which operation you would like to perform by entering the corresponding number: \n")
        try:
            int_option = int(user_entry)
            if lower_bound <= int_option <= upper_bound:
                break
            else:
                print(f"Invalid input. Your number must be a whole number between {lower_bound} and {upper_bound}. Please enter a valid number: ")
                print(f"Please indicate which operation you would like to perform by entering the corresponding number: \n")
        except ValueError:
            print(f"Your number must be an integer. Decimal numbers, text and special characters, etc. are not allowed: ")

    Execute_option(int_option)

"""
Option 0
"""

def Help():
    print(help_text)

"""
Option 1:
This function adds the rows necessary to create a new year and copies the row for stocks of this year's grafts from the 
grafts-year-zero to the plants worksheet. It puts the current year out of reach of the relevant seasonal planning and work tasks.
"""
def Create_year():
    rootstock_year = rootstock.acell('a1').value
    new_rootstock_year = int(rootstock_year) + 1

    print(f"The last year created was {rootstock_year}")
    cuttings_last_year = rootstock.acell('c2').value
    if input(f"Would you like to create a record for {new_rootstock_year}? Type 'y' for yes and 'n' for no: \n").lower() == 'y':
        print(f"\nInfo: You took {cuttings_taken} cuttings last year and successfully potted {rootstocks_potted} ({round(cutting_success * 100)}%) of them.\
        \nYou currently have {mature_rootstocks} maturing rootstocks in stock.")
        num_cuttings = int(input(f"How many cuttings would you like to plan for {new_rootstock_year}? \
        \n(Enter 0 if you would like to plan the number of cuttings to be taken later): \n"))
        values = [new_rootstock_year, num_cuttings, 0, 0, 0]
        rootstock.insert_row(values)  
        print(f"Year {new_rootstock_year} created. {num_cuttings} cuttings planned for this year.")
        if num_cuttings == 0:
            print("You've chosen to plan your cutting campaign later!")
        
        year_zero_stocks = grafts_year_zero.get('c4:h4') [0]

        year_zero_stocks_int = [int(value) for value in year_zero_stocks]
        plants.insert_rows([year_zero_stocks_int], 2)

        graft_starting_values = [
            [new_rootstock_year, 'planned', 0, 0, 0, 0, 0, 0],
            [new_rootstock_year, 'grafted', 0, 0, 0, 0, 0, 0],
            [new_rootstock_year, 'stock', 0, 0, 0, 0, 0, 0],
            ]

        grafts_year_zero.insert_rows(graft_starting_values, 2)

    else:
        print(f"The year {new_rootstock_year} has not been created. The current year is still {rootstock_year}")

"""
Option 2:
Helps plan cuttings task
"""
def Plan_cutting_campaign():
    planned_cuttings = rootstock.acell('b1').value
    last_year_cuttings = rootstock.acell('c2').value
    if int(planned_cuttings) > 0:
        if input(f"So far you have planned to take {planned_cuttings} cuttings! Would you like replace that number with a new one?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
            planned_cuttings = int(input(f"You took {last_year_cuttings} cuttings last year. The present planned figure for this year is {planned_cuttings}. Please enter a new figure for planned cuttings for this year: \n"))
            rootstock.update_acell('b1', planned_cuttings)
            print("Cuttings campaign planning session completed")
        else:
            Print("Plan cuttings action cancelled.")
    else:
        if input(f"Would you like to plan the number of cuttings you intend to take this season? \
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
            planned_cuttings = int(input(f"Please enter the number of cuttings you want to take this year: \n"))
            rootstock.update_acell('b1', planned_cuttings)
            print("Cuttings campaign planning session completed")
        else:
            Print("Plan cuttings action cancelled.")

"""
Option 3:
Lets user record cuttings.
Ideally used daily during the cuttings campaign (in Autumn).
"""
def Record_cuttings_taken():
    cuttings_taken = int(rootstock.acell('c1').value)
    cuttings_planned = int(rootstock.acell('b1').value)
    if input(f"So far you have taken {cuttings_taken} cuttings! Would you like to add to that number?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        cuttings_taken += int(input(f"How many cuttings have you now taken in addition to the ones already recorded: \n"))
        rootstock.update_acell('c1', cuttings_taken)
        print(f"You have now taken a total of {cuttings_taken} cuttings out of a planned_total of {cuttings_planned}!")
    else:
        print("Record new cuttings taken action cancelled.")

"""
Option 4:
Lets user record progress in potting up the successfully rooted cuttings (taken the previous Autumn).
Ideally used daily during the potting campaign (in the Spring).
"""
def Record_potted_cuttings():
    cuttings_taken = int(rootstock.acell('c1').value)
    cuttings_potted = int(rootstock.acell('d1').value)
    new_rootstocks = int(rootstock.acell('e1').value)
    if input(f"So far you have taken {cuttings_taken} cuttings! Would you like to add to that number?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        newly_potted = int(input(f"How many cuttings have you now potted up in addition to the ones already recorded: \n"))
        cuttings_potted += newly_potted
        new_rootstocks += newly_potted
        rootstock.update_acell('d1', cuttings_potted)
        rootstock.update_acell('e1', cuttings_potted)
        print(f"You have now potted up a total of {cuttings_potted} cuttings out of a total of {cuttings_taken}! That means you now have {new_rootstocks} immature rootstocks for grafting next year.")
    else:
        print("Record new cuttings potted action cancelled.")

"""
Option 5:
Lets user add a planned number of grafts for each cultivar.
Should be used in late winter.
Shows the user the total number of rootstocks ready for grafting and the number left.
Warns the user when they're planning to use more rootstocks than they actually have.
"""
def Plan_grafting_campaign():
    rootstocks_available = int(rootstock.acell('e2').value)

    row_values = grafts_year_zero.row_values(1)
    first_empty_index = next((i for i, val in enumerate(row_values) if not val), len(row_values))
    last_column = chr(ord('A') + first_empty_index)
    print(last_column)
    name_range = f"c1:{last_column}1"
    value_range = f"c2:{last_column}2"

    row_numbers = [1, 2]

    ranges = [f'A{row}:{last_column}{row}' for row in row_numbers]

    data = {}

    for range_to_read in ranges:
        values =grafts_year_zero.get(range_to_read)[0]
        keys = grafts_year_zero.get(range_to_read.replace(str(row_numbers[0]), str(row_numbers[1])))[0]
        data.update(dict(zip(keys, values)))

    print(data)

    cultivars = grafts_year_zero.get(name_range) [0]
    planned_numbers = grafts_year_zero.get(value_range) [0]
    count = 0
    print(f"For which cultivar would you like to plan a grafting campaign?\
    \nYou currently have {rootstocks_available} rootstocks available for use in grafting. \n")
    for cultivar in cultivars:
        count += 1
        print(f"{count}. {cultivar}")

    print("For which cultivar would you like to plan your grafting?\n")
    cultivar_value = int(input("Please enter the number of the cultivar for which you want to plan grafting (see the cultivar listed above): \n"))

"""
Option 6:
Lets user record the number of grafts taken for each cultivar.
Should be used in late winter.
Shows the user the total number of rootstocks ready for grafting and the number left.
Warns the user when they've used more rootstocks than they actually have. 
"""
def Record_grafts():
    print("Grafts recorded")    

"""
Option 7:
Lets user record losses in stocks for any cultivar in any year. 
Works for both rooted cuttings and grafted cultivars.
May be used throughout the year.
Losses of cuttings are not recorded until the time comes to pot up those of them that have rooted successfully.
"""
def Record_loss():
    print("Loss recorded")

"""
Option 8:
Essentially the opposite of Option 7.
"""
def Record_gain():
    print("Acquisition_recorded")

"""
Option 9:
Essentially a combination of Options 7 and 8.
Results in the number of cultivars from year n being removed and then added to year n-1.
"""
def Hold_back():
    print("Stocks held back")

"""
Option 10:
The same as Option 9, but in the opposite direction.
Results in the number of cultivars from year n being removed and then added to year n-1.
"""
def Bring_forward():
    print("Stocks brought forward")

"""
Option 11:
Reports on the current situation for the current year showing 
on screen a list of all planned and actual cutting and graft numbers for the year.
"""
def Check_plant_stock():
    print("Plant stocks checked")



"""
Executes the option chosen by the user
"""   
def Execute_option(operation):
    if operation == 0:
        print("You have chosen HELP.")
        Help()
    elif operation == 1:
        print("You have chosen to close out the current year and open a new one.")
        Create_year()
    elif operation == 2:
        print("You have chosen to plan this year's cutting campaign.")
        Plan_cutting_campaign()
    elif operation == 3:
        print("You have chosen to record having taken some cuttings.")
        Record_cuttings_taken()
    elif operation == 4:
        print("You have chosen to record having potted some rooted cuttings.")
        Record_potted_cuttings()
    elif operation == 5:
        print("You have chosen to plan your grafting campaign.")
        Plan_grafting_campaign()
    elif operation == 6:
        print("You have chosen to record having created a number of new grafts")
        Record_grafts()
    elif operation == 7:
        print("You have chosen to record the loss of a number of grafted plants")
        Record_loss()
    elif operation == 8:
        print("You have chosen to record the acquisition of a number of grafted plants")
        Record_gain()
    elif operation == 9:
        print("You have chosen to hold back a number of grafted plants from their cohort to the previous one")
        Hold_back()
    elif operation == 10:
        Bring_forward()
        print("You have chosen bring a number of grafted plants forward from their cohort to next one")
    elif operation == 11:
        Check_plant_stock()
    else:
        Print("Please enter a valid integer between 1 and 11")

Startup_instructions()
