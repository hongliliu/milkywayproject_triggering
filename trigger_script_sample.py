# THIS IS THE PUBLIC VERSION OF A SCRIPT TO RUN THE CORRELATION FUNCTION COMPUTATIONS. 
# SHOWS HOW TO RUN THE CALC_CORR FUNCTIONS WITH SOME SAMPLE LINES.
# S. Kendrew, Heidelberg June 2013

# Requires Python packages: math, os, numpy, scipy, matplotlib, astropy, time, itertools, and calc_corr.py
# Tested on Python 2.6.6, should be compative with 2.7 as well.
# 

import math
import sys
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import astropy.io.ascii as ascii
from scipy import stats
from scipy import optimize
import time
import itertools 
from matplotlib import rc 

import calc_corr

plt.close('all')   

#==================================================================
def writeData(t, c, e, outFile='data/new/test.dat', bubCat='cat1', ysoCat='cat2', rSize=50, nbStrap=100):
	dFile=open(outFile, 'w')
	dFile.write('Data cats: ' + bubCat + ' / ' + ysoCat + ' ysos; rSize: ' + repr(rSize) + '; nbStrap: ' + repr(nbStrap)+ ' \n')
	dFile.write('Bin, w(theta), err_w(theta)\n')
	for i in range(0,np.size(c)):
		dFile.write('%.4f,%.4f,%.4f\n' %(t[i], c[i], e[i]))
	dFile.close()
	return 0
#===================================================================
   

#set rc params for plotting
lines={'linewidth' : 1.5, 'markeredgewidth' : 1.0, 'markersize' : 8.}#, 'markerfacecolor' : None}   
text={'usetex' : 'True'}
axes={'facecolor' : 'white', 'linewidth' : 1.0, 'titlesize' : 'medium', 'labelsize' : 'medium', 'grid' : True}
xtick={'labelsize' : 'small'}
ytick={'labelsize' : 'small'}
figure={'figsize' : [5,3.5]}  
legend={'fontsize' : 'medium'}#, 'frameon' : 'False'}
font={'family' : 'serif', 'style' : 'normal', 'size' : 12., 'serif': ['Times', 'Palatino']}
rc('lines', **lines)
rc('font', **font) 
rc('axes', **axes)
rc('xtick', **xtick)
rc('ytick', **ytick)
rc('text', **text)
rc('figure', **figure)  
rc('legend', **legend)
rc('ps', fonttype=42)  
rc('xtick.major', size=2)
rc('ytick.major', size=2)
rc('xtick.minor', size=1)
rc('ytick.minor', size=1)


#read in the official dr1-LARGE catalogue:
dr1Lfile = 'cats/mwp-bubble-lists-DR1/mwp-large-bubbles-dr1-29-02-2012.csv'
dr1Lcols = ["id","churchid","lon","lat","reff","thick","ecc","angle", "hitrate","disp","hierarchy"]
dr1L=ascii.read(dr1Lfile, delimiter=',', names=dr1Lcols, comment='#', data_start=1)   
# DR1 table lists effective diameter! but it's actually the radius.
# in 29/02 file all RADII, in arcmin
#dr1['reff']=dr1['reff']/2.
neg=dr1L['lon'] > 180.
dr1L['lon'][neg]=dr1L['lon'][neg]-360.
print '# MWP-DR1 bubbles before clipping: %i' %(np.size(dr1L)) 
clipcond =(np.abs(dr1L['lon']) >= 10.)
dr1L = dr1L[clipcond]
print '# MWP-DR1 bubbles after clipping: %i' %(np.size(dr1L)) 
# Add any additional clipping criteria here:
 
tq1=dr1L.thick >= stats.scoreatpercentile(dr1L.thick, 25.)
tq2=dr1L.thick >= stats.scoreatpercentile(dr1L.thick, 50.)
tq3=dr1L.thick >= stats.scoreatpercentile(dr1L.thick, 75.)
tq4=dr1L.thick >= stats.scoreatpercentile(dr1L.thick, 90.)

# END

# read in official dr1-SMALL catalogue:
dr1Sfile = '../catalogs/public_DR1/mwp-bubble-lists-DR1/mwp-small-bubbles-dr1-29-02-2012.csv'
dr1Scols = ["id","churchid","lon","lat","reff","hitrate","hierarchy"]
dr1S=ascii.read(dr1Sfile, delimiter=',', names=dr1Scols, data_start=1)   
neg=dr1S['lon'] > 180.
dr1S['lon'][neg]=dr1S['lon'][neg]-360.
print '# MWP-DR1 Small bubbles before clipping: %i' %(np.size(dr1S)) 
#eliminate those in |l|<10
clipcond =(np.abs(dr1S['lon']) >= 10.)
dr1S = dr1S[clipcond]
print '# MWP-DR1 Small bubbles after clipping: %i' %(np.size(dr1S)) 
# Add any additional clipping criteria here:



# END

