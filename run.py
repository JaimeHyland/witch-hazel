"""
This file is the main module for the witch-hazel App.
"""

import sys
import re
import warnings
import string
import gspread
from google.oauth2.service_account import Credentials
import help_texts
import input_texts
import msgs
import config
import error_msgs
import commands
import new_year_controller


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hamamelis')

LOWER_BOUND = 0
UPPER_BOUND = 9

rootstock = SHEET.worksheet('rootstock')
grafts_year_zero = SHEET.worksheet('grafts-year-zero')
plants = SHEET.worksheet('plants')
completed = SHEET.worksheet('completed')


def first_empty_cell_in_row(sheet, start_row, start_col):
    """
    Counts a row of cells from start_col and column til it finds the first empty cell
    """
    start_col = string.ascii_uppercase.index(start_col.upper()) + 1
    row_values = sheet.row_values(start_row, value_render_option='UNFORMATTED_VALUE')

    return len(row_values)


def first_empty_cell_in_column(sheet, start_col): # enter column as a letter
    """
    Function to find the first empty cell in a column starting from a specific row
    """
    start_col_index = string.ascii_uppercase.index(start_col.upper()) + 1
    col_values = sheet.col_values(start_col_index, value_render_option='UNFORMATTED_VALUE')
    return len(col_values)


# Find the column to stop at (first column on the plants page that contains no data).
first_empty_column = first_empty_cell_in_column(plants, 'B')
if first_empty_column:
    last_column = first_empty_column - 1

# Find the row to stop at (first row on the plants page that contains no data).
first_empty_row = first_empty_cell_in_row(plants, 1, 'A')
if first_empty_row:
    last_row =  first_empty_row - 1

name_range = f"b1:{last_column}1"  # Names of cultivars
cultivars = plants.get(name_range)[0]

CUTTINGS_TAKEN = int(rootstock.acell('c2').value)
MATURE_ROOTSTOCKS = int(rootstock.acell('e2').value)

rootstock_data = rootstock.get_all_values()
grafts_data = grafts_year_zero.get_all_values()
plants_data = plants.get_all_values()
completed_data = completed.get_all_values()


def list_cultivars(cultivar_list):
    """
    Lists out cultivars
    """
    count = 0
    for cultivar in cultivar_list:
        count += 1
        print(f"{config.INDENT}{config.INDENT}{count}. {cultivar}")
    print()
    return count


def exit_program(num):
    """
    Closes the App in an orderly manner.
    """
    print(f"{config.INDENT}{config.EXIT_MSG}")
    sys.exit(int(num))


def completed_for_year(affected_cell, affected_task):
    """
    This function closes out each individual task for the year.
    When all tasks are closed out, you can create a new year (Option 0)
    """
    user_input = parse_yn_input(input(input_texts.completed_for_year(affected_task)))
    if user_input == commands.YES:
        completed.update_acell(affected_cell, 'y')
        print(msgs.task_completed(affected_task))
    else:
        completed.update_acell(affected_cell, 'n')
        print(msgs.task_not_completed(affected_task))


def parse_num_input(user_input, mini=0, maxi=10000,
    not_a_number_blurb=error_msgs.DEFAULT_NOT_A_NUMBER_BLURB,
    not_in_range_blurb=error_msgs.DEFAULT_NOT_IN_RANGE_BLURB):
    """
    This recursive function does one of the following things:
    - It returns a number if the user input is convertible into a non-negative integer.
    - It returns nothing and exits the program if the user input parses to "exit".
    - It returns 'help' if the user input parses to 'help'.
    - It returns 'help [n]' if the user input parses to 'help [n]' (where [n] is an integer
      between 0 and the number of options available for the relevant function)
    - If the user input is anything else, it calls itself, asking the user to enter number 
      within the allowable range or some other valid input.
    The arguments it takes are fairly self-explanatory.
    """
    exiting = 'n'

    # Is the input a number?
    user_input = user_input.strip().lower()
    if user_input.isnumeric():
        number = int(user_input)
        # Is it in range?
        if mini <= number <= maxi:
            return_value = number
        else:
            return_value = parse_num_input(input(error_msgs.a_and_b(f"{config.INDENT}\
{not_in_range_blurb}{mini}", maxi)),mini, maxi)

    else:
        user_input = user_input.strip().lower()
        # Is it another valid input?
        if user_input=="":
            return_value = parse_num_input(input(error_msgs.a_and_b(\
f"{config.INDENT}'{user_input}'{not_a_number_blurb}{mini}", maxi)),  mini, maxi)
        elif user_input==commands.EXIT:
            exiting = 'y'
            return_value = None
        elif user_input==commands.HELP:
            return_value = 'help'
        elif user_input.split()[0]==commands.HELP:
            # Does it start with "help "?
            return_value = detailed_help_routine(user_input, mini, maxi)
        else:
            return_value = parse_num_input(input(error_msgs.a_and_b(\
f"{config.INDENT}'{user_input}'{not_a_number_blurb}{mini}", maxi)), mini, maxi)
            # If it's none of the legitimate options ... start again!

    if exiting=='y':
        exit_program(0)
    else:
        return return_value
    return None

