; benchmark generated from python API
(set-info :status unknown)
(declare-fun rv_output_arr__2 () Real)
(declare-fun rv_output_arr__1 () Real)
(declare-fun rv_output_arr__0 () Real)
(declare-fun iv_float_state_arr__6 () Real)
(declare-fun rv_float_state_arr__6 () Real)
(declare-fun rv_float_state_arr__5 () Real)
(declare-fun rv_float_state_arr__4 () Real)
(declare-fun rv_float_state_arr__3 () Real)
(declare-fun iv_float_state_arr__2 () Real)
(declare-fun iv_x_arr__7 () Real)
(declare-fun iv_x_arr__9 () Real)
(declare-fun rv_float_state_arr__2 () Real)
(declare-fun iv_float_state_arr__1 () Real)
(declare-fun rv_float_state_arr__1 () Real)
(declare-fun iv_float_state_arr__0 () Real)
(declare-fun rv_float_state_arr__0 () Real)
(declare-fun iv_x_arr__8 () Real)
(declare-fun iv_float_state_arr__4 () Real)
(declare-fun iv_float_state_arr__5 () Real)
(declare-fun iv_float_state_arr__3 () Real)
(declare-fun iv_x_arr__10 () Real)
(assert
(let (($x85 (= rv_output_arr__2 (/ 147.0 10.0))))
(let (($x84 (= rv_output_arr__1 1.0)))
(let (($x90 (= rv_output_arr__0 (/ 13.0 100.0))))
(let (($x82 (= rv_float_state_arr__6 iv_float_state_arr__6)))
(let (($x119 (= rv_float_state_arr__5 0.0)))
(let (($x99 (= rv_float_state_arr__4 1.0)))
(let (($x79 (= rv_float_state_arr__3 1.0)))
(let ((?x58 (* (* (* iv_float_state_arr__2 iv_float_state_arr__2) iv_x_arr__7) (- (/ 337.0 10000.0)))))
(let ((?x59 (+ (+ (* (* iv_float_state_arr__2 iv_x_arr__7) (/ 8979.0 100000.0)) (- (/ 183.0 500.0))) ?x58)))
(let ((?x64 (+ ?x59 (* (* (* iv_x_arr__7 iv_x_arr__7) iv_float_state_arr__2) (/ 1.0 10000.0)))))
(let ((?x76 (+ iv_float_state_arr__2 (* (* (+ iv_x_arr__9 (- ?x64)) (/ 2583.0 6250.0)) (/ 1.0 100.0)))))
(let (($x77 (= rv_float_state_arr__2 ?x76)))
(let (($x70 (= rv_float_state_arr__1 iv_float_state_arr__1)))
(let ((?x43 (+ iv_float_state_arr__0 (/ 1.0 100.0))))
(let (($x69 (= rv_float_state_arr__0 ?x43)))
(let ((?x66 (/ ?x64 (/ 147.0 10.0))))
(let (($x89 (< ?x66 (/ 13.0 100.0))))
(let (($x87 (<= ?x66 (/ 83.0 50.0))))
(let (($x95 (>= iv_x_arr__8 50.0)))
(let (($x47 (and (distinct iv_float_state_arr__4 0.0) true)))
(let (($x118 (= iv_float_state_arr__5 0.0)))
(let (($x45 (< ?x43 10.0)))
(let (($x41 (and (distinct iv_float_state_arr__3 0.0) true)))
(let (($x39 (> iv_x_arr__10 (- 1.0))))
(and $x39 $x41 $x45 $x118 $x47 $x95 $x87 $x89 $x69 $x70 $x77 $x79 $x99 $x119 $x82 $x90 $x84 $x85))))))))))))))))))))))))))
;(check-sat)