# read in the concatenated table of SMALL+LARGE bubbles
dr1file = '../catalogs/public_DR1/mwp-bubble-lists-DR1/mwp-all-bubbles-dr1-29-02-2012.csv'
dr1cols = ["id","churchid","lon","lat","reff","thick","ecc","angle", "hitrate","disp","hierarchy"]
dr1=ascii.read(dr1file, delimiter=',', names=dr1cols, comment='#', data_start=1)   
# DR1 table lists effective diameter! but it's actually the radius - see evernote comments of 24/02
# in 29/02 file all RADII, in arcmin
neg=dr1['lon'] > 180.
dr1['lon'][neg]=dr1['lon'][neg]-360.
print '# MWP-DR1 bubbles before clipping: %i' %(np.size(dr1)) 

# the RMA survey doesn't cover |l| < 10. so exclude those bubbles as well.
clipcond =(np.abs(dr1['lon']) >= 10.)
dr1 = dr1[clipcond]
print '# MWP-DR1 bubbles after clipping: %i' %(np.size(dr1)) 
# Add any additional clipping criteria here:

# divide into quartiles according to size

rq1=dr1['reff'] >= stats.scoreatpercentile(dr1['reff'], 25.)
rq2=dr1['reff'] >= stats.scoreatpercentile(dr1['reff'], 50.)
rq3=dr1['reff'] >= stats.scoreatpercentile(dr1['reff'], 75.)
rq4=dr1['reff'] >= stats.scoreatpercentile(dr1['reff'], 90.)

# END


# Read in YSOs file.
ysofile = 'cats/rms_allyoung_full_nokda.csv'
ysocols = ['id','rmsid','name','type','rahex','dechex','flux8','flux12','flux14','flux21','jmag','hmag','kmag','vlsr','rgc','kds','d','blank','firlum','firflux','blank2','lon','lat']
ysoexc = ['id','rahex', 'dechex', 'blank', 'firflux', 'blank2']
yso = ascii.read(ysofile, delimiter=',', names=ysocols, exclude_names=ysoexc,  data_start=0)
neg = yso['lon'] > 180.
yso['lon'][neg]=yso['lon'][neg]-360. 
#trim the ? out of the types field:
yso.type[np.char.endswith(yso.type, '?')]=np.char.rstrip(yso.type, '?')
print '# YSOs before clipping: {0}' .format(np.size(yso))

# the RMS survey covers more in longitude and latitude than MWP so exclude beyond |l| = 65 and |b| = 1
coord_lim =  (np.abs(yso['lat']) <= 1.) & (np.abs(yso['lon']) <= 65.) 
yso = yso[coord_lim]
print '# YSOs after clipping: {0}' .format(np.size(yso))
# Add any additional clipping criteria here:
# do counts for the different source types:
types=np.unique(yso.type)
counts=np.zeros((len(types),3))
for i in range(0,len(types)):
	counts[i,0] = np.size(yso[yso.type == types[i]])



# the divSample function is kind of independent but I've included it in the calc_corr file.
dr1_assoc, dr1_assoc2, dr1_control = calc_corr.divSample(yso, dr1)
c06_assoc, c06_assoc2, c06_control = calc_corr.divSample(yso, c06)


#sample correlation calls, with optional data file output of the results:

# all MWP bubbles and RMS sources:
mwprms_theta, mwprms_corr, mwprms_err = calc_corr.calc_corr(dr1, yso, corrType='x', rSize=50, nbStrap=100, binStep=0.2)
x=writeData(mwprms_theta, mwprms_corr, mwprms_err, outFile='mwprms_all.dat', bubCat='dr1', ysoCat='rms', rSize=50, nbStrap=100 )

# just the large bubbles and RMS sources:
mwpLrms_theta, mwpLrms_corr, mwpLrms_err = calc_corr.calc_corr(dr1L, yso, corrType='x', rSize=50, nbStrap=100, binStep=0.2)
x=writeData(mwpLrms_theta, mwpLrms_corr, mwpLrms_err, outFile='mwpLrms.dat', bubCat='dr1L', ysoCat='rms', rSize=50, nbStrap=100 )

# RMS YSOsauto-correlations:
ysodr1_theta, ysodr1_acorr, ysodr1_err = calc_corr.calc_corr(dr1, yso, corrType='a', rSize=50, nbStrap=100, binStep=0.5)
x=writeData(ysodr1_theta, ysodr1_acorr, ysodr1_err, outFile='mwpyso_acorr_all.dat', bubCat='dr1', ysoCat='rms all', rSize=50, nbStrap=100 )

# Sample correlation function plot:
 
mwpFig = plt.figure()
plt.errorbar(mwprms_theta, mwprms_corr, yerr=mwprms_err, c='k', marker='o', ls='None', mew=1.5, mec='k', mfc='None', label='MWP all + RMS YSOs')  
plt.errorbar(mwpLrms_theta, mwpLrms_corr, yerr=mwpLrms_err, c='r', marker='x', ls='None', mew=1.5, mec='r', mfc='None', label='MWP-L + RMS YSOs')  
plt.xlabel(r'$\theta$ (R$_{\rm eff})$')
plt.ylabel(r'$w(\theta$)')
plt.legend(loc='best')
mwpFig.show()  
#plt.savefig('figs/paper/new/mwprms_corr_b100r50.eps')

