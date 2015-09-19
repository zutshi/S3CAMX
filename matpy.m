%% Helper Functions
function y = matpy()
y.serialize_array = @serialize_array;
y.deserialize_array = @deserialize_array;
%y.sim = @simulate_system_external;
y.load_system = @load_system;
y.deserialize_prop = @deserialize_prop;

%% arrays are de-serialized
%
%% scalars are forced to be double [this prevents crazy Matlab errors]
%   for e.g., when running S-Taliro
%           Error using  :
%           Double operands interacting with int64 operands must have integer values.
%           Error in Compute_Robustness_Sub (line 85)
%                   steptime = (0:staliro_opt.SampTime:staliro_SimulationTime)';
% This is because class(staliro_opt.SampTime) = double is not the same as
% class(staliro_SimulationTime) = int64.
% staliro_SimulationTime comes from matpy as T!
    function prop = deserialize_prop(prop_ser)
        % Transpose cons arrays to bring them to more traditional format
        prop.init_cons = deserialize_array(prop_ser.init_cons);
        prop.final_cons = deserialize_array(prop_ser.final_cons);
        prop.w = deserialize_array(prop_ser.w);
        prop.T = double(prop_ser.T);
        prop.num_segments = double(prop_ser.num_segments);
        prop.delta_t = double(prop_ser.delta_t);
    end

    function [one_shot_sim, prop] = load_system(file_path)
        sim_and_prop = py.matpy.load_system(file_path);
        one_shot_sim_py = sim_and_prop{1};
        prop_ser = sim_and_prop{2};
        prop = deserialize_prop(prop_ser);
        % X: plant states
        % T: [t0, tf]
        % W: exogenous input array. Currently zoh parameterized and only for controller
        % pvt: read only, in-accessible structure, similar to simStates. To be used for
        % stopping and restarting simulations.
        % pvt encapsulates: controller states, pvt sim states, and plant discrete
        % states
        % TODO: plant discrete states need to be fixed as soon as its fixed at the core
        % of the implementaiton.
        function [T, X, pvt_] = sim_wrapper(X, T, W)
            t0 = T(1);
            tf = T(2);
            x_ser = serialize_array(X);
            w_ser = serialize_array(W);
            trace = one_shot_sim_py(x_ser, t0, tf, w_ser);
            T = deserialize_array(trace{1});
            X = deserialize_array(trace{2});
            %TODO: FIX IT later, currently S-Taliro does not need it.
            % pvt_ = trace{3};
            pvt_ = 0;
        end
        % can not inline funcs with multiple args
        % one_shot_sim = inline('sim_wrapper(X, T, W)')
        one_shot_sim = @sim_wrapper;
    end


% Converts matlab array to python representation
% currently converts matlab array to python array
    function x_ser = serialize_array(x)
        if ndims(x) > 2
            error('only maltab arrays of dim <= 2 supported.')
        end
        s = size(x);
        flat_x = reshape(x',1,[]);
        x_ser = [s flat_x];
    end

% reverses the serialization
    function x = deserialize_array(x_ser)
        mat_array = double(x_ser);
        s = mat_array(1:2);
        % reverse s
        s = fliplr(s);
        flat_x = mat_array(3:end);
        x = reshape(flat_x, s)';
    end

%     % Converts matlab array to python representation
%     % currently converts matlab array to python array
%     function x_ser = serialize_array(x)
%     if ndims(x) > 2
%         error('onyl maltab arrays of dim <= 2 supported.')
%     end
%     % The below dimensionailty differs from ndims(x).
%     % It is the same as numpy's ndim
%     [r,c] = size(x);
%     if r == 1
%         s = c
%         dim = 1;
%     elseif c == 1
%         s = r
%         dim = 1;
%     else
%         s = s;
%         dim = 2;
%     end
%     flat_x = x(:)';
%     % let matlab do an auto conversion to Python array
%     x_ser = [dim s flat_x];
%     % convert to list
%     %py_x = py.list(flat_x);
%     end
%
%     % reverses the
%     function x = deserialize_array(x_ser)
%     mat_array = double(x_ser);
%     offset = 0;
%     dim_size = 1;
%     dim = mat_array(1+offset:offset+dim_size);
%     % size
%     offset = offset + dim_size;
%     s_size = dim;
%     s = mat_array(1+offset:offset+s_size);
%     offset = offset + s_size;
%     flat_x = mat_array(1+offset:end);
%     x = reshape(flat_x, s);
%     end

end
