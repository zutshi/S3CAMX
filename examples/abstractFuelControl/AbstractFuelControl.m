function [tt,YY,D,P,prop_violated_flag] = AbstractFuelControl(t,T,XX,D,P,U,I,property_check)
display(XX)
fprintf('%f, %f\n', t, T);
%figure(1)
%hold on
%figure(2)
%hold on
%figure(3)
%hold on

% TODO: call only once!
init()

set_states(XX);

%warning('forcing control inputs!')
%U = [0.441 0 14.7];
% set control inputs
set_param('AbstractFuelControl_M1/Model 1/AFC/commanded_fuel_c', 'Value', num2str(U(1)));
set_param('AbstractFuelControl_M1/Model 1/AFC/airbyfuel_ref_c', 'Value', num2str(U(3))); 

% Run the model

% options=simset('SrcWorkspace','current','DstWorkspace','base', 'ReturnWorkspaceOutputs', 'on');
mySimOut = sim(model_name, 'StartTime', num2str(t),'StopTime', num2str(T), 'SaveFinalState', 'on', 'FinalStateName',[model_name 'SimState'], 'SaveCompleteFinalSimState', 'on', 'SaveFormat', 'dataset', 'SimulationMode', 'accelerator');
%assignin('base', 'mySimOut', mySimOut);
YY = get_states(mySimOut);
YY(13) = XX(13);  % engine speed
YY(14) = XX(14);  % engine speed

%figure(1)
%plot(mySimOut.get('verification_measurement_wk').Time, mySimOut.get('verification_measurement_wk').Data);

