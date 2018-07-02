from Q_Algorithm_Spin import simu_sec_I_C
from Search_Theta_i import search_Theta_i
import math

# Initialization (N, Theta, h)
N = int(input("Number N: "))
print("N = %i\n" %N)
Theta = 0.0
theta = [Theta] * N
print(theta)
h = 0

# Calculating theta(i)=0
E1 = 0.0    # Smallest eigenvalue
E2 = 0.0    # Second small eigenvalue
E1 = simu_sec_I_C(N, theta, h)

# Searching the smallest eigenvalue theta(i) one by one
theta_i = [0.0]
for i in range(2**N-1):
    theta_i.append( (i+1)*2*math.pi/(2**N) )
# Searching theta(i) one by one for the smallest eigenvalue
for i in range(N):
    tempTheta_i1 = 0.0
    tempTheta_i2 = 0.0
    for j in range(2**N):
        theta[i] = theta_i[j]
        temp = simu_sec_I_C(N, theta, h)
        if temp < E1:
            E2 = E1
            E1 = temp
            tempTheta_i2 = tempTheta_i1
            tempTheta_i1 = theta[i]
    #E1, theta[i] = search_Theta_i(N, theta, h, E1, E2, i, tempTheta_i1, tempTheta_i2)

# Result
print ("The ground state energy is: %f\n" %E1)
print ("Theta of every qubit: \n")
print (theta)