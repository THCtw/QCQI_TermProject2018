% Input number N
N = input('Number N: ');
    
% Creating identity matrix 
I = [1, 0; 0, 1];
Sz = [1, 0; 0, -1];
Sx = [0, 1; 1, 0];
I_N = I;
for i = 1:N-1 
    I_N = kron(I_N, I);
end

% Getting Hamiltonian 
H1 = zeros(2^N);
H2 = zeros(2^N);
%H1
for i = 1:N-1
    if i == 1
        temp = Sz;
    else
        temp = I;
    end
    for j = 2:N
        if j == i || j == i+1
            temp = kron(temp, Sz);
        else
            temp = kron(temp, I);
        end
    end
    H1 = H1 + temp;
end
%H2
for i = 1:N
    if i == 1
        temp = Sx;
    else
        temp = I;
    end
    for j = 2:N
        if j == i
            temp = kron(temp, Sx);
        else
            temp = kron(temp, I);
        end
    end
    H2 = H2 + temp;
end

% Diagonalization & Finding ground state
% H = -H1 - h*H2
E = zeros(1, 31);
for i = 1:31
    h = (i-1)/10;
    H = -H1 - h*H2;
    E(i) = min(eig(H));
end

%Plot 
index = 1:31;
plot ( (index-1)/10, E, 'o');