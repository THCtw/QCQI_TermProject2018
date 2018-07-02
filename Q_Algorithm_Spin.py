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
    print(result.get_counts(circuit))

    deltaPi=[0.0]*2*n
    total = 0
    for i in result.get_counts(circuit):
        total = total+result.get_counts(circuit)[i]
        for j in range(2*n):
            r = list(i)
            r.reverse()
            if r[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result.get_counts(circuit)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result.get_counts(circuit)[i])
            
    Ej = 0.0

    for i in range(n-1):
        Ej = Ej - ( (deltaPi[i]/total) * (deltaPi[i+1]/total) )
    
    Ej=Ej - ( (deltaPi[0]/total) * (deltaPi[n-1]/total) )
    for i in range(n, 2*n):
        Ej=Ej-(deltaPi[i]*h/total)
    return Ej/4
#print(simu_sec_I_C(4,[3,.15,1,3.1],3))


def simu_fir_I_C(n, theta,h):
    #import math
    #import sys, time, getpass
    #from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
    #from qiskit import available_backends, execute, register, get_backend

    k = range(n)
    q = QuantumRegister(n)
    c = ClassicalRegister(2*n)

    circuit = QuantumCircuit(q, c)

    for i in k:
        circuit.u3(theta[i],0,0,q[i])

    for i in k:
        circuit.barrier(q[i])

    for i in k:
        circuit.measure(q[i],c[i])
    
    circuit.reset(q)

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
            r = list(i)
            r.reverse()
            if r[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result.get_counts(circuit)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result.get_counts(circuit)[i])
            
    Ej = 0.0

    for i in range(n-1):
        Ej = Ej - ( (deltaPi[i]/total) * (deltaPi[i+1]/total) ) 
    
    Ej=Ej - ( (deltaPi[0]/total) * (deltaPi[n-1]/total)  )

    for i in range(n, 2*n):
        Ej=Ej-(deltaPi[i]*h/total)

    return Ej/4

def ibm_sec_I_C(n, theta, h):
    #import math
    #import sys, time, getpass
    #from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
    #from qiskit import available_backends, execute, register, get_backend
    #import Qconfig
    try:
        sys.path.append("../../") # go to parent dir
        qx_config = {
            "APItoken": Qconfig.APItoken,
            "url": Qconfig.config['url']}
        print('Qconfig loaded from %s.' % Qconfig.__file__)
    except:
        APItoken = getpass.getpass('Please input your token and hit enter: ')
        qx_config = {
            "APItoken": APItoken,
            "url":"https://quantumexperience.ng.bluemix.net/api"}
        print('Qconfig.py not found in qiskit-tutorial directory; Qconfig loaded using user input.')

    #quantum circuit
    k = range(n)
    f = range(1,n)
    q = QuantumRegister(n)
    c1 = ClassicalRegister(n)
    c2 = ClassicalRegister(n)
    circuit1 = QuantumCircuit(q, c1)
    circuit2 = QuantumCircuit(q, c2)
    thetafix = math.pi/6
    phifix = math.pi/2
    #circuit1
    circuit1.u3(thetafix, phifix, 0, q[0])

    for i in f:
        circuit1.cx(q[0], q[i])
    
    for i in k:
        circuit1.u3(theta[i],0,0,q[i])

    for i in k:
        circuit1.barrier(q[i])

    for i in k:
        circuit1.measure(q[i],c1[i])
    
    register(qx_config['APItoken'], qx_config['url'])
    def lowest_pending_jobs():
        """Returns the backend with lowest pending jobs."""
        list_of_backends = available_backends(
            {'local': False, 'simulator': False})
        device_status = [get_backend(backend).status
                for backend in list_of_backends]

        best = min([x for x in device_status if x['available'] is True],
            key=lambda x: x['pending_jobs'])
        return best['name']
    backend = lowest_pending_jobs()
    print("the best backend is " + backend)
    shots = 1024           # Number of shots to run the program (experiment); maximum is 8192 shots.
    max_credits = 3          # Maximum number of credits to spend on executions. 
    job_exp = execute(circuit1, backend=backend, shots=shots, max_credits=max_credits)
    lapse = 0
    interval = 10
    while not job_exp.done:
        print('Status @ {} seconds'.format(interval * lapse))
        print(job_exp.status)
        time.sleep(interval)
        lapse += 1
    print(job_exp.status)
    result_real = job_exp.result()
    result_real.get_counts(circuit1)

    #jobID = job_exp.job_id
    #print('JOB ID: {}'.format(jobID))
    #jobID
    result_real.get_counts(circuit1)
    deltaPi=[0.0]*n
    total = 0
    for i in result_real.get_counts(circuit1):
        total = total+result_real.get_counts(circuit1)[i]
        for j in range(n):
            r = list(i)
            r.reverse()
            if r[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result_real.get_counts(circuit1)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result_real.get_counts(circuit1)[i])
            
    Ej = 0.0

    for i in range(n-1):
        Ej = Ej - ( (deltaPi[i]/total) * (deltaPi[i+1]/total) )
    
    Ej=Ej - ( (deltaPi[0]/total) * (deltaPi[n-1]/total) )

    #circuit2

    circuit2.u3(thetafix, phifix, 0, q[0])

    for i in f:
        circuit2.cx(q[0], q[i])

    for i in k:
        circuit2.u3(theta[i],0,0,q[i])

    for i in k:
        circuit2.barrier(q[i])

    for i in k:
        circuit2.h(q[i])

    for i in k:
        circuit2.measure(q[i],c2[i])

    job_exp = execute(circuit2, backend=backend, shots=shots, max_credits=max_credits)
    lapse = 0
    while not job_exp.done:
        print('Status @ {} seconds'.format(interval * lapse))
        print(job_exp.status)
        time.sleep(interval)
        lapse += 1
    print(job_exp.status)
    result_real = job_exp.result()
    result_real.get_counts(circuit2)

    for i in result_real.get_counts(circuit2):
        total = total+result_real.get_counts(circuit2)[i]
        for j in range(n):
            r = list(i)
            r.reverse()
            if i[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result_real.get_counts(circuit2)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result_real.get_counts(circuit2)[i])


    for i in range(n):
        Ej=Ej-(deltaPi[i]*h/total)
    
    return Ej/4

