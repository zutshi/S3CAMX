; benchmark generated from python API
(set-info :status unknown)
(declare-fun rv_output_arr__0 () Real)
(declare-fun iv_float_state_arr__0 () Real)
(declare-fun iv_input_arr__0 () Real)
(declare-fun iv_x_arr__0 () Real)
(declare-fun rv_float_state_arr__0 () Real)
(assert
(let ((?x18 (+ (+ 1.0 (- (+ iv_x_arr__0 iv_input_arr__0))) iv_float_state_arr__0)))
(let (($x22 (= rv_float_state_arr__0 ?x18)))
(let ((?x19 (+ (* (+ 1.0 (- (+ iv_x_arr__0 iv_input_arr__0))) 40.0) ?x18)))
(and (> ?x19 20.0) $x22 (= rv_output_arr__0 20.0))))))
;(check-sat)
