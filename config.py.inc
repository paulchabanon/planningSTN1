
class PlanningConfig:
  def __init__(self):
    ### personnal param
    self.trigram = 'PCH'
    # number of days to process (0 is infinite and goes to end of excel file)
    self.parse_days = 0
    self.max_date = '2050-01-01'


    ### Param excel file
    self.path  = '\\\\sw3735\\projets_nationaux\\DirectionOperations\\ExploitationClient\\Exploitation\\AdministrationH24\\Planning Support Technique n1\\'
    self.path += 'Planning STn1 - 2015.xlsx'
    self.tab_name = 'Planning STN1 2015'
    self.trigram_row = 2
    self.date_col = 3

    ### Param google api
    self.api = {}
    self.api['clientid'] = '211688405034-4v821nh068ncmaoue2of0ipmmruddoil.apps.googleusercontent.com'
    self.api['secret'] = 'FZLCSjEdMuWI8kFY8DlZS7VU'
    self.calendarName = 'Shifts'
    self.calendarGMT = '+02:00'
    #self.location = 'Bureau'
    self.location = ''
    self.use_colors = True

    ### Param shifts
    self.day_type = {
      u'P-Matin':   {'start':'07:00:00','end':'15:00:00','color':7},
      u'P-Journée': {'start':'09:30:00','end':'17:30:00','color':7},
      u'P-Soir':    {'start':'12:00:00','end':'20:00:00','color':7},
      u'F-Matin':   {'start':'07:00:00','end':'15:00:00','color':9},
      u'F-soir':    {'start':'12:00:00','end':'20:00:00','color':9},
      u'GRS-P':     {'start':'07:00:00','end':'15:00:00','color':6},
      u'GRS':       {'start':'07:00:00','end':'15:42:00','color':6},
      u'FO-1':      {'start':'07:00:00','end':'15:42:00','color':9},
      u'FO-4':      {'start':'12:18:00','end':'21:00:00','color':9},
      u'BO-1':      {'start':'07:00:00','end':'15:42:00','color':7},
      u'BO-3':      {'start':'09:00:00','end':'17:42:00','color':7},
      u'BO-4':      {'start':'12:18:00','end':'21:00:00','color':7}
    }

    
### Notes

### colour code (fr)

#  1 bleu
#  2 vert pale
#  3 violet
#  4 rose
#  5 jaune
#  6 orange
#  7 turquoise
#  8 gris
#  9 bleu azur
# 10 vert vif
# 11 rouge vif