def ibm_fir_I_C(n, theta, h):
    #import math
    #import sys, time, getpass
    #from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
    #from qiskit import available_backends, execute, register, get_backend
    #import Qconfig
    try:
        sys.path.append("../../") # go to parent dir
        qx_config = {
            "APItoken": Qconfig.APItoken,
            "url": Qconfig.config['url']}
        print('Qconfig loaded from %s.' % Qconfig.__file__)
    except:
        APItoken = getpass.getpass('Please input your token and hit enter: ')
        qx_config = {
            "APItoken": APItoken,
            "url":"https://quantumexperience.ng.bluemix.net/api"}
        print('Qconfig.py not found in qiskit-tutorial directory; Qconfig loaded using user input.')

    #quantum circuit
    k = range(n)
    q = QuantumRegister(n)
    c1 = ClassicalRegister(n)
    c2 = ClassicalRegister(n)
    circuit1 = QuantumCircuit(q, c1)
    circuit2 = QuantumCircuit(q, c2)
    thetafix = math.pi/6
    phifix = math.pi/2
    #circuit1   

    for i in k:
        circuit1.u3(theta[i],0,0,q[i])

    for i in k:
        circuit1.barrier(q[i])

    for i in k:
        circuit1.measure(q[i],c1[i])
    
    register(qx_config['APItoken'], qx_config['url'])
    def lowest_pending_jobs():
        """Returns the backend with lowest pending jobs."""
        list_of_backends = available_backends(
            {'local': False, 'simulator': False})
        device_status = [get_backend(backend).status
                for backend in list_of_backends]

        best = min([x for x in device_status if x['available'] is True],
            key=lambda x: x['pending_jobs'])
        return best['name']
    backend = lowest_pending_jobs()
    print("the best backend is " + backend)
    shots = 1024           # Number of shots to run the program (experiment); maximum is 8192 shots.
    max_credits = 3          # Maximum number of credits to spend on executions. 
    job_exp = execute(circuit1, backend=backend, shots=shots, max_credits=max_credits)
    lapse = 0
    interval = 10
    while not job_exp.done:
        print('Status @ {} seconds'.format(interval * lapse))
        print(job_exp.status)
        time.sleep(interval)
        lapse += 1
    print(job_exp.status)
    result_real = job_exp.result()
    result_real.get_counts(circuit1)

    #jobID = job_exp.job_id
    #print('JOB ID: {}'.format(jobID))
    #jobID
    result_real.get_counts(circuit1)
    deltaPi=[0.0]*n
    total = 0
    for i in result_real.get_counts(circuit1):
        total = total+result_real.get_counts(circuit1)[i]
        for j in range(n):
            r = list(i)
            r.reverse()
            if r[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result_real.get_counts(circuit1)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result_real.get_counts(circuit1)[i])
            
    Ej = 0.0

    for i in range(n-1):
        Ej = Ej - ( (deltaPi[i]/total) * (deltaPi[i+1]/total) )
    
    Ej=Ej - ( (deltaPi[0]/total) * (deltaPi[n-1]/total) )

    #circuit2
    
    for i in k:
        circuit2.u3(theta[i],0,0,q[i])

    for i in k:
        circuit2.barrier(q[i])

    for i in k:
        circuit2.h(q[i])

    for i in k:
        circuit2.measure(q[i],c2[i])

    job_exp = execute(circuit2, backend=backend, shots=shots, max_credits=max_credits)
    lapse = 0
    while not job_exp.done:
        print('Status @ {} seconds'.format(interval * lapse))
        print(job_exp.status)
        time.sleep(interval)
        lapse += 1
    print(job_exp.status)
    result_real = job_exp.result()
    result_real.get_counts(circuit2)

    for i in result_real.get_counts(circuit2):
        total = total+result_real.get_counts(circuit2)[i]
        for j in range(n):
            r = list(i)
            r.reverse()
            if i[j]=='1':
                deltaPi[j]=deltaPi[j]-float(result_real.get_counts(circuit2)[i])
            else:
                deltaPi[j]=deltaPi[j]+float(result_real.get_counts(circuit2)[i])


    for i in range(n):
        Ej=Ej-(deltaPi[i]*h/total)
    
    return Ej/4
