import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']    #= {'january', 'february', 'march', 'april', 'may', 'june'}
              
days = ['all', 'monday', 'tuesday', 'wedensday', 'thursday', 'friday', 'sathurday', 'sunday']
              
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs 
    city = input('Enter the City (chicago, new york city or washington): ') 
    while city.lower() not in CITY_DATA:
        city = input("Error: data for {} is not available, please select chicago, new york city or washington: ".format(city))
        
    # get user input for month (all, january, february, ... , june)
    month = input('Enter the month to filter by or else type all: ')
    while month.lower() not in months or month == '\n':
        month = input('Error {} is not a valid input, please enter a month from january to june or press type all: '.format(month))
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter the day to filter by or type all: ')
    while day.lower() not in days or day == '':
        day = input('Error {} is not a valid input, please enter a valid day or press enter for all: '.format(month))
        
    print('-'*40)
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
    df = pd.read_csv('./' + CITY_DATA[city])
       
    

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

         
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_popular_month = df['month'].value_counts().idxmax()
    print("The month with most journeys is : {} ".format(months[most_popular_month - 1].title()))


    # display the most common day of week
    most_popular_day = df['day_of_week'].value_counts().idxmax()
    print("The busiest day is : {} ".format(most_popular_day)) 

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour 
    busiest_hour = df['hour'].mode()[0]
    print("The busiest hour of the day is : {}.00".format(busiest_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stn = df.groupby(['Start Station'])['Trip Duration'].value_counts() 
    busiest_start = start_stn.idxmax()
    print("The most popular Start Station is {} station".format(busiest_start[0]))

    # display most commonly used end station
    end_stn = df.groupby(['End Station'])['Trip Duration'].value_counts()
    busiest_end = end_stn.idxmax()
    print("The most popular Ending Station is {} station".format(busiest_end[0]))

    # display most frequent combination of start station and end station trip
    trips = df.groupby(['Start Station', 'End Station'])['Trip Duration'].value_counts() 
    busiest_route = trips.idxmax()
    print('The businest route is from {} station to {} station'.format(busiest_route[0],busiest_route[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_secs = df['Trip Duration'].sum()
    #print(tot_secs)
    mins, secs = divmod(tot_secs, 60)
    hr, min = divmod(mins, 60)
    print('The total travel duration is {} seconds or {} hours, {} minutes and {} seconds'.format(tot_secs, hr, min, int(secs)))
    
    # display mean travel time
    avg_secs = df['Trip Duration'].mean()
    #print(avg_secs)
    mins, secs = divmod(avg_secs, 60)
    hr, min = divmod(mins, 60)
    print('The average travel duration is {} seconds or {} hours, {} minutes and {} seconds'.format(avg_secs, hr, min, int(secs)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts(dropna=True))
    #counts for each gender
    
    # Display counts of gender if city is not washington
    if city != 'washington':
        print(df['Gender'].value_counts(dropna=True))
    # Display earliest, most recent, and most common year of birth
        #   year_earliest = df['Birth Year'].min().astype(int)
        print('The earliest user year of birth is {}'.format(df['Birth Year'].min().astype(int)))
        print('The most recent user year of birth is {}'.format(df['Birth Year'].max().astype(int)))
        print('The most common user year of birth is {}'.format(df['Birth Year'].mode()[0].astype(int)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
