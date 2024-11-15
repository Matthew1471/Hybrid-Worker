#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of Hybrid-Worker <https://github.com/Matthew1471/Hybrid-Worker>
# Copyright (C) 2023 Matthew1471!
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

# We manipulate dates.
import datetime

# This script makes heavy use of JSON parsing.
import json

# We handle connection errors.
import requests

# We delay.
import time

# All the shared Condeco® functions are in this package.
from hybrid_worker.condeco import Condeco

def book_week(condeco, candidate_dates):
    # Try for around 120 seconds (server delay/retries make it longer).
    for _ in range(120):

        # Leave when there is nothing further to do.
        if not candidate_dates:
            return True

        # Get the first candidate date.
        candidate_date = candidate_dates.pop(0)

        # Notify user.
        print(f'{datetime.datetime.now()} - Booking for {candidate_date}:', flush=True)

        try:
            # Attempt to book.
            if not book_single_day(condeco, candidate_date):
                # We will come back to this date.
                candidate_dates.append(candidate_date)

                # Wait 1 second.
                time.sleep(1)
        except requests.exceptions.ConnectionError:
                # Notify the user.
                print(f'{datetime.datetime.now()} -  * Failure due to repeated connection errors.', flush=True)

                # We will come back to this date.
                candidate_dates.append(candidate_date)

        # Add a new line.
        print(flush=True)

    # Not able to book all dates within the time allocated.
    return False

def book_single_day(condeco, candidate_date):
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
        print(f'{datetime.datetime.now()} -  * Failure due to "{response_json["CallResponse"]["ResponseMessage"]}".', flush=True)
        return False

    # Take each of the desks.
    for desk in response_json['SearchedDesks']:
        # Check the desk is available for booking.
        if desk['CanBeBooked']:
            # About to book.
            print(f'{datetime.datetime.now()} -  * Attempting to book "{desk["DeskName"]}" (#{desk["DeskID"]}).', flush=True)

            # Attempt booking.
            if book_desk(condeco, date_string, desk['DeskID']):
                # We now have a booking for this day.
                return True

def book_desk(condeco, date_string, desk_id):
    # bookDesk
    response = condeco.bookDesk(
        access_token=access_token,
        session_token=session_token,
        user_id=None,
        location_id=settings['location_id'],
        group_id=settings['group_id'],
        floor_id=settings['floor_id'],
        desk_id=desk_id,
        start_date=date_string + '|' + str(Condeco.BOOKING_TYPE['AllDay'])
    )

    # Parse the response as JSON.
    response_json = response.json()

    # Did it get booked?
    if response_json['CallResponse']['ResponseCode'] == 100:
        # Succeeded.
        if len(response_json["CreatedBookings"]) > 0:
            print(f'{datetime.datetime.now()} -  * Booked #{response_json["CreatedBookings"][0]["BookingID"]}.', flush=True)
        else:
            # Sometimes API does not return booking details.
            print(f'{datetime.datetime.now()} -  * Booked.', flush=True)
        return True
    else:
        # Failure.
        print(f'{datetime.datetime.now()} -  * Failure due to "{response_json["CallResponse"]["ResponseMessage"]}".', flush=True)
        return False

def main():
    """
    Main function for automatic booking.

    Args:
        None

    Returns:
        None
    """

    # Load configuration.
    with open('configuration.json', mode='r', encoding='utf-8') as json_file:
        configuration = json.load(json_file)

    # Create an initialised Condeco® object.
    condeco = Condeco(unique_key=configuration['authentication']['unique_key'])

    # Do we already have a token to use the app?
    if configuration['authentication'].get('token'):
        # Add 3 weeks to the current Monday.
        current_date = datetime.date.today()
        start_of_week = current_date + datetime.timedelta(days=-current_date.weekday(), weeks=3)

        # Gather the Monday and Friday dates to book for.
        candidate_dates = [ start_of_week + datetime.timedelta(days=4), start_of_week ]
        print(f'{datetime.datetime.now()} - Starting booking for {", ".join(map(str, candidate_dates))}.\n', flush=True)

        # Obtain JWT.
        global access_token
        access_token = configuration['authentication']['token']

        # Check JWT.
        decoded_jwt = Condeco.decode_jwt(access_token)

        # Obtain opaque session token from the JWT access token.
        global session_token
        session_token = decoded_jwt['id']

        # Obtain reference to auto_book settings.
        global settings
        settings = configuration['auto_book']

        # List access token expiration details.
        expiry_date = datetime.datetime.fromtimestamp(decoded_jwt['exp'])
        time_delta = expiry_date - datetime.datetime.now()
        print(f'{datetime.datetime.now()} - Token expires in {time_delta}.\n', flush=True)

        # Perform the booking attempts.
        if book_week(condeco=condeco, candidate_dates=candidate_dates):
            print(f'{datetime.datetime.now()} - Finished, booking completed successfully.', flush=True)
        else:
            print(f'{datetime.datetime.now()} - Finished, unable to book one or more spaces.', flush=True)

        # Add a new line.
        print(flush=True)
    # Is the user wanting to validate a validation key?
    elif configuration['authentication'].get('validation_key'):
        # Validate the validation key and return a token.
        response = condeco.loginWithMagicLink(
            validation_key=configuration['authentication']['validation_key']
        )
        print(response.text, flush=True)
    else:
        # Send a validation key to this user.
        response = condeco.sendMagicLink(
            email=configuration['authentication']['email']
        )
        print(response.text, flush=True)

# Launch the main method if invoked directly.
if __name__ == '__main__':
    main()