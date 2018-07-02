# Searching the smallest eigenvalue depends on theta(i)
import math
from Q_Algorithm_Spin import simu_sec_I_C

def search_Theta_i(N, theta, h, E1, E2, i, theta_i1, theta_i2):

    e1 = E1
    e2 = E2
    th1 = theta_i1
    th2 = theta_i2
    d = (e2-e1)/e1
    limit = 0.1

    # Stop searching when d < limit
    while d < limit:
        theta[i] = (th1+th2)/2
        etemp = simu_sec_I_C(N, theta, h)
        if etemp < E1:
            e2 = e1
            e1 = etemp
            th2 = th1
            th1 = theta[i]
        else:
            e2 = etemp
            th2 = theta[i]
        d = (e2-e1)/e1
    
    E = e1
    theta[i] = th1

    return E, theta