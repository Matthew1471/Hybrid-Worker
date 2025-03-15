#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Hybrid-Worker <https://github.com/Matthew1471/Hybrid-Worker>
# Copyright (C) 2023-2025 Matthew1471!
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This example provides functionality to routinely book personal spaces with Condeco®.
"""

# We support command line arguments.
import argparse

# We use calendar to convert day names.
import calendar

# We manipulate dates.
import datetime

# This script makes heavy use of JSON parsing.
import json

# We delay.
import time

# We handle connection errors.
import requests

# All the shared Condeco® functions are in this package.
from hybrid_worker.condeco import Condeco

def book_day(condeco, access_token, session_token, settings, candidate_date):
    """
    Find desks on a specific day and then attempt to book them.

    Args:
        condeco (Condeco): An initalised Condeco object.
        access_token (str): The JWT for authentication.
        session_token (str): The opaque session token also used as part of authentication.
        settings (dict): auto_book desk search settings.
        candidate_date (datetime.date): The date to book.

    Returns:
        True on success, False on failure.
    """

    # Format candidate_date.
    date_string = candidate_date.strftime('%d/%m/%Y')

    # searchDeskByFeatures
    desk_search_request_with_features = {
        'accessToken': session_token,
        'locationID': settings['location_id'],
        'groupID': settings['group_id'],
        'floorID': settings['floor_id'],
        'bookingType': Condeco.BOOKING_TYPE['None'],
        'startDate': date_string,
        'userID': settings['user_id'],
        'deskAttributes': [],
        'wsTypeID': settings['ws_type_id']
    }

    response = condeco.searchDeskByFeatures(
        access_token=access_token,
        desk_search_request_with_features=desk_search_request_with_features
    )

    # Parse the response as JSON.
    response_json = response.json()

    # Did we return desks?
    if response_json['CallResponse']['ResponseCode'] != 100:
        response_message = response_json["CallResponse"]["ResponseMessage"]
        print(f'{datetime.datetime.now()} -  * Failure due to "{response_message}".', flush=True)
        return False

    # Take each of the desks.
    for desk in response_json['SearchedDesks']:
        # Check the desk is available for booking.
        if desk['CanBeBooked']:
            # About to book.
            print(f'{datetime.datetime.now()} -  * Attempting to book "{desk["DeskName"]}" (#{desk["DeskID"]}).', flush=True)

            # bookDesk
            response = condeco.bookDesk(
                access_token=access_token,
                session_token=session_token,
                user_id=None,
                location_id=settings['location_id'],
                group_id=settings['group_id'],
                floor_id=settings['floor_id'],
                desk_id=desk['DeskID'],
                start_date=date_string + '|' + str(Condeco.BOOKING_TYPE['AllDay'])
            )

            # Parse the response as JSON.
            response_json = response.json()

            # Did it get booked?
            if response_json['CallResponse']['ResponseCode'] == 100:
                # Succeeded.
                if len(response_json["CreatedBookings"]) > 0:
                    booking_id = response_json["CreatedBookings"][0]["BookingID"]
                    print(f'{datetime.datetime.now()} -  * Booked #{booking_id}.')
                else:
                    # Sometimes API does not return booking details.
                    print(f'{datetime.datetime.now()} -  * Booked.')
                return True

            # Specific failure.
            response_message = response_json["CallResponse"]["ResponseMessage"]
            print(f'{datetime.datetime.now()} -  * Failure due to "{response_message}".', flush=True)
            return False

    # No bookable desks returned.
    return False

def main():
    """
    Main function for automatic booking.

    Args:
        None

    Returns:
        None
    """

    # Create an instance of argparse to handle any command line arguments.
    parser = argparse.ArgumentParser(prefix_chars='/-', add_help=False, description='A program that automatically books desks.')

    # Allowed program arguments.
    parser.add_argument('/Attempts', '-Attempts', '--Attempts', default=120, type=int, help='The number of attempts to book.', dest='attempts')
    parser.add_argument('/Config', '-Config', '--Config', default='auto_book', help='The configuration file section to use.', dest='config')
    parser.add_argument('/Day', '-Day', '--Day', default='Monday', choices=['AnyWeekday'] + list(calendar.day_name), help='The day of the week to book.', dest='day')
    parser.add_argument('/Weeks', '-Weeks', '--Weeks', default=3, type=int, choices=range(53), help='The number of weeks in the future to book.', dest='weeks')

    # We want this to appear last in the argument usage list.
    parser.add_argument('/?', '/Help', '/help', '-h','--help','-help', action='help', help='Show this help message and exit.')

    # Handle any command line arguments.
    args = parser.parse_args()

    # Load configuration.
    with open('configuration.json', mode='r', encoding='utf-8') as json_file:
        configuration = json.load(json_file)

    # Create an initialised Condeco® object.
    condeco = Condeco(unique_key=configuration['authentication']['unique_key'])

    # Do we already have a token to use the app?
    if configuration['authentication'].get('token'):

        # Allow support for booking any day.
        if args.day == 'AnyWeekday':
            # First five days of the week.
            days_to_book = range(5)

            # State we will book for any weekday.
            print(f'{datetime.datetime.now()} - Starting booking for any weekday.\n')
        else:
            # Create a dictionary with day name strings to integers.
            days_index = dict(zip(calendar.day_name, range(7)))

            # Map the specified day name to an integer.
            days_to_book = [days_index[args.day]]

            # State the day of the week to book for.
            print(f'{datetime.datetime.now()} - Starting booking for {args.day}.\n')

        # Obtain JWT.
        access_token = configuration['authentication']['token']

        # Check JWT.
        decoded_jwt = Condeco.decode_jwt(access_token)

        # Obtain opaque session token from the JWT access token.
        session_token = decoded_jwt['id']

        # Obtain reference to auto_book settings.
        settings = configuration[args.config]

        # List access token expiration details.
        time_delta = datetime.datetime.fromtimestamp(decoded_jwt['exp']) - datetime.datetime.now()
        print(f'{datetime.datetime.now()} - Token expires in {time_delta}.')

        # Add args.weeks number of weeks to the current Monday.
        current_date = datetime.date.today()
        start_of_week = current_date + datetime.timedelta(days=-current_date.weekday(), weeks=args.weeks)

        # Repeat for each of the days to book until a booking is made.
        for day in days_to_book:
            # Gather the future date to book for.
            candidate_date = start_of_week + datetime.timedelta(days=day)

            # Notify user.
            print(f'\n{datetime.datetime.now()} - Booking for {candidate_date}:', flush=True)

            # Try for around args.attempts seconds (server delay/retries make it longer).
            for _ in range(args.attempts):
                try:
                    # Attempt to book.
                    if book_day(condeco, access_token, session_token, settings, candidate_date):
                        print(f'\n{datetime.datetime.now()} - Finished, booking completed successfully.\n')

                        # Break out of the function.
                        return

                    # Wait 1 second before retrying.
                    time.sleep(1)
                except requests.exceptions.ConnectionError:
                    # Notify the user.
                    print(f'{datetime.datetime.now()} -  * Failure due to repeated connection errors.', flush=True)

        # Not able to book a date within the time allocated.
        print(f'\n{datetime.datetime.now()} - Finished, unable to book a space.\n')

    # Is the user wanting to validate a validation key?
    elif configuration['authentication'].get('validation_key'):
        # Validate the validation key and return a token.
        response = condeco.loginWithMagicLink(
            validation_key=configuration['authentication']['validation_key']
        )
        print(response.text)
    else:
        # Send a validation key to this user.
        response = condeco.sendMagicLink(
            email=configuration['authentication']['email']
        )
        print(response.text)

# Launch the main method if invoked directly.
if __name__ == '__main__':
    main()
