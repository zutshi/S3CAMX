function funH = simulate_m_file(funID)
delete 'log_matlab'
diary log_matlab

if funID == 1
    funH = @simulate_system;
elseif funID == 2
    funH = @simulate_system_par;
elseif funID == 3
    funH = @simulate_entire_trajectories;
elseif funID == 4
    funH = @simulate_entire_trajectories_cont;
else
    error('')
end
end

function [ret_t, ret_X, ret_D, ret_P, pvf] = simulate_system(sim_function, t, T, initial_continuous_states, initial_discrete_states, initial_pvt_states, control_inputs, inputs, property_check)

plot_to_debug = 0;
pvf = 0;

% % create plot windows
% figure(1)
% hold on
% figure(2)
% hold on
% figure(3)
% hold on


num_initial_conditions = size(initial_continuous_states, 1);
if num_initial_conditions ~= size(initial_discrete_states, 1) || num_initial_conditions ~= size(initial_pvt_states, 1) || num_initial_conditions ~= size(inputs, 1)
        error('size of state arrays or input arrays do not match')
end

my_print('num_initial_conditions', num_initial_conditions)
my_print('control inputs', control_inputs)

num_continuous_states = size(initial_continuous_states, 2);
num_discrete_states = size(initial_discrete_states, 2);
num_private_states = size(initial_pvt_states, 2);

my_print('num_continuous_states', num_continuous_states)
my_print('num_discrete_states', num_discrete_states)
my_print('num_private_states', num_private_states)

ret_t = zeros(num_initial_conditions, 1);
ret_X = zeros(num_initial_conditions, num_continuous_states);
ret_D = zeros(num_initial_conditions, num_discrete_states);
ret_P = zeros(num_initial_conditions, num_private_states);

data_set = cell(1, num_initial_conditions);

for i = 1:num_initial_conditions
    my_print('i', i)
    t0 = t(i,:);
    X0 = initial_continuous_states(i,:);
    D0 = initial_discrete_states(i,:);
    P0 = initial_pvt_states(i,:);
    U0 = control_inputs(i,:);
    I0 = inputs(i,:);
    %TODO: SIM function can give back arrays describing multiple points on
    %the simulation traces, but need NOT.
    %Is this OK?
    [t_arr,X_arr,D_arr,P_arr,prop_violated_flag] = sim_function(t0,t0+T,X0,D0,P0,U0,I0,property_check);

    if property_check == 1
        pvf = prop_violated_flag;
    end
    
    my_print('t', t_arr)
    my_print('X', X_arr)
    my_print('D', D_arr)
    my_print('P', P_arr)
    
    ret_t(i,:) = t_arr(end,:);
    ret_X(i,:) = X_arr(end,:);
    ret_D(i,:) = D_arr(end,:);
    ret_P(i,:) = P_arr(end,:);
    
    data_set{i} = [X_arr t_arr];
    
%     % plot
%     figure(1)
%     plot(t,X(:,1));
%     figure(2)
%     plot(t,X(:,2));
%     figure(3)
%     plot(X(:,1),X(:,2));
%     % drawnow

end
if plot_to_debug == 1   
    % plot
    figure(1);xlabel('t');ylabel('x1');hold on;
    % equivalent: plot(t_arr,X_arr(:,1));
    for j = 1:length(data_set)
        plot(data_set{j}(:,num_continuous_states+1),data_set{j}(:,1))
    end
    
    figure(2);xlabel('t');ylabel('x2');hold on;
    % equivalent: plot(t_arr,X_arr(:,2));
    for j = 1:length(data_set)
        plot(data_set{j}(:,num_continuous_states+1),data_set{j}(:,2))
    end
    
    figure(3);xlabel('x1');ylabel('x2');hold on;
    % equivalent: plot(X_arr(:,1),X_arr(:,2));
    for j = 1:length(data_set)
        plot(data_set{j}(:,1),data_set{j}(:,2))
    end
end
my_print('Function Ends, with outpus...', [])

my_print('ret_X', ret_X)
my_print('ret_P', ret_D)
my_print('ret_P', ret_D)
end


function [ret_X, ret_D, ret_P] = simulate_system_par(sim_function, initial_continuous_states, initial_discrete_states, initial_pvt_states, inputs, T)