def detailed_help_routine(input_string, mini, maxi):
    """
    This routine parses inputs beginning with "help "
    """
    try:
        help_option = int(input_string.split()[1])
        # Is the second bit an integer in range?
        if mini <= help_option <= maxi:
            return_value = input_string
        else:
            return_value = parse_num_input(input(error_msgs.detailed_help_not_int\
(input_string, mini, maxi)),mini, maxi)
            # If the second bit's a number out of range ...
    except:
        return_value = parse_num_input(input(error_msgs.detailed_help_not_int\
(input_string, mini, maxi)), mini, maxi)
        # If the second bit's not a number ...
    return return_value

def parse_yn_input(user_input, not_a_yn_answer_blurb=error_msgs.DEFAULT_NOT_A_YN_ANS_BLURB,\
        mini=LOWER_BOUND, maxi=UPPER_BOUND):
    """
    This recursive function similar to the above, but for when yes/no (or help or exit) are
    the only valid answers.
    It doesn't require a try structure, meaning that sys.exit(0) can be called directly from
    within it.
    """
    answer = user_input.strip().lower()
    if answer in ('y', 'n'):
        return_value = answer
    elif answer == "":
        return_value = parse_yn_input(input(f"{config.INDENT}'{answer}'\
{not_a_yn_answer_blurb}"))
    elif user_input.lower()==commands.EXIT:
        exit_program(0)
    elif user_input.lower()==commands.HELP:
        general_help()
    elif user_input.lower().split()[0]==commands.HELP:
        if mini <= int(user_input.lower().split()[1]) <= maxi:
            print(f"{config.INDENT}{msgs.detailed_help_choice(user_input.split()[1])}")
            return_value = answer
    else:
        return_value = parse_yn_input(input(f"{config.INDENT}'{answer}'\
{not_a_yn_answer_blurb}"))

    return return_value


def startup_instructions():
    """
    Welcomes the user to the app.
    Presents general info on it purpose and functions.
    """

    print(help_texts.intro_text)
    input(f"{config.BACK_TO_MENU}")
    print(config.CURSOR_UP_ONE + config.ERASE_LINE)
    main_menu(LOWER_BOUND, UPPER_BOUND)


def main_menu(lower, upper):
    """
    The program's main menu on startup and after every option or help message.
    """
    controller = new_year_controller.NewYearController(completed.acell('j4').value)
    print(help_texts.MENU_TITLE)
    print(help_texts.menu_text(controller.get_color()))
    user_input = parse_num_input(input(msgs.main_menu_prompt(lower, upper)), lower, upper)
    execute_option(user_input)


def general_help():
    """
    General help messages on how to use the app print to screen one after another.
    """
    controller = new_year_controller.NewYearController(completed.acell('j4').value)
    print(help_texts.help_text1(controller.get_color()))
    input(f"{config.MORE_GEN_HELP}")
    print(help_texts.help_text2)
    input(f"{config.MORE_GEN_HELP}")
    print(help_texts.help_text3)
    input(f"{config.BACK_TO_MENU}")
    main_menu(LOWER_BOUND, UPPER_BOUND)


def option_help(option_no):
    """
    Specific help messages for each option
    """
    if option_no==0:
        print(help_texts.help_text_option0)

    elif option_no == 1:
        print(help_texts.help_text_option1)

    elif option_no == 2:
        print(help_texts.help_text_option2)

    elif option_no == 3:
        print(help_texts.help_text_option3)

    elif option_no == 4:
        print(help_texts.help_text_option4)

    elif option_no == 5:
        print(help_texts.help_text_option5)

    elif option_no == 6:
        print(help_texts.help_text_option6)

    elif option_no == 7:
        print(help_texts.help_text_option7)

    elif option_no == 8:
        print(help_texts.help_text_option8)

    elif option_no == 9:
        print(help_texts.help_text_option9)

    else:
        print(msgs.SPECIFIC_HELP_PROMPT)

    print(config.BACK_TO_MENU)
    input()


