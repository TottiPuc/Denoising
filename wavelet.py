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
from scikits.audiolab import wavread, wavwrite
import pywlt
import sys

filenameClean = 'a.wav'

dataIn, sample, frequency = wavread (sys.argv[1])

cleanSignal = pywlt.denoisingPUC.denoising(dataIn)

wavwrite (cleanSignal, filenameClean, sample, frequency )