my_print('simulate_system_par','simulate_system_par')

plot_to_debug = 0;

% % create plot windows
% figure(1)
% hold on
% figure(2)
% hold on
% figure(3)
% hold on


num_initial_conditions = size(initial_continuous_states, 1);
if num_initial_conditions ~= size(initial_discrete_states, 1) || num_initial_conditions ~= size(initial_pvt_states, 1) || num_initial_conditions ~= size(inputs, 1)
        error('size of state arrays or input arrays do not match')
end

my_print('num_initial_conditions', num_initial_conditions)

num_continuous_states = size(initial_continuous_states, 2);
num_discrete_states = size(initial_discrete_states, 2);
num_private_states = size(initial_pvt_states, 2);

my_print('num_continuous_states', num_continuous_states)
my_print('num_discrete_states', num_discrete_states)
my_print('num_private_states', num_private_states)



ret_X = zeros(num_initial_conditions, num_continuous_states);
ret_D = zeros(num_initial_conditions, num_discrete_states);
ret_P = zeros(num_initial_conditions, num_private_states);

my_print('ret_X', ret_X)
my_print('ret_D', ret_D)
my_print('ret_P', ret_P)

data_set = cell(1, num_initial_conditions);

parfor i = 1:num_initial_conditions
    my_print('i', i)
    X0 = initial_continuous_states(i,:);
    D0 = initial_discrete_states(i,:);
    P0 = initial_pvt_states(i,:);
    I0 = inputs(i,:);
    %TODO: SIM function can give back arrays describing multiple points on
    %the simulation traces, but need NOT.
    %Is this OK?
    [t_arr,X_arr,D_arr,P_arr] = sim_function(T,X0,D0,P0,I0);
    
    my_print('t', t_arr)
    my_print('X', X_arr)
    my_print('D', D_arr)
    my_print('P', P_arr)
    
    ret_X(i,:) = X_arr(end,:);
    ret_D(i,:) = D_arr(end,:);
    ret_P(i,:) = P_arr(end,:);
    
    data_set{i} = [X_arr t_arr];
    
%     % plot
%     figure(1)
%     plot(t,X(:,1));
%     figure(2)
%     plot(t,X(:,2));
%     figure(3)
%     plot(X(:,1),X(:,2));
%     % drawnow

end
if plot_to_debug == 1   
    % plot
    figure(1);xlabel('t');ylabel('x1');hold on;
    % equivalent: plot(t_arr,X_arr(:,1));
    for j = 1:length(data_set)
        plot(data_set{j}(:,num_continuous_states+1),data_set{j}(:,1))
    end
    
    figure(2);xlabel('t');ylabel('x2');hold on;
    % equivalent: plot(t_arr,X_arr(:,2));
    for j = 1:length(data_set)
        plot(data_set{j}(:,num_continuous_states+1),data_set{j}(:,2))
    end
    
    figure(3);xlabel('x1');ylabel('x2');hold on;
    % equivalent: plot(X_arr(:,1),X_arr(:,2));
    for j = 1:length(data_set)
        plot(data_set{j}(:,1),data_set{j}(:,2))
    end
end
my_print('Function Ends, with outpus...', [])

my_print('ret_X', ret_X)
my_print('ret_P', ret_D)
my_print('ret_P', ret_D)
end

% return values
% data_mat: set of trajectories
% idx_arr: contains the row indices indicating the begining of a new trajectory
%
% data_mat and idx_arr shown for a system with two state variables, 1 discrete and pvt state
% idx_arr = [1,5]                           -- 1st trajectory begins at index 1 and 2nd trajectory begins at index 5
% data_mat:
% 1: [ x1(t0) x2(t0) t0 d(t0) p(t0)         -- 1st trajectory
% 2:   x1(t1) x2(t1) t1 d(t1) p(t1)
% 3:   x1(t2) x2(t2) t2 d(t2) p(t2)
% 4:   x1(t3) x2(t3) t3 d(t3) p(t3)
% 5:   x1(t0) x2(t0) t0 d(t0) p(t0)         -- 2nd trajectory
% 6:   x1(t1) x2(t1) t1 d(t1) p(t1)
% ]

