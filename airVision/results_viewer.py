from dateutil import parser
import tiger_log
import os
import re
import time
import datetime
import pytz
import shutil

def terminate_main():
    print "\nExiting..."
    exit(0) 


# Delete the directory with the passed in name. 
def delete_directory(name):
    try:    
        shutil.rmtree(name)
    except Exception, e:
        print e

# Make a directory with the given name, if it doesn't
# already exist.
def make_directory(name):
    if not os.path.exists(name):
        os.makedirs(name)  


##############################################
# Sort alphanumerically
def tryint(s):
    try:
        return int(s)
    except:
        return s
    
def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)',s) ]

def sort_nicely(l):
    l.sort(key=alphanum_key)
##############################################

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

# Convert local time to UTC time
def local_to_utc(time):
    utc = pytz.timezone("UTC")
    time = time.astimezone(utc)
    return time

# convert UTC time to local time
def utc_to_local(time):
    time = add_utc_timezone(time)
    pacific = pytz.timezone("US/Pacific")
    time = time.astimezone(pacific)
    return time

# add pacific timezone to time
def add_pacific_timezone(time):
    # get user's timezone
    pacific = pytz.timezone("US/Pacific")
    # set formatted date timezone
    dt = pacific.localize(time)
    return dt  
             

# add utc timezone to time
def add_utc_timezone(time):
    # get user's timezone
    utc = pytz.timezone("UTC")
    # set formatted date timezone
    dt = utc.localize(time)
    return dt  


# Format the given input time.
# Return the formatted time string.
def format_time(time):
    return time.strftime("%Y/%m/%d/%H")


# Query tiger_log for all dates with saved positive 
# footage.  Sort them, and return that sorted list.
def sort_available_dates():
    to_sort = []
    date_times = []    
    #all_dates = tiger_log.select_dates_with_concatenated_footage()
    all_dates = tiger_log.select_dates_with_pos_footage()    
    for item in all_dates:
        time_string = "".join(item)
        to_sort.append(time_string)
    to_sort.sort()
    for item in to_sort:
        dt = parser.parse(item)
        dt = utc_to_local(dt) # convert to local time
        date_times.append(dt)
    return date_times
    

# Take a list of sorted dates, and print them out
# not printing any duplicate dates.
def print_sorted_dates(to_print):
    if len(to_print) == 0:
        print "Woops, no footage available..."        
        return       
    else:   
        # print the dates, skipping duplicates 
        current = to_print[0]
        print format_time(current)
        for item in to_print:
            if item != current:
                print format_time(item)
                current = item


# Given a directory, sort all the video files
# into temporal order.  Return the absolute paths
# to those files.
def get_and_sort(directory):
    all_files = glob.glob(directory + "/" + "*.ts")
    for i in range(0, len(all_files)):
        all_files[i] = os.path.basename(all_files[i])
    getPositives.sort_nicely(all_files)
    for i in range(0, len(all_files)):
        all_files[i] = directory + "/" + all_files[i]
    return all_files


# Given a  list of files, concatenate them
# Put output file in specified
# destination directory.
# Return the path to the outputted video.
def cat_files(all_files, dest_directory, output_name):
    to_concat = " ".join(all_files)
    output_path = dest_directory + "/" + output_name + ".mpeg"
    cmd = 'cat ' + to_concat + " > " + output_path
    ret_val = os.system(cmd)
    return output_path





# Give user option of viewing available dates.
def view_available_dates():
    to_print = yes_or_no("\nWould you like to see what dates are available for viewing?")
    if to_print:
        sorted_dates = sort_available_dates()
        print_sorted_dates(sorted_dates)
        

# Give user option of exiting.
def exit_choice():
    to_exit = yes_or_no("\nWould you like to continue? (Say 'N' if you want to exit).")
    if to_exit == False:
        terminate_main()


# Get all files from the given directory.
# Sort them alphanumerically (to put the videos
# in temporal order.
def get_and_sort(directory):
    all_files = os.listdir(directory)
    sort_nicely(all_files) # put the video clips in temporal order
    for i in range(0, len(all_files)): # make these absolute paths
        all_files[i] = directory + "/" + all_files[i]
    return all_files

  




################################################
# "Main":
################################################


print "\n\nWelcome to the results viewer for the camera system in the tiger enclosure."
print "We can retrieve all the tiger-positive footage from a given hour on a given day for you."

# give user option of viewing available dates
view_available_dates()


continue_looping = True
while continue_looping:
    # get a valid time from the user   
    parsed_time = ask_for_time()

    # make sure the time has a timezone
    dt = add_pacific_timezone(parsed_time)
    
    # convert to utc
    dt = local_to_utc(dt)

    # format the time so it matches tiger_log: YYYY/MM/DD/HH
    formatted_time = format_time(dt)


    # grab rows in the database that have the corresponding time
    #videos = tiger_log.select_dirs_with_concatenated_footage(formatted_time)
    videos = tiger_log.select_dirs_with_positive_footage(formatted_time)
    # make sure we have videos before continuing through this code
    if len(videos) == 0:
        print "Oops no videos."
        view_available_dates() # give user option of viewing available dates       
        exit_choice()  # give user option of exiting
        continue

    print "\nFetching the " + str(len(videos)) + " available angle(s) at this date."


    # start vlc windows for all videos
    tmp_dir = "results_tmp"
    make_directory(tmp_dir)
    count = 1
    for item in videos:
        print "Fetching video from angle number " + str(count) + "..."
        abs_path = "".join(item)
        temporal_order = get_and_sort(abs_path) # put clips in temporal order
        catted = cat_files(temporal_order, tmp_dir, "seg" + str(count))
        final_path = catted
        #video_file = os.listdir(abs_path)
        #final_path = abs_path + "/" + "".join(video_file)
        vlc_cmd = "vlc " + " --quiet " + final_path + " > /dev/null 2> /dev/null" + " &"
        os.system(vlc_cmd)
        count = count + 1

    continue_looping = yes_or_no("\nWould you like to look at another set of videos?  Answering this question will exit the videos you currently have up.")
    os.system("killall vlc")
    delete_directory(tmp_dir)



# Exit
terminate_main()