def execute_option(user_input):
    """
    Executes the option typed in by the user
    It assumes error handling has been done in the input parser.
    If it's called from an input not run through an error-handling
    parser, then an error handler will need to be added.
    """
    rootstocks = int(rootstock.acell('D4').value)
    rootstocks_plannable = int(rootstock.acell('H4').value)

    print(config.LINE_OF_UNDERSCORES)
    if user_input == 1:
        print(f"{config.INDENT}{msgs.PLAN_GRAFTS}")
        plan_grafting_campaign(rootstocks, rootstocks_plannable)
    elif user_input == 2:
        print(f"{config.INDENT}{msgs.TAKE_GRAFTS}")
        record_grafts(rootstocks_plannable)
    elif user_input == 3:
        print(f"{config.INDENT}{msgs.POT_UP_CUTTINGS}")
        record_potted_cuttings()
    elif user_input == 4:
        print(f"{config.INDENT}{msgs.PLAN_CUTTINGS}")
        plan_cutting_campaign()
    elif user_input == 5:
        print(f"{config.INDENT}{msgs.TAKE_CUTTINGS}")
        record_cuttings_taken()
    elif user_input == 6:
        print(f"{config.INDENT}{msgs.RECORD_LOSS}")
        record_loss()
    elif user_input == 7:
        print(f"{config.INDENT}{msgs.RECORD_ACQ}")
        record_gain()
    elif user_input == 8:
        print(f"{config.INDENT}{msgs.HOLD_BACK}")
        hold_back()
    elif user_input == 9:
        print(f"{config.INDENT}{msgs.BRING_FORWARD}")
        bring_forward()
    elif user_input == 0:
        print(f"{config.INDENT}{msgs.NEW_YEAR}")
        # The user doesn't need to see the warnings produced by create_year()!
        # See readme file for details.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            create_year()
    elif user_input == 'help':
        general_help()
    # If the parser handles errors correctly,
    # then the only remaining option is an
    # an input of the form "help [n]"!
    else:
        option_help(int(user_input.split()[1]))

    main_menu(LOWER_BOUND, UPPER_BOUND)


def complete_cuttings_taken_record(taken, planned, task):
    """
    Cuttings taken (for the first time ... or ... again).
    """
    if taken >= planned:
        print(msgs.planned_cuttings_taken(taken, planned))

    if taken > 0:
        info_msg = msgs.cuttings_taken(taken, planned)
        input_string = input_texts.TAKE_MORE_CUTTINGS
        in_addition = input_texts.cuttings_in_addition(taken)
    else:
        info_msg = msgs.no_cuttings_yet_taken(planned)
        input_string = input_texts.TAKE_CUTTINGS_NOW
        in_addition = ""

    print(info_msg)

    if parse_yn_input(input(input_string)) == commands.YES:
        taken += parse_num_input(input(input_texts.record_how_many_cuttings(in_addition)))
        rootstock.update_acell('c2', taken)
        if taken >= planned:
            print(msgs.planned_cuttings_reached(planned, taken))
        else:
            print(msgs.planned_cuttings_not_reached(planned, taken))

        print(msgs.CUTTINGS_SUCCESSFUL)
        print(msgs.a_out_of_b(taken, planned))
        run_cuttings_session(taken, task)
    else:
        print(msgs.CUTTINGS_CANCELLED)

    print(config.BACK_TO_MENU)
    input()
    main_menu(LOWER_BOUND, UPPER_BOUND)

def check_is_complete(cell, task):
    """
    Checks if a particular task is complete for the year. 
    And asks users if they want to reopen it if so.
    """
    complete = completed.acell(cell).value.lower()
    if complete == 'y':
        if parse_yn_input(input(input_texts.task_closed_reopen(task))) == commands.YES:
            print(msgs.REOPENING)
            completed.update_acell(cell, 'n')
            return False
        else:
            print(msgs.do_not_reopen(task))
            return True
    else:
        return False

