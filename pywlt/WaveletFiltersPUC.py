#!user/bin/even python
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
import filterDaubechiesPUC
import functionPUC
from wavepy import filter

__all__=["NumberFilter", "FiltersList"]

def NumberFilter(W):

	F = filterDaubechiesPUC.filtros (W)

###################   applying filters to the orthogonality  ########################################
#####################################################################################################
	(Lo_D, Hi_D, Lo_R, Hi_R) = functionPUC.orthfilter (F)
	return (Lo_D, Hi_D)

def FiltersList(W):
	[lpd,hpd,lpr,hpr]=filter.filtcoef(W)
	len_lpfilt=int(len(lpd))
	len_hpfilt=int(len(hpd))
	lf=len_lpfilt
	D=int(2)
	return (lpd, hpd)
