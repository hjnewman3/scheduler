# -------------------------------------------------------------
# demonstrates a task scheduler, displaying the time when the 
# the next job will run based on the scheduler configuration
# input and the 'current time'.
#
# Harold "Chip" Newman
# chip@computerchip.tech
# -------------------------------------------------------------

import sys

def run_me_daily(config_hour, config_minute, command):
    config_hour = int(config_hour)
    config_minute = int(config_minute)
    print_job(config_hour, config_minute, determine_day(config_hour, config_minute), command)

def run_me_hourly(config_hour, config_minute, command):
    config_hour = current_hour
    config_minute = int(config_minute)
    # Determines whether to roll over to the next hour by comparing
    # the current minute to the scheduler configuration input minute.
    if (current_minute > config_minute):
        config_hour += 1

        # Rolls over to the next day if the increase causes
        # the hour to exceed 23 hours.
        if (config_hour > 23):
            config_hour = config_hour - 24

    print_job(config_hour, config_minute, determine_day(config_hour, config_minute), command)

def run_me_every_minute(config_hour, config_minute, command):
    config_hour = current_hour
    config_minute = current_minute
    print_job(config_hour, config_minute, determine_day(config_hour, config_minute), command)

# Number of executions will be limited by the counter.
def run_me_sixty_times(config_hour, config_minute, command):
    config_hour = int(config_hour)
    config_minute = current_minute
    global counter

    # Starts at the top of the hour if current hour and 
    # scheduled configuration input hour aren't the same.
    # (current minute == minutes) returns true if the scheduled
    # configuration input minute value is "*".
    if (current_hour != config_hour) and (current_minute == config_minute):
        config_minute = 0

    if (counter < 60):
        print_job(config_hour, config_minute, determine_day(config_hour, config_minute), command)
        counter += 1

# Determines what day to display by comparing the current time
# passed in and the scheduled configuration input time.
def determine_day(config_hour, config_minute):
    if (current_hour > config_hour) or \
        ((current_hour == config_hour) and (current_minute > config_minute)):
        return 'tomorrow'

    return 'today'

def print_job(config_hour, config_minute, day, command):
    sys.stdout.write('{}:{:02} {} - {}\n'.format(config_hour, config_minute, day, command))

def main():
    for line in sys.stdin:
        config_minute, config_hour, command = line.split()

        # runs if neither min nor hour are '*'
        if (config_minute != '*' and config_hour != '*'):
            run_me_daily(config_hour, config_minute, command)

        # runs only if hour is '*'
        elif (config_minute != '*' and config_hour == '*'):
            run_me_hourly(config_hour, config_minute, command)

        # runs only if both min and hour are '*'
        elif (config_minute == '*' and config_hour == '*'):
            run_me_every_minute(config_hour, config_minute, command)

        # runs only if min is '*'
        elif (config_minute == '*' and config_hour != '*'):
            run_me_sixty_times(config_hour, config_minute, command)


if __name__ == '__main__':
    # Obtains the current time from the command-line
    current_time = sys.argv[1]

    # Obtains the current hour and current minute as an int
    current_hour, current_minute = (int(t) for t in current_time.split(':'))

    counter = 0
    
    main()