def plan_grafting_campaign(rootstocks, rootstocks_plannable):
    """
    Option 1:
    Lets user add a planned number of grafts for each cultivar.
    Should be used in late winter (February or March).
    Shows the number of rootstocks ready for grafting and the number left.
    Stops the user when they're planning to use more rootstocks than they have.
    """

    planned_numbers = grafts_year_zero.get(f"c2:{last_column}2")[0]
    planned_numbers = [int(x) for x in planned_numbers]

    print(msgs.WHICH_CULTIVAR_P)

    # List out the cultivars you have in your data in an ordered list.
    count = list_cultivars(cultivars)

    cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_P), 1, count)
    current_cultivar = cultivars[cultivar_value-1]
    address_current_cultivar  = f"{chr(ord('C') + cultivar_value - 1)}2"
    task_check_complete_address = f"{chr(ord('D') + cultivar_value - 1)}2"
    task = msgs.plan_for(current_cultivar)
    rootstocks_available = rootstocks_plannable + planned_numbers[cultivar_value - 1]

    if check_is_complete(task_check_complete_address, task) is False:

        print(msgs.planned_for(current_cultivar))
        print(msgs.rootstocks_unplanned(rootstocks, rootstocks_plannable \
        + planned_numbers[cultivar_value - 1]))

        if planned_numbers[cultivar_value - 1] > 0:
            info_msg = input_texts.replace_graft_value(planned_numbers[cultivar_value - 1])
        else:
            info_msg = input_texts.NO_GRAFTS_YET_PLANNED

        user_input = parse_yn_input(input(info_msg))
        if user_input == commands.YES:
            new_planned_value = parse_num_input(input(input_texts.new_planned_value\
            (current_cultivar)))
            if new_planned_value > rootstocks_available:
                print(error_msgs.too_many_grafts_planned(new_planned_value, rootstocks_available))
                new_planned_value = parse_num_input(input(error_msgs.valid_option_number\
(0, rootstocks_available)))

            grafts_year_zero.update_acell(address_current_cultivar, new_planned_value)
            print(msgs.planned_grafts_changed(current_cultivar, new_planned_value))
            completed_for_year(f"{chr(ord('d') + cultivar_value - 1)}2", task)
        else:
            print(msgs.task_cancelled(task, current_cultivar))
            completed_for_year(task_check_complete_address, task)

    print(config.BACK_TO_MENU)
    input()


def record_grafts(rootstocks_plannable):
    """
    Option 2:
    Lets user record the number of grafts taken for a chosen cultivar.
    Should be used in late winter; at grafting time.
    Shows the total for rootstocks ready for grafting and the number left.
    Warns the user when they've used more rootstocks than they actually have.
    """

    planned_numbers = grafts_year_zero.get(f"c2:{last_column}2")[0]

    # Converts the strings in the planned numbers list into integers
    # to make it possible to sum them together.
    planned_numbers = [int(x) for x in planned_numbers]
    grafts_this_year = grafts_year_zero.get(f"c3:{last_column}3")[0]
    grafts_this_year = [int(x) for x in grafts_this_year]

    print(msgs.WHICH_CULTIVAR_M)

    # List out the names of the cultivars you have in your data
    # in an ordered list.
    count = list_cultivars(cultivars)

    cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_M), 1, count)
    task_check_complete_address = f"{chr(ord('d') + cultivar_value - 1)}3"
    current_cultivar = cultivars[cultivar_value - 1]
    address_current_cultivar = f"{chr(ord('c') + cultivar_value - 1)}3"
    task = msgs.make_grafts(current_cultivar)

    if check_is_complete(task_check_complete_address, task) is False:
        grafts_this_cultivar = grafts_this_year[cultivar_value - 1]
        planned_this_cultivar = planned_numbers[cultivar_value -1]

        print(msgs.cultivar_chosen(current_cultivar))
        print(msgs.cultivar_grafts_planned(planned_this_cultivar))
        if grafts_this_cultivar > 0:
            confirm_string = input_texts.grafts_made(grafts_this_cultivar, rootstocks_plannable)
        else:
            confirm_string = input_texts.NO_GRAFTS_YET_MADE
        if parse_yn_input(input(confirm_string)) == commands.YES:
            newly_made_grafts = parse_num_input(input\
                (input_texts.grafts_now_made(current_cultivar)))
            if newly_made_grafts > rootstocks_plannable:
                print(error_msgs.too_many_grafts_made(newly_made_grafts, rootstocks_plannable))
                newly_made_grafts = parse_num_input(input\
                    (input_texts.grafts_now_made(current_cultivar)))

            grafts_this_cultivar += newly_made_grafts
            grafts_year_zero.update_acell(address_current_cultivar,\
                int(grafts_this_cultivar))
            print(msgs.grafts_successfully_made(current_cultivar, grafts_this_cultivar,\
                planned_this_cultivar))
            completed_for_year(task_check_complete_address, task)
        else:
            print(msgs.grafts_cancelled(current_cultivar))
            completed_for_year(task_check_complete_address, task)

    print(config.BACK_TO_MENU)
    input()


