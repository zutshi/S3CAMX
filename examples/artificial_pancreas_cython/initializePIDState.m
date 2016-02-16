function ctrlState = initializePIDState(curGs,basal,tPeriod, params)
    
    tdi = 30;
    Kp = tdi/1300;
    
    ctrlState = struct('oldG',curGs,'Kp',Kp,'Td',60,'Ti',160,...
    'insulinMax',5*basal + 6* params.weight * Kp,...
    'I', basal,'target',100,'dt',tPeriod,...
    'iMax',3 * basal, 'gamma',0.5);  
end