function [data_mat, idx_arr] = simulate_entire_trajectories(sim_function, initial_continuous_states, initial_discrete_states, initial_pvt_states, inputs, T)
%figure(1)
%hold on

num_initial_conditions = size(initial_continuous_states, 1);
%if num_initial_conditions ~= size(initial_discrete_states, 1) || num_states ~= size(initial_pvt_states, 1) || num_states ~= size(inputs, 1)
%    error('size of state arrays or input arrays do not match')
%end

num_continuous_states = size(initial_continuous_states, 2);
num_discrete_states = size(initial_discrete_states, 2);
num_private_states = size(initial_private_states, 2);

data_set = cell(1, num_initial_conditions);

parfor i = 1:num_initial_conditions
    X0 = initial_continuous_states(i,:);
    D0 = initial_discrete_states(i,:);
    P0 = initial_pvt_states(i,:);
    I0 = inputs(i,:);
    [t_arr,X_arr,D_arr,P_arr] = sim_function(T,X0,D0,I0);
    data_set{i} = [X_arr t_arr D_arr P_arr];
end

% index array keeps track of starting indices for each trajectory in the big coalesced data_set
idx_arr = zeros(num_initial_conditions, 1);
% length array keeps track of lengths for each trajectory in the big coalesced data_set
len_arr = zeros(num_initial_conditions, 1);
% index for the current trajectory
curr_idx = 1;
for i = 1:length(data_set)
    len_of_current_traj = size(data_set{i},1);
    idx_arr(i) = curr_idx;
    len_arr(i) = len_of_current_traj;
    curr_idx = curr_idx + len_of_current_traj;
end

% due to Matlab's indexing begining from 1, adjust total length
total_len = curr_idx - 1;
% Add 1 for time
data_mat = zeros(total_len, num_continuous_states + num_discrete_states + num_private_states + 1);

for j = 1:length(data_set)
    % sys_opt.plotFun(plotSet{j}(:,NUM_STATE_VARS+1),plotSet{j}(:,1:NUM_STATE_VARS),currMode);
    plot(data_set{j}(:,num_continuous_states+1),data_set{j}(:,1))
    % TODO: not sure is appending in parfor is faster or this, need to check
    data_mat(idx_arr(j) : idx_arr(j) + len_arr(j) - 1) = data_set{j};
end
%drawnow;
end

function [data_mat, idx_arr] = simulate_entire_trajectories_cont(sim_function, initial_continuous_states, T)

figure(1)
hold on

num_initial_conditions = size(initial_continuous_states, 1);
num_continuous_states = size(initial_continuous_states, 2);

data_set = cell(1, num_initial_conditions);

parfor i = 1:num_initial_conditions
    X0 = initial_continuous_states(i,:);
    [t_arr,X_arr,~,~] = sim_function(T,X0,[],[]);   
    data_set{i} = [X_arr t_arr];
end
% index array keeps track of starting indices for each trajectory in the big coalesced data_set
idx_arr = zeros(num_initial_conditions, 1);

% length array keeps track of lengths for each trajectory in the big coalesced data_set
len_arr = zeros(num_initial_conditions, 1);
% index for the current trajectory
curr_idx = 1;
for i = 1:length(data_set)
    len_of_current_traj = size(data_set{i},1);
    idx_arr(i) = curr_idx;
    len_arr(i) = len_of_current_traj;
    curr_idx = curr_idx + len_of_current_traj;
end

% due to Matlab's indexing begining from 1, adjust total length
total_len = curr_idx - 1;
% Add 1 for time
data_mat = zeros(total_len, num_continuous_states + 1);

for j = 1:length(data_set)
    % sys_opt.plotFun(plotSet{j}(:,NUM_STATE_VARS+1),plotSet{j}(:,1:NUM_STATE_VARS),currMode);
    plot(data_set{j}(:,1),data_set{j}(:,2))
    % TODO: not sure is appending in parfor is faster or this, need to check
    data_mat(idx_arr(j) : idx_arr(j) + len_arr(j) - 1, :) = data_set{j};
end
%drawnow;
diary off

end

function my_print(msg, data)

fprintf(['==========\n' msg '\n==========\n'])
display(data)
end
