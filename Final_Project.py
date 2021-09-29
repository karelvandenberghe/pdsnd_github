import time
import pandas as pd

section_divider = '-'*50

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York, or Washington? ').title().strip()
    while city not in ['Chicago', 'New York', 'Washington']:
        print('Please enter a correct city')
        city = input('Would you like to see data for Chicago, New York, or Washington? ').title()
    print('\nAlright, let\'s get that data for {}!'.format(city))

    # get user input for month (January, February, ... , June or none)
    month = input('Which month would you like to filter by: January, February, March, April, May or June? \nPlease '
                  'type the full month or "none" for no month filter: ').title().strip()
    while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'None']:
        month = input('Please enter a correct month: ').title()
    print('\nAlright, let\'s filter the months by {}!'.format(month))

    # get user input for day of week (Monday, Tuesday, ... Sunday or none)
    day = input('Which day would you like to filter by: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday '
                'or Sunday? \nPlease type the full day or "none" for no day filter: ').title()
    while day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'None']:
        day = input('Please enter a correct day: ').title().strip()

    print(section_divider)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    CITY_DATA = {'Chicago': 'chicago.csv',
                  'New York': 'new_york_city.csv',
                  'Washington': 'washington.csv'}

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'None':
        # filter by day of week to create the new dataframe
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month was {}.'.format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day was {}.'.format(common_day))

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour was between {}:00 and {}:00 hours.'.format(common_hour, common_hour+1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(section_divider)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station was {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station was {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_both_stations = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print('The most common start and end station combination was: {} and {}.'.format(common_both_stations[0],
                                                                                     (common_both_stations[1])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(section_divider)


def seconds_to_hours_minutes_seconds(time_in_seconds):
    global hours
    hours = int(time_in_seconds / 3600)
    global minutes
    minutes = int((time_in_seconds - (hours*3600))/60)
    global seconds
    seconds = int(time_in_seconds - (hours*3600) - (minutes*60))
    return hours, minutes, seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    seconds_to_hours_minutes_seconds(total_travel_time)
    print("The total travel time for the selected city and filters was {} hours, {} minutes and {} seconds."
          .format(hours, minutes, seconds))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    seconds_to_hours_minutes_seconds(mean_travel_time)
    print("The mean travel time for the selected city and filters was {} hours, {} minutes and {} seconds."
          .format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(section_divider)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('The user types and counts for the selected filters were: \n{}'.format(user_types_count))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe gender of travellers for the selected filters were: \n{}'.format(gender_count))
    except KeyError:
        print('\nGender details were not provided in this database.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('\nThe oldest person for the selected filters was born in {}.'. format(earliest))
        print('The youngest person for the selected filters was born in {}.'. format(latest))
        print('Most of the travellers for the selected filters were born in {}.'.format(common_year))
    except KeyError:
        print('\nYear of birth details were not provided in this database.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(section_divider)


def raw_data(df):
    print('\nThe first 5 rows of individual data for these filters were:')
    i = 0
    while True:
        print(df[i:(i+5)])
        i += 5

        more = input('Would you like to see more individual data? Enter yes or no. ')
        if more.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for reviewing my project.")
            break


if __name__ == "__main__":
    main()