def record_potted_cuttings():
    """
    Option 3:
    Lets user record progress in potting up the successfully rooted cuttings
    (taken the previous Autumn).
    Ideally used daily during the potting campaign (in the Spring).
    """
    cuttings_taken = int(rootstock.acell('c3').value)
    cuttings_potted = int(rootstock.acell('d3').value)
    new_rootstocks = int(rootstock.acell('f3').value)
    task = msgs.POT_ROOTED

    if check_is_complete('c3', task) is False:
        if cuttings_potted > 0:
            confirm_string = input_texts.add_potted(cuttings_potted)
            qualifier_clause = msgs.IN_ADDITION
        else:
            confirm_string = input_texts.RECORD_POTTED
            qualifier_clause = ""
        if parse_yn_input(input(confirm_string)) == commands.YES:
            newly_potted = parse_num_input(input(input_texts.how_many_potted(qualifier_clause)))
            if cuttings_potted + newly_potted > cuttings_taken:
                print(msgs.more_potted_than_taken(newly_potted, new_rootstocks, cuttings_taken))
            else:
                cuttings_potted += newly_potted
                rootstock.update_acell('d3', cuttings_potted)
                print(msgs.potted_up(cuttings_potted, cuttings_taken))
                completed_for_year('c3', task)
        else:
            print(msgs.POTTING_CANCELLED)
            completed_for_year('c3', task)

    print(config.BACK_TO_MENU)
    input()


def run_cuttings_plan(cuttings, task):
    """
    Tells the user the planned no of cutting has changed and
    asks if the user has finished that task for the year.
    """
    rootstock.update_acell('b2', cuttings)
    print(msgs.PLANNED_CUTTINGS_CHANGED)
    completed_for_year('b2', task)


def  cancel_cuttings_plan():
    """
    Just tells the user that the cutting planning task is has been cancelled.
    """
    print(msgs.PLAN_CUTTINGS_CANCELLED)


def run_cuttings_session(cuttings, task):
    """
    Tells the user the no of cuttings taken has changed and
    asks if the user has finished that task for the year.
    """
    rootstock.update_acell('c2', cuttings)
    print(msgs.ADDED_CUTTINGS)
    completed_for_year('b3', task)


def plan_cutting_campaign():
    """
    Option 4:
    Helps plan cuttings task
    """
    planned_cuttings = int(rootstock.acell('b2').value)
    last_year_cuttings = int(rootstock.acell('c3').value)
    last_year_rooted_cuttings = int(rootstock.acell('d3').value)
    this_year_cuttings_taken = int(rootstock.acell('c2').value)
    current_year = int(rootstock.acell('a2').value)
    task = msgs.PLAN_CUTTINGS
    if check_is_complete('b2', task) is False:
        if int(planned_cuttings) > 0:
            user_confirmation = parse_yn_input(input(input_texts.replace_value\
                (planned_cuttings, current_year)))
            planned_cuttings_string = msgs.planned_cuttings(planned_cuttings)
            text_segment = msgs.NEW
        else:
            user_confirmation =parse_yn_input(input(input_texts.PLAN_CUTTINGS))
            planned_cuttings_string = ""
            text_segment = ""
        if user_confirmation == commands.YES:
            planned_cuttings = parse_num_input(input(input_texts.enter_planned_cuttings(\
                last_year_cuttings, last_year_rooted_cuttings, planned_cuttings_string,\
                text_segment)))
            if planned_cuttings <= this_year_cuttings_taken:
                user_confirmation =parse_yn_input(input(input_texts.replace_value_confirm(\
                    this_year_cuttings_taken)))
                if user_confirmation == commands.YES:
                    run_cuttings_plan(planned_cuttings, task)
                else:
                    cancel_cuttings_plan()
            else:
                run_cuttings_plan(planned_cuttings, task)
        else:
            cancel_cuttings_plan()
            completed_for_year('B2', task)

    print(config.BACK_TO_MENU)
    input()


