; benchmark generated from python API
(set-info :status unknown)
(declare-fun rv_output_arr__2 () Real)
(declare-fun rv_output_arr__1 () Real)
(declare-fun rv_output_arr__0 () Real)
(declare-fun iv_float_state_arr__1 () Real)
(declare-fun iv_x_arr__10 () Real)
(declare-fun rv_float_state_arr__6 () Real)
(declare-fun rv_float_state_arr__5 () Real)
(declare-fun rv_float_state_arr__4 () Real)
(declare-fun rv_float_state_arr__3 () Real)
(declare-fun iv_float_state_arr__2 () Real)
(declare-fun iv_x_arr__7 () Real)
(declare-fun iv_x_arr__9 () Real)
(declare-fun rv_float_state_arr__2 () Real)
(declare-fun rv_float_state_arr__1 () Real)
(declare-fun iv_float_state_arr__0 () Real)
(declare-fun rv_float_state_arr__0 () Real)
(declare-fun iv_x_arr__8 () Real)
(declare-fun iv_float_state_arr__4 () Real)
(declare-fun iv_float_state_arr__5 () Real)
(declare-fun iv_float_state_arr__3 () Real)
(assert
(let (($x85 (= rv_output_arr__2 (/ 147.0 10.0))))
(let (($x162 (= rv_output_arr__1 0.0)))
(let (($x83 (= rv_output_arr__0 (/ 83.0 50.0))))
(let ((?x153 (+ (* (* (/ 7.0 50.0) (+ iv_x_arr__10 (- (/ 147.0 10.0)))) (/ 1.0 100.0)) iv_float_state_arr__1)))
(let (($x161 (= rv_float_state_arr__6 (+ (* (/ 1.0 25.0) (+ iv_x_arr__10 (- (/ 147.0 10.0)))) ?x153))))
(let (($x81 (= rv_float_state_arr__5 1.0)))
(let (($x80 (= rv_float_state_arr__4 0.0)))
(let (($x160 (= rv_float_state_arr__3 0.0)))
(let ((?x58 (* (* (* iv_float_state_arr__2 iv_float_state_arr__2) iv_x_arr__7) (- (/ 337.0 10000.0)))))
(let ((?x59 (+ (+ (* (* iv_float_state_arr__2 iv_x_arr__7) (/ 8979.0 100000.0)) (- (/ 183.0 500.0))) ?x58)))
(let ((?x64 (+ ?x59 (* (* (* iv_x_arr__7 iv_x_arr__7) iv_float_state_arr__2) (/ 1.0 10000.0)))))
(let ((?x76 (+ iv_float_state_arr__2 (* (* (+ iv_x_arr__9 (- ?x64)) (/ 2583.0 6250.0)) (/ 1.0 100.0)))))
(let (($x77 (= rv_float_state_arr__2 ?x76)))
(let (($x159 (= rv_float_state_arr__1 ?x153)))
(let ((?x43 (+ iv_float_state_arr__0 (/ 1.0 100.0))))
(let (($x69 (= rv_float_state_arr__0 ?x43)))
(let ((?x66 (/ ?x64 (/ 147.0 10.0))))
(let ((?x175 (* ?x66 100.0)))
(let (($x176 (> ?x175 (/ 83.0 50.0))))
(let ((?x155 (+ 1.0 (+ (* (/ 1.0 25.0) (+ iv_x_arr__10 (- (/ 147.0 10.0)))) ?x153))))
(let (($x174 (> ?x155 100.0)))
(let (($x49 (< iv_x_arr__8 50.0)))
(let (($x47 (and (distinct iv_float_state_arr__4 0.0) true)))
(let (($x46 (and (distinct iv_float_state_arr__5 0.0) true)))
(let (($x45 (< ?x43 10.0)))
(let (($x145 (= iv_float_state_arr__3 0.0)))
(let (($x39 (> iv_x_arr__10 (- 1.0))))
(and $x39 $x145 $x45 $x46 $x47 $x49 $x174 $x176 $x69 $x159 $x77 $x160 $x80 $x81 $x161 $x83 $x162 $x85)))))))))))))))))))))))))))))
;(check-sat)
