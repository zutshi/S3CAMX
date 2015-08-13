% Generate Random Tests
%% finding states in the simulink diagram
% Method 1:
%   - sldebug <name>
%       e.g. sldebug AbstractFuelControl_M1
%   - states
% Method 2:
%   - Simulink.BlockDiagram.getInitialState('<name>')
%       e.g. Simulink.BlockDiagram.getInitialState('AbstractFuelControl_M1')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Currently inputs must be constant
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% function simulink_sim(X0, I, NUM_O, plot_or_not, sim_mode, FR)

% t: Ti
% T: Tf
% X0
% D: <unused>
% P: <unused>
% U: control inputs, assumed to be constants in the model
% W: noise inputs: assumed as inputs to the model
% prop_check: <unused>

classdef autotrans_plant
    %% props
    properties
        paramNameValStruct = struct();
        NUM_State_Blocks = 2;
        NUM_X = 2;
        NUM_W = 0;
        NUM_CI = 2;
        NUM_O = 0;
        NUM_PO = 1;
        NUM_U = 3;
        MODEL_NAME = 'autotrans';
        MODEL_PATH = '/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/branches/RB-0.75/examples/autotrans/autotrans.slx';
        plot_or_not = false;
        SaveFormat = 'Dataset';
        FR = false;
        sim_mode = 'normal';
        delta_t = 1.0;
        
        % blocks with states
        % format: block name, state name, num elements (if vector), lower bound, upper bound
        states = {'plant/Vehicle/WheelSpeed', 'InitialCondition', 1, -inf, inf;
            'plant/Engine/Integrator', 'InitialCondition', 1, 600, 6000};
        
        % control inputs to the plant
        % format: block name, value name
        control_inputs = {'SIL_controller/computed_gear', 'value';
            'SIL_controller/disturbance_throttle', 'value';
            'SIL_controller/disturbance_brake', 'value'};
        % plant outputs
        % format: variable name
        plant_outputs = {'vehicle_speed_wk'};
    end
    methods
        %% Initializer
        function obj = autotrans_plant()
            load_system(obj.MODEL_PATH);
            % output format
            % SaveFormat = 'Dataset';
            % SaveFormat = 'Array'
            % SaveFormat = 'Structure'
            % ... several others
                        
            if obj.plot_or_not
                figure(420);
                hold on
                figI = cell(1, obj.NUM_W);
                for i = 1:obj.NUM_W
                    figI{i} = figure(i);
                    title(['input ' num2str(i)]);
                    hold on
                end
                figX = cell(1, obj.NUM_State_Blocks);
                for i = 1:obj.NUM_State_Blocks
                    figX{i} = figure(100+i);
                    title(['x ' num2str(i)]);
                    hold on
                end
                figO = cell(1, obj.NUM_O);
                for i = 1:obj.NUM_O
                    figO{i} = figure(200+i);
                    title(['output ' num2str(i)]);
                    hold on
                end
            end
            
            if obj.FR
                
                param_listing = ...
                    {'StartTime', num2str(0);
                    'StopTime', num2str(obj.delta_t);
                    'LoadExternalInput', 'on';
                    'ExternalInput', 'input0';
                    'SaveFormat', obj.SaveFormat;
                    'SaveCompleteFinalSimState', 'on';
                    'SaveFinalState', 'on';
                    'FinalStateName', 'xFinal';
                    'SaveTime', 'on';
                    'SaveState', 'on';
                    'SaveOutput', 'on';
                    'TimeSaveName', 'tout';
                    'StateSaveName', 'xout';
                    'OutputSaveName', 'yout';
                    'LimitDataPoints', 'off';
                    'SimulationMode', obj.sim_mode;
                    };
                
                hAcs = getActiveConfigSet(obj.MODEL_NAME);
                for i = 1:size(param_listing, 1)
                    hAcs.set_param(param_listing{i,1}, param_listing{i,2});
                end
                
                my_sim_init(obj.MODEL_NAME)
                
            else
