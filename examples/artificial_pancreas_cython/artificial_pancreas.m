%[t_arr,X_arr,D_arr,P_arr,prop_violated_flag] = sim_function(t0,t0+T,X0,D0,P0,U0,I0,property_check);

function [tt,YY,D_,P_,prop_violated_flag] = artificial_pancreas(t_start,T_end,XX,D,P,U,I,property_check)

inps = [
    29.4881
    249.3545
    295.7785
    1.2403
    -5.1326
    0.0077
    14.7322
    0.003
    0.9654
    53.0687
    155.6477
    ];

prop_violated_flag = 0;

totTime = D(1);
% t_start
% T_end

% Time Elapsed; cumulated
timeElapsed = D(2);

% Update time elapsed for the next iteration
D(2) = D(2)+(T_end-t_start);

%Controller Start Time
D(3) = inps(10,1);

isPIDInitialized = D(14);

% Random Number Generator For Noise
% rng('shuffle','twister');

%Load Patient Parameters from the external file
% patientParams = load ('d1.mat');

params.weight= 102.3200;
params.EGPb= 2.2758;
params.Fcns= 1;
params.Gb= 138.5600;
params.Gpb= 265.3701;
params.Gtb= 162.4571;
params.HEb= 0.6000;
params.Ib= 100.2500;
params.Ilb= 3.2076;
params.Ipb= 5.5043;
params.Km0= 253.5200;
params.Ts= 10;
params.Vg= 1.9152;
params.Vi= 0.0549;
params.Vm0= 3.2667;
params.Vmx= 0.0313;
params.b= 0.7039;
params.d= 0.2106;
params.f= 0.9000;
params.kp1= 4.7314;
params.kp2= 0.0047;
params.kp3= 0.0121;
params.isc1ss= 72.4342;
params.isc2ss= 141.1538;
params.k1= 0.0581;
params.k2= 0.0871;
params.ka1= 0.0019;
params.ka2= 0.0078;
params.kabs= 0.0891;
params.kd= 0.0152;
params.ke1= 5.0000e-04;
params.ke2= 339;
params.ki= 0.0046;
params.kmax= 0.0461;
params.kmin= 0.0038;
params.ksc= 0.0766;
params.m1= 0.1545;
params.m2= 0.2250;
params.m30= 0.2317;
params.m4= 0.0900;
params.m5= 0.0273;
params.p2u= 0.0278;
params.u2ss= 1.2386;
params.Sb= 1.2386;
params.m6= 0.6339;

simParams = pidSimulationWrapper(totTime,inps,XX,D);
[tt, times, YY, YY_,D] = simulatePIDSystem(simParams,params,timeElapsed,isPIDInitialized,D,XX,t_start,T_end,I);
% Y=[]; L= []; CLG = []; GRD=[];


if any(YY_(:,1) < 75.0)
    %     YY_
    prop_violated_flag = 1;
end

D_ = D;
P_ = P;

end     %end of artificial_pancreas()

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function simParams = pidSimulationWrapper(totTime,inps,XX,D)
mealTimes = [inps(1,1); inps(3,1) ];
mealCarbs = [inps(2,1); inps(4,1) ];
simParams = struct('mealTimes',mealTimes,...
    'mealCarbs',mealCarbs,...
    'bolusTimes',[inps(5,1); inps(7,1)] + mealTimes,...
    'bolusAmts',[inps(6,1); inps(8,1)] .* mealCarbs,...
    'openLoopBasal',inps(9,1),...
    'controllerStartTime',D(3),...
    'totalSimulationTime',totTime,...
    'ctrlTimePeriod',5,...
    'startingGlucose',XX(:,1));

%%simParams.cgmNoisePattern = inps(12:111,1);
%%simParams.cgmNoisePattern=zeros(100,1);
end     %end of pidSimulationWrapper()

%%%%%%%%%%%%%%%%%%%%%%%%%% simulatePIDSystem.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [tt, times, YY, YY_, D] = simulatePIDSystem(simParams,params,timeElapsed,isPIDInitialized,D,XX,t_start,T_end,I)

%1. Get the meal rate of appearance.
mealData.times = simParams.mealTimes;
mealData.carbs = simParams.mealCarbs;
[RATimes,gRA]  = simMealsToObtainRateOfAppearance(mealData, simParams.totalSimulationTime, params);
mealRA.times   = RATimes;
mealRA.values  = gRA;

insulinBolus.times   = simParams.bolusTimes;
insulinBolus.values  = simParams.bolusAmts;

