import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    city_list = ['chicago', 'new york city', 'washington']
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    while True:
        city = input("Please enter city name (chicago, new york city, washington): ").lower()
        if city in city_list:
            break
        else:
            print("Please input a valid city of chicago, new york city, or washington.")

    while True:
        month = input("Please enter a period based on months (all, january, february, ... , june): ").lower()
        if month in month_list:
            break
        else:
            print("Please input a valid month from the list or input 'all' to apply no month filter.")

    while True:
        day = input("Please enter a day of the week (all, monday, tuesday, ... sunday): ").lower()
        if day in day_list:
            break
        else:
            print("Please input a valid day from the list or input 'all' to apply no day filter.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"File for {city} not found. Please make sure the CSV file is in the same directory.")
        return None

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_raw_data(df):
    start_row = 0
    while True:
        display = input("Do you want to check the first 5 rows of the dataset related to the chosen city? Type 'yes' or 'no': ").lower()
        if display == 'yes':
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
            if start_row >= len(df):
                print("End of data reached.")
                break
        else:
            break

def time_stats(df):
    if df is None:
        print("No data to display.")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    if df is None:
        print("No data to display.")
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', popular_end_station)

    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    popular_combination = df['Start-End Combination'].mode()[0]
    print('Most Frequent Combination of Start and End Station Trip:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    if df is None:
        print("No data to display.")
        return

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    if df is None:
        print("No data to display.")
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)

    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nEarliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            display_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
