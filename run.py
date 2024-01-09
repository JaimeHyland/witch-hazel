import gspread
import help_messages
from google.oauth2.service_account import Credentials
import sys

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

def check_is_numeric(user_input, min=0, max=10000, not_a_number_blurb=" is not a number. Please enter a number between ", 
        not_in_range_blurb="That number is out of range. Please enter a number between "):
    try:
        number = int(user_input)
        if min <= number <= max:
            return number
        else:
            return check_is_numeric(input(f"{not_in_range_blurb}{min} and {max}:"), min, max)
    except:
        if user_input.lower()=='exit':
            exit()
        elif user_input.lower().split()[0]=='help' and int(user_input.lower().split()[1]):
            if min <= int(user_input.lower().split()[1]) <= max:
                help(user_input.lower())
            else:
                return check_is_numeric(input(f"{user_input}{not_a_number_blurb}{min} and {max}:"), min, max)
        else:
            return check_is_numeric(input(f"{user_input}{not_a_number_blurb}{min} and {max}:"), min, max)

def Get_survival_rate(start_num, end_num):
    if int(start_num) == 0:
        return 'The starting number is not recorded.'
    elif int(end_num) > int(start_num):
        return 'You ended up with more units than you started with.'
    else:
        return int(end_num) / int(start_num)

cutting_success = Get_survival_rate(cuttings_taken, rootstocks_potted)
potting_success = Get_survival_rate(rootstocks_potted, mature_rootstocks)


def Startup_instructions():
    """
    The program's main menu on startup
    The user may need to scroll up to see the whole text.
    """

    lower_bound = 0
    upper_bound = 11

    print(help_messages.intro_text1)
    print("Press Enter to continue ...")
    input()
    print(help_messages.intro_text2)

    while True:
        user_input = input(f"Please indicate which operation you would like to perform by\
        \nentering the corresponding number: \n")
        try:
            int_option = int(user_input)
            if lower_bound <= int_option <= upper_bound:
                break
            else:
                print(f"Invalid input. Your number must be a whole number between {lower_bound} and\
                \n{upper_bound}. Please enter a valid number: ")
        except ValueError:
            if user_input.lower() == 'exit':
                print("Exiting witch-hazel app")
                exit()
            else:
                print(f"Your number must be a positive integer or 0. Negative and\
                \ndecimal-point numbers, text and special characters, etc. are not allowed:\n")

    Execute_option(int_option)


