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
Condeco Module
This module provides classes and methods for interacting with the Condeco® software.
It supports obtaining an authenticated session and querying the system.
"""

# We can check JWT claims/expiration first before making a request
# ("pip install pyjwt" if not already installed).
#import jwt

# Third party library for making HTTP(S) requests;
# "pip install requests" if getting import errors.
from pickle import NONE
import requests


class Condeco:
    """
    A class to talk to Condeco®'s Cloud based software.
    """

    # This creates an expected user-agent and encourages JSON responses.
    HEADERS = {'User-Agent': 'okhttp/4.10.0', 'Accept': 'application/json'}

    # This sets a 1 minute connect and read timeout.
    TIMEOUT = 60

    ATTENDANCE_TYPE = {
        'PresentInOffice': 0,
        'WorkingFromHome': 1,
        'OnLeave': 2,
        'None': 3,
        'Unknown': 4
    }

    BOOKING_STATUS = {
        'None': 0,
        'ReadyToCheckIn': 1,
        'ReadyToRelease': 2,
        'NotReady': 3
    }

    BOOKING_TYPE = {
        'None': 0,
        'Morning': 1,
        'Evening': 2,
        'AllDay': 3
    }

    CHECK_IN_STATUS = {
        'NotCheckedIn': 0,
        'CheckedIn': 1
    }

    TEAM_INVITATION_STATUS = {
        'Declined': 0,
        'Accepted': 1,
        'NotResponded': 2,
    }

    WORKSPACE_TYPE = {
        'None': 0,
        'Room': 1,
        'Desk': 2,
        'TeamDay': 3
    }

    # Parameterized constructor.
    def __init__(self, unique_key):
        """
        Initalise the Condeco class with a unique_key.

        Args:
            unique_key (str): The hostname of the Condeco instance.
        """

        # The Condeco® instance to interact with.
        self.unique_key = unique_key

    def bookDesk(self, access_token, session_token, user_id, location_id, group_id, floor_id, desk_id, start_date):
        """
        Book a desk.

        Args:
            access_token (str): The JWT access token for authentication.
            session_token (str): The opaque session access token.
            user_id (int): The user to book the desk for.
            location_id (int): The location the desk is in.
            group_id (int): The group the desk is in.
            floor_id (int): The floor the desk is in.
            desk_id (int): The desk identification number.
            start_date (str): The date to book the desk (in the format dd/MM/yyyy|booking_type).

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&userID={user_id}'
        query += f'&locationID={location_id}'
        query += f'&groupID={group_id}'
        query += f'&floorID={floor_id}'
        query += f'&deskID={desk_id}'
        query += f'&startDate={requests.utils.quote(start_date)}'

        # Send the desk booking request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/Book?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def bookReservedTeamDayDesk(self, access_token, book_reserved_team_day_desk_request):
        """
        Book a reserved team day desk.

        Args:
            access_token (str): The JWT access token for authentication.
            book_reserved_team_day_desk_request (str): The request to book the desk.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the team day desk booking request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/BookReservedTeamDayDesk',
            headers=headers,
            json=book_reserved_team_day_desk_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def cancelBooking(self, access_token, delete_booking):
        """
        Cancel a room booking.

        Args:
            access_token (str): The JWT access token for authentication.
            delete_booking (str): The request to delete the room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the delete room booking request.
        response = requests.post(
            url=f'https://{self.unique_key}/mobileapi/MobileService.svc/RoomBookings/DeleteRoomBookingWithBody',
            headers=headers,
            json=delete_booking,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def checkIn(self, access_token, session_token, location_id, desk_id, qr_code):
        """
        Check in to a desk.

        Args:
            access_token (str): The JWT access token for authentication.
            session_token (str): The opaque session access token.
            location_id (int): The location the desk is in.
            desk_id (int): The desk identification number.
            qr_code (int): The QR code for the desk.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&locationID={location_id}'
        query += f'&deskID={desk_id}'
        query += f'&qrCode={qr_code}'

        # Send the desk check in request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/CheckIn?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def createBooking(self, access_token, add_booking):
        """
        Create a room booking.

        Args:
            access_token (str): The JWT access token for authentication.
            add_booking (str): The request to add the room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the create room booking request.
        response = requests.put(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/Add',
            headers=headers,
            json=add_booking,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def createMyTeamDay(self, access_token, create_team_day_request):
        """
        Create a team day.

        Args:
            access_token (str): The JWT access token for authentication.
            create_team_day_request (str): The request to create a team day.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the create team day request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/CreateMyTeamDay',
            headers=headers,
            json=create_team_day_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def deleteBooking(self, access_token, session_token, booking_id, desk_id, start_date, end_date, booking_type):
        """
        Delete a desk booking.

        Args:
            access_token (str): The JWT access token for authentication.
            session_token (str): The opaque session access token.
            booking_id (int): The desk booking id.
            desk_id (int): The desk identification number.
            start_date (str): The start date to delete the booking.
            end_date (str): The end date to delete the booking.
            booking_type (int): The type of booking to delete.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&bookingID={booking_id}'
        query += f'&deskID={desk_id}'
        query += f'&startDate={requests.utils.quote(start_date)}'
        query += f'&endDate={requests.utils.quote(end_date)}'
        query += f'&bookingType={booking_type}'

        # Send the delete desk booking request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/Delete?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def deleteTeamDay(self, access_token, delete_team_day):
        """
        Cancel a team day.

        Args:
            access_token (str): The JWT access token for authentication.
            delete_team_day (str): The request to cancel a team day.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the cancel team day request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/CancelTeamDay',
            headers=headers,
            json=delete_team_day,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def deskAuthenticateUserSecure(self, user_authentication):
        """
        Start the desk authentication process with Condeco®.

        Args:
            user_authentication (str): The user's authentication details.

        Returns:
            Response: The full response object.
        """

        # Send the desk authentication request.
        response = requests.post(
            url=f'https://{self.unique_key}/LoginAPI/auth/authenticateusersecure',
            headers=Condeco.HEADERS,
            json=user_authentication,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def deskGlobalSettings(self):
        """
        Get the global settings.

        Returns:
            Response: The full response object.
        """

        # Send the global settings request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/Configuration/GetGlobalSettings',
            headers=Condeco.HEADERS,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def deskSystemInfo(self):
        """
        Get the desk system information.

        Returns:
            Response: The full response object.
        """

        # Send the system information request.
        response = requests.get(
            url=f'https://{self.unique_key}/api/systeminfo',
            headers=Condeco.HEADERS,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def endBooking(self, access_token, end_booking_request):
        """
        End a room booking.

        Args:
            access_token (str): The JWT access token for authentication.
            end_booking_request (str): The request to end a room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the end room booking request.
        response = requests.put(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/End',
            headers=headers,
            json=end_booking_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def extendBooking(self, access_token, extend_booking_request):
        """
        End a room booking.

        Args:
            access_token (str): The JWT access token for authentication.
            extend_booking_request (str): The request to extend a room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the extend room booking request.
        response = requests.put(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/Extend',
            headers=headers,
            json=extend_booking_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def findColleagues(self, access_token, session_token, name):
        """
        Find colleagues.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            name (str): The colleague to find booking information for.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&name={name}'

        # Send the find colleagues request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/FindColleague?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def geoFencingCheckIn(self, access_token, session_token, locations):
        """
        Geofence check in.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            locations (str): The location to check into.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&locations={locations}'

        # Send the geofence check in request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/GeoFencingCheckIn?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getAttendancesRecord(self, access_token, session_token, start_date, end_date, user_id):
        """
        Get attendance record for a user.

        Args:
            access_token (str): The JWT proving authorisation.
            start_date (str): The start date to find booking information for.
            end_date (str): The end date to find booking information for.
            user_id (int): The user identification number to find booking information for.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&startDate={start_date}'
        query += f'&endDate={end_date}'
        query += f'&UserId={user_id}'

        # Send the attendance record request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/GetAttendanceRecord?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getColleagueBookings(self, access_token, session_token, start_date, end_date, time_zone_id, user_id):
        """
        Get colleague booking records for a user.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            start_date (str): The start date to find booking information for.
            end_date (str): The end date to find booking information for.
            time_zone_id (str): The time zone.
            user_id (int): The user identification number to find booking information for.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&startDate={start_date}'
        query += f'&endDate={end_date}'
        query += f'&timeZoneID={time_zone_id}'
        query += f'&userId={user_id}'

        # Send the colleague bookings request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/UserBookings?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getDeskSessionToken(self, access_token, current_culture=None):
        """
        Get desk booking session token.

        Args:
            access_token (str): The JWT proving authorisation.
            current_culture (str, optional): The current culture information.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        if current_culture is not None:
            query = f'currentCulture={current_culture}'
        else:
            query = ''

        # Send the desk booking session token request.
        response = requests.get(
            url=f'https://{self.unique_key}/mobileapi/MobileService.svc/User/GetSessionTokenV2?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getFloorPlan(self, access_token, session_token, location_id, group_id, floor_id):
        """
        Get floor plan.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            location_id (int): The specified location identifier.
            group_id (int): The specified group identifier.
            floor_id (int): The specified floor identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&locationId={location_id}'
        query += f'&groupId={group_id}'
        query += f'&floorId={floor_id}'

        # Send the floor plan request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/floors/Floorplan?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getGroupSettingsWithRestrictions(self, access_token, session_token, booking_for_user_id, location_id, group_ids):
        """
        Get floor plan.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            booking_for_user_id (int): The specified user id.
            location_id (int): The specified location identifier.
            group_ids (str): The specified group identifiers.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&bookingForUserId={location_id}'
        query += f'&locationId={group_id}'
        query += f'&groupIds={floor_id}'

        # Send the desk booking session token request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/groupSettingsWithRestrictions?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getLoginInformation(self, access_token, session_token, language_id, current_date_time, curent_culture):
        """
        Get login information.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            language_id (int): The language id.
            current_date_time (str): The current date and time.
            curent_culture (str): The current culture identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'token={session_token}'
        query += f'&languageId={language_id}'
        query += f'&currentDateTime={current_date_time}'
        query += f'&currentCulture={curent_culture}'

        # Send the login information request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/User/LoginInformationsV2?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getMyTeams(self, access_token, user_long_id):
        """
        Get team information.

        Args:
            access_token (str): The JWT proving authorisation.
            user_long_id (int): The user identification number to find team information for.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'userlongId={user_long_id}'

        # Send the team request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/GetMyTeams?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getReservedDeskStatus(self, access_token, user_long_id, team_day_id):
        """
        Get reserved desk status information.

        Args:
            access_token (str): The JWT proving authorisation.
            user_long_id (int): The user identification number to find reserved desk information for.
            team_day_id (int): The team day identification number.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'userlongId={user_long_id}'
        query += f'teamDayId={team_day_id}'

        # Send the reserved desk status request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/GetReservedDeskStatus?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getRoomAvailabilities(self, access_token, room_request):
        """
        Get room availability information.

        Args:
            access_token (str): The JWT proving authorisation.
            room_request (str): The room request.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the room availabilities request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/RoomAvailability',
            headers=headers,
            json=room_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getRoomInfos(self, access_token, room_request):
        """
        Get room information.

        Args:
            access_token (str): The JWT proving authorisation.
            room_request (str): The room request.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the room information request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/RoomInfo',
            headers=headers,
            json=room_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getSelfCertificationContent(self, access_token, session_token, location_id):
        """
        Get self certification content.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            location_id (int): The location identification number to find certification status.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'locationID={location_id}'

        # Send the self certification content request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/SelfCertificationContent?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getSelfCertificationStatus(self, access_token, session_token, location_id):
        """
        Get self certification status.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            location_id (int): The location identification number to find certification status.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'locationID={location_id}'

        # Send the self certification status request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/SelfCertificationStatus?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def getSessionToken(self, access_token):
        """
        Get session token.

        Args:
            access_token (str): The JWT proving authorisation.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the session token request.
        response = requests.get(
            url=f'https://{self.unique_key}/mobileapi/MobileService.svc/User/GetSessionToken',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def globalSettings(self):
        """
        Get the global settings.

        Returns:
            Response: The full response object.
        """

        # Send the global settings request.
        response = requests.get(
            url=f'https://{self.unique_key}/mobileapi/MobileService.svc/Configuration/GetGlobalSettings',
            headers=Condeco.HEADERS,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def listBookings(self, access_token, session_token, language_id, desk_start_date, desk_end_date, room_start_date, time_zone_id, page_size, page_index):
        """
        Get booking information.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            language_id (int): The language id.
            desk_start_date (str): The desk start date.
            desk_end_date (str): The desk end date.
            room_start_date (str): The room start date.
            time_zone_id (str): The time zone identifier.
            page_size (int): The number of records on each page.
            page_index (int): The page number to request.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'sessionGuid={session_token}'
        query += f'&languageId={language_id}'
        query += f'&deskStartDate={desk_start_date}'
        query += f'&deskEndDate={desk_end_date}'
        query += f'&roomStartDate={room_start_date}'
        query += f'&timeZoneID={time_zone_id}'
        query += f'&pageSize={page_size}'
        query += f'&pageIndex={page_index}'

        # Send the booking information request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/MyBookings/ListV2?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def loginWithMagicLink(self, validation_key):
        """
        Login with magic link.

        Args:
            validation_key (str): The authentication code to exchange for a JWT access token.

        Returns:
            Response: The full response object.
        """

        # Send the login request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/User/LoginWithMagicLink',
            headers=Condeco.HEADERS,
            json={'validationKey':validation_key},
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def releaseDesk(self, access_token, session_token, location_id, desk_id):
        """
        Release desk.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            location_id (int): The location identifier.
            desk_id (int): The desk identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&locationID={location_id}'
        query += f'&deskID={desk_id}'

        # Send the release desk request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/Release?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def roomSearch(self, access_token, room_search_criteria):
        """
        Search for room.

        Args:
            access_token (str): The JWT proving authorisation.
            room_request (str): The room search criteria.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the room search request.
        response = requests.post(
            url=f'https://{self.unique_key}/mobileapi/MobileService.svc/RoomBookings/RoomSearch',
            headers=headers,
            json=room_search_criteria,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def roomSearchByFeatures(self, access_token, room_search_request_with_features):
        """
        Search for room with specific features.

        Args:
            access_token (str): The JWT proving authorisation.
            room_search_request_with_features (str): The room search request with features.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the room search request with features.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/RoomSearchByFeatures',
            headers=headers,
            json=room_search_request_with_features,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def saveDefaultSettings(self, access_token, settings_request):
        """
        Save default settings.

        Args:
            access_token (str): The JWT proving authorisation.
            settings_request (str): The settings to save.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the save default settings request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/User/SaveDefaultSettingsV2',
            headers=headers,
            json=settings_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def search(self, access_token, session_token, user_id, location_id, group_id, floor_id, start_date, booking_type, ws_type_id):
        """
        Search for a desk.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            user_id (int, optional): The user to search for.
            location_id (int): The location identifier.
            group_id (int): The group identifier.
            floor_id (int): The floor identifier.
            start_date (str): The start date.
            booking_type (int): The booking type.
            ws_type_id (int, optional): The workstation type identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'

        if user_id is not None:
            query += f'&userId={user_id}'

        query += f'&locationID={location_id}'
        query += f'&groupId={group_id}'
        query += f'&floorId={floor_id}'
        query += f'&startDate={start_date}'
        query += f'&bookingType={booking_type}'

        if ws_type_id is not None:
            query += f'&WSTypeId={ws_type_id}'

        # Send the release desk request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/Search?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def searchAllByRoomFeatures(self, access_token, room_search_request_with_features):
        """
        Search for room with specific features.

        Args:
            access_token (str): The JWT proving authorisation.
            room_search_request_with_features (str): The room search request with features.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the room search request with features.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/SearchAllByRoomFeatures',
            headers=headers,
            json=room_search_request_with_features,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def searchDeskByFeatures(self, access_token, desk_search_request_with_features):
        """
        Search for desk with specific features.

        Args:
            access_token (str): The JWT proving authorisation.
            desk_search_request_with_features (str): The desk search request with features.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the desk search request with features.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/DeskSearchByFeatures',
            headers=headers,
            json=desk_search_request_with_features,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def selfCertifyUser(self, access_token, self_certify_user_request):
        """
        Self certify user.

        Args:
            access_token (str): The JWT proving authorisation.
            self_certify_user_request (str): The self certify user request.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the self certify user request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/SelfCertifyUser',
            headers=headers,
            json=self_certify_user_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def sendMagicLink(self, email):
        """
        Start the magic link authentication process.

        Args:
            email (str): The user's e-mail address for authentication.

        Returns:
            Response: The full response object.
        """

        # Send the magic link request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/User/SendMagicLink',
            headers=Condeco.HEADERS,
            json={'email':email},
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def startBooking(self, access_token, start_booking_request):
        """
        Start a room booking request.

        Args:
            access_token (str): The JWT access token for authentication.
            start_booking_request (str): The request to start the room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the start room booking request.
        response = requests.put(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/Start',
            headers=headers,
            json=start_booking_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def teamDayAcceptDecline(self, access_token, team_day_accept_decline_request):
        """
        Team day response.

        Args:
            access_token (str): The JWT access token for authentication.
            team_day_accept_decline_request (str): The response to the team day.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the team day response.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/TeamDayAcceptDecline',
            headers=headers,
            json=team_day_accept_decline_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def teamMemberOperation(self, access_token, team_member_operation_request):
        """
        Team member operation request.

        Args:
            access_token (str): The JWT access token for authentication.
            team_member_operation_request (str): The team member operation request.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the team member operation request.
        response = requests.post(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/team/TeamMemberOperation',
            headers=headers,
            json=team_member_operation_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def updateAttendanceRecord(self, access_token, session_token, start_date, end_date, attendance_type, location_id):
        """
        Update attendance record.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            start_date (str): The start date.
            end_date (str): The end date.
            attendance_type (int): The attendance type.
            location_id (int): The location identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&startDate={start_date}'
        query += f'&endDate={end_date}'
        query += f'&attendenceType={attendance_type}'
        query += f'&LocationId={location_ud}'

        # Send the update attendance record request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/UpdateAttendanceRecord?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def updateBooking(self, access_token, update_booking_request):
        """
        Update a room booking.

        Args:
            access_token (str): The JWT access token for authentication.
            update_booking (str): The request to update the room booking.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Send the update room booking request.
        response = requests.put(
            url=f'https://{self.unique_key}/MobileAPI/MobileService.svc/RoomBookings/Update',
            headers=headers,
            json=update_booking_request,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response

    def updateDefaultSettings(self, access_token, session_token, country_id, location_id, group_id, floor_id):
        """
        Update attendance record.

        Args:
            access_token (str): The JWT proving authorisation.
            session_token (str): The opaque session access token.
            country_id (int): The country identifier.
            location_id (int): The location identifier.
            group_id (int): The group identifier.
            floor_id (int): The floor identifier.

        Returns:
            Response: The full response object.
        """

        # Create a copy of the original header dictionary.
        headers = Condeco.HEADERS.copy()

        # We append an OAuth 2.0 bearer token.
        headers['Authorization'] = f'Bearer {access_token}'

        # Query parameters.
        query = f'accessToken={session_token}'
        query += f'&countryID={country_id}'
        query += f'&locationID={location_id}'
        query += f'&groupID={group_id}'
        query += f'&floorID={floor_id}'

        # Send the update default settings request.
        response = requests.get(
            url=f'https://{self.unique_key}/MobileAPI/DeskBookingService.svc/SaveDefaultSettings?{query}',
            headers=headers,
            timeout=Condeco.TIMEOUT
        )

        # Return the response.
        return response