function [tt,YY,D,P,prop_violated_flag] = sample_plant(t,T,XX,D,P,U,I,property_check)

[tt,YY] = ode45(@dyn, [t,T], XX);

prop_violated_flag = 0;
if YY(1) >= 10.0 && YY(1) <= 11.0
  prop_violated_flag = 1;
end

end

function y = dyn(t, x)
    y(1) = 1;
end
