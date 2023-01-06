roluri=[
  [1,"Voluntar","Voluntar", 885],
  [2,"Media","Media", 218],
  [2,"Mecanic","Mecanic", 937],
  [2,"Programator","Programator", 205],
  [2,"Designer","Designer", 186],
  [2,"Alumni","Alumni", 926],
  [3,"Responsabil_Designer","Designer", 186],
  [3,"Responsabil_Mecanic","Mecanic", 937],
  [3,"Responsabil_Programator","Programator", 205],
  [4,"Mentor","Mentor", 183],
  [4,"Responsabil_Alumni","Alumni", 926],
  [5,"Responsabil_Media","Media", 218],
  [100,"Minutz","Programator/ Team leader", 205]
]

def getRolByDisp(disp):
  for rol in roluri:
    if rol[1] == disp:
      return rol
  return roluri[0]