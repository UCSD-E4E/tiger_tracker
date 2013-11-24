from dateutil import parser
import tiger_log


def terminate_main():
    print "\nExiting..."
    exit(0) 

# Prompt user for a yes or no response.
# Paramters: the Prompt to print with a Y/N response.
# Return: True on Y.  False on N.
def yes_or_no(message):
    while True:
        response = raw_input(message + " [Y/N]: ")
        if response == 'Y' or response == 'y':
            return True
        elif response == 'N' or response == 'n':
            return False
        else:
            print "Oops.  We need a Yes (Y) or No (N) answer."
   

# Prompt the user for a time, return
# their raw input.  
def grab_time_from_user():
    input_time = raw_input("\nEnter the date and time you'd like to view footage from: ")
    return input_time


# Is a given time parsable.
# Returns True if it is parsable.  False otherwise.
def is_parsable(input_time):
    try:    
        their_time = parser.parse(input_time)
    except:
        print "Woops, had trouble understanding your time. Let's try again." 
        return False 
    return True


# Parse a time string with the dateutil parser.
# Return that parsed time.
def parse_time(input_time):
    their_time = parser.parse(input_time)
    return their_time



# Loop until a valid time is inputted.
# Return that valid time.
def get_valid_time():
    valid_time = False
    while valid_time == False:
        input_time = grab_time_from_user()
        valid_time = is_parsable(input_time)
    return input_time


# Loop until a valid time is given and accepted.
# Return that valid time, parsed.  
def ask_for_time():
    accepted_time = False
    while accepted_time == False:
        time = get_valid_time()
        parsed_time = parse_time(time)
        accepted_time = yes_or_no("Is " + str(parsed_time) + " the time you'd like?")
    return parsed_time


# Format the given input time.
# Return the formatted time string.
def format_time(time):
    return time.strftime("%Y/%m/%d/%H")



################
# "Main":
################

print "\n\nWelcome to the results viewer for the camera system in the tiger enclosure."
print "We can retrieve all the tiger-positive footage from a given hour on a given day for you."

continue_looping = True
while continue_looping:
    # get a valid time from the user   
    parsed_time = ask_for_time()

    # format the time so it matches tiger_log: YYYY/MM/DD/HH
    formatted_time = format_time(parsed_time)



    ################
    # Select the appropriate directories from tiger_log, display videos for user, kill the
    # videos when user is done.  
    ################



    continue_looping = yes_or_no("\nWould you like to look at another set of videos?")


# Exit
terminate_main()
