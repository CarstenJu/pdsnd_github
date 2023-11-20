from calendar import month
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = input("Which city would you like to analyze first?: ").lower()
    while city not in CITY_DATA:
        print("We do not have information about {}. Please select one of the following cities: \n".format(city))
        for key in CITY_DATA:
            print("{} \n".format(key))
        city = input("Which city do you want to analyze first: ").lower()
    
              

    # get user input for month (all, january, february, ... , june)
    month = input("Which month would like to filter on? The data is available for first have of the year. \nPlease enter name of the month: \n").lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        print("We do not have information about {}. Please select one of the following months: \n".format(month))
        for element in months:
            print("{} \n".format(element))
        month = input("Which month do you want to analyze: ").lower()
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would like to filter on? \nPlease enter name of the day: \n").lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        print("We do not have information about {}. Please select one of the following days: \n".format(day))
        for element in days:
            print("{} \n".format(element))
        day = input("Which day do you want to analyze: ").lower()

    
    print("In summary: You would like to anayse the city of {}. During {} and for {}".format(city, month, day))
    
    print('-'*40)
    return city, month, day
    

def load_data(city, month, day):
    """
   Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all days" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df
    

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months_frequency = df['month'].value_counts()
    most_common_month = months_frequency.idxmax()
    max_month_frequency = months_frequency.max()
    if month == 'all':
        print("The most freuquent month is {}. It had {} trips".format(most_common_month,max_month_frequency))
    else: 
        print("The selected month of {} had {} trips.".format(most_common_month,max_month_frequency))
    

    # display the most common day of week
    day_frequency = df['day_of_week'].value_counts()
    most_common_day = day_frequency.idxmax()
    max_day_frequency = day_frequency.max()
    if day == 'all':
        print("The most freuquent day is {}. It had {} trips".format(most_common_day,max_day_frequency))
    else: 
        print("{} as the selected day had {} trips.".format(most_common_day,max_day_frequency))


    # display the most common start hour
    df['Start hour'] = df['Start Time'].dt.hour
    start_hour_frequency = df['Start hour'].value_counts()
    most_common_hour = start_hour_frequency.idxmax()
    max_hour_frequency = start_hour_frequency.max()
    print("The most freuquent start hour is {} o'clock. It had {} trips".format(most_common_hour,max_hour_frequency))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_frequency = df['Start Station'].value_counts()
    most_common_start_station = start_station_frequency.idxmax()
    max_start_station_count = start_station_frequency.max()
    print("The most frequent start station is {}. It had {} trips".format(most_common_start_station,max_start_station_count))

    # display most commonly used end station
    end_station_frequency = df['End Station'].value_counts()
    most_common_end_station = end_station_frequency.idxmax()
    max_end_station_count = end_station_frequency.max()
    print("The most frequent end station is {}. It had {} trips".format(most_common_end_station,max_end_station_count))

    # display most frequent combination of start station and end station trip
    start_stop_combined = start_station_frequency.add(end_station_frequency, fill_value=0)
    most_common_start_stop = start_stop_combined.idxmax()
    max_start_stop_count = int(start_stop_combined.max())
    print("The most frequent combination of start and end station is {}. It had {} trips".format(most_common_start_stop, max_start_stop_count))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    def translate_seconds_to_days(seconds):
        days, remainder = divmod(seconds, 86400)  # 1 day = 24 * 60 * 60 seconds
        hours, remainder = divmod(remainder, 3600)  # 1 hour = 60 * 60 seconds
        minutes, seconds = divmod(remainder, 60)

        return days, hours, minutes, seconds
    total_travel_time_dhms = translate_seconds_to_days(total_travel_time)
    days, hours, minutes, seconds = total_travel_time_dhms
    print("The total travel time is: {} days, {} hours, {} minutes, {} seconds".format(days,hours,minutes,seconds))

    # display mean travel time
    median_travel_time = int(df['Trip Duration'].median() // 60)
    print("The mean travel time is about {} minutes".format(median_travel_time))
    mean_travel_time = int(df['Trip Duration'].meann() // 60)
    print("The mean travel time is about {} minutes".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The user split by type is: \n {} \n ".format(user_types.to_string()))



    # Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print("The user split by gender is: \n {} \n ".format(gender_count.to_string()))


    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year = int(df['Birth Year'].min())
        print("The lowest year of birth is: {} \n".format(earliest_year))
        most_recent_year = int(df['Birth Year'].max())
        print("The most recent year of birth is: {} \n".format(most_recent_year))

        most_common_year = df['Birth Year'].value_counts()
        most_common_year_id = int(most_common_year.idxmax())
        most_common_year_count = most_common_year.max()
        print("The most common year of birth is {}. Theer are {} customers born in {}".format(most_common_year_id,most_common_year_count,most_common_year_id))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    agree = input("Would you like to see the underlying raw data? \nPlease enter yes or no. \n")
    counter_low = 0
    counter_high = 10
    
    while agree == 'yes' and df.shape[0]>counter_low:
        print(df.iloc[counter_low : counter_high])
        counter_low += 10
        counter_high += 10
        agree = input("Would you like to see more lines of the raw data? \nPlease enter yes or no. \n")
        



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
