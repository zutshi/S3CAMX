% Must satisfy the signature
% [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

function [tt,YY,dummy_D,dummy_P] = vanDerPol(T,XX,D,P,~)

%TODO: push odeset() in some init function
optionsODE = odeset('Refine',4,'RelTol',1e-6);

[tt,YY] = ode45(@dyn,[0 T],XX,optionsODE);
l = length(tt);
dummy_D = zeros(l, size(D,2));
dummy_P = zeros(l, size(P,2));
end

function Y = dyn(~,X,~,~)
    Y(1) = X(2);
    Y(2) = 5 * (1 - X(1)^2) * X(2) - X(1);
    Y = Y';
end