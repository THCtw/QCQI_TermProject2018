def simu_sec_I_C(n,theta,h):
    import math
    import sys, time, getpass
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
    from qiskit import available_backends, execute, register, get_backend
    k = range(n)
    f = range(1,n)
    q = QuantumRegister(n)
    c = ClassicalRegister(2*n)


    thetafix = math.pi/6
    phifix = math.pi/2

    circuit = QuantumCircuit(q, c)

    circuit.u3(thetafix, phifix, 0, q[0])

    for i in f:
        circuit.cx(q[0], q[i])

    for i in k:
        circuit.u3(theta[i],0,0,q[i])

    for i in k:
        circuit.barrier(q[i])

    for i in k:
        circuit.measure(q[i],c[i])
    
    circuit.reset(q)

    circuit.u3(thetafix, phifix, 0, q[0])

    for i in f:
        circuit.cx(q[0], q[i])

    for i in k:
        circuit.u3(theta[i],0,0,q[i])

    for i in k:
        circuit.barrier(q[i])

    for i in k:
        circuit.h(q[i])

    for i in k:
        circuit.measure(q[i],c[i+n])
    
    # QASM from a program

    #QASM_source = circuit.qasm()

    #print(QASM_source)
    backend = 'local_qasm_simulator' 
    job = execute(circuit, backend)
    job.status
    result = job.result()
    result.get_counts(circuit)

    deltaPi=[0.0]*2*n
    total = 0
    for i in result.get_counts(circuit):
        total = total+result.get_counts(circuit)[i]
        for j in range(2*n):
            if i[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result.get_counts(circuit)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result.get_counts(circuit)[i])
            
    Ej = 0.0

    for i in range(n-1):
        Ej = Ej-(deltaPi[i]*deltaPi[i+1]/(total^2))
    
    Ej=Ej-(deltaPi[0]*deltaPi[n-1]/(total^2))

    for i in range(n, 2*n):
        Ej=Ej-(2*deltaPi[i]*h/total)
    #To have the same number with paper
    Ej=Ej/4
    return Ej
