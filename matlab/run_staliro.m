function run_staliro(num_runs)
% filename = 'heat.tst';
% path = '/examples/heat';

% filename = 'dci.tst';
% path = '/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/examples/dc_motor_float';

% filename = 'fuzzy_invp.tst';
% path = '/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/examples/fuzzy_invp_float';

% filename = 'heater.tst';
% path = '/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/examples/heater_float';

%filename = 'toy_model_10u.tst';
%path = '/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/examples/toy_model_10u';}


init();

system_details = {
'heat.tst', './examples/heat';
'dci.tst', './examples/dc_motor';
'fuzzy_invp.tst', './examples/fuzzy_invp';
'heater.tst', './examples/heater';
'toy_model_10u.tst', './examples/toy_model_10u';
'spi.tst', './examples/spi';
};

display 'Enter a system to test...'
for i = 1:size(system_details, 1)
    fprintf('%d: %s\n', i, [system_details{i,2} '/' system_details{i,1}])
end
system_num = input('system number: ');
filename = system_details{system_num, 1};
path = system_details{system_num, 2};
run_example(filename, path,num_runs);

end

function run_all_examples(num_runs)
%systems_to_run = {'heater', 'dci'};
% systems_to_run = {'dci'};
systems_to_run = {'/home/zutshi/work/RA/cpsVerification/HyCU/symbSplicing/splicing/examples/heater_float'};

% read example_list and get system details

egl = py.example_list.get_example_list();
eg_cell_array = {};
for eg = egl
    eg_cell_array = [eg_cell_array struct(eg{1})];
end
for eg_ = eg_cell_array
    %display(eg{1})
    eg = eg_{1};
    %     disp(char(eg.description));
    path = char(eg.path);
    filename = char(eg.filename);
    % TODO: platform dependant file path construction!!
    file_path = [path '/' filename];
    
    %     if any(strmatch(filename, systems_to_run, 'exact'))
    if any(strmatch(path, systems_to_run, 'exact'))
        run_example(filename, path, num_runs);
    end
end
end

function run_example(filename, path, num_runs)
regression_dir_path = './regression_results/'
file_path = [path '/' filename];
diary_log =  [regression_dir_path filename '_staliro_log'];
results_summary_dump =  [regression_dir_path filename '_staliro_results'];
diary(diary_log);
diary on;
summary_fileID = fopen(results_summary_dump,'a');

matpy_funs = matpy();
[one_shot_sim, prop] = matpy_funs.load_system(file_path);
run(one_shot_sim, prop, num_runs, summary_fileID);
fclose(summary_fileID);
diary off;
end

function run(one_shot_sim, prop, num_runs, summary_fileID)

% Currently uses the approach MATLAB R2015a uses to send data to Python.
% It uses python array module, which supports only 1XN arrays.
% This can be changed by using list/tuples if really needed.
% Currently, S-Taliro will need it only if there are more than one noise inputs
% to the system (U)
% Ignores TU: sim_wrapper_for_staliro(X, T, TU, U)
% args:     S-Taliro sends X as a row vector
% return:   S-Taliro expects XT and T as row vectors
    function [T, XT, YT, LT, CLG, GRD] = sim_wrapper_for_staliro(X, T, ~, U)
