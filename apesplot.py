'''
This script is to plot the excited-state adiabatic potential energy surface
based on ORCA SCAN-TDDFT calculation.
coding:UTF-8
env:vis2c
'''

from numpy import linspace
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

nm2eV = 1239.84
har2eV = 27.2113863
nstat  = 5    # number of excited states, same as TD(nstates)
nscan  = 21   # number of scan points
xlabel = 'C-S Length / Angstrom'     # might be bond length or sth
ylabel = 'Electronic Energy / eV'
count = linspace(1.7, 2.7, nscan)      # linspace(start, end, nscan)
count_smooth = linspace(1.7, 2.7, 100) # linspace(start, end, nscan)
diabaticlow = [[]]
labeldiabaticlow = []
colordiabaticlow = []
diabaticmid = [[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]]
labeldiabaticmid = ['D4 diabatic state']
colordiabaticmid = ['#005b23']
diabatichigh = [[]]
labeldiabatichigh = []
colordiabatichigh = []
nmlines = [390]    # axhline in nm

# determine the possible excited state spin multiplicity
# using the Wigner-Eckart theorem
with open('0001.out', 'r') as f:
  while True:
    line = f.readline()
    if not line:
      break
    if line.find('Multiplicity =') != -1:
      spin = int(line.split()[5])
      break
colorgs = "#0F0F0F"
ESmid = [[] for _ in range(nscan)]
S2mid = 0.5*float(spin-1)*(0.5*float(spin-1)+1.0)
colormid = '#005ba0'
EShigh = [[] for _ in range(nscan)]
S2high = 0.5*float(spin+1)*(0.5*float(spin+1)+1.0)
colorhigh = '#00978d'
if spin == 1 or spin == 2:
  ESlow = [[] for _ in range(nscan)]
  S2low = 0.5*float(spin-3)*(0.5*float(spin-3)+1.0)
  colorlow = '#BF1D2D'
if spin == 1:
  labelmid = 'single adiabatic state'
  labelhigh = 'triplet adiabatic state'
elif spin == 2:
  labelmid = 'doublet adiabatic state'
  labelhigh = 'quartet adiabatic state'
elif spin == 3:
  labellow = 'singlet adiabatic state'
  labelmid = 'triplet adiabatic state'
  labelhigh = 'quintet adiabatic state'
elif spin == 4:
  labellow = 'doublet adiabatic state'
  labelmid = 'quartet adiabatic state'
  labelhigh = 'sextet adiabatic state'
elif spin == 5:
  labellow = 'triplet adiabatic state'
  labelmid = 'quintet adiabatic state'
  labelhigh = 'septet adiabatic state'
elif spin == 6:
  labellow = 'quartet adiabatic state'
  labelmid = 'sextet adiabatic state'
  labelhigh = 'octet adiabatic state'
elif spin == 7:
  labellow = 'quintet adiabatic state'
  labelmid = 'septet adiabatic state'
  labelhigh = 'nonet adiabatic state'
elif spin == 8:
  labellow = 'sextet adiabatic state'
  labelmid = 'octet adiabatic state'
  labelhigh = 'decuplet adiabatic state'
labelgs = 'ground state'
# characterization of ground states
GS = []
j = 1
while j <= nscan:
  if len(str(j)) == 1:
    filename = '000' + str(j) + '.out'
  elif len(str(j)) == 2:
    filename = '00' + str(j) + '.out'
  elif len(str(j)) == 3:
    filename = '0' + str(j) + '.out'
  try:
    with open(filename,'r') as f:
      while True:
        line = f.readline()
        if not line:
          break
        if line.startswith('Total Energy       :'):
          break
  except FileNotFoundError:
    exit("can't find output file, check nscan")
  # set the ground state energy of the first point to zero
  if j == 1:
    ZERO = float(line.split()[3])
  GS.append((float(line.split()[3])-ZERO)*har2eV)
  j += 1

# characterization of excited states
i = 1
while i <= nstat:
  j = 1
  while j <= nscan:
    if len(str(j)) == 1:
      filename = '000' + str(j) + '.out'
    elif len(str(j)) == 2:
      filename = '00' + str(j) + '.out'
    elif len(str(j)) == 3:
      filename = '0' + str(j) + '.out'
    try:
      with open(filename,'r') as f:
        while True:
          line = f.readline()
          if not line:
            break
          if line.startswith('STATE  '+str(i)):
            break
    except FileNotFoundError:
      exit("can't find output file, check nscan")
    S2 = float(line[line.find('<S**2> =')+11:line.find('<S**2> =')+18])
    if spin == 1 or spin == 2:
      if abs(S2-S2high) < abs(S2-S2mid):
        EShigh[j-1].append(float(line[line.find('eV')-6:line.find('eV')-2])+\
                           GS[j-1])
      else:
        ESmid[j-1].append(float(line[line.find('eV')-6:line.find('eV')-2])+\
                           GS[j-1])
    else:
      if abs(S2-S2high) < abs(S2-S2mid) and abs(S2-S2high) < abs(S2-S2low):
        EShigh[j-1].append(float(line[line.find('eV')-6:line.find('eV')-2])+\
                           GS[j-1])
      elif abs(S2-S2mid) < abs(S2-S2high) and abs(S2-S2mid) < abs(S2-S2low):
        ESmid[j-1].append(float(line[line.find('eV')-6:line.find('eV')-2])+\
                           GS[j-1])
      else:
        ESlow[j-1].append(float(line[line.find('eV')-6:line.find('eV')-2])+\
                          GS[j-1])
    j += 1
  i += 1

