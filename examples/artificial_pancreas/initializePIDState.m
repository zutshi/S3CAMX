function ctrlState = initializePIDState(curGs,basal,tPeriod, params)
    ctrlState.oldG = curGs;
    tdi = 30;
    ctrlState.Kp = tdi/1300;
    ctrlState.Td = 60;
    ctrlState.Ti = 160;
    ctrlState.insulinMax = 5*basal + 6* params.weight * ctrlState.Kp;
    ctrlState.I = basal;
    ctrlState.target = 100;
    ctrlState.dt = tPeriod;
    ctrlState.iMax = 3 * basal;
    ctrlState.gamma = 0.5;
end