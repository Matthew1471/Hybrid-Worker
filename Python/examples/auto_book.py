#!/usr/bin/env python
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

# We delay.
import time

# All the shared Condeco® functions are in this package.
from hybrid_worker.condeco import Condeco

def book_week(condeco):
    # Add 3 weeks to the current Monday.
    current_date = datetime.date.today()
    start_of_week = current_date + datetime.timedelta(days=-current_date.weekday(), weeks=3)

    # Gather the Monday and Friday dates to book for.
    candidate_dates = [ start_of_week + datetime.timedelta(days=4), start_of_week ]
    print(f'{datetime.datetime.now()} - Starting booking for {", ".join(map(str, candidate_dates))}.\n', flush=True)

    # Repeated failures have a 5 second back-off time.
    last_attempt_also_failed = False

    # Try for up to 120 seconds (24 * 5 second maximum delay).
    for _ in range(24):

        # Leave when there is nothing further to do.
        if not candidate_dates:
            return True

        # Get the first candidate date.
        candidate_date = candidate_dates.pop(0)

        # Notify user.
        print(f'{datetime.datetime.now()} - Booking for {candidate_date}:', flush=True)

        # Attempt to book.
        if book_single_day(condeco, candidate_date):
            # This was a success, perhaps the new slots have just been released.
            last_attempt_also_failed = False
        else:
            # We will come back to this date.
            candidate_dates.append(candidate_date)

            # Wait 5 seconds.
            if last_attempt_also_failed:
                time.sleep(5)

            # Tell the next attempt that this attempt failed.
            last_attempt_also_failed = True

        # Add a new line.
        print(flush=True)

    # Not able to book all dates within the time allocated.
    return False

def book_single_day(condeco, candidate_date):
    # searchDeskByFeatures
    desk_search_request_with_features = {
        'accessToken':configuration['authentication']['sessionToken'],
        'locationID':configuration['auto_book']['location_id'],
        'groupID':configuration['auto_book']['group_id'],
        'floorID':configuration['auto_book']['floor_id'],
        'bookingType':Condeco.BOOKING_TYPE['None'],
        'startDate':candidate_date.strftime('%d/%m/%Y'),
        'userID':configuration['auto_book']['user_id'],
        'deskAttributes':[],
        'wsTypeID':configuration['auto_book']['ws_type_id']
    }

    response = condeco.searchDeskByFeatures(
        access_token=configuration['authentication']['token'],
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
            if book_desk(condeco, candidate_date, desk['DeskID']):
                # We now have a booking for this day.
                return True

def book_desk(condeco, date, desk_id):
    # bookDesk
    response = condeco.bookDesk(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        user_id=None,
        location_id=configuration['auto_book']['location_id'],
        group_id=configuration['auto_book']['group_id'],
        floor_id=configuration['auto_book']['floor_id'],
        desk_id=desk_id,
        start_date=date.strftime('%d/%m/%Y') + '|' + str(Condeco.BOOKING_TYPE['AllDay'])
    )

    # Parse the response as JSON.
    response_json = response.json()

    # Did it get booked?
    if response_json['CallResponse']['ResponseCode'] == 100:
        # Succeeded.
        print(f'{datetime.datetime.now()} -  * Booked #{response_json["CreatedBookings"][0]["BookingID"]}.', flush=True)
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
        global configuration
        configuration = json.load(json_file)

    # Create an initialised Condeco® object.
    condeco = Condeco(unique_key=configuration['authentication']['unique_key'])

    # Do we already have a token to use the app?
    if configuration['authentication'].get('token'):
        # Perform the booking attempts.
        if book_week(condeco):
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