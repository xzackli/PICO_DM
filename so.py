import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
from astropy.table import Table

import fishchips

def getSO(SENS_mode, fsky_mode, deproj_mode=0, planck_fsky=0.2):
    """
    fsky_mode can be 
    0 - 0.1
    1 - 0.2
    2 - 0.4
    
    SENS_mode can be
    0 - threshold
    1 - baseline
    2 - goal
    """
    
    if fsky_mode==0: 
        fsky=0.1
        mask = '04000'
    elif fsky_mode==1: 
        fsky=0.2
        mask = '08000'
    elif fsky_mode==2: 
        fsky=0.4
        mask = '16000'
    else:
        return
        
    T_str = 'SOV3_T_default1-4-2_noisecurves_deproj'+str(deproj_mode)+\
        '_SENS' + str(SENS_mode) + \
        '_mask_' +mask+ '_ell_TT_yy.txt'
    E_str = 'SOV3_pol_default1-4-2_noisecurves_deproj'+str(deproj_mode)+\
        '_SENS' + str(SENS_mode) + \
        '_mask_' +mask+ '_ell_EE_BB.txt'
    k_str = 'Apr17_mv_nlkk_deproj' + str(deproj_mode)+\
        '_SENS' + str(SENS_mode) + \
        '_fsky_' + mask + '_iterOn.csv'
    

    dataT = Table.read('data/hill_nlkk/TT_primary/' + T_str,
                format='ascii.fast_no_header', 
               names=['ell', 'NlTT', 'Nlyy'])
    dataE = Table.read('data/hill_nlkk/EE_BB/' + E_str,
                format='ascii.fast_no_header', 
               names=['ell', 'NlEE', 'NlBB'])
    datak = Table.read('data/WgMV/' + k_str, 
           format='ascii', names=['ell', 'Nlkk'])
    
#     print(datak)
#     assert 1==0
    
    l_max = 5000
    dataT = dataT[dataT['ell'] < l_max+1]
    dataE = dataE[dataE['ell'] < l_max+1]
    datak = datak[datak['ell'] < l_max+1]
    
    primary = fishchips.experiments.CMB_Primary(theta_fwhm=1e8, sigma_T=1e8, sigma_P=1.4e8, f_sky=fsky, l_min=100, l_max=l_max)
    lensing = fishchips.cmb_lensing.CMB_Lensing_Only(lens_beam=1e8, lens_f_sky=fsky, lens_noiseT=1.0e8,
                           lens_noiseP=1e8, lens_pellmax = 4000,lens_kmax = 3000)
    
    
    for ell_temp, NlTT_temp in zip(dataT['ell'].astype(int), dataT['NlTT'] ): 
        primary.noise_T[ell_temp] = NlTT_temp
    for ell_temp, NlEE_temp in zip(dataE['ell'].astype(int), dataE['NlEE'] ): 
        primary.noise_P[ell_temp] = NlEE_temp
        
    lensing.noise_k = np.ones(3000) * 1e100
    for ell_temp, kk_temp in zip(datak['ell'].astype(int), datak['Nlkk'] ): 
        lensing.noise_k[ell_temp] = kk_temp
        
    # now the Planck combinations
    lowHFI = fishchips.experiments.CMB_Primary(
                          theta_fwhm=[ 10, 7, 5, 5], 
                           sigma_T = [65, 43,66,200],
                           sigma_P = [103,81,134,406],
                           f_sky = 0.8,
                           l_min = 2,
                           l_max = 30)
    
    planckTEB = fishchips.experiments.CMB_Primary(
                           theta_fwhm=[33,    23,  14,  10, 7, 5, 5], 
                           sigma_T = [145,  149,  137,65, 43,66,200],
                           sigma_P = [1e100,1e100,450,103,81,134,406],
                           f_sky = planck_fsky,
                           l_min = 30,
                           l_max = 2500)
    print('planck fsky', planck_fsky)
    return [primary,lensing,planckTEB,lowHFI]