import time
import re
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

city = ""


def display_rawdata(df):
    """
    Displays five rows of data at the users request.
    :param: df: DataFrame of the city loaded.
    :return: Function returns nothing.
    """
    print("Displaying Raw Data ...")


    index = 0
    num_of_rows = df.shape[0]
    while (index + 5) <= num_of_rows:

        if index != 0:
            user_input = input("Do you want to see another five rows of data? Enter yes or no\n")
        else:
            user_input = input("Do you want to see the first five rows of data? Enter yes or no\n")

        if user_input.lower() == 'yes':
            print(df.loc[index:index + 5])
            index += 5
            print('-' * 80)
        elif user_input.lower() == 'no':
            return
        else:
            print("Invalid input. Please enter 'yes' or 'no'")

def validate_input(user_inputs):
    """
    Checks and validates if user input is A-Z (including whitespace) only.

    Args:
        (list) user_inputs: A list of inputs by the user (string)

    Returns:
        (boolean) True if all inputs are valid
        (boolean) False if either one or all inputs are invalid.
    """

    months_filter = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days_filter = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    city, month, day = user_inputs

    if month in months_filter and day in days_filter and city in CITY_DATA.keys():
        pattern = re.compile("^[a-zA-Z ]+$")
        for usr_input in user_inputs:
            match = pattern.match(usr_input)
            if match is None:
                print("Make sure you've typed the city/month/day correctly")
                return False
    else:
        print("Invalid Input. Correct input: city [chicago/new york/washington], month: [jan through june / all], day: [sunday through saturday / all].")
        return False

    return True


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
    while True:
        print("To ignore month and day filters: input 'all' in their respective fields")
        city, month, day = [user_input.strip().lower() for user_input in input("Enter city, month, day (comma separated): ").split(',')]
        if validate_input([city, month, day]):
            break

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['Month'] == month.title()]

    if day != 'all':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].value_counts().idxmax()
    print(f'Most Common Month: {most_common_month}')

    # display the most common day of week
    most_common_weekday = df['Day'].value_counts().idxmax()
    print(f'Most Common Weekday: {most_common_weekday}')

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print(f'Most Common Start Hour: {most_common_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print(f'Most Common Start Station: {most_common_start_station}')

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print(f'Most Common End Station: {most_common_end_station}')

    # display most frequent combination of start station and end station trip
    most_common_start_combo, most_common_end_combo = df[['Start Station', 'End Station']].value_counts().idxmax()
    print(f'Most Common Start & End: {most_common_start_combo} - {most_common_end_combo}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time / 3600} hours")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time: {average_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Type Count:")
    print("-"*25)
    user_count = "\n".join(str(df['User Type'].value_counts()).split('\n')[:-1])
    print(user_count)

    # Display counts of gender
    if city == 'chicago' or city == 'new york':
        print("\nGender Count:")
        print("-"*25)
        gender_count = "\n".join(str(df['Gender'].value_counts()).split('\n')[:-1])
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].value_counts().idxmax())
        print(f"\nEarliest Year of Birth: {earliest_year}\nMost Recent Year: {most_recent_year}\nMost Common Year: {most_common_year}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
