#!/user/bin/env python
# coding: utf-8
'''
################################################
#==============================================#
##### Christian Dayan Arcos Gordillo  ##########
#####       Reconhecimento de voz      #########
#####     christian@cetuc.puc-rio.br    ########
#######       CETUC - PUC - RIO       ##########
#==============================================#
################################################
'''
##########################   importing modules   ##########################
###########################################################################
import pywt
from scikits.audiolab import wavread, wavwrite 
import numpy as np
import math
import pywlt
import pylab

waveFile = 'x.wav'
filename = 'luna_2.wav'
Numero_levels = 5
wavelet = 'db10'
levels_denoise = [1,2,3,4,5,6]
mode = 'sym'
softhreshold =1
data, sample, frequency = wavread (waveFile)


dec = pywlt.multilevelPUC.wavedec(data, wavelet, mode, Numero_levels)

lDes = [0]*(Numero_levels+2)
        
s = len (data)
  
lDes[-1] = int(s) 
  
print "decomposition:"
  
cA =  "cA%d:" % (len(dec) - 1)
cAd = ' '.join([("%.3f" % val) for val in dec[0]])
lDes[0] = int (len(dec[0]))
  
for i, d in enumerate(dec[1:]):
    cD = "cD%d:" % (len(dec) - 1 - i)
    lDes[i+1] = int (len(d))
    cDd =  ' '.join([("%.3f" % val) for val in d])

################################################################################################################
####################################   Starting denoising   ####################################################

LevelEndIndex = 0

for i in xrange(len(levels_denoise)):
    LevelStartIndex = LevelEndIndex  
    LevelEndIndex = LevelStartIndex + lDes[i] 
    
    if i != len(levels_denoise):
        levelCoefficients = dec [i]
        ####################################################################################
        ##################### calculate median and edges ###################################
	lenborda = int(len(levelCoefficients)*0.2)
	borda1 = levelCoefficients[0 : lenborda]
	borda2 = levelCoefficients[-lenborda :]
	center = levelCoefficients[lenborda : -lenborda]
        g1 = map(abs, borda1)
        s1 = np.median(g1)/0.6745
        n1 = len(borda1)
        
        Thresholdborda1 = 0.05 * s1 * math.sqrt(math.log(n1))

	g2 = map(abs, center)
        s2 = np.median(g2)/0.6745
        n2 = len(center)

        Thresholdcenter = 0.2 * s2 * math.sqrt(math.log(n2))

	g3 = map(abs, borda2)
        s3 = np.median(g3)/0.6745
        n3 = len(borda2)

        Thresholdborda2 = 0.05 * s3 * math.sqrt(math.log(n3))


        ###########################################################################
        ########################  soft Thresholding function ######################
        
        if softhreshold ==1:
            newLevelCoefficientsborda1 = pywlt.functionPUC.softThresholding (borda1 , Thresholdborda1)

            newLevelCoefficientscenter = pywlt.functionPUC.softThresholding (center , Thresholdcenter)

            newLevelCoefficientsborda2 = pywlt.functionPUC.softThresholding (borda2 , Thresholdborda2)

        else:
            print ("função threshol não escolhida")
        
        ############################################################################
        ##################  reconstrução novos coeficientes  #######################
        
	newLevelCoefficientsEnd = []
	newLevelCoefficientsEnd.extend(newLevelCoefficientsborda1)
        newLevelCoefficientsEnd.extend(newLevelCoefficientscenter)
        newLevelCoefficientsEnd.extend(newLevelCoefficientsborda2)

        dec [i] = np.array (newLevelCoefficientsEnd)



print
print "reconstruction:"
  
DenoiseSignal = pywlt.multilevelPUC.waverec(dec, wavelet, mode)

wavwrite (DenoiseSignal, filename, sample, frequency )

