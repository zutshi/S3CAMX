; benchmark generated from python API
(set-info :status unknown)
(declare-fun rv_int_state_arr__3 () Int)
(declare-fun rv_output_arr__0 () Real)
(declare-fun iv_int_state_arr__2 () Int)
(declare-fun rv_int_state_arr__2 () Int)
(declare-fun rv_int_state_arr__1 () Int)
(declare-fun iv_int_state_arr__0 () Int)
(declare-fun rv_int_state_arr__0 () Int)
(declare-fun iv_int_state_arr__1 () Int)
(declare-fun iv_int_state_arr__3 () Int)
(declare-fun iv_x_arr__0 () Real)
(assert
(let (($x33 (= rv_int_state_arr__3 0)))
(let (($x80 (= rv_output_arr__0 2.0)))
(let (($x29 (= rv_int_state_arr__2 (+ iv_int_state_arr__2 1))))
(let (($x78 (= rv_int_state_arr__1 2)))
(let (($x60 (= rv_int_state_arr__0 iv_int_state_arr__0)))
(let (($x59 (<= iv_int_state_arr__0 2)))
(let (($x82 (= iv_int_state_arr__1 2)))
(let (($x39 (< iv_int_state_arr__2 5)))
(let (($x38 (< iv_int_state_arr__3 5)))
(let (($x21 (< iv_x_arr__0 70.0)))
(let (($x67 (>= iv_x_arr__0 66.0)))
(and $x67 $x21 $x38 $x39 $x82 $x59 $x60 $x78 $x29 $x80 $x33)))))))))))))
(check-sat)
