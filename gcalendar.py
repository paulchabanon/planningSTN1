import httplib2
import sys

from datetime import date
from datetime import datetime
from pprint import pprint
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class Gcalendar:
  def __init__(self, calendarName, calendarGMT, client_id, client_secret):
    self.client_id = client_id
    self.client_secret = client_secret
    self.calendarName = calendarName
    self.calendarGMT = calendarGMT
    self.calendarId = ''
    
    self.events = {}
    
    # The scope URL for read/write access to a user's calendar data
    self.scope = 'https://www.googleapis.com/auth/calendar'

  def connect(self):
    # Create a flow object. This object holds the client_id, client_secret, and
    # scope. It assists with OAuth 2.0 steps to get user authorization and
    # credentials.
    flow = OAuth2WebServerFlow(self.client_id, self.client_secret, self.scope)

    # Create a Storage object. This object holds the credentials that your
    # application needs to authorize access to the user's data. The name of the
    # credentials file is provided. If the file does not exist, it is
    # created. This object can only hold credentials for a single user, so
    # as-written, this script can only handle a single user.
    storage = Storage('credentials.dat')

    # The get() function returns the credentials for the Storage object. If no
    # credentials were found, None is returned.
    credentials = storage.get()

    # If no credentials are found or the credentials are invalid due to
    # expiration, new credentials need to be obtained from the authorization
    # server. The oauth2client.tools.run() function attempts to open an
    # authorization server page in your default web browser. The server
    # asks the user to grant your application access to the user's data.
    # If the user grants access, the run() function returns new credentials.
    # The new credentials are also stored in the supplied Storage object,
    # which updates the credentials.dat file.
    if credentials is None or credentials.invalid:
      credentials = run(flow, storage)

    # Create an httplib2.Http object to handle our HTTP requests, and authorize it
    # using the credentials.authorize() function.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # The apiclient.discovery.build() function returns an instance of an API service
    # object can be used to make API calls. The object is constructed with
    # methods specific to the calendar API. The arguments provided are:
    #   name of the API ('calendar')
    #   version of the API you are using ('v3')
    #   authorized httplib2.Http() object that can be used for API calls
    self.service = build('calendar', 'v3', http=http)
    
    # Find calendar
    calendar_list = self.service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
      if calendar_list_entry['summary'] == self.calendarName:
        self.calendarId = calendar_list_entry['id']
    
    if not self.calendarId:
      raise Exception('Error', 'No Calendare named '+calendarName+' found')
    
    self.loadEvents()
    
  def loadEvents(self):
    page_token = None
    while True:
      events = self.service.events().list(calendarId=self.calendarId, pageToken=page_token, timeMin=str(date.today())+'T00:00:00.000'+self.calendarGMT).execute()
      for event in events['items']:
        edate = event['start']['dateTime'].split('T')[0]
        if not edate in self.events: 
          self.events[edate] = []
        
        self.events[edate].append(event)
      
      page_token = events.get('nextPageToken')
      if not page_token:
        break
  
  def listAllEvents(self):
    r = []
    for edate in self.events.iterkeys():
      r.append(self.listEvents(edate))
    return r
        
  def listEvents(self,edate):
    if not edate in self.events:
      return []
    
    return self.events[edate]
  
  # does not update loaded events list
  def addEvent(self, name, edate, time_start, time_end, options):
    event = {
      'summary': name,
      'start': {
        'dateTime': time_start
      },
      'end': {
        'dateTime': time_end
      }
    }
    
    if 'location' in options:
      event['location'] = options['location']
    
    if 'color' in options:
      event['colorId'] = options['color']

    created_event = self.service.events().insert(calendarId=self.calendarId, body=event).execute()

    return created_event['id']
  
  # does not update loaded events list
  def rmEvent(self, id):
    return self.service.events().delete(calendarId=self.calendarId, eventId=id).execute()
    
  
  