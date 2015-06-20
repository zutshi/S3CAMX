function [tt,YY,dummy1,dummy2] = vanDerPol(T,XX,~,~)
dummy1 = [];
dummy2 = [];
%TODO: push odeset() in some init function
optionsODE = odeset('Refine',4,'RelTol',1e-6);

[tt,YY] = ode45(@dyn,[0 T],XX,optionsODE);

end

function Y = dyn(~,X,~,~)
    Y(1) = X(2);
    Y(2) = 5 * (1 - X(1)^2) * X(2) - X(1);
    Y = Y';
end