def record_cuttings_taken():
    """
    Option 5:
    Lets the user record cuttings actually taken.
    Ideally used daily during the cuttings campaign (in Autumn).
    """
    task = msgs.TAKING_CUTTINGS

    if check_is_complete('b3', task) is False:
        cuttings_taken = int(rootstock.acell('c2').value)
        cuttings_planned = int(rootstock.acell('b2').value)
        complete_cuttings_taken_record(cuttings_taken, cuttings_planned, task)

    completed_for_year('B2', task)

    print(config.BACK_TO_MENU)
    input()


def record_loss():
    """
    Option 6:
    Lets user record losses in stocks for any cultivar in any year.
    Works for both rooted cuttings and grafted cultivars.
    May be used throughout the year.
    Losses of cuttings are not recorded until the time comes to pot
    up those of them that have rooted successfully.
    """
    # Did we lose new_rootstocks?
    if parse_yn_input(input(input_texts.LOSS_OF_ROOTSTOCKS)) == commands.YES:
        total_rootstocks = int(rootstock.acell('G3').value)
        remaining_rootstocks = int(rootstock.acell('G3').value)

        total_losses = int(rootstock.acell('E3').value)
        print(msgs.total_rootstocks(remaining_rootstocks))
        number_lost = parse_num_input(input(input_texts.HOW_MANY_ROOTSTOCKS_LOST),\
        0, total_rootstocks)
        rootstock.update_acell('E3', total_losses + number_lost)
        print(msgs.rootstock_loss_recorded(number_lost, remaining_rootstocks))
    else:
        # List the names of the cultivars in the data in an ordered list.
        print(msgs.LOST_WHICH_CULTIVAR)
        count = list_cultivars(cultivars)

        cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_LOST), 1, count)
        affected_year = parse_num_input(input(input_texts.CHOOSE_YEAR_LOST), 1, last_column)
        current_cultivar = cultivars[cultivar_value - 1]
        address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year + 1}"

        current_number = int(plants.acell(address_affected).value)
        print(msgs.loss_chosen(current_cultivar, affected_year, current_number))
        while True:
            number_lost = input(input_texts.HOW_MANY_PLANTS_LOST)
            try:
                number_lost = int(number_lost)
                if 0 <= number_lost <= current_number:
                    break
                print(error_msgs.too_many_plants_lost(current_number))
            except ValueError:
                print(error_msgs.POSITIVE_INT)

        current_number -= number_lost
        plants.update_acell(address_affected, current_number)
        print(msgs.plants_lost_recorded(number_lost, current_cultivar, affected_year,\
            plants.acell(address_affected).value))

        # number_lost
    print(msgs.LOSS_RECORDED)

    print(config.BACK_TO_MENU)
    input()


def record_gain():
    """
    Option 7:
    Essentially the opposite of Option 6.
    """
    # Did we acquire new_rootstocks ...?
    if parse_yn_input(input(input_texts.GAIN_OF_ROOTSTOCKS)) == commands.YES:

        remaining_rootstocks = int(rootstock.acell('G3').value)
        total_gains = int(rootstock.acell('F3').value)
        print(msgs.total_rootstocks(remaining_rootstocks))
        number_gained = parse_num_input(input(input_texts.HOW_MANY_GAINED), 0)
        rootstock.update_acell('F3', total_gains + number_gained)
        print(msgs.rootstock_gain_recorded(number_gained, rootstock.acell('G3').value))
    else:
        # List the cultivars in the data in an ordered list.
        print(msgs.GAINED_WHICH_CULTIVAR)
        count = list_cultivars(cultivars)

        cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_GAINED), 1, count)
        affected_year = parse_num_input(input(input_texts.CHOOSE_YEAR_GAINED), 1, last_column)
        address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year + 1}"
        current_cultivar = cultivars[cultivar_value - 1]
        current_number = int(plants.acell(address_affected).value)
        print(msgs.gain_chosen(current_cultivar, affected_year, current_number))
        while True:
            number_gained = input(input_texts.HOW_MANY_GAINED)
            try:
                number_gained = int(number_gained)
                break
            except ValueError:
                print(error_msgs.POSITIVE_INT)
        current_number += number_gained
        plants.update_acell(address_affected, current_number)
        print(msgs.plants_gain_recorded(number_gained, current_cultivar,affected_year,\
            plants.acell(address_affected).value))

        # number_lost
    print(msgs.GAIN_RECORDED)
    print(config.BACK_TO_MENU)
    input()


