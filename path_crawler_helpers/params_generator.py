HEADER = '''
:- module(test_parameters).

:- import create_input_val/3 from substitution.

:- export dom/4.
:- export create_input_vals/2.
:- export unquantif_preconds/2.
:- export quantif_preconds/2.
:- export strategy/2.
:- export precondition_of/2.
'''


IV_INPUT_ARR = '''
% IV_INPUT_ARR
dom('controller',dim(cont(cont('input__controller',_),0)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('input__controller',_),0),_),[],float([{lb}..{ub}])).
'''

IV_INT_STATE_ARR = '''
% IV_INT_STATE_ARR
dom('controller',dim(cont(cont('input__controller',_),1)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('input__controller',_),1),_),[],int([{lb}..{ub}])).
'''

IV_INT_FLOAT_STATE_ARR = '''
% IV_INT_FLOAT_STATE_ARR
dom('controller',dim(cont(cont('input__controller',_),2)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('input__controller',_),2),_),[],float([{lb}..{ub}])).
'''

IV_X_ARR = '''
% IV_X_ARR
dom('controller',dim(cont(cont('input__controller',_),3)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('input__controller',_),3),_),[],float([{lb}..{ub}])).
'''

RV_INT_STATE_ARR = '''
% RV_INT_STATE_ARR
dom('controller',dim(cont(cont('ret_val__controller',_),0)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('ret_val__controller',_),0),_),[],int([{lb}..{ub}])).
'''

RV_INT_FLOAT_STATE_ARR = '''
% RV_INT_FLOAT_STATE_ARR
dom('controller',dim(cont(cont('ret_val__controller',_),1)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('ret_val__controller',_),1),_),[],float([{lb}..{ub}])).
'''

RV_OUTPUT_ARR = '''
% RV_OUTPUT_ARR
dom('controller',dim(cont(cont('ret_val__controller',_),2)),[],int([{dim}..{dim}])).
dom('controller',cont(cont(cont('ret_val__controller',_),2),_),[],float([{lb}..{ub}])).
'''

FOOTER = '''
% add new array domain e.g.:
%  dom('yourFunName',cont('yourArray',_),[],int([min..max])).

create_input_vals('controller',Ins):-
  create_input_val(dim('ret_val__controller'),int([{dim}..{dim}]),Ins),
  create_input_val(dim('input__controller'),int([{dim}..{dim}]),Ins),
  true.
% add new variable domain e.g.:
%  create_input_val(yourVarName,int([min..max]),Ins), 


unquantif_preconds('controller',[]).

quantif_preconds('controller',[]).

strategy('controller',[]).

precondition_of(0,0).

'''

DOUBLE_UB = '1.7976931348623157e+308'
DOUBLE_LB = '-1.7976931348623157e+308'

INT_UB = '2147483647'
INT_LB = '-2147483648'

########################################
# Start printing!
########################################
controller_disturbances = raw_input('controller_disturbances: ')
plant_states = raw_input('plant_states: ')
controller_int_states = raw_input('controller_int_states: ')
controller_float_states = raw_input('controller_float_states: ')
controller_outputs = raw_input('controller_outputs: ')

output_str = ''

#print HEADER
output_str += HEADER

output_str += IV_INPUT_ARR.format(dim=controller_disturbances, lb=DOUBLE_LB, ub=DOUBLE_UB)
#print IV_INPUT_ARR.format(dim=dim, lb=DOUBLE_LB, ub=DOUBLE_UB)

output_str += IV_INT_STATE_ARR.format(dim=controller_int_states, lb=INT_LB, ub=INT_UB)
#print IV_INT_STATE_ARR.format(dim=dim, lb=INT_LB, ub=INT_UB)

output_str += IV_INT_FLOAT_STATE_ARR.format(dim=controller_float_states, lb=DOUBLE_LB, ub=DOUBLE_UB)
#print IV_INT_FLOAT_STATE_ARR.format(dim=dim, lb=DOUBLE_LB, ub=DOUBLE_UB)

output_str += IV_X_ARR.format(dim=plant_states, lb=DOUBLE_LB, ub=DOUBLE_UB)
#print IV_X_ARR.format(dim=dim, lb=DOUBLE_LB, ub=DOUBLE_UB)

output_str += RV_INT_STATE_ARR.format(dim=controller_int_states, lb=INT_LB, ub=INT_UB)
#print RV_INT_STATE_ARR.format(dim=dim, lb=INT_LB, ub=INT_UB)

output_str += RV_INT_FLOAT_STATE_ARR.format(dim=controller_float_states, lb=DOUBLE_LB, ub=DOUBLE_UB)
#print RV_INT_FLOAT_STATE_ARR.format(dim=dim, lb=DOUBLE_LB, ub=DOUBLE_UB)

output_str += RV_OUTPUT_ARR.format(dim=controller_outputs, lb=DOUBLE_LB, ub=DOUBLE_UB)
#print RV_OUTPUT_ARR.format(dim=dim, lb=DOUBLE_LB, ub=DOUBLE_UB)

output_str += FOOTER.format(dim=1)
#print FOOTER.format(dim=1)

print '#############################################'

print output_str