%figure(2)
%plot(mySimOut.get('compare_wk').Time, mySimOut.get('compare_wk').Data)
%display(mySimOut.get('compare_wk').Data')
  
%figure(3)
%plot(t, U(1), '*')

YY = YY';
tt = T;
prop_violated_flag = 0;
D = D;
P = P;

if YY(12) >= 0.02
  prop_violated_flag = 1;
end
end

function [state_path, state_name, state_abbrv] = state_id_map(state_id)

switch state_id
    case 1 % X0 = 0
        state_path = [model_name M1 CnE '/Integrator'];
        state_name = 'InitialCondition';
        state_abbrv = 'cyl_ex';
    case 2 % X0 = 0
        state_path = [model_name M1 '/Throttle delay'];
        state_name = 'X0';
        state_abbrv = 'throttle_delay';
    case 3 % X0 = 0.982000
        state_path = [model_name M1 IM '/p0 = 0.543 (bar)'];
        state_name = 'InitialCondition';
        state_abbrv = 'intake_manifold';
    case 4 % X0 = 0.011200
        state_path = [model_name M1 '/Wall wetting/Integrator'];
        state_name = 'InitialCondition';
        state_abbrv = 'wall_wetting';
    case 5 % X0 = 0
        state_path = [model_name '/V&V stub system/Calcuate Error/RMS error/Integrator'];
        state_name = 'InitialCondition';
        state_abbrv = 'vnv';
    case 6  % X0 \in [0 61.1];
        state_path = [model_name '/Pedal Angle (deg)'];
        state_name = 'Amplitude';
        state_abbrv = 'NA';
    case 7  % X0 \in [10 30];
        state_path = [model_name '/Pedal Angle (deg)'];
        state_name = 'Period';
        state_abbrv = 'NA';
%     case 8
%         % output modeled as a pseudo state...this should not be called
%         Omega -> engine_speed_wk
%     case 9
%         % output modeled as a pseudo state...this should not be called
%         s_out -> throttle_angle_wk        
%     case 10
%         % output modeled as a pseudo state...this should not be called
%         s_out -> throttle_flow_wk        
%     case 11
%         % output modeled as a pseudo state...this should not be called
%         s_out -> airbyfuel_meas_wk        
%     case 12
%         % output modeled as a pseudo state...this should not be called
%         s_out -> verification_measurement_wk        
    otherwise
        error(['Unknown state_id: ' num2str(state_id)])
end
end


function set_states(X)
%display('setting states')
for i = 1:7
    [state_path, state_name, ~] = state_id_map(i);
    %display(['setting' state_path state_name ' = ' num2str(X(i))])
    set_param(state_path, state_name, num2str(X(i)));
end

assignin('base', 'en_speed', X(13));
assignin('base', 'AF_sensor_tol', X(14));
end

function Y = get_states(mySimOut)
%% plant states
xf = mySimOut.get([model_name 'SimState']);
assignin('base', 'xf', xf);
Y_str = cell(NUM_TOTAL_STATES, 1);
Y = zeros(NUM_TOTAL_STATES, 1);

%% old code, when simstates were of type 'structure'
%for i = 1:NUM_STATES-2
%    [state_path, state_name] = state_id_map(i);
%    Y(i) = xf.loggedStates(i).values;
%    Y_str{i} = xf.loggedStates(i).blockName;
%    % Verify that strings are the same, if not raise error.
%    if strcmp(state_path,Y_str{i}) ~= 1
%        error('state string mismatch: %s != %s', state_path,Y_str{i});
%    end
%end

%% sim states are datasets now
for i = 1:NUM_STATES-2
    [state_path, state_name, state_abbrv] = state_id_map(i);
    Y(i) = xf.loggedStates.get(state_abbrv).Values.Data;
    % TODO: below is redundant. Retained as an assertion ...
    Y_str{i} = xf.loggedStates.get(state_abbrv).BlockPath.getBlock(1);
    % Verify that strings are the same, if not raise error.
    if strcmp(state_path,Y_str{i}) ~= 1
        error('state string mismatch: %s != %s', state_path,Y_str{i});
    end
end

%% parameters
% The pedal amplitude and period remains the same and can be read using
% get_param
[state_path, state_name, ~] = state_id_map(6);
Y(6) = str2double(get_param(state_path, state_name));
[state_path, state_name, ~] = state_id_map(7);
Y(7) = str2double(get_param(state_path, state_name));
%% outputs
% get engine_speed. Only 1 data point is stored
Y(8) = mySimOut.get('engine_speed_wk').Data;
Y(9) = mySimOut.get('throttle_angle_wk').Data;
Y(10) = mySimOut.get('throttle_flow_wk').Data;
Y(11) = mySimOut.get('airbyfuel_meas_wk').Data;
% get the last data point of verification measurement, as all dat apoitns
% are stored
Y(12) = mySimOut.get('verification_measurement_wk').Data(end);
Y(13) = 0; % set it in the main func
Y(14) = 0; % set it in the main func
end

function y = NUM_STATES()
y = 7;
end

function y = NUM_TOTAL_STATES()
% The system has 4 states 
%   + 1 verification module states 
%   + 3 parameters 
%   + 4 outputs modeled as pseudo state
%   + 1 aux verification output modeled again as a pseudo state
% The other outputs are just states...will be fixed later
y = 4+1+3+4+1; % = 12
end

function y = model_name()
y = 'AbstractFuelControl_M1';
end

function y = mdl_path()
y = './examples/abstractFuelControl/AbstractFuelControl_M1.slx';
end
function y = M1()
y = '/Model 1';
end
function y = IM()
y = '/Intake Manifold';
end
function y = CnE()
y = '/Cylinder and Exhaust';
end


function init()
disp('loading simulink model...')
load_system(mdl_path);
disp('done...')

% TODO: fix simtime using pvt data!
% simulation time (sec)
simTime = 12;
assignin('base', 'simTime', simTime);
% engine speed (rpm)
%en_speed = 1000;
%assignin('base', 'en_speed', en_speed);
% time to start to measurement for verification (sec)
measureTime = 1;
assignin('base', 'measureTime', measureTime);
% time to introduce sensor failure (sec)
fault_time = 60;
assignin('base', 'fault_time', fault_time);
% measurement method for verification
spec_num = 1;
assignin('base', 'spec_num', spec_num);
% fule injection actuator error factor, c25
fuel_inj_tol = 1.0;
assignin('base', 'fuel_inj_tol', fuel_inj_tol);
% MAF sensor error factor, c23
MAF_sensor_tol = 1.0;
assignin('base', 'MAF_sensor_tol', MAF_sensor_tol);
% A/F sensor error factor, c24
AF_sensor_tol = 1.0;
assignin('base', 'AF_sensor_tol', AF_sensor_tol);
end
