

X = [2689.06, 2726.88, 6049.935, -6.53545, -1.16479, 3.40109];
t = 0;
delta_t = 50;
T = delta_t;
D = 0;
I = 0;
P = 0;
pc = 0;
U = 0;
XX = X;
tt = t;

for i = t:delta_t:8000
    [t_,X_,~,~, prop_violated_flag] = satellite_MEE(t,T,X,D,P,U,I,pc,1);
    X = X_(end, :);
    t = t + delta_t;
    T = T + delta_t;
    XX = [XX; X_];
    tt = [tt; t_];
end

plot(XX(:,1), XX(:,2))
plot3(XX(:,1), XX(:,2), XX(:,3))