def hold_back():
    """
    Option 8:
    Essentially a Option 6 with a twist.
    Results in the given number of the chosen cultivar from year n
    being removed and then added to year n-1.
    """

    # List out the cultivars in the data in an ordered list.
    print(msgs.HOLD_WHICH_CULTIVAR)
    count = list_cultivars(cultivars)

    cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_HOLD), 1, count)
    while True:
        affected_year = parse_num_input(input(input_texts.CHOOSE_YEAR_HOLD), 1)
        try:
            affected_year = int(affected_year)
            if affected_year > 1:
                break
            if affected_year == 1:
                print(msgs.NO_HOLD_YEAR_ONE)
            else:
                print(msgs.ENTER_HOLD_YEAR)
        except ValueError:
            print(error_msgs.POSITIVE_INT)

    current_cultivar = cultivars[cultivar_value - 1]
    from_address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year + 1}"
    to_address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year}"

    current_number_from = int(plants.acell(from_address_affected).value)
    current_number_to = int(plants.acell(to_address_affected).value)
    print(msgs.hold_chosen(current_cultivar, affected_year, current_number_from, current_number_to))
    while True:
        number_held_back = input(input_texts.HOW_MANY_HELD)
        try:
            number_held_back = int(number_held_back)
            if 0 <= number_held_back <= current_number_from:
                break
            print(error_msgs.too_many_plants_held(current_number_from))
        except ValueError:
            print(error_msgs.POSITIVE_INT)

    current_number_from -= number_held_back
    current_number_to += number_held_back
    plants.update_acell(from_address_affected, current_number_from)
    plants.update_acell(to_address_affected, current_number_to)
    print(msgs.successfully_held(number_held_back, current_cultivar, affected_year,\
        plants.acell(from_address_affected).value, plants.acell(to_address_affected).value))

    print(msgs.HOLD_RECORDED)

    print(config.BACK_TO_MENU)
    input()


def bring_forward():
    """
    Option 9:
    The same as Option 9, but in the opposite direction.
    Results in the given number of cultivars from year n being removed
    and then added to year n+1.
    """

    # List out the cultivars in the data in an ordered list.
    print(msgs.BRING_WHICH_CULTIVAR)
    count = list_cultivars(cultivars)

    cultivar_value = parse_num_input(input(input_texts.CHOOSE_CULTIVAR_BRING), 1, count)

    while True:
        affected_year = parse_num_input(input(input_texts.CHOOSE_YEAR_BRING), 1, last_row - 1)
        try:
            affected_year = int(affected_year)
            if affected_year >= 1:
                break
            print(msgs.ENTER_BRING_YEAR)
        except ValueError:
            print(error_msgs.POSITIVE_INT)


    from_address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year + 1}"
    to_address_affected = f"{chr(ord('b') + cultivar_value - 1)}{affected_year + 2}"

    current_cultivar = cultivars[cultivar_value - 1]
    current_number_from = int(plants.acell(from_address_affected).value)
    current_number_to = int(plants.acell(to_address_affected).value)
    print(msgs.bring_chosen(current_cultivar, affected_year, current_number_from,
        current_number_to))
    while True:
        number_brought_forward = input(input_texts.HOW_MANY_BROUGHT)
        try:
            number_brought_forward = int(number_brought_forward)
            if 0 <= number_brought_forward <= current_number_from:
                break
            print(error_msgs.too_many_plants_brought(current_number_from))
        except ValueError:
            print(error_msgs.POSITIVE_INT)

    current_number_from -= number_brought_forward
    current_number_to += number_brought_forward
    plants.update_acell(from_address_affected, current_number_from)
    plants.update_acell(to_address_affected, current_number_to)
    print(msgs.successfully_brought(number_brought_forward, current_cultivar, affected_year,
        plants.acell(from_address_affected).value, plants.acell(to_address_affected).value))

    print(msgs.BRING_RECORDED)

    print(config.BACK_TO_MENU)
    input()


