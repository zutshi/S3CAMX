function [t_arr,x_arr,D,P, prop_violated_flag] = satellite_MEE(t,T,XX,D,P,~,~,~)
format long
options = odeset('RelTol',1e-6,'AbsTol',1e-12);
prop_violated_flag = 0;
global mu J2 Re omega Cd
mu=398603.2;% earth gravitational constant (km**3/sec**2)
J2=0.00108263;
Re=6378.165;% earth equatorial radius (kilometers)
omega = 7.292115486e-5;% earth inertial rotation rate (radians/second)
Cd=2.0e-8;% coef. of atmospheric drag

t0=t;
reci0=XX(1:3);
veci0=XX(4:6);


%coordinate transformation from Cartesian state to MEE state
mee0=eci2mee(reci0, veci0);

[tt,mee]=ode45(@ode_mee, [t0 T], mee0,options);


[nt nt1]=size(tt);
reci=zeros(nt,3);
veci=zeros(nt,3);
for i=1:nt
 mee1=mee(i,:);   
[reci1 veci1]=mee2eci(mee1);
 for j=1:3
  reci(i,j)=reci1(j);
  veci(i,j)=veci1(j);
 end
end
  if(any(reci(:,1))>1250 & any(reci(:,1))<1750 & any(reci(:,2))>1350 & any(reci(:,2))<1850  & any(reci(:,3))>6500 & any(reci(:,3))<7000 )
    
  prop_violated_flag = 1;
  end

x_arr=zeros(6,1);
x_arr(1:3,1)=reci(end,:);
x_arr(4:6,1)=veci(end,:);
x_arr=x_arr';
t_arr=tt(end);


%plot3(reci(:,1),reci(:,2),reci(:,3))
%hold on

end
function [ accd ] = acc_drag( reci,veci )
% atmospheric drag
global omega Cd
% velocity vector of atmosphere relative to spacecraft
vs(1) = veci(1) + omega * reci(2);
vs(2) = veci(2) - omega * reci(1);
vs(3) = veci(3);

vrel = norm(vs);
% acceleration 
accd=zeros(3,1);
for i=1:3
accd(i) = -Cd*vs(i)/vrel;
end
end

function [accg]= acc_gravity (reci,veci)
%compute acceleration caused by J2

global mu J2 Re

radius = norm(reci);

% construct unit vectors for local horizontal frame

zhat = -reci / radius;

zdotr = zhat(3);

for i = 1:3
    
    xhat(i) = -zdotr * zhat(i);
    
end

xhat(3) = 1.0 + xhat(3);

xnorm = norm(xhat);

xhat = xhat / xnorm;

%compute gravitational acceleration in a local horizontal reference frame
% compute sin and cosine of latitude
sinphi = reci(3) / radius;
cosphi = sqrt(1.0 - sinphi^2);
P2=1/2*(3*sinphi^2-1);
dP2=3*sinphi;

% construct acceleration local horizontal n r direction 
accg_n=-mu/(radius^4)*cosphi*(Re^2)*dP2*J2;
accg_r=-mu/(radius^4)*3*(Re^2)*P2*J2;

 
 % accelerations in the eci frame
for i = 1:3
    
    ageci(i) = accg_n * xhat(i) + accg_r * zhat(i);
    
end

% compute radial frame unit vectors

[ex, ey, ez] = eci2rdl (reci, veci);

% transform eci gravity vector to mee gravity components
accg=zeros(3,1);
accg(1) = dot(ageci, ex);

accg(2) = dot(ageci, ey);

accg(3) = dot(ageci, ez);

 


end

function y = atan3 (a, b)

% four quadrant inverse tangent

% input

%  a = sine of angle
%  b = cosine of angle

% output

%  y = angle (radians; 0 =< c <= 2 * pi)

% Orbital Mechanics with MATLAB

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

epsilon = 0.0000000001;

pidiv2 = 0.5 * pi;

if (abs(a) < epsilon)
    y = (1 - sign(b)) * pidiv2;
    return;
else
    c = (2 - sign(a)) * pidiv2;
end

if (abs(b) < epsilon)
    y = c;
    return;
else
    y = c + sign(a) * sign(b) * (abs(atan(a / b)) - pidiv2);
end
end
function mee = eci2mee(reci, veci)
global mu
% convert eci state vector to
% modified equinoctial elements

% input

%  mu   = gravitational constant (km**3/sec**2)
%  reci = eci position vector (kilometers)
%  veci = eci velocity vector (kilometers/second)

% output

%  mee(1) = semiparameter (kilometers)
%  mee(2) = f equinoctial element
%  mee(3) = g equinoctial element
%  mee(4) = h equinoctial element
%  mee(5) = k equinoctial element
%  mee(6) = true longitude (radians)

% Orbital Mechanics with MATLAB

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

radius = norm(reci);

hv = cross(reci, veci);

hmag = norm(hv);

pmee = hmag^2 / mu;

rdotv = dot(reci, veci);

rzerod = rdotv / radius;

eccen = cross(veci, hv);

uhat = reci / radius;

vhat = (radius * veci - rzerod * reci) / hmag;

eccen = eccen / mu - uhat;

% unit angular momentum vector

hhat = hv / norm(hv);

% compute kmee and hmee

denom = 1.0 + hhat(3);

kmee = hhat(1) / denom;

hmee = -hhat(2) / denom;

% construct unit vectors in the equinoctial frame

fhat(1) = 1.0 - kmee^2 + hmee^2;
fhat(2) = 2.0 * kmee * hmee;
fhat(3) = -2.0 * kmee;

ghat(1) = fhat(2);
ghat(2) = 1.0 + kmee^2 - hmee^2;
ghat(3) = 2.0 * hmee;

ssqrd = 1.0 + kmee^2 + hmee^2;

% normalize

fhat = fhat / ssqrd;

ghat = ghat / ssqrd;

% compute fmee and gmee

fmee = dot(eccen, fhat);

gmee = dot(eccen, ghat);

% compute true longitude

cosl = uhat(1) + vhat(2);

sinl = uhat(2) - vhat(1);

lmee = atan3(sinl, cosl);

% load modified equinoctial orbital elements array

mee(1) = pmee;
mee(2) = fmee;
mee(3) = gmee;
mee(4) = hmee;
mee(5) = kmee;
mee(6) = lmee;


end
function [ex, ey, ez] = eci2rdl (reci, veci)
% radial frame unit vectors: ex ey ez
%  reci = eci position vector (kilometers)
%  veci = eci velocity vector (kilometers/second)



ex = reci / norm(reci);

a = cross(reci, veci);

ez = a / norm(a);

ey = cross(ez, ex);
end
function [reci veci]=mee2eci(mee)
%transformation from mee to Cartitien r,v 
global mu
eta=1+mee(2)*cos(mee(6))+mee(3)*sin(mee(6));
r=mee(1)/eta;
alpha=mee(4)^2-mee(5)^2;
ka=sqrt(mee(4)^2+mee(5)^2);
s_2=1+ka^2;
reci=[r/s_2*(cos(mee(6))+alpha*cos(mee(6))+2*mee(4)*mee(5)*sin(mee(6))); r/s_2*(sin(mee(6))-alpha*sin(mee(6))+2*mee(4)*mee(5)*cos(mee(6))); 2*r/s_2*(mee(4)*sin(mee(6))-mee(5)*cos(mee(6)))];
veci=[-1/s_2*sqrt(mu/mee(1))*(sin(mee(6))+alpha*sin(mee(6))-2*mee(4)*mee(5)*cos(mee(6))+mee(3)-2*mee(2)*mee(4)*mee(5)+alpha*mee(3)); -1/s_2*sqrt(mu/mee(1))*(-cos(mee(6))+alpha*cos(mee(6))+2*mee(4)*mee(5)*sin(mee(6))-mee(2)+2*mee(3)*mee(4)*mee(5)+alpha*mee(2)); 2/s_2*sqrt(mu/mee(1))*(mee(4)*cos(mee(6))+mee(5)*sin(mee(6))+mee(2)*mee(4)+mee(3)*mee(5))];

end
function dx = ode_mee(t, x)
global mu J2 Re

% compute eci state vector
[reci, veci] = mee2eci(x);
%compute disturbing acceleration
accg=acc_gravity (reci,veci);
accd= acc_drag( reci,veci );
ad=accg+accd;

eta=1+x(2)*cos(x(6))+x(3)*sin(x(6));
ka=sqrt(x(4)^2+x(5)^2);
s_2=1+ka^2;
A=[0 2*x(1)/eta*sqrt(x(1)/mu) 0; sqrt(x(1)/mu)*sin(x(6)) sqrt(x(1)/mu)/eta*((eta+1)*cos(x(6))+x(2)) -sqrt(x(1)/mu)*x(3)/eta*(x(4)*sin(x(6))-x(5)*cos(x(6))); -sqrt(x(1)/mu)*cos(x(6))  sqrt(x(1)/mu)/eta*((eta+1)*sin(x(6))+x(3)) sqrt(x(1)/mu)*x(2)/eta*(x(4)*sin(x(6))-x(5)*cos(x(6))); 0 0 sqrt(x(1)/mu)*s_2*cos(x(6))/2/eta; 0 0 sqrt(x(1)/mu)*s_2*sin(x(6))/2/eta; 0 0 sqrt(x(1)/mu)/eta*(x(4)*sin(x(6))-x(5)*cos(x(6)))];
b=[0;0;0;0;0;sqrt(mu*x(1))*(eta/x(1))^2];
dx=A*ad+b;
end
