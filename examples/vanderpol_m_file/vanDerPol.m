% Must satisfy the signature
% [t,X,D,P] = sim_function(T,X0,D0,P0,I0);

% def sim(TT, XX, D, P, U, I, property_checker, property_violated_flag):
function [tt,YY,D,P,prop_violated_flag] = vanDerPol(t,T,XX,D,P,U,I,property_check)

error_set = [-1, -6.5; -0.7, -5.6]
prop_violated_flag = 0;

%TODO: push odeset() in some init function
optionsODE = odeset('Refine',4,'RelTol',1e-6);

[tt,YY] = ode45(@dyn,[0 T-t],XX,optionsODE);
l = length(tt);

% dummy_D = zeros(l, size(D,2));
% dummy_P = zeros(l, size(P,2));
D = D;
P = P;
% x(find(all(x >= repmat(es(1,:),rows,1) & x <= repmat(es(2,:),rows,1), 2)),:)
if property_check == 1
    n = size(YY,1);
    idx_list = find(all(YY >= repmat(error_set(1,:),n,1) & YY <= repmat(error_set(2,:),n,1), 2));
    if length(idx_list) > 0
        prop_violated_flag = 1;
        first_violation_idx = idx_list(1);
        YY = YY(1:first_violation_idx,:);
        tt = tt(1:first_violation_idx,:);
    end
end
tt = tt + repmat(t,size(tt,1),1);
end

function Y = dyn(~,X,~,~)
    Y(1) = X(2);
    Y(2) = 5 * (1 - X(1)^2) * X(2) - X(1);
    Y = Y';
end
