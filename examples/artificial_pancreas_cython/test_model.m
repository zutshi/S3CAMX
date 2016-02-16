% Runs the simulator and plots the traces for a sanity check.

figure(1)

X = [100,90,0];
D = [720 0 40 zeros(1,21)];
delta_t = 10;

YY = X;
tt = 0;
T = delta_t;
t = 0;
U = 0;
P = 0;
for i = 0:delta_t:720
    pi = 10;
%     function [tt,YY,D_,P_,prop_violated_flag] = artificial_pancreas(t_start,T_end,XX,D,P,U,I,property_check)
    [t_,X,D_,P_,prop_violated_flag] = artificial_pancreas(t,T,X,D,P,U,pi,0);
    D = D_;
    P = P_;
    t = t + delta_t;
    T = T + delta_t;
    YY = [YY;X];
    tt = [tt;t_];
end

plot(tt,YY(:,1));