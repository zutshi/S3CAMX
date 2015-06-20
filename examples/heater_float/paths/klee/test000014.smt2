; This file conforms to SMTLIBv2 and was generated by KLEE
(set-logic QF_AUFBV )
; Array declarations
;(declare-fun dummy_nextstate_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
;(declare-fun dummy_output_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
;(declare-fun state_arr () (Array (_ BitVec 32) (_ BitVec 8) ) )
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
              (?B1 (concat 
                           (select 
                                   state_arr
                                   (_ bv15 32)
                           )
                           (concat 
                                   (select 
                                           state_arr
                                           (_ bv14 32)
                                   )
                                   (concat 
                                           (select 
                                                   state_arr
                                                   (_ bv13 32)
                                           )
                                           (select 
                                                   state_arr
                                                   (_ bv12 32)
                                           )
                                   )
                           )
                   )
              )
            )
            (and
                (= 
                   false
                   (bvslt 
                          ?B0
                          (_ bv660 32)
                   )
                )
                (and
                    (= 
                       false
                       (bvsle 
                              (_ bv700 32)
                              ?B0
                       )
                    )
                    (and
                        (bvslt 
                               (_ bv4 32)
                               ?B1
                        )
                        (and
                            (= 
                               (_ bv2 32)
                               (concat 
                                       (select 
                                               state_arr
                                               (_ bv7 32)
                                       )
                                       (concat 
                                               (select 
                                                       state_arr
                                                       (_ bv6 32)
                                               )
                                               (concat 
                                                       (select 
                                                               state_arr
                                                               (_ bv5 32)
                                                       )
                                                       (select 
                                                               state_arr
                                                               (_ bv4 32)
                                                       )
                                               )
                                       )
                               )
                            )
                            (and
                                (bvsle 
                                       (_ bv5 32)
                                       (concat 
                                               (select 
                                                       state_arr
                                                       (_ bv11 32)
                                               )
                                               (concat 
                                                       (select 
                                                               state_arr
                                                               (_ bv10 32)
                                                       )
                                                       (concat 
                                                               (select 
                                                                       state_arr
                                                                       (_ bv9 32)
                                                               )
                                                               (select 
                                                                       state_arr
                                                                       (_ bv8 32)
                                                               )
                                                       )
                                               )
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
        (_ bv0 32)
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
        (concat 
                (select 
                        dummy_nextstate_arr
                        (_ bv15 32)
                )
                (concat 
                        (select 
                                dummy_nextstate_arr
                                (_ bv14 32)
                        )
                        (concat 
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv13 32)
                                )
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv12 32)
                                )
                        )
                )
        )
        (bvadd 
               (_ bv1 32)
               ?B1
        )
     )
     (_ bv1 1)
     (_ bv0 1)
                                                                            )
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
                        (_ bv11 32)
                )
                (concat 
                        (select 
                                dummy_nextstate_arr
                                (_ bv10 32)
                        )
                        (concat 
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv9 32)
                                )
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv8 32)
                                )
                        )
                )
        )
     )
     (_ bv1 1)
     (_ bv0 1)
                                                                                   )
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
                        (_ bv7 32)
                )
                (concat 
                        (select 
                                dummy_nextstate_arr
                                (_ bv6 32)
                        )
                        (concat 
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv5 32)
                                )
                                (select 
                                        dummy_nextstate_arr
                                        (_ bv4 32)
                                )
                        )
                )
        )
     )
     (_ bv1 1)
     (_ bv0 1)
                                                                                          )
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
            )
        )
        
)
;(check-sat)
;(exit)
