# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 04:51:55 2018

@author: Hornyt0x
"""

import numpy as np

def geo_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
    
    
    
if( __name__ == '__main__'):
    print(geo_distance( -32.2981, -59.1394, -32.4833, -58.2283))