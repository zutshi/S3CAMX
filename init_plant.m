% Initializes the plant defined using a class by calling its
% constructor

function obj = init_plant(class_str)
constructor = str2func(class_str);
obj = constructor();
end
