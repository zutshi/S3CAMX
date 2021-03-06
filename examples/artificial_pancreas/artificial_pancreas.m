function [tt,YY,D,P,prop_violated_flag] = artificial_pancreas(t_start,T_end,XX,D,P,~,I,~)

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
patientParams = load ('d1.mat');
params = patientParams.params;

[tt, times, YY, YY_] = pidSimulationWrapper(params,totTime);

if any(YY_(:,1) < 75.0)
%     YY_
    prop_violated_flag = 1;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [tt, times, YY, YY_, Y, L, CLG, GRD, simParams] = pidSimulationWrapper(params,totTime)
    simParams.mealTimes=[inps(1,1); inps(3,1) ];
    simParams.mealCarbs=[inps(2,1); inps(4,1) ];
    simParams.bolusTimes = [inps(5,1); inps(7,1)] + simParams.mealTimes;
    simParams.bolusAmts = [inps(6,1); inps(8,1)] .* simParams.mealCarbs;
    simParams.openLoopBasal=inps(9,1);
	simParams.controllerStartTime = D(3);
	simParams.totalSimulationTime = totTime;
	simParams.ctrlTimePeriod = 5;
    simParams.startingGlucose = XX(:,1); %inps(11,1); 
    %%simParams.cgmNoisePattern = inps(12:111,1);
    %%simParams.cgmNoisePattern=zeros(100,1);
	[tt, times, YY, YY_] = simulatePIDSystem(simParams,params);
	Y=[]; L= []; CLG = []; GRD=[];
end     %end of pidSimulationWrapper()


%%%%%%%%%%%%%%%%%%%%%%%%%% simulatePIDSystem.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%
function [tt, times, YY, YY_] = simulatePIDSystem(simParams,params) 

    %1. Get the meal rate of appearance.
    mealData.times = simParams.mealTimes;
    mealData.carbs = simParams.mealCarbs;
    [RATimes,gRA]  = simMealsToObtainRateOfAppearance(mealData, simParams.totalSimulationTime, params);
    mealRA.times   = RATimes;
    mealRA.values  = gRA;    
    
    insulinBolus.times   = simParams.bolusTimes;
    insulinBolus.values  = simParams.bolusAmts;
    
    sz=0;
    
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
        times        = [];
        gValues      = [];
        gsValues     = [];
        iValues      = [];
        %intrnlValues = zeros(1,1);
        
        % copy data over
        sz = size(t0,1);
        times    = [times; t0];
        gValues  = [gValues; gOutOrig];
        gsValues = [gsValues; gsOutOrig];
        iValues  = [iValues; simParams.openLoopBasal * ones(sz,1)];
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
        times(1,1) = t_start;
        iValues(1,1) = XX(:,3);
        
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


%%%%%%%%%%%%%%%%%%%% simMealsToObtainRateOfAppearance.m %%%%%%%%%%%%%%%%%%%
function [T,glucoseRA,Te] = simMealsToObtainRateOfAppearance(mealData,endTime,params)
   options = odeset('Events',@(t,x)mealEvents(mealData,t,x),'MaxStep',1.0);
   mFun = @(t, x) mealModelODE(mealData, t, x);
   [T,x,Te] = ode45(  mFun, [0,endTime], zeros(3,1), options);  %0:1:(endTime)
   glucoseRA = getRateOfAppearance(x);

%% Equation (13) in dallaman
%% Parameters   
function y = getRateOfAppearance(x)
    kabs = params.kabs;
    weight= params.weight;
    f = params.f;
    y = f * kabs * x(:,3) / weight;
end     %end of getRateOfAppearance()

function [value,isTerminal,direction] = mealEvents(mealData,t,~)
    tMealCurrent = Inf;
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

function y = mealModelODE(mealData,  t, x)
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

end     %end of simMealsToObtainRateOfAppearance()

end     %end of artificial_pancreas()