def help(option_no=0):
    if option_no==0:
        print(help_messages.help_text1)
        input("Press Enter to see more help!")
        print(help_messages.help_text2)

        print("Press Enter to continue ...")
        input()
        Startup_instructions()
    elif option_no==0:
        print("Typing a 0 from the main menu takes you into the general Help function, which\
        \ngives you summary details on each of the eleven functions of the App.")
        input("Would you like to go to the general Help function now?")
    elif input == "help 1":
        print("Option 1 tells you what the current year is, gives you detailed statistics\
        on the work you've already planned and recorded as completed for that year, and\
        \nasks you if you're sure you want to close out that year and create a new year.\
        \nIf you confirm, it will close out the year and create a new set of records for\
        \nthe new current year, which will be the previous year plus one.\
        \n\nBe very careful all your planning is done and all your work for the current year\
        \nhas been completed and recorded before confirming that you want to create a new year.\
        \n\nYou should run this option only once a year. We recommend doing so either on\
        \n31 December of the old current year or as early as possible in January of the new\
        current year.")
    elif input == "Option 2":
        print("Option 2 lets you record the number of cuttings for future rootstocks that\
        \nyou plan to make for the current year. Later, when you use Option 3 to record\
        \nthe cuttings you've actually taken (which you can do as often as you like), the App\
        \nwill let you know when you've reached the number of cuttings you originally planned\
        \nfor the current year.\
        \n\nIf you run Option 2 a second time, the App will tell how many cuttings you planned\
        \nin the previous session and asks you to confirm whether you want to change this number.\
        \nIf you confirm and enter a new number, this new entry will REPLACE the previous number.\
        \nIt will not be summed together with the old number!")
    elif operation == "Option 3":
        print("Option 3 lets you record the number of cuttings you have taken since you last ran\
        \nthat Option (or, if you are running the Option for the first time in the current year,\
        \nthe number of cuttings you have taken so far in the current year).\
        \n\nYou can run Option 3 as often as you like, though we recommend running it every time\
        \nyou've completed a session of cutting taking, while the number of cuttings you've taken\
        \nin that session is still fresh in your mind.\
        \n\nEach time you record a number of cuttings made, that number is added to the previous\
        \ntotal.\
        \n\nThe App will tell you when you've reached (or exceeded) the number of cuttings you\
        \nplanned to make (using Option 2).")
    elif operation == "Option 4":
        print("Option 4 lets you record the number of rooted cuttings you have potted up\
        \nsince you last ran that Option (or, if you are running the Option for the first time\
        \nin the current year, the number of rooted cuttings you have potted up so far\
        \nin the current year).\
        \n\nYou can run Option 4 as often as you like, though we recommend running it every time\
        \nyou've completed a session of potting up rooted cuttings, while the number you've potted\
        \nup in that session is still fresh in your mind.\
        \n\nEach time you record some rooted cuttings being potted up, that number is added to\
        \nthe previous total.\
        \n\nThe App will warn you when you've reached (or exceeded) the number of cuttings you\
        \nhave recorded as being available for potting up (i.e. the number of cuttings made,\
        \nminus any losses you have recorded since then).")
    elif operation == "help 5":
        print("Option 5 lets you record the number of grafts you plan to make for each cultivar\
        \nof Hamamelis in the current year. Later, when you use Option 6 to record\
        \nthe grafts you've actually taken for the chosen cultivar (which you can do as often\
        \nas you like), the App will let you know when you've reached the number of grafts\
        \nof that cultivar you originally planned for the current year.\
        \n\nWhen you choose Option 5, the App will output the list of cultivars recorded in\
        \nyour data and ask you choose the number of the cultivar whose grafting program you\
        \nwish to plan for the year.\
        \n\nIf you run Option 5 a second time for the same cultivar, the App will tell how\
        \nmany grafts you planned in the previous session and asks you to confirm whether\
        \nyou want to change this number. If you confirm and enter a new number, this new\
        \nentry will REPLACE the previous number. It will not be summed together with the\
        \nold number!")
    elif operation == "help 6":
        print("Option 6 lets you record the number of grafts of your chosen cultivar you have\
        \ntaken since you last ran that Option for that cultivar (or, if you are running\
        \nthe Option for the first time in the current year, the number of grafts you have\
        \ntaken so far of that graft in the current year).\
        \n\nWhen you choose Option 5, the App will output the list of cultivars recorded in\
        \nyour data and ask you choose the number of the cultivar for which you want to\
        \nrecord new grafts.\
        \n\nYou can run Option 6 as often as you like for any cultivar, though we recommend\
        \nrunning it every time you've completed a session of grafting , while the number\
        \nof grafts you've taken in that session is still fresh in your mind.\
        \n\nEach time you record a number of grafts made for a particular cultivar, that\
        \nnumber is added to the previous total for that cultivar.\
        \n\nThe App will tell you when you've reached (or exceeded) the number of grafts you\
        \nplanned to make for that cultivar (using Option 2).")
    elif operation == "help 7":
        print("Option 7 lets you record any losses of grafted plants you may suffer. It first\
        \nasks you to identify the cultivar that has suffered losses and the age of that cultivar\
        \n(1 for year-one plants, 2 for year-two plants and so on).\
        \n\nThe number you enter will then be subtracted from the numbers of plants recorded as\
        \nbeing in stock for that cultivar and that age.\
        \n\nWe recommend running this option as soon as you can after noting and disposing of\
        \ndead or irreversibly damaged plants.\
        \n\nThe App will not allow you to record losses greater than the total stock of the\
        \naffected cultivar and age. It will let you know when stocks of the affected plants\
        \nreach zero.")
    elif operation == "help 8":
        print("Option 8 lets you record any acquisitions of grafted plants you may make. It first\
        \nasks you to identify the cultivar you have purchased or otherwise acquired and the age\
        \nof that cultivar (1 for year-one plants, 2 for year-two and so on).\
        \n\nThe number you enter will then be added to the numbers of plants recorded as\
        \nbeing in stock for that cultivar and that age.\
        \n\nWe recommend running this option as soon as you can after acquiring new plants.\
        \n\nThe App will let you know when stocks of the affected plants reach the originally\
        \nplanned number.")
    elif operation == "help 9":
        print("A grafted plant assugned a particular age, is not necessarily of that age. The best way\
        \nof putting it would be to say that Year-Two plants are plants of the size and quality\
        \ntypical of plants in their second year of growth after grafting. Any plants that have\
        \ngrown more slowly or faster during the year may need to be reclassified to reflect their\
        \nprogress. Options 9 and 10 allow you to do this.\
        \n\nOption 9 allows you to hold back slower plants for a year, so that a number of Year-Three\
        \nplants, for example, are held back to Year Two.\
        \n\nIt first asks you to identify the cultivar you want to hold back and then the age\
        \nof that cultivar (1 for Year-One grafted plants, 2 for Year-Two plants and so on).\
        \n\nThe affected plants will be held back by one year.\
        \n\nThe App will not let you know hold back more of the affected plants than there are in\
        \nstock.\
        \n\nWe recommend recording such changes as soon as you have physically moved the affected\
        \nplants to the appropriate section of the nursery.")
        Hold_back()
    elif operation == 10:
        print("A grafted plant assigned a particular age is not necessarily of that age. The best way\
        \nof putting it would be to say that Year-Two plants are plants of the size and quality\
        \ntypical of plants in their second year of growth after grafting. Any plants that have\
        \ngrown more slowly or faster during the year may need to be reclassified to reflect their\
        \nprogress. Options 9 and 10 allow you to do this.\
        \n\nOption 10 allows you to bring forward stronger plants by a year, so that a number of\
        \nYear-Three plants, for example, are brought forward to Year Four.\
        \n\nIt first asks you to identify the cultivar you want to bring forward and then the age\
        \nof that cultivar (1 for Year-One grafted plants, 2 for Year-Two plants and so on).\
        \n\nThe affected plants will be brought forward by one year.\
        \n\nThe App will not let you know bring forward more of the affected plants than there are in\
        \nstock.\
        \n\nWe recommend recording such changes as soon as you have physically moved the affected\
        \nplants to the appropriate section of the nursery.")
        Bring_forward()
    elif operation == 11:
        print("Sorry! This functionality has not yet been implemented.")
        Add_new_cultivar()
    else:
        print("Please enter a valid integer between 0 and 11")


