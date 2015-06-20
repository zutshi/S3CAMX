test_id = 'test_interface';
% test_id = 'test_sim';
matpy_funs = matpy();

if strcmp(test_id, 'test_interface') == 1
    % TEST: 1
    % DESCRIPTION: send 2-dim array
    A = [1, 2, 3; 4, 5, 6; 7, 8, 9; 10, 11, 12];
    A_ser = matpy_funs.serialize_array(A);
    A_py = py.matpy.deserialize_array(A_ser);
    A_py_ser = py.matpy.serialize_array(A_py);
    B = matpy_funs.deserialize_array(A_py_ser);
    if isequal(A,B)
        disp('Test1: passed')
    else
        fprintf('Test1: failed! A!=B');
        A
        B
    end
    % TEST: 2
    % DESCRIPTION: send column vector
    A = [1:10];
    A_ser = matpy_funs.serialize_array(A);
    A_py = py.matpy.deserialize_array(A_ser);
    A_py_ser = py.matpy.serialize_array(A_py);
    B = matpy_funs.deserialize_array(A_py_ser);
    if isequal(A,B)
        disp('Test2: passed')
    else
        fprintf('Test2: failed! A!=B');
        A
        B
    end
    % TEST: 3
    % DESCRIPTION: send row vector
    A = [1:10]';
    A_ser = matpy_funs.serialize_array(A);
    A_py = py.matpy.deserialize_array(A_ser);
    A_py_ser = py.matpy.serialize_array(A_py);
    B = matpy_funs.deserialize_array(A_py_ser);
    if isequal(A,B)
        disp('Test3: passed')
    else
        fprintf('Test13 failed! A!=B');
        A
        B
    end
    
elseif strcmp(test_id, 'test_sim') == 1
    % add path for genRandVectors
    addpath('/home/zutshi/work/RA/cpsVerification/HyCU/matlabProt');
    
    [one_shot_sim, prop] = matpy_funs.load_system('heater', './examples/heater/');
    
    NUM_SIMS = 100;
    %TODO: fix this transpose issue!!
    x0_bounds = prop.init_cons';
    x_unsafe = prop.final_cons';
    w = prop.w;
    NUM_STATES = size(x0_bounds, 1);
    randPoints = rand(NUM_SIMS, NUM_STATES);
    x_samples = genRandVectors(randPoints, x0_bounds);
    
    dummy_w = zeros(prop.num_segments, 1);
    
    figure(1)
    hold on
    tic
    for i = 1:NUM_SIMS
        x0 = x_samples(i,:);
        [T, X, ~] = one_shot_sim(x0, [0.0, prop.T], dummy_w);
        plot(T, X)
        %trace_list.append(trace)
    end
    toc
else
    error('unknown test id: %s', test_id)
end