def create_year():

    """
    Option 0:
    This function adds the rows necessary to create a new year and copies the
    row for stocks of this year's grafts from the grafts-year-zero to the
    plants worksheet. It puts the figures for the current year out of reach 
    of the relevant seasonal planning and work tasks. They can no longer be
    modified by the seasonal tasks. Year-one plants become Year-Two plants
    and so on down the line.
    It resets all seasonal tasks to "not completed" ('n').
    """

    controller = new_year_controller.NewYearController(completed.acell('j4').value)
    if controller.year_finished is True:
        rootstock_year = rootstock.acell('a2').value
        new_rootstock_year = int(rootstock_year) + 1

        print(msgs.last_year(rootstock_year))

        # Asks user to confirm
        if parse_yn_input(input(input_texts.create_new_year(new_rootstock_year))) == commands.YES:
            # Gives info on cutting numbers for last year to user and collects planned cutting
            # numbers from user for coming year
            print(msgs.rootstocks_in_stock(CUTTINGS_TAKEN, MATURE_ROOTSTOCKS))
            num_cuttings = parse_num_input(input(input_texts.how_many_cuttings(new_rootstock_year)))
            """
            Add columns for new current year in grafts-year-zero sheet.
            This has to be done first because otherwise the addition of new columns
            will move the named range to the incorrect "used or reserved" mature rootstocks
            address ("'grafts-year-zero'!$I$4").
            """
            graft_starting_values = [
                 [new_rootstock_year, 'planned', 0, 0, 0, 0, 0, 0, '=SUM(C2:H2)'],
                 [new_rootstock_year, 'grafted', 0, 0, 0, 0, 0, 0, '=SUM(C3:H3)'],
                 [new_rootstock_year, 'used or reserved','=IF(completed!D3="n", MAX(C2:C3),C3)',\
                 '=IF(completed!E3="n", MAX(D2:D3),D3)', '=IF(completed!F3="n", MAX(E2:E3),E3)',\
                 '=IF(completed!G3="n", MAX(F2:F3),F3)', '=if(G2>G3, G2, G3)',\
                 '=IF(completed!I3="n", MAX(H2:H3),H3)', '=SUM(C4:H4)'],
                 [new_rootstock_year, 'lost', 0, 0, 0, 0, 0, 0, '=SUM(C5:H5)'],
                 ]

            total_previous_years = ['total for year', '=C7-C9','=D7-D9','=E7-E9',\
            '=F7-G9','=G7-G9','=H7-H9']

            grafts_year_zero.insert_rows(graft_starting_values, 2,
                value_input_option='USER_ENTERED')

            grafts_year_zero.update("B8:H8", [total_previous_years],\
                value_input_option='USER_ENTERED')

            # new top row for rootstock table
            init_roots_values = [new_rootstock_year, num_cuttings, 0, 0, 0, 0, '=D2-E2+F2', 0]
            rootstock.insert_row(init_roots_values, 2, value_input_option='USER_ENTERED')
            # new totals column for rootstock table
            column_formulae = [["=G3"],["=g4-'grafts-year-zero'!$I$4"],[0]]
            cell_range = "H3:H5"
            rootstock.update(cell_range, column_formulae, value_input_option='USER_ENTERED')

            print(msgs.year_created(new_rootstock_year, num_cuttings))
            if num_cuttings == 0:
                print(f"{config.INDENT}{msgs.CUTTINGS_LATER}")

            # replace 'completed' values
            cell_range = 'B2:I3'
            completed_starting_values = [
                 ['n', '-', 'n', 'n', 'n', 'n', 'n', 'n'],
                 ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
            ]
            completed.update(cell_range, completed_starting_values,
                value_input_option='USER_ENTERED')

            # transfer the grafts made in the old current year to the new previous year.
            year_zero_stocks = grafts_year_zero.get('c7:h7')[0]
            year_zero_stocks.insert(0, 'Year 0')
            plants.insert_row(year_zero_stocks, 2)

            # Finally, correct the texts in column A so that they show the right numbers
            for index, cell_value in enumerate(plants.col_values(1), start=1):
                if index == 1:
                    continue
                if cell_value:
                    # This changes any number in each title string to itself plus
                    # one using regular expressions
                    new_years_value = re.sub(r'\d+', lambda x: str(int(x.group(0)) + 1), cell_value)
                    plants.update_cell(index, 1, new_years_value)

        else:
            print(msgs.new_year_cancelled(new_rootstock_year, rootstock_year))

    else:
        print(error_msgs.YEAR_NOT_FINISHED)

    print(config.BACK_TO_MENU)
    input()


startup_instructions()
# Program runs from here