%         U = zeros(10,1); HACK for fuzzy to go thru!
        % ignore TU for now.
        % Input is assumed to be parameterized as
        % a uniform random zoh signal at delta_t intervals
        [T_, X_, ~] = one_shot_sim(X', [0.0, T], U);
        % For now we don't differentiate between plant output and plant states
        % Is an explicit assignment to T ever needed?
        T = T_';
        XT = X_;
        YT = [];
        LT = [];
        CLG = [];
        GRD = [];
    end


x0_bounds = prop.init_cons;
ci_bounds = prop.w;
ni = size(ci_bounds, 1);
% fix below
input_range = ci_bounds;
% cp_array = 2*ones(1,ni);
cp_array = prop.num_segments*ones(1,ni);
% cp_array = prop.num_segments;
% interpolationtype = {};
% for i = 1:ni
%     interpolationtype = [interpolationtype 'UR'];
% end
interpolationtype = repmat({'pconst'}, 1, ni);


phi = '!<>p';
poly = cubeToPoly(prop.final_cons);
preds(1).str = 'p';
preds(1).A = poly.A;
preds(1).b = poly.b+0;

preds(1).A
preds(1).b

% SampTime = prop.ci_zoh_time;
SampTime = prop.delta_t;
% SampTime = 0.03;

% ci_bounds
% x0_bounds
% poly.A
% poly.b
% pausg

simTime = prop.T;
opt = staliro_options();
opt.SampTime = SampTime;
opt.black_box = 1;
opt.taliro_metric = 'none';
opt.optimization_solver= 'SA_Taliro' ;
opt.spec_space = 'X';
opt.interpolationtype = interpolationtype;

opt.n_workers = 1;
opt.runs = 1;
% opt.sa_params.n_tests = 1000;
% modified for SPI
% opt.optim_params.n_tests = 5000;
opt.optim_params.n_tests = 1000;


% figure(1)
% hold on

disp('Running S-TaLiRo with chosen solver ...')

TO = 3600;

run_time = zeros(1, num_runs);

for i = 1:num_runs
    % initialize while loop
    num_runs_staliro = 0;
    falsified = 0;
    timed_out = 0;
    staliroTime = tic;
    run_id_str = ['run_' num2str(i)]
    
    while falsified == 0 && timed_out == 0
        [results, history] = staliro(@sim_wrapper_for_staliro,x0_bounds,input_range,cp_array,phi,preds,simTime,opt);
        results.run(results.optRobIndex).bestRob;
        num_runs_staliro = num_runs_staliro + 1;
        falsified = results.run.falsified;
        if toc(staliroTime) >= 3600
            timed_out = 1;
        end
    end
    
    run_time(i) = toc(staliroTime);
    
    fprintf(summary_fileID, 'number of S-Taliro runs: %d\t', num_runs_staliro);
    fprintf(summary_fileID, 'run_time: %f\t', run_time(i));
    
    if timed_out == 1
        warning('timed out!')
        fprintf(summary_fileID, 'result: TO\n');
    elseif falsified == 1
        fprintf(summary_fileID, 'result: Falsified\n');
        disp('FALSIFIED!')
    else
        fprintf(summary_fileID, 'result: Failed\n');
    end
    
    assignin('base', ['cp_array' '_' run_id_str], cp_array);
    assignin('base', ['results' '_' run_id_str],  results);
    assignin('base', ['run_time' '_' run_id_str], run_time);
    assignin('base', ['history' '_' run_id_str],  history);
end
total_time = sum(run_time);
average_time_per_run = total_time/num_runs;

fprintf(summary_fileID, '            =====================             \n');
fprintf(summary_fileID, '%s: %f\n', 'total_time', total_time);
fprintf(summary_fileID, '%s: %f\n', 'average_time_per_run', average_time_per_run);
fprintf(summary_fileID, '****************** END ***********************\n');

% disp('inputSignal')
% disp(inputSignalStore')
% disp('X0')
% disp(results.run(results.optRobIndex).bestSample')

end

function init()
%clear;  % clear command history
%clc;    % clear variables

% Add S-Taliro path
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/Polarity/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/dp_taliro/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/dp_t_taliro/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/fw_taliro/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/ha_robust_tester/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/Distances/')
% addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/s_taliro_ver1_4/auxiliary/')
addpath('/home/zutshi/work/RA/cpsVerification/HyCU/s_taliro/')
setup_public
end

function poly = cubeToPoly(cube)
NUM_STATE_VARS = size(cube,1);

Al = -eye(NUM_STATE_VARS);
bl = -cube(:,1);
Ah = eye(NUM_STATE_VARS);
bh = cube(:,2);

% collect indices of elements in b with infinity as the value
arrInf = [];
% remove all constraints such as x > -inf
for i = 1:NUM_STATE_VARS
    if bl(i) == inf %|| poly.b(i) == -inf, redundant. will never occur
        arrInf = [arrInf i];
    end
end

Al(arrInf,:) = 0;
bl(arrInf) = 0;

arrInf = [];
% remove all constraints such as x < inf
for i = 1:NUM_STATE_VARS
    if bh(i) == inf %|| poly.b(i) == -inf, redundant. will never occur
        arrInf = [arrInf i];
    end
end
Ah(arrInf,:) = 0;
bh(arrInf) = 0;

poly.A = [Al;Ah];
poly.b = [bl;bh];
end

function disable_warnings()
warnStruct = warning('query', 'last');
msgid_integerCat = warnStruct.identifier;
warning('off', msgid_integerCat);
end
