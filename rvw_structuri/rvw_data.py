from datetime import datetime
from datetime import date

def nowToString():
  acum = datetime.now()
  return acum.strftime("%d/%m/%Y, %H:%M:%S")

def dateToString(data):
  return data.strftime("%d/%m/%Y, %H:%M:%S")

def stringToDate(string_data):
  try:
    return datetime.utcfromtimestamp(string_data)
  except: pass
  return datetime.strptime(string_data, "%d/%m/%Y, %H:%M:%S")

def sedinta_a_trecut(data_sedinta):
  return datetime.now().time() > data_sedinta.time() and calc_date_diff_now(data_sedinta) <= 0

def calc_date_diff(date1, date2):
  delta = date2.date() - date1.date()
  return abs(delta.days)
  
def calc_date_diff_now(date1):
  delta = date1.date() - date.today()
  return delta.days

def calculate_age(born):
    born = born.date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))