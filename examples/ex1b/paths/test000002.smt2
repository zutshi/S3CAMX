; This file conforms to SMTLIBv2 and was generated by KLEE
(set-logic QF_AUFBV )
; Array declarations
;(declare-fun dummy_nextstate_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
;(declare-fun dummy_output_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
;(declare-fun x_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
(assert
        (let
            ( 
              (?B0 (concat 
                           (select 
                                   x_arr
                                   (_ bv3 32)
                           )
                           (concat 
                                   (select 
                                           x_arr
                                           (_ bv2 32)
                                   )
                                   (concat 
                                           (select 
                                                   x_arr
                                                   (_ bv1 32)
                                           )
                                           (select 
                                                   x_arr
                                                   (_ bv0 32)
                                           )
                                   )
                           )
                   )
              )
            )
            (and
                (= 
                   false
                   (bvsle 
                          ?B0
                          (_ bv2799 32)
                   )
                )
                (and
                    (= 
                       false
                       (bvslt 
                              (_ bv2805 32)
                              ?B0
                       )
                    )
                    (and
                        (= 
                           false
                           (= 
                              (_ bv0 32)
                              (bvand 
                                     (bvand 
                                            ((_ zero_extend 31) 
                                                                
                                                                ;Performing implicit bool to bitvector cast
(ite
     (= 
        (_ bv4294957296 32)
        (concat 
                (select 
                        dummy_output_arr
                        (_ bv3 32)
                )
                (concat 
                        (select 
                                dummy_output_arr
                                (_ bv2 32)
                        )
                        (concat 
                                (select 
                                        dummy_output_arr
                                        (_ bv1 32)
                                )
                                (select 
                                        dummy_output_arr
                                        (_ bv0 32)
                                )
                        )
                )
        )
     )
     (_ bv1 1)
     (_ bv0 1)
                                                                )
                                            )
                                            (_ bv1 32)
                                     )
                                     (bvand 
                                            ((_ zero_extend 31) 
                                                                
                                                                ;Performing implicit bool to bitvector cast
(ite
     (= 
        (_ bv0 32)
        (concat 
                (select 
                        dummy_nextstate_arr
                        (_ bv3 32)
                )
                (concat 
                        (select 
                                dummy_nextstate_arr
                                (_ bv2 32)
                        )
                        (concat 
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv1 32)
                                )
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv0 32)
                                )
                        )
                )
        )
     )
     (_ bv1 1)
     (_ bv0 1)
                                                                )
                                            )
                                            (_ bv1 32)
                                     )
                              )
                           )
                        )
                        ; query
                        true
                    )
                )
            )
        )
        
)
;(check-sat)
;(exit)
