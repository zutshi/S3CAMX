; benchmark generated from python API
(set-info :status unknown)
(declare-fun rv_int_state_arr__3 () Int)
(declare-fun rv_output_arr__0 () Real)
(declare-fun iv_int_state_arr__2 () Int)
(declare-fun rv_int_state_arr__2 () Int)
(declare-fun rv_int_state_arr__1 () Int)
(declare-fun rv_int_state_arr__0 () Int)
(declare-fun iv_int_state_arr__1 () Int)
(declare-fun iv_int_state_arr__3 () Int)
(declare-fun iv_x_arr__0 () Real)
(assert
(let (($x33 (= rv_int_state_arr__3 0)))
(let (($x31 (= rv_output_arr__0 1.0)))
(let (($x29 (= rv_int_state_arr__2 (+ iv_int_state_arr__2 1))))
(let (($x27 (= rv_int_state_arr__1 1)))
(let (($x26 (= rv_int_state_arr__0 1)))
(let (($x25 (and (distinct iv_int_state_arr__1 1) true)))
(let (($x23 (>= iv_int_state_arr__3 5)))
(let (($x21 (< iv_x_arr__0 70.0)))
(let (($x19 (< iv_x_arr__0 66.0)))
(and $x19 $x21 $x23 $x25 $x26 $x27 $x29 $x31 $x33)))))))))))
(check-sat)
