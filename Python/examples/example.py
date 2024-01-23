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
This example provides functionality to interact with the Condeco® software.
"""

# We manipulate dates.
import datetime

# This script makes heavy use of JSON parsing.
import json

# All the shared Condeco® functions are in this package.
from hybrid_worker.condeco import Condeco

#region Examples

def bookDesk():
    # bookDesk
    response = condeco.bookDesk(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        user_id=configuration['examples']['user_id'],
        location_id=configuration['examples']['location_id'],
        group_id=configuration['examples']['group_id'],
        floor_id=configuration['examples']['floor_id'],
        desk_id=configuration['examples']['desk_id'],
        start_date=next_weekday(datetime.date.today(), 5).strftime('%d/%m/%Y') + '|' + str(Condeco.BOOKING_TYPE['AllDay'])
    )
    print(response.text)

def deleteBooking():
    # deleteBooking
    response = condeco.deleteBooking(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        booking_id=configuration['examples']['booking_id'],
        desk_id=configuration['examples']['desk_id'],
        start_date=next_weekday(datetime.date.today(), 5).strftime('%d/%m/%Y') + ' 00:00 AM',
        end_date=next_weekday(datetime.date.today(), 5).strftime('%d/%m/%Y') + ' 23:59 PM',
        booking_type=Condeco.BOOKING_TYPE['AllDay']
    )
    print(response.text)

def findColleagues():
    # findColleagues
    response = condeco.findColleagues(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        name=configuration['examples']['name']
    )
    print(response.text)

def getAttendancesRecord():
    # getAttendancesRecord
    response = condeco.getAttendancesRecord(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        start_date=(datetime.date.today() - datetime.timedelta(7)).strftime('%d/%m/%Y'),
        end_date=datetime.date.today().strftime('%d/%m/%Y'),
        user_id=configuration['examples']['user_id_other']
    )
    print(response.text)

def getColleagueBookings():
    # getColleagueBookings
    response = condeco.getColleagueBookings(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        start_date=datetime.date.today().strftime('%d/%m/%Y'),
        end_date=(datetime.date.today() + datetime.timedelta(7)).strftime('%d/%m/%Y'),
        time_zone_id='""',
        user_id=configuration['examples']['user_id_other']
    )
    print(response.text)

def getMyTeams():
    # getMyTeams
    response = condeco.getMyTeams(
        access_token=configuration['authentication']['token'],
        user_long_id=configuration['authentication']['sessionToken']
    )
    print(response.text)

def getDeskSessionToken():
    # getDeskSessionToken (V2)
    response = condeco.getDeskSessionToken(
        access_token=configuration['authentication']['token']
    )
    print(response.text)

def getFloorPlan():
    # getFloorPlan
    response = condeco.getFloorPlan(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        location_id=configuration['examples']['location_id'],
        group_id=configuration['examples']['group_id'],
        floor_id=configuration['examples']['floor_id'],
    )
    print(response.text)

def getSessionToken():
    # getSessionToken
    response = condeco.getSessionToken(
        access_token=configuration['authentication']['token']
    )
    print(response.text)

def deskGlobalSettings():
    # deskGlobalSettings
    response = condeco.deskGlobalSettings()
    print(response.text)

def search():
    # search
    response = condeco.search(
        access_token=configuration['authentication']['token'],
        session_token=configuration['authentication']['sessionToken'],
        user_id=configuration['examples']['user_id'],
        location_id=configuration['examples']['location_id'],
        group_id=configuration['examples']['group_id'],
        floor_id=configuration['examples']['floor_id'],
        start_date=next_weekday(datetime.date.today(), 5).strftime('%d/%m/%Y'),
        booking_type=Condeco.BOOKING_TYPE['AllDay'],
        ws_type_id=configuration['examples']['ws_type_id']
    )
    print(response.text)

def searchDeskByFeatures():
    # searchDeskByFeatures
    desk_search_request_with_features = {
        'accessToken':configuration['authentication']['sessionToken'],
        'locationID':configuration['examples']['location_id'],
        'groupID':configuration['examples']['group_id'],
        'floorID':configuration['examples']['floor_id'],
        'bookingType':Condeco.BOOKING_TYPE['AllDay'],
        'startDate':next_weekday(datetime.date.today(), 5).strftime('%d/%m/%Y'),
        'userID':configuration['examples']['user_id'],
        'deskAttributes':{},
        'wsTypeID':configuration['examples']['ws_type_id']
        }

    response = condeco.searchDeskByFeatures(
        access_token=configuration['authentication']['token'],
        desk_search_request_with_features=desk_search_request_with_features
    )
    print(response.text)

#endregion

def next_weekday(date, weekday):
    days_ahead = weekday - date.weekday()

    # Target day already happened this week
    if days_ahead <= 0:
        days_ahead += 7

    return date + datetime.timedelta(days_ahead)

def main():
    """
    Main function for displaying Condeco® software interaction.

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
    global condeco
    condeco = Condeco(unique_key=configuration['authentication']['unique_key'])

    # Do we already have a token to use the app?
    if configuration['authentication'].get('token'):

        # bookDesk()
        # bookReservedTeamDayDesk()
        # cancelBooking()
        # checkIn()
        # createBooking()
        # createMyTeamDay()
        # deleteBooking()
        # deleteTeamDay()
        # deskAuthenticateUserSecure()
        # deskGlobalSettings()
        # deskSystemInfo()
        # endBooking()
        # extendBooking()
        # findColleagues()
        # geoFencingCheckIn()
        # getAttendancesRecord()
        # getColleagueBookings()
        # getDeskSessionToken()
        # getFloorPlan()
        # getGroupSettingsWithRestrictions()
        # getLoginInformation()
        # getMyTeams()
        # getReservedDeskStatus()
        # getRoomAvailabilities()
        # getRoomInfos()
        # getSelfCertificationContent()
        # getSelfCertificationStatus()
        # getSessionToken()
        # globalSettings()
        # listBookings()
        # deskGlobalSettings()
        # releaseDesk()
        # roomSearch()
        # roomSearchByFeatures()
        # saveDefaultSettings()
        # search()
        # searchAllByRoomFeatures()
        # searchDeskByFeatures()
        # selfCertifyUser()
        # startBooking()
        # teamDayAcceptDecline()
        # teamMemberOperation()
        # updateAttendanceRecord()
        # updateBooking()
        # updateDefaultSettings()

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