%                 paramNameValStruct.StartTime = num2str(Ti);
%                 paramNameValStruct.StopTime = num2str(Tf);
                obj.paramNameValStruct.LoadExternalInput = 'on';
                obj.paramNameValStruct.ExternalInput = 'input0';
                obj.paramNameValStruct.SaveFormat = obj.SaveFormat;
                obj.paramNameValStruct.SaveCompleteFinalSimState = 'on';
                obj.paramNameValStruct.SaveFinalState = 'on';
                obj.paramNameValStruct.FinalStateName = 'xFinal';
                obj.paramNameValStruct.SaveTime = 'on';
                obj.paramNameValStruct.SaveState = 'on';
                obj.paramNameValStruct.SaveOutput = 'on';
                obj.paramNameValStruct.TimeSaveName = 'tout';
                obj.paramNameValStruct.StateSaveName = 'xout';
                obj.paramNameValStruct.OutputSaveName = 'yout';
                obj.paramNameValStruct.LimitDataPoints = 'off';
                obj.paramNameValStruct.SrcWorkspace = 'current';
                obj.paramNameValStruct.SimulationMode = obj.sim_mode;
            end
        end
        %% sim function
        function [tt,YY,D,P,prop_violated_flag] = sim(obj, t,T,X0,D,P,U,W,property_check)            
            for j = 1:obj.NUM_U
                [u_path, u_name] = obj.control_inputs{j, :};
                set_param([obj.MODEL_NAME, '/', u_path], u_name, num2str(U(j)));
            end
            
            % delta_t does not matters for now, as INPUT.time should be 0
            input0.time = 0;
            % FIXME: ASSUMES ordering between plant disturbances(w) and controller
            % disturbances(ci). Fix this by using structure instead of dataset as the SaveFormat
            model_inputs = [W zeros(1,obj.NUM_CI)];
            for j = 1:obj.NUM_W+obj.NUM_CI
                input0.signals(j).values = model_inputs(j);
                input0.signals(j).dimensions = 1;
            end
            
            % set states
            j = 1;
            k = 1;
            while j <= obj.NUM_X
                [state_path, state_name, num_dim, LB, UB] = obj.states{k, :};
                
                % An integrator can take a vector of states!
                X0_vector = X0(j:j + num_dim - 1);
                
                % Compute saturated values for the case of integrators with in built
                % saturations. Such Integrator blocks can not accept arbitrary state
                % values
                X0_saturated = min(max(X0_vector, LB), UB);
                
                % set the state vector
                set_param([obj.MODEL_NAME, '/', state_path], state_name, mat2str(X0_saturated));
                
                j = j + num_dim;
                k = k + 1;
            end
            
            if obj.FR
                assignin('base', 'input0', input0);
                
                my_sim(obj.MODEL_NAME)
                
                tout = evalin('base', 'tout');
                xout = evalin('base', 'xout');
                yout = evalin('base', 'yout');
            else
                obj.paramNameValStruct.StartTime = num2str(t);
                obj.paramNameValStruct.StopTime = num2str(T);
                mySimOut = sim(obj.MODEL_NAME, obj.paramNameValStruct);
                tout = mySimOut.get('tout');
                xout = mySimOut.get('xout');
                yout = mySimOut.get('yout');
            end
            
            % retrieve plant outputs to controller
            YY = zeros(1, obj.NUM_PO);
            if obj.FR
                for j = 1:obj.NUM_PO
                    op_str = obj.plant_outputs{j};
                    YY(j) = evalin('base', op_str);
                end
            else
                %% same for now
                for j = 1:obj.NUM_PO
                    op_str = obj.plant_outputs{j};
                    YY(j) = mySimOut.get(op_str);
                    % None of the below work
                    % hws = get_param(MODEL_NAME, 'modelworkspace');
                    % YY(j) = evalin('base', op_str);
                    % YY(j) = evalin('caller', op_str);
                    % YY(j) = evalin(hws, op_str);
                end
            end
            % TODO: blind assumption
            tt = T;
            
            % assignin('base', 'mySimOut', mySimOut)
            
            if strcmp(obj.SaveFormat, 'Array') == 1
                yt = repmat(tout, 1, obj.NUM_O);
                y = yout;
                xt = repmat(tout, 1, obj.NUM_State_Blocks);
                x = xout;
            elseif strcmp(obj.SaveFormat, 'Dataset') == 1
                % get yout
                yt = []; y = [];
                for j = 1:obj.NUM_O
                    yt_j = yout.getElement(j).Values.Time;
                    y_j = yout.getElement(j).Values.Data;
                    yt = [yt yt_j];
                    y = [y y_j];
                end
                % get xout
                xt = []; x = [];
                for j = 1:obj.NUM_State_Blocks
                    xt_j = xout.getElement(j).Values.Time;
                    x_j = xout.getElement(j).Values.Data;
                    xt = [xt xt_j];
                    x = [x x_j];
                end
            else
                error('unsupported SaveFormat: %s', obj.SaveFormat)
            end
            
            if obj.plot_or_not
                % plot
                for j = 1:obj.NUM_O
                    figure(figO{j});
                    plot(yt(:, j), y(:, j))
                end
                
                for j = 1:obj.NUM_State_Blocks
                    figure(figX{j});
                    plot(xt(:, j), x(:, j))
                end
            end
            
            prop_violated_flag = 0;
            
            %% de init
            if obj.FR
                my_sim_deinit(obj.MODEL_NAME)
            end
        end
        
    end
end

%% setting state in configset using a variable name
% Might be more uniform and portable than doing set params
% on each block with specified state name(e.g., InitialCondition, etc)

% xin.signals(2).blockName = 'plant1/S2'
% xin.signals(2).dimensions = 1
% xin.signals(2).label = 'CSTATE'
% xin.signals(2).values = 0;
% xin.signals(2).inReferencedModel = false