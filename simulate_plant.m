%function [ret_t, ret_X, ret_D, ret_P, pvf] = simulate_system(sim_function, t, T, initial_continuous_states, initial_discrete_states, initial_pvt_states, control_inputs, inputs, property_check)
function ret_cell = simulate_plant(obj, t, T, initial_continuous_states, initial_discrete_states, initial_pvt_states, control_inputs, inputs, property_check)
delete 'log_matlab'
diary log_matlab

%sim_function = str2func(sim_function);

plot_to_debug = 0;

% t
% T
% initial_continuous_states
% initial_discrete_states
% initial_pvt_states
% control_inputs
% inputs
% property_check

% % create plot windows
% figure(1)
% hold on
% figure(2)
% hold on
% figure(3)
% hold on

num_initial_conditions = size(initial_continuous_states, 1);

%num_initial_conditions
%initial_discrete_states
%initial_pvt_states
%inputs

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

pvf_array = zeros(num_initial_conditions, 1);

data_set = cell(1, num_initial_conditions);

for i = 1:num_initial_conditions
    my_print('i', i)
    t0 = t(i,:);
    X0 = initial_continuous_states(i,:);
    D0 = initial_discrete_states(i,:);
    P0 = initial_pvt_states(i,:);
    U0 = control_inputs(i,:);
    I0 = inputs(i,:);

%    class(t0)
%    class(T)
%    class(X0)
%    class(D0)
%    class(P0)
%    class(U0)
%    class(I0)
%    class(property_check)

    %TODO: SIM function can give back arrays describing multiple points on
    %the simulation traces, but need NOT.
    %Is this OK?
    [t_arr,X_arr,D_arr,P_arr,prop_violated_flag] = obj.sim(t0,t0+T,X0,D0,P0,U0,I0,property_check);

    if property_check == 1
        pvf_array(i) = prop_violated_flag;
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
pvf = any(pvf_array);
ret_cell = {ret_t, ret_X, ret_D, ret_P, pvf};
end

function my_print(msg, data)

%fprintf(['==========\n' msg '\n==========\n'])
%display(data)
end
