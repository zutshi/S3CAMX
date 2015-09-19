%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% AbstractFuelController with FR but as a BlackBox
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [tt,YY,D,P,prop_violated_flag] = AbstractFuelControl_BB(t,T,XX,D,P,U,I,property_check)

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
% set time.
% TODO: Ideally should be done in set_states()
set_param([model_name '/ext_time'], 'InitialCondition', num2str(t));

% Run the model

% options=simset('SrcWorkspace','current','DstWorkspace','base', 'ReturnWorkspaceOutputs', 'on');

if FR == 1
    %hAcs = getActiveConfigSet(model_name);
    %hAcs.set_param('StartTime', num2str(t));
    %hAcs.set_param('StopTime', num2str(T));
    try
        my_sim(model_name);
    catch
        disp('An error occurred while simulating...ignoring');
    end
    YY = get_states_FR();
else
    mySimOut = sim(model_name, 'StartTime', num2str(t),'StopTime', num2str(T), 'SaveFinalState', 'on', 'FinalStateName',[model_name 'SimState'], 'SaveCompleteFinalSimState', 'on', 'SaveFormat', 'dataset', 'SimulationMode', 'accelerator');
    YY = get_states(mySimOut);
end


%assignin('base', 'mySimOut', mySimOut);

YY(13) = XX(13);  % engine speed
% AF_tol
YY(14) = XX(14);  % AF_tol
% get external time.
% NOTE: Assumption is that the simulation indeed ran till T
% TODO: A better way to do this?
YY(15) = T;

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
ds = discrete_states();
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
        
        % discrete states
        
    case 16
        state_path = [model_name ds{1, 3}];
        state_name = '';
        state_abbrv = ds{1, 1};
    case 17
        state_path = [model_name ds{2, 3}];
        state_name = '';
        state_abbrv = ds{2, 1};
    case 18
        state_path = [model_name ds{3, 3}];
        state_name = '';
        state_abbrv = ds{3, 1};
    case 19
        state_path = [model_name ds{4, 3}];
        state_name = '';
        state_abbrv = ds{4, 1};
    case 20
        state_path = [model_name ds{5, 3}];
        state_name = '';
        state_abbrv = ds{5, 1};
    case 21
        state_path = [model_name ds{6, 3}];
        state_name = '';
        state_abbrv = ds{6, 1};
        
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
for i = 1:NUM_STATES
    [state_path, state_name, ~] = state_id_map(i);
    %display(['setting' state_path state_name ' = ' num2str(X(i))])
    set_param(state_path, state_name, num2str(X(i)));
end

assignin('base', 'en_speed', X(13));
% AF_tol
assignin('base', 'AF_sensor_tol', X(14));

% external time. Ideally should be done in set_states().
%set_param([model_name '/ext_time'], 'InitialCondition', num2str(X(14)));


% set discrete states
% initial state name, initial state value, block path

ds = discrete_states();

for i = 1:size(ds, 1)
    %     display('setting discrete states...')
    %     ds{i,1}
    assignin('base', [ds{i,1} '_init'], X(15+i));
end

end

function Y = get_states_FR()
bws = 'base';
%% plant states
xf = evalin(bws, [model_name 'SimState']);

% is this for debugging?
assignin(bws, 'xf', xf);

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


%% sim states are datasets now
for i = 16:21
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

tmp = evalin(bws, 'engine_speed_wk'); Y(8) = tmp.Data;
tmp = evalin(bws, 'throttle_angle_wk'); Y(9) = tmp.Data;
tmp = evalin(bws, 'throttle_flow_wk'); Y(10) = tmp.Data;
tmp = evalin(bws, 'airbyfuel_meas_wk'); Y(11) = tmp.Data;
% get the last data point of verification measurement, as all dat apoitns
% are stored
tmp = evalin(bws, 'verification_measurement_wk'); Y(12) = tmp.Data(end);
Y(13) = 0; % set it in the main func
% AF_tol
Y(14) = 0; % set it in the main func

% external time
% TODO: Ideally should be retrieved using loggedStates as above
%Y(14) = str2num(get_param([model_name '/ext_time'], 'InitialCondition'));
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
% external time
% TODO: Ideally should be retrieved using loggedStates as above
%Y(14) = str2num(get_param([model_name '/ext_time'], 'InitialCondition'));
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
y = 'AbstractFuelControl_M1_BB';
end

function y = mdl_path()
y = 'AbstractFuelControl_M1_BB.slx';
% y = './examples/abstractFuelControl/AbstractFuelControl_M1_BB.slx';
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

if FR == 1
    %TODO: It should not know about delta!
    % But its needed to support FR. A better idea?
    delta = 4.0;
    
    %'StartTime', num2str(t);
    %'StopTime', num2str(T);
    param_listing = ...
        {'StartTime', num2str(0);
        'StopTime', num2str(delta);
        'SaveFinalState', 'on';
        'FinalStateName', [model_name 'SimState'];
        'SaveCompleteFinalSimState', 'on';
        'SaveFormat', 'dataset';
        'SimulationMode', 'accelerator';
        %     'LoadExternalInput', 'on';
        %     'ExternalInput', 'input0';
        %     'SaveTime', 'on';
        %     'SaveState', 'on';
        %     'SaveOutput', 'on';
        %     'TimeSaveName', 'tout';
        %     'StateSaveName', 'xout';
        %     'OutputSaveName', 'yout';
        %     'LimitDataPoints', 'off';
        %         'SrcWorkspace', 'current';
        
        };
    hAcs = getActiveConfigSet(model_name);
    for i = 1:size(param_listing, 1)
        hAcs.set_param(param_listing{i,1}, param_listing{i,2});
    end
    my_sim_init(model_name);
end
% TODO: fix simtime using pvt data!
% simulation time (sec)
simTime = 12.0;
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

function deinit()
if FR == 1
    my_sim_deinit(model_name);
end
end

function y = FR()
y = 1;
end

function y = discrete_states()
y = ...
    {'nmd_ud2', 0, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_mode_10ms/normal_mode_detection/unit_delay2';
    'nmd_ud1', 0, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_mode_10ms/normal_mode_detection/unit_delay1';
    'fpi_ud', 0, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_10ms/feedback_PI_controller/UnitDelay1';
    'ae_ud1', 0.982, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_10ms/air_estimation/UnitDelay1';
    'sfd_ud', 0, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_mode_10ms/sensor_failure_detection/Unit Delay';
    'pmd_ud1', 0, '/Model 1/Z_AF_Controller/fuel_controller/fuel_controller_mode_10ms/power_mode_detection/Unit Delay1';
    };
end
