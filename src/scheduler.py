# -------------------------------------------------------------
# demonstrates a task scheduler, displaying the time when the 
# the next job will run based on the scheduler configuration
# input and the 'current time'.
#
# Harold "Chip" Newman
# chip@computerchip.tech
# -------------------------------------------------------------

import sys

def run_me_daily(hour, minute, command):
    print_job(hour, minute, determine_day(hour, minute), command)

def run_me_hourly(hour, minute, command):
    # Determines whether to roll over to the next hour by comparing
    # the current minute to the scheduler configuration input minute.
    if (current_minute > minute):
        hour += 1

        # Rolls over to the next day if the increase causes
        # the hour to exceed 23 hours.
        if (hour > 23):
            hour = hour - 24

    print_job(hour, minute, determine_day(hour, minute), command)

def run_me_every_minute(hour, minute, command):
    print_job(hour, minute, determine_day(hour, minute), command)

# Number of executions will be limited by the counter.
def run_me_sixty_times(hour, minute, command):
    global counter

    # Starts at the top of the hour if current hour and 
    # scheduled configuration input hour aren't the same.
    # (current minute == minutes) returns true if the scheduled
    # configuration input minutes is "*".
    if (current_hour != hour) and (current_minute == minute):
        minute = 0

    if (counter < 60):
        print_job(hour, minute, determine_day(hour, minute), command)
        counter += 1

# Determines what day to display by comparing the current time
# passed in and the scheduled configuration input time.
def determine_day(hour, minute):
    if (current_hour > hour):
        return 'tomorrow'

    if (current_hour == hour) and (current_minute > minute):
        return 'tomorrow'
    
    return 'today'

def print_job(hour, minute, day, command):
    sys.stdout.write('{}:{:02} {} - {}\n'.format(hour, minute, day, command))

def main():
    for line in sys.stdin:
        minute, hour, command = line.split()

        if (minute == '*'):
            minute = current_minute
        else:
            minute = int(minute)

        if (hour == '*'):
            hour = current_hour
        else:
            hour = int(hour)

        if (command == '/bin/run_me_daily'):
            run_me_daily(hour, minute, command)

        if (command == '/bin/run_me_hourly'):
            run_me_hourly(hour, minute, command)

        if (command == '/bin/run_me_every_minute'):
            run_me_every_minute(hour, minute, command)

        if (command == '/bin/run_me_sixty_times'):
            run_me_sixty_times(hour, minute, command)

if __name__ == '__main__':
    current_time = sys.argv[1]

    current_hour, current_minute = current_time.split(':')
    current_hour = int(current_hour)
    current_minute = int(current_minute)

    counter = 0
    main()
