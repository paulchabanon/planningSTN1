from gcalendar import Gcalendar

class Shifts:
  def __init__(self, gcal, config):
    self.gcal = gcal
    self.config = config

  def setShift(self, name, edate):
    time_start = edate+'T'+self.config.day_type[name]['start']+self.config.calendarGMT
    time_end = edate+'T'+self.config.day_type[name]['end']+self.config.calendarGMT
    
    # search if shift already set for this day
    for e in self.gcal.listEvents(edate):
      if e['organizer']['displayName'] == self.config.calendarName:
      
        # do we have to modify it ?
        if e['start']['dateTime'] == time_start and e['end']['dateTime'] == time_end:
          print 'no change'
          return
        
        print 'old',e['start']['dateTime']
        print 'new',time_start
        print 'comp',(e['start']['dateTime'] == time_start)
        print 'old',e['end']['dateTime']
        print 'new',time_end
        print 'comp',(e['end']['dateTime'] == time_end)
        print 'remove event'
        
        # Yes we have to delete an recreate
        self.gcal.rmEvent(e['id'])
        break
    
    # add event (if new or after deleting old one)
    print 'add event'
    options = {}
    
    if not self.config.location == '':
      options['location'] = self.config.location
    
    if self.config.use_colors:
      options['color'] = self.config.day_type[name]['color']
    
    self.gcal.addEvent(name, edate, time_start, time_end, options)
  
  def rmShift(self, edate):   
    # search if shift already set for this day
    for e in self.gcal.listEvents(edate):
      if e['organizer']['displayName'] == self.config.calendarName:
        print 'remove event'
        self.gcal.rmEvent(e['id'])
        break