# plot GS
GS_smooth = make_interp_spline(count, GS)(count_smooth)
plt.plot(count_smooth, GS_smooth, linewidth=2, color=colorgs)
# plot ESmid
midmin = len(ESmid[0])
for i in range(nscan):
  if len(ESmid[i]) < midmin:
    midmin = len(ESmid[i])
print(f'totally {midmin} {labelmid} PESs')
if midmin != 0:
  for i in range(midmin):
    ES = []
    for j in range(nscan):
      ES.append(ESmid[j][i])
    ES_smooth = make_interp_spline(count, ES)(count_smooth)
    plt.plot(count_smooth,ES_smooth,linewidth=2,color=colormid)
# plot EShigh
highmin = len(EShigh[0])
for i in range(nscan):
  if len(EShigh[i]) < highmin:
    highmin = len(EShigh[i])
print(f'totally {highmin} {labelhigh} PESs')
if highmin != 0:
  for i in range(highmin):
    ES = []
    for j in range(nscan):
      ES.append(EShigh[j][i])
    ES_smooth = make_interp_spline(count, ES)(count_smooth)
    plt.plot(count_smooth,ES_smooth,linewidth=2,color=colorhigh)
if spin != 1 and spin != 2:
  # plot ESlow
  lowmin = len(ESlow[0])
  for i in range(nscan):
    if len(ESlow[i]) < lowmin:
      lowmin = len(ESlow[i])
  print(f'totally {lowmin} {labellow} PESs')
  if lowmin != 0:
    for i in range(lowmin):
      ES = []
      for j in range(nscan):
        ES.append(ESlow[j][i])
      ES_smooth = make_interp_spline(count, ES)(count_smooth)
      plt.plot(count_smooth,ES_smooth,linewidth=2,color=colorlow)
if spin == 1 or spin == 2:
  if highmin != 0:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid),
      Line2D([0], [0], color=colorhigh, lw=2, label=labelhigh)
    ]
  else:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid)
    ]
else:
  if highmin != 0 and lowmin != 0:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colorlow, lw=2, label=labellow),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid),
      Line2D([0], [0], color=colorhigh, lw=2, label=labelhigh)
    ]
  elif highmin != 0 and lowmin == 0:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid),
      Line2D([0], [0], color=colorhigh, lw=2, label=labelhigh)
    ]
  elif highmin == 0 and lowmin != 0:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colorlow, lw=2, label=labellow),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid)
    ]
  else:
    legend_handles = [
      Line2D([0], [0], color=colorgs, lw=2, label=labelgs),
      Line2D([0], [0], color=colormid, lw=2, label=labelmid)
    ]

# plot diabatic states
if len(diabaticlow[0]) != 0:
  for i in range(len(diabaticlow)):
    DES = []
    for j in range(len(diabaticlow[i])):
      DES.append(ESlow[j][diabaticlow[i][j]-1])
    DES_smooth = make_interp_spline(count, DES)(count_smooth)
    plt.plot(count_smooth,DES_smooth,linewidth=2,\
             color=colordiabaticlow[i],label=labeldiabaticlow[i])
if len(diabaticmid[0]) != 0:
  for i in range(len(diabaticmid)):
    DES = []
    for j in range(len(diabaticmid[i])):
      DES.append(ESmid[j][diabaticmid[i][j]-1])
    DES_smooth = make_interp_spline(count, DES)(count_smooth)
    plt.plot(count_smooth,DES_smooth,linewidth=2,\
             color=colordiabaticmid[i],label=labeldiabaticmid[i])
if len(diabatichigh[0]) != 0:
  for i in range(len(diabatichigh)):
    DES = []
    for j in range(len(diabatichigh[i])):
      DES.append(EShigh[j][diabatichigh[i][j]-1])
    DES_smooth = make_interp_spline(count, DES)(count_smooth)
    plt.plot(count_smooth,DES_smooth,linewidth=2,\
             color=colordiabatichigh[i],label=labeldiabatichigh[i])

# plot axhline
if len(nmlines) != 0:
  for i in range(len(nmlines)):
    plt.axhline(y=nm2eV/nmlines[i], linestyle='--', linewidth=1.0, color='k')
    plt.text(min(count),nm2eV/nmlines[i]-0.15,f'{nmlines[i]}nm',va='center',ha='left')
ax = plt.gca()
existing_handles, existing_labels = ax.get_legend_handles_labels()
all_handles = legend_handles + existing_handles
plt.legend(handles=all_handles)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.show()