sz=0;

times = t_start;
iValues = XX(:,3);

%% Nonsense

gValues = 0;
gsValues = 0;
intrnlValues = 0;
intrnlInsulin = 0;
curState = 0;

%Switch between open-loop and closed-loop
if timeElapsed < simParams.controllerStartTime
    %         fprintf('\nOpen Loop');
    %2. Simulate until the start of the controller.
    GStart      = simParams.startingGlucose;
    params.Gb   = GStart;
    params.Gpb  = params.Vg * GStart;
    params.Gtb  = ( params.k1 * params.Gpb - params.EGPb  + params.Fcns)/params.k2;
    
    startState  = [0; params.isc1ss; params.isc2ss; params.Gtb; params.Gpb; params.Ilb; params.Ipb; params.Ib; params.Ib; params.Gb];
    openLoopBasal.times  = [0; simParams.controllerStartTime];
    openLoopBasal.values = [simParams.openLoopBasal; 0];
    
    [t0, gOutOrig, gsOutOrig, curState] = simDallaManModel(startState, t_start, T_end, mealRA, openLoopBasal, insulinBolus, params);
    
    % Initialize the outputs
    %     times        = [];
    %     gValues      = [];
    %     gsValues     = [];
    %     iValues      = [];
    %intrnlValues = zeros(1,1);
    
    % copy data over
    sz = size(t0,1);
    times    = t0;
    times(1,1) = t_start;
    gValues  = gOutOrig;
    gsValues = gsOutOrig;
    iValues  = simParams.openLoopBasal * ones(sz,1);
    iValues(1,1) = XX(:,3);
    intrnlValues = zeros(sz,1);
    
else
    %         fprintf('\nClosed Loop');
    %3. Simulate in closed loop.
    curGs     = XX(:,2);
    curTime   = timeElapsed;
    if (isPIDInitialized == 0)
        ctrlState = initializePIDState(curGs, simParams.openLoopBasal, simParams.ctrlTimePeriod, params);
        D(15) = ctrlState.oldG;
        D(16) = ctrlState.Kp;
        D(17) = ctrlState.Td;
        D(18) = ctrlState.Ti;
        D(19) = ctrlState.insulinMax;
        D(20) = ctrlState.I;
        D(21) = ctrlState.target;
        D(22) = ctrlState.dt;
        D(23) = ctrlState.iMax;
        D(24) = ctrlState.gamma;
        isPIDInitialized = 1;
    else
        ctrlState.oldG  = D(15);
        ctrlState.Kp    = D(16);
        ctrlState.Td    = D(17);
        ctrlState.Ti    = D(18);
        ctrlState.insulinMax = D(19);
        ctrlState.I      = D(20);
        ctrlState.target = D(21);
        ctrlState.dt     = D(22);
        ctrlState.iMax   = D(23);
        ctrlState.gamma     = D(24);       
    end
    
    %% Nonsense
    % Allocate a known bound (guesstimate) of memory
    % The code after the while loop makes up for this nonsense by
    % re-assigning only the right amount of data
    times    = zeros(100,1);
    gValues = zeros(100,1);
    gsValues = zeros(100,1);
    iValues = zeros(100,1);
    intrnlValues = zeros(100,1);
    
    while(curTime < T_end)
        curGs = curGs + I;   % adding noise generated by SECAM
        %% Run the controller
        IpPred =  computeInsulinOnBoard(insulinBolus, times(1:sz,:), iValues(1:sz,:), curTime);
        % [curTime IpPred]
        
        [bValue, ctrlState, intrnlInsulin] =  computeControlValue(curGs,IpPred,ctrlState);
        
        clBasal.times=[curTime; curTime + simParams.ctrlTimePeriod];
        clBasal.values=[bValue; bValue];
        
        [tcl, gOut,gsOut,curState] = simDallaManModel(D(:,4:13), curTime, curTime + simParams.ctrlTimePeriod, mealRA, clBasal, insulinBolus, params);
        
        newSz = size(tcl,1);
        times(sz+1:sz+newSz,:) = tcl;
        
        gValues(sz+1:sz+newSz,:) = gOut;
        gsValues(sz+1:sz+newSz,:) = gsOut;
        iValues(sz+1:sz+newSz,:) = bValue * ones(newSz,1);
        intrnlValues(sz+1:sz+newSz,:) = 1000*intrnlInsulin* ones(newSz,1);
        curGs = gsOut(end,1);
        curTime = curTime + simParams.ctrlTimePeriod;
        sz = sz + newSz;
    end
end




D(14) = isPIDInitialized;

%% Nonsense: Prevents stuff from going nuts!
times    = times(1:sz,:);

gValues  = gValues(1:sz,:);
gsValues = gsValues (1:sz,:);
iValues  = iValues(1:sz,:);
intrnlValues      = intrnlValues(1:sz,:);
hyperGlycemiaTime = computeTimeInHyperGlycemia(times,gValues);
YY_ = [gValues gsValues iValues];

tt = times(end,:);  %T_end

YY = YY_(end,:);     %YY = [YY_(end,:) curState];

D(:,4:13) = curState;

end		% end of simulatePIDSystem()

%% Equation (13) in dallaman
%% Parameters
function y = getRateOfAppearance(x,params)
kabs = params.kabs;
weight= params.weight;
f = params.f;
y = f * kabs * x(:,3) / weight;
end     %end of getRateOfAppearance()

function [value,isTerminal,direction] = mealEvents(t,~,mealData,~)
%% Nonsense: replace Inf by a sufficiently large value
% tMealCurrent = Inf;
tMealCurrent = 10000;

[m ~]=size(mealData.times);
for i = 1:m
    if (t  >= mealData.times(i,1))
        tMealCurrent = mealData.times(i,1);
    end
end

if (t >= tMealCurrent && t <= tMealCurrent + 15)
    value = 0.0;
else
    value = 1.0;
end
isTerminal=0;
direction = 0;
end     %end of mealEvents()

function [mCarbsCurrent, D_, dImp]= getMeal(mealData,  t)
[m,~] = size(mealData.times); %number of meals
tMealCurrent = mealData.times(1,1); % time of first meal
mCarbsCurrent = mealData.carbs(1,1); % carbs of the first meal
mDurationCurrent = 15;% meal duration
for i = 1:m % for all the meals
    if (t  >= mealData.times(i,1))
        tMealCurrent = mealData.times(i,1);
        mCarbsCurrent = mealData.carbs(i,1)*1000;
        mDurationCurrent = 15; %% Assume that we have 15 minutes for each meal.
    end
end
D_ = mCarbsCurrent;
if (t > tMealCurrent && t < tMealCurrent + mDurationCurrent)
    dImp = mCarbsCurrent/mDurationCurrent;
    D_ = mCarbsCurrent * ( t- tMealCurrent)/mDurationCurrent;
else
    dImp = 0;
    mCarbsCurrent = 0.0;
end

end     %end of getMeal()

function y = mealModelODE(t,x,mealData,params)
y = zeros(3,1);
Qsto1 = x(1,1);
Qsto2 = x(2,1);
Qgut = x(3,1);
[mCarbsCurrent, D_, dImp] = getMeal(mealData,t);

%% Meal Gut absorption submodel taken from  DM2006
%% Parameters
b = params.b;
d = params.d;
kmin = params.kmin; %% 0.0038;
kmax = params.kmax; %% 0.0461;
kabs = params.kabs; %% 0.0891;

Qsto = Qsto1 + Qsto2;
alpha = 5 / ( 2 * (0.01+mCarbsCurrent) * (1- b)); %% hack to avoid division by zero is to add 0.01 to mCarbsCurrent.
beta = 5/ (2 * (0.01+mCarbsCurrent) * d);%% ..hack to avoid a division by zero

kempt =  kmin + (kmax - kmin)/2 * ( 2+  tanh( alpha * (Qsto - b * D_) ) - tanh( beta * (Qsto - d * D_)));%see paper[17] equation 18
d_Qsto1 = - kmax * Qsto1 + dImp;
d_Qsto2 = - kempt * Qsto2 + kmax * Qsto1;
d_Qgut = - kabs * Qgut + kempt * Qsto2;

y(1,1) = d_Qsto1;
y(2,1) = d_Qsto2;
y(3,1) = d_Qgut;

end     %end of mealModelODE()
%%%%%%%%%%%%%%%%%%%% simMealsToObtainRateOfAppearance.m %%%%%%%%%%%%%%%%%%%
function [T,glucoseRA,Te] = simMealsToObtainRateOfAppearance(mealData,endTime,params)
options = odeset('Events',@mealEvents,'MaxStep',1.0);
[T,x,Te] = ode45(@mealModelODE, [0,endTime], zeros(3,1), options,mealData,params);  %0:1:(endTime)
glucoseRA = getRateOfAppearance(x,params);

end     %end of simMealsToObtainRateOfAppearance()