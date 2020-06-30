import time
import pandas as pd
import numpy as np
import calendar as calendar

CITY_DATA = { 'chicago': 'chicago.csv',
               'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
accepted_cities = ["new york city", "chicago", "washington"]
accepted_months = ["january", "february", "march", "april", "may", "june", "all"]
accepted_day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all" ]
accepted_display = ["yes", "no"]

def user_selection(options, prompt):
     """
    Asks user for input with a prompt. Checks to make sure input fits valid global list. Returns a valid response(human_reply( to a given prompt.

    """
    while True:
        #Input to prompt is assigned to variable human_reply
        human_reply = input(prompt).strip().lower()
        #Checks if reply is valid in global list
        if human_reply in options:
               return human_reply
        else:
            print("Not valid. Please enter a valid option.\n")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = user_selection(accepted_cities, "What data would you like to see for Chicago, New York City, or Washington?\n")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = user_selection(accepted_months,"Would you like to filter data by month? January, February, March, April, May, June, or all? Type all for no filters\n")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = user_selection(accepted_day, "Would you like to filter data by day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? Type 'all' for no filters\n")


    print('-'*50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    popular_month = calendar.month_abbr[df['month'].mode()[0]]
    print("\nThe most common month is: {}".format(popular_month))
    # TO DO: display the most common day of week

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print("\nThe most common day of week is: {}".format(popular_day))

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common hour is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most used start station is: {}".format(popular_start_station))


    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe most used end station is: {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print("\nThe most combined start and end station is:\n {}".format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total travel time: {}\n".format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Average travel time: {}\n".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    total_count = df["User Type"].value_counts()
    print("Types of User Breakdown:\n {}".format(total_count))

    # TO DO: Display counts of gender
    gender_count = df["Gender"].value_counts()
    print("Gender Breakdown:\n {}".format(gender_count))

    # TO DO: Display earliest, most recent, and most common year of birth
    early_birth = int(df["Birth Year"].min())
    recent_birth = int(df["Birth Year"].max())
    common_birth = int(df["Birth Year"].value_counts().idxmax())
    print("Early Year of Birth: {}\n".format(early_birth))
    print("Latest Year of Birth: {}\n".format(recent_birth))
    print("Common Year of Birth: {}\n".format(common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def raw_data_output(df):
     """Prompts user if he/she wants to view more data. Yes will spit out 5 lines of raw data from top to bottom. No will end the program"""
        start = 0
        end = 5
        while True:
            display = user_selection(accepted_display, "Would you like to view individual raw data?Type 'yes' or 'no'\n")
            if display == "yes":
                print(df[start:end])
                start+=5
                end+=5
            else:
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