def Create_year():
    """
    Option 1:
    This function adds the rows necessary to create a new year and copies the
    row for stocks of this year's grafts from the
    grafts-year-zero to the plants worksheet. It puts the current year out of
    reach of the relevant seasonal planning and work tasks.
    """
    rootstock_year = rootstock.acell('a1').value
    new_rootstock_year = int(rootstock_year) + 1

    print(f"The last year created was {rootstock_year}")
    cuttings_last_year = rootstock.acell('c2').value
    if input(f"Would you like to create a record for {new_rootstock_year}?\
    \nType 'y' for yes and 'n' for no: \n").lower() == 'y':
        print(f"\nInfo: You took {cuttings_taken} cuttings last year.\
        \nYou now have {mature_rootstocks} maturing rootstocks in stock.")
        num_cuttings = check_is_numeric(input(f"How many cuttings would you like to plan for {new_rootstock_year}? \
        \n(Enter 0 if you want to plan cutting numbers later): \n"))
        values = [new_rootstock_year, num_cuttings, 0, 0, 0]
        rootstock.insert_row(values)
        rootstock.update_acell('e3', 0)
        print(f"Year {new_rootstock_year} created. {num_cuttings} cuttings planned\
        \nfor this year.")
        if num_cuttings == 0:
            print("You've chosen to plan your cutting campaign later!")

        year_zero_stocks = grafts_year_zero.get('c4:h4')[0]

        year_zero_stocks_int = [int(value) for value in year_zero_stocks]
        plants.insert_rows([year_zero_stocks_int], 2)

        graft_starting_values = [
            [new_rootstock_year, 'planned', 0, 0, 0, 0, 0, 0],
            [new_rootstock_year, 'grafted', 0, 0, 0, 0, 0, 0],
            [new_rootstock_year, 'stock', 0, 0, 0, 0, 0, 0],
            ]

        grafts_year_zero.insert_rows(graft_starting_values, 2)

    else:
        print(f"The year {new_rootstock_year} has not been created.\
        \nThe current year is still {rootstock_year}")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Plan_cutting_campaign():
    """
    Option 2:
    Helps plan cuttings task
    """
    planned_cuttings = int(rootstock.acell('b1').value)
    last_year_cuttings = int(rootstock.acell('c2').value)
    last_year_rooted_cuttings = int(rootstock.acell('d2').value)
    this_year_cuttings_taken = int(rootstock.acell('c1').value)
    current_year = int(rootstock.acell('a1').value)
    if int(planned_cuttings) > 0:
        if input(f"So far you have planned to take {planned_cuttings} cuttings for {current_year}! Would you like replace that number with a new one?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
            
            planned_cuttings = check_is_numeric(input(f"You took {last_year_cuttings} cuttings last year, resulting in {last_year_rooted_cuttings} successfully rooted cuttings.\
            \nThe present planned figure for this year is {planned_cuttings}.\
            \nEnter a new figure for planned cuttings for this year: \n"))
            if planned_cuttings <= this_year_cuttings_taken:
                if input(f"You have already taken {this_year_cuttings_taken} cuttings this year. This is more than your new planned figure!\
                \nAre you sure you want to replace the planned figure with this one?\
                \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
                    rootstock.update_acell('b1', planned_cuttings)
                    print("Planned number of cuttings successfully changed.\
                    \nCuttings campaign planning session completed")
            else:
                rootstock.update_acell('b1', planned_cuttings)
                print("Planned number of cuttings successfully changed.\
                \nCuttings campaign planning session completed")
        else:
            print("Plan cuttings action cancelled.\
            \nNo changes have been made to the data.")
    else:
        if input(f"Would you like to plan the number of cuttings you intend to take this season?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
            planned_cuttings = check_is_numeric(input(f"Please enter the number of cuttings\
            \nthat you want to take this year: \n"))
            rootstock.update_acell('b1', planned_cuttings)
            print("Planned number of cuttings successfully changed.\
            \nCuttings campaign planning session completed")
        else:
            print("Plan cuttings action cancelled.\
            \nNo changes have been made to the data.")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Run_main_if_clause(taken, planned):
    """
    Option 3:
    Lets user record cuttings.
    Ideally used daily during the cuttings campaign (in Autumn).
    """
    if taken >= planned:
        print(f"You have already reached the number of cuttings you planned to take this year: \
        \n{taken} cuttings taken out of {planned} planned!")
    else:
        print(f"So far you have taken {taken} cuttings!")

    if input("Would you like to add to that number?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        taken += check_is_numeric(input(f"How many cuttings have you now taken in addition to the ones\
        \nyou've already recorded: \n"))
        rootstock.update_acell('c1', taken)
        if taken >= planned:
            print(f"Congratulations! You have achieved the planned number of cuttings: \
            \n{taken} cuttings taken out of {planned} planned!")
        else:
            print(f"You have now taken a total of {taken} cuttings out of a planned total\
            \nof {planned}!")

        print("Cuttings campaign record added successfully.")
    else:
        print("Cuttings taken action cancelled.\
        \nNo changes have been made to the data.")
    
    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Record_cuttings_taken():
    cuttings_taken = int(rootstock.acell('c1').value)
    cuttings_planned = int(rootstock.acell('b1').value)
    cuttings_rooted = int(rootstock.acell('d1').value)
    if cuttings_rooted > 0:
        if input("You have already begun potting up cuttings for this year.\
        \nAre you sure you want to take cuttings at this time?\
        \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
            Run_main_if_clause(cuttings_taken, cuttings_planned)
        else:
            print("Record new cuttings taken action cancelled.\
            \nNo changes have been made to the data.")
    else:
        Run_main_if_clause(cuttings_taken, cuttings_planned)

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Record_potted_cuttings():
    """
    Option 4:
    Lets user record progress in potting up the successfully rooted cuttings
    (taken the previous Autumn).
    Ideally used daily during the potting campaign (in the Spring).
    """
    cuttings_taken = int(rootstock.acell('c1').value)
    cuttings_potted = int(rootstock.acell('d1').value)
    new_rootstocks = int(rootstock.acell('e1').value)
    if input(f"So far you have potted up {cuttings_potted} cuttings! Would you like to add to that number?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        newly_potted = check_is_numeric(input(f"How many cuttings have you now potted up in addition\
        \nto the ones already recorded: \n"))
        if cuttings_potted + newly_potted > cuttings_taken:
            print(f"If {newly_potted} is added to the existing figure of newly rooted cuttings ({new_rootstocks}), then you'll have potted up more cuttings than you took in the Autumn.\
            \nThat is not normally possible!\
            \nIf you're sure that the total number of newly potted rootstocks is in fact {newly_potted + new_rootstocks}, \
            \nthen you must first change the figure for cuttings (Option 3) before continuing!\
            \nRecord new cuttings potted action cancelled.\
            \nNo changes have been made to the data.")
        else:
            cuttings_potted += newly_potted
            new_rootstocks += newly_potted
            rootstock.update_acell('d1', cuttings_potted)
            rootstock.update_acell('e1', new_rootstocks)
            print(f"You have now potted up a total of {cuttings_potted} cuttings out of a total of {cuttings_taken}!\
            \nThat means you now have {new_rootstocks} immature rootstocks available for grafting next year\
            \n(minus any losses in the meantime).")
    else:
        print("Record new cuttings potted action cancelled.\
        \nNo changes have been made to the data.")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Plan_grafting_campaign():
    """
    Option 5:
    Lets user add a planned number of grafts for each cultivar.
    Should be used in late winter (February or March).
    Shows the number of rootstocks ready for grafting and the number left.
    Warns the user when they're planning to use more rootstocks than they have.
    """
    rootstocks_available = int(rootstock.acell('e2').value)

    row_values = grafts_year_zero.row_values(1)
    # Find the column to stop at (first column that contains no data)
    first_empty_index = next((i for i,
                              val in enumerate(row_values) if not val),
                             len(row_values))
    last_column = chr(ord('a') + first_empty_index)

    name_range = f"c1:{last_column}1"
    planned_range = f"c2:{last_column}2"

    cultivars = grafts_year_zero.get(name_range)[0]
    planned_numbers = grafts_year_zero.get(planned_range)[0]
    """
    Converts the strings in the planned numbers list into integers
    to make it possible to sum them together.
    """
    planned_numbers = [int(x) for x in planned_numbers]
    total_planned = sum(planned_numbers)

    print(f"For which cultivar would you like to plan a grafting campaign?\
    \nYou currently have {rootstocks_available} rootstocks available for use in grafting.\
    \nOf these, {rootstocks_available - total_planned} are not yet\
    \nreserved in your plan")

    # List out the cultivars you have in your data in an ordered list.
    count = 0
    for cultivar in cultivars:
        count += 1
        print(f"{count}. {cultivar}")

    print("For which cultivar would you like to plan your grafting?\n")
    cultivar_value = check_is_numeric(input("Please enter the number of the cultivar for which you want to plan grafting\
    \n(see the cultivars listed above): \n"), 1, count)
    cell_address = f"{chr(ord('c') + cultivar_value - 1)}2"
    print(cell_address)
    print(f"You have chosen to plan graft numbers\
    \nfor {cultivars[cultivar_value - 1]}")
    print(f"So far, you have planned to make\
    \n{planned_numbers[cultivar_value - 1]} grafts of this cultivar.")
    if input("Would you like to replace this value?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        new_planned_value = check_is_numeric(input(f"Type in the new planned value\
        \nfor {cultivars[cultivar_value - 1]}: \n"))
        grafts_year_zero.update_acell(cell_address, new_planned_value)
        print(f"Planned number of grafts for {cultivars[cultivar_value - 1]} successfully changed.\
            \nCuttings campaign planning session completed")

    else:
        print(f"Plan grafts action for {cultivars[cultivar_value - 1]} cancelled.\
        \nNo changes have been made to the data.")
    
    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Record_grafts():
    """
    Option 6:
    Lets user record the number of grafts taken for a chosen cultivar.
    Should be used in late winter; at grafting time.
    Shows the total for rootstocks ready for grafting and the number left.
    Warns the user when they've used more rootstocks than they actually have.
    """
    rootstocks_available = int(rootstock.acell('e2').value)

    row_values = grafts_year_zero.row_values(1)

    # Find the column to stop at (first column that contains no data).
    first_empty_index = next((i for i,
                              val in enumerate(row_values) if not val),
                             len(row_values))
    last_column = chr(ord('a') + first_empty_index)

    name_range = f"c1:{last_column}1"  # Names of cultivars
    planned_range = f"c2:{last_column}2"  # Numbers of planned grafts
    grafted_range = f"c3:{last_column}3"  # Plants already grafted

    cultivars = grafts_year_zero.get(name_range)[0]
    planned_numbers = grafts_year_zero.get(planned_range)[0]
    # Converts the strings in the planned numbers list into integers
    # to make it possible to sum them together.
    planned_numbers = [int(x) for x in planned_numbers]
    total_planned = sum(planned_numbers)
    grafts_this_year = grafts_year_zero.get(grafted_range)[0]
    grafts_this_year = [int(x) for x in grafts_this_year]
    total_grafted = sum(grafts_this_year)

    print(f"For which cultivar would you like record new grafts completed?\
    \nYou currently have {rootstocks_available} rootstocks available for use in grafting.\
    \nOf these, {rootstocks_available - total_planned} are not yet reserved\
    \nin your plan.")

    # List out the names of the cultivars you have in your data
    # in an ordered list.
    count = 0
    for cultivar in cultivars:
        count += 1
        print(f"{count}. {cultivar}")

    print("Which cultivar has been grafted?\n")

    cultivar_value = check_is_numeric(input("Please enter the cultivar number of the new grafts you want to record\
    \n(see the cultivars listed above): \n"), 1, count)
    address_grafts = f"{chr(ord('c') + cultivar_value - 1)}3"
    address_rootstocks = 'e2'
    grafts_this_cultivar = grafts_this_year[cultivar_value - 1]
    print(f"You have chosen to record grafts of\
    \n{cultivars[cultivar_value - 1]}")
    print(f"So far, you have grafted {grafts_this_cultivar} of this cultivar.")
    if input("Would you like to add to this value?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        newly_made_grafts = check_is_numeric(input(f"Type in the number of new grafts you have made of\
        \n{cultivars[cultivar_value - 1]}: \n"))
        grafts_this_cultivar += newly_made_grafts
        grafts_year_zero.update_acell(address_grafts, grafts_this_cultivar)
        rootstock.update_acell(address_rootstocks,
                               int(rootstock.acell(address_rootstocks).value) -
                               newly_made_grafts)
        print(f"Number of grafts made for {cultivars[cultivar_value - 1]} successfully changed.\
            \nThe new total of grafts made this year\
            \nfor this cultivar is {grafts_year_zero.acell(address_grafts).value}\
            \nSuccessfully completed record of new grafts made.")

    else:
        print(f"Plan grafts action for {cultivars[cultivar_value - 1]} cancelled.\
        \nNo changes have been made to the data.")
    
    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Record_loss():
    """
    Option 7:
    Lets user record losses in stocks for any cultivar in any year.
    Works for both rooted cuttings and grafted cultivars.
    May be used throughout the year.
    Losses of cuttings are not recorded until the time comes to pot
    up those of them that have rooted successfully.
    """
    # Did we lose new_rootstocks?
    if input(f"Would you like to record a loss of new rootstocks?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        address_affected = 'e1'
        total_rootstocks = int(rootstock.acell(address_affected).value)

        print(f"At the last count there were {total_rootstocks} new rootstocks in the nursery")

        while True:
            number_lost = input("How many rootstocks have been lost since then? \n")
            try:
                number_lost = int(number_lost)
                if 0 <= number_lost <= total_rootstocks:
                    break
                else:
                    print(f"You can't have lost more rootstocks than you actually had in the nursery!\
                    \nPlease enter an integer between 0 and\
                    {total_rootstocks}: ")
            except ValueError:
                print(f"Your number must be a positive integer or 0. Negative and decimal-point numbers,\
                \ntext and special characters, etc. are not allowed: ")

        rootstock.update_acell(address_affected,
                               total_rootstocks - number_lost)
        print(f"Loss of {number_lost} new rootstocks recorded.\
        \nYou now have a stock of {rootstock.acell(address_affected).value} new rootstocks.")
    else:
        """
        If what's been lost is grafted plants
        First define the cultivar affected
        """
        row_values = plants.row_values(1)
        # Find the column to stop at (first column that contains no data).
        first_empty_index = next((i for i,
                                  val in enumerate(row_values) if not val),
                                 len(row_values))
        last_column = chr(ord('a') + first_empty_index)

        name_range = f"a1:{last_column}1"  # Names of cultivars
        cultivars = plants.get(name_range)[0]

        # List the names of the cultivars in the data in an ordered list.
        print(f"For which cultivar would you like record a loss?")
        count = 0
        for cultivar in cultivars:
            count += 1
            print(f"{count}. {cultivar}")

        cultivar_value = check_is_numeric(input("Please enter the cultivar number for which you want to record a loss\
        \n(see the cultivars listed above): \n"))
        affected_year = check_is_numeric(input("Please enter the age of the plants for which you want to record a loss\
        \n(typing '1' for year-one plants, '2' for year-two plants, and so on): \n"))
        address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year + 1}"

        current_number = int(plants.acell(address_affected).value)
        print(f"You have chosen to register a loss of {cultivars[cultivar_value - 1]} of age year-{affected_year}.\
        \nThere are currently {current_number} plants of that category\
        recorded in the system.")
        while True:
            number_lost = input("How many plants of that category have been lost since then? \n")
            try:
                number_lost = int(number_lost)
                if 0 <= number_lost <= current_number:
                    break
                else:
                    print(f"You can't have lost more plants of this category than you actually had in the nursery!\
                    \nPlease enter an integer between 0 and {current_number}.")
            except ValueError:
                print(f"Your number must be a positive integer or 0.\
                \nNegative and decimal-point numbers, text and special characters, etc. \
                are not allowed: ")
        current_number -= number_lost
        plants.update_acell(address_affected, current_number)
        print(f"Loss of {number_lost} {cultivars[cultivar_value - 1]} of year-{affected_year} recorded.\
        \nYou now have a remaining stock of {plants.acell(address_affected).value} plants of that category.")

        # number_lost
    print("Loss recorded successfully.")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Record_gain():
    """
    Option 8:
    Essentially the opposite of Option 7.
    """
    # Did we acquire new_rootstocks ...?
    if input(f"Would you like to record an acquisition of new rootstocks?\
    \nType 'y' for yes or 'n' for no: \n").lower() == 'y':
        address_affected = 'e1'
        total_rootstocks = int(rootstock.acell(address_affected).value)

        print(f"At the last count there were {total_rootstocks} \
        new rootstocks in the nursery")

        while True:
            number_gained = input("How many rootstocks have\
            been acquired since then? \n")
            try:
                number_gained = int(number_gained)
                break
            except ValueError:
                print(f"Your number must be a positive integer or 0.\
                \nNegative and decimal-point numbers, text and special characters, \
                etc. are not allowed: ")

        rootstock.update_acell(address_affected,
                               total_rootstocks + number_gained)
        print(f"Acquisition of {number_gained} new rootstocks recorded.\
        \nYou now have a stock of {rootstock.acell(address_affected).value}\
        new rootstocks.")
    else:
        """
        If what's been gained is grafted plants
        First define the cultivar affected
        """
        row_values = plants.row_values(1)
        # Find the column to stop at (first column that contains no data).
        first_empty_index = next((i for i,
                                  val in enumerate(row_values) if not val),
                                 len(row_values))
        last_column = chr(ord('a') + first_empty_index)

        name_range = f"a1:{last_column}1"  # Names of cultivars
        cultivars = plants.get(name_range)[0]

        # List the cultivars in the data in an ordered list.
        print(f"For which cultivar would you like record an acquisition?")
        count = 0
        for cultivar in cultivars:
            count += 1
            print(f"{count}. {cultivar}")

        cultivar_value = check_is_numeric(input("Please enter the cultivar number for which you want to enter an acquisition\
        \n(see the cultivars listed above): \n"), 1, count)
        affected_year = check_is_numeric(input("Please enter the age of the plants for which you want to enter an acquisition\
        \n(typing '1' for year-one plants, '2' for year-two plants, and so on): \n"), 1, 5)
        address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year + 1}"

        current_number = int(plants.acell(address_affected).value)
        print(f"You have chosen to register an acquisition of {cultivars[cultivar_value - 1]} of age year-{affected_year}.\
        \nThere are currently {current_number} plants of that category recorded in the system.")
        while True:
            number_gained = input("How many plants of that category have been acquired since the last recorded entry? \n")
            try:
                number_gained = int(number_gained)
                break
            except ValueError:
                print(f"Your number must be a positive integer or 0.\
                \nNegative and decimal-point numbers, text and special characters, etc. \
                are not allowed: ")
        current_number += number_gained
        plants.update_acell(address_affected, current_number)
        print(f"Acquisition of {number_gained} {cultivars[cultivar_value - 1]} of year-{affected_year} recorded.\
        \nYou currently have a stock of {plants.acell(address_affected).value} plants of that category.")

        # number_lost
    print("Acquisition recorded successfully.")
    
    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Hold_back():
    """
    Option 9:
    Essentially a Option 7 with a twist.
    Results in the given number of the chosen cultivar from year n
    being removed and then added to year n-1.
    """

    # First define the cultivar affected
    row_values = plants.row_values(1)
    # Find the column to stop at (first column that contains no data).
    first_empty_index = next((i for i,
                              val in enumerate(row_values) if not val),
                             len(row_values))
    last_column = chr(ord('a') + first_empty_index)

    name_range = f"a1:{last_column}1"  # Names of cultivars
    cultivars = plants.get(name_range)[0]

    # List out the cultivars in the data in an ordered list.
    print(f"For which cultivar would you like hold back plants?")
    count = 0
    for cultivar in cultivars:
        count += 1
        print(f"{count}. {cultivar}")

    cultivar_value = check_is_numeric(input("Please enter the cultivar number for which you want to hold plants back (see\
    \nthe cultivars listed above): \n"))
    while True:
        affected_year = check_is_numeric(input("Please enter the age of the plants that you want to hold back (typing '2'\
        \nfor year-two plants or '3' for year-three plants, and so on): \n"))
        try:
            affected_year = int(affected_year)
            if affected_year > 1:
                break
            elif affected_year == 1:
                print(f"Year-one plants cannot be held back. Enter 2 or higher. But remember there's\
                \nno point in entering an age greater than the age of the \
                nursery.")
            else:
                print(f"Please enter an integer between 2 and \
                the age of the nursery.")
        except ValueError:
            print(f"Your number must be an integer greater than 2 and less than the age of the\
            \nnursery. Negative and decimal-point numbers, text and special characters, etc.\
            \nare not allowed: ")

    from_address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year + 1}"
    to_address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year}"

    current_number_from = int(plants.acell(from_address_affected).value)
    current_number_to = int(plants.acell(to_address_affected).value)
    print(f"You have chosen to hold back {cultivars[cultivar_value - 1]} plants of age year-{affected_year}.\
    \nThere are currently {current_number_from} plants of that category recorded in the system.\
    \nThere are now {current_number_to} plants of that cultivar listed as being a year younger.\
    \nThe specified number of plants will be held back for a year.")
    while True:
        number_held_back = input("How many plants of that category do you want to hold back a year? \n")
        try:
            number_held_back = int(number_held_back)
            if 0 <= number_held_back <= current_number_from:
                break
            else:
                print(f"You can't hold back more plants of this category than you actually have in the\
                \nnursery! Please enter an integer between 0 and \
                {current_number_from}: ")
        except ValueError:
            print(f"Your number must be a positive integer or 0. Negative and decimal-point numbers,\
            \ntext and special characters, etc. are not allowed: ")

    current_number_from -= number_held_back
    current_number_to += number_held_back
    plants.update_acell(from_address_affected, current_number_from)
    plants.update_acell(to_address_affected, current_number_to)
    print(f"Successfully recorded holding back {number_held_back} {cultivars[cultivar_value - 1]} plants of year-{affected_year}.\
    \nYou now have a remaining stock of {plants.acell(from_address_affected).value} plants of that category\
    \nand a total stock of {plants.acell(to_address_affected).value} of year-{affected_year - 1} plants of that cultivar.")

    print("Plants held back successfully.")

    print("Press )any key to continue ...")
    input()
    Startup_instructions()


def Bring_forward():
    """
    Option 10:
    The same as Option 9, but in the opposite direction.
    Results in the given number of cultivars from year n being removed
    and then added to year n+1.
    """

    # First define the cultivar affected
    row_values = plants.row_values(1)
    # Find the column to stop at (first column that contains no data).
    first_empty_index = next((i for i,
                              val in enumerate(row_values) if not val),
                             len(row_values))
    last_column = chr(ord('a') + first_empty_index)

    name_range = f"a1:{last_column}1"  # Names of cultivars
    cultivars = plants.get(name_range)[0]

    # List out the cultivars in the data in an ordered list.
    print(f"For which cultivar would you like bring plants forward?")
    count = 0
    for cultivar in cultivars:
        count += 1
        print(f"{count}. {cultivar}")

    cultivar_value = check_is_numeric(input("Please enter the cultivar number for which you want to bring plants forward\
    \n(see the cultivars listed above): \n"))
    while True:
        affected_year = check_is_numeric(input("Please enter the age of the plants for which you want to bring plants forward\
        \n(typing '1' for year-one plants or '2' for year-two plants, and so on): \n"))
        try:
            affected_year = int(affected_year)
            if affected_year >= 1:
                break
            else:
                print(f"Please enter an integer between 1 and the \
                age of the nursery.")
        except ValueError:
            print(f"Your number must be an integer and must be at least 1, and less than the age of\
            \nthe nursery. Negative and decimal-point numbers, text and special characters, etc.\
            \nare not allowed: ")

    from_address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year + 1}"
    to_address_affected = f"{chr(ord('a') + cultivar_value - 1)}{affected_year + 2}"

    current_number_from = int(plants.acell(from_address_affected).value)
    current_number_to = int(plants.acell(to_address_affected).value)
    print(f"You have chosen to bring forward {cultivars[cultivar_value - 1]} plants of age year-{affected_year}.\
    \nThere are currently {current_number_from} plants of that category recorded in the system.\
    \nThere are now {current_number_to} plants of that cultivar listed as being a year older.\
    \nThe specified number of plants will be brought forward by a year.")
    while True:
        number_brought_forward = input("How many plants of that category do you want to bring forward for a year? \n")
        try:
            number_brought_forward = int(number_brought_forward)
            if 0 <= number_brought_forward <= current_number_from:
                break
            else:
                print(f"You can't bring forward more plants of this category than you actually have in\
                the nursery!\
                \nPlease enter an integer between 0 and \
                {current_number_from}: ")
        except ValueError:
            print(f"Your number must be a positive integer or 0. Negative and decimal-point numbers,\
            \ntext and special characters, etc. are not allowed: ")

    current_number_from -= number_brought_forward
    current_number_to += number_brought_forward
    plants.update_acell(from_address_affected, current_number_from)
    plants.update_acell(to_address_affected, current_number_to)
    print(f"Successfully recorded bringing forward {number_brought_forward} {cultivars[cultivar_value - 1]} plants of year-{affected_year}.\
    \nYou now have a remaining stock of {plants.acell(from_address_affected).value} plants of that category\
    \nand a total stock of {plants.acell(to_address_affected).value} of year-{affected_year + 1} plants of that cultivar.")

    print("Plants brought forward successfully.")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Add_new_cultivar():
    """
    Option 11:
    Adds new cultivar to the list of Hamamelis plants grown in the nursery.
    """
    print("This functionality has not yet been implemented.\
    \nPlease watch this space!")

    print("Press Enter to continue ...")
    input()
    Startup_instructions()


def Execute_option(operation):
    """
    Executes the option chosen by the user
    """

    print("_____________________________________________________________________________")
    print(" ")
    if operation == 0:
        print("You've chosen HELP.")
        help()
    elif operation == 1:
        print("You've chosen to close out the current year and open a new one.")
        Create_year()
    elif operation == 2:
        print("You've chosen to plan this year's cutting campaign.")
        Plan_cutting_campaign()
    elif operation == 3:
        print("You've chosen to record having taken some cuttings.")
        Record_cuttings_taken()
    elif operation == 4:
        print("You've chosen to record potting up some rooted cuttings.")
        Record_potted_cuttings()
    elif operation == 5:
        print("You've chosen to plan your grafting campaign.")
        Plan_grafting_campaign()
    elif operation == 6:
        print("You've chosen to record a number of new grafts.")
        Record_grafts()
    elif operation == 7:
        print("You've chosen to record the loss of a number of plants.")
        Record_loss()
    elif operation == 8:
        print("You've chosen to record the acquisition of a number of plants.")
        Record_gain()
    elif operation == 9:
        print("You've chosen to hold a number of grafted plants back a year.")
        Hold_back()
    elif operation == 10:
        print("You've chosen to bring a number of grafted plants forward a year.")
        Bring_forward()
    elif operation == 11:
        print("Sorry! This functionality has not yet been implemented.")
        Add_new_cultivar()
    else:
        print("Please enter a valid integer between 0 and 11")

def detailed_help(input):
    """
    Gives detailed information on the function indicated by the user
    """

    if input == "help 0":
        print("Typing "help" from the main menu takes you into the general Help function, which\
        \ngives you summary details on each of the eleven functions of the App.")
        input("Would you like to go to the general Help function now?")
    if input == "help 0":
        print(help_messages.help_text_option0)
    elif input == "help 1":
        print(help_messages.help_text_option1)
    elif input == "help 2":
        print(help_messages.help_text_option2)
    elif input == "help 3":
        print(help_messages.help_text_option3)
    elif operation == "help 4":
        print(help_messages.help_text_option4)
    elif operation == "help 5":
        print(help_messages.help_text_option5)
    elif operation == "help 6":
        print(help_messages.help_text_option6)
    elif operation == "help 7":
        print(help_messages.help_text_option7)
    elif operation == "help 8":
        print(help_messages.help_text_option8)
        Hold_back()
    elif operation == 9:
        print(help_messages.help_text_option9)
        Bring_forward()
    elif operation == 11:
        print(help_messages.help_text_option10)
        Add_new_cultivar()
    else:
        print("Please enter a valid integer between 0 and 11")

Startup_instructions()
