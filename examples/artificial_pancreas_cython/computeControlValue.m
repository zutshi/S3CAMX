function [basalCmd,newState, intrnlInsulin] = computeControlValue(G,IpPred,ctrlState)
    dG = (G - ctrlState.oldG)/ctrlState.dt;
    P = ctrlState.Kp * (G  - ctrlState.target);
    I = ctrlState.I + ctrlState.Kp/ctrlState.Ti * (G - ctrlState.target);
    D = ctrlState.Kp * ctrlState.Td * dG;
    
%     if ( I >= ctrlState.iMax)
%        I = ctrlState.iMax; 
%     end
    
    rawBasal = P + I + D;
    rawBasal = rawBasal - ctrlState.gamma * IpPred;
    intrnlInsulin = rawBasal;
    if (rawBasal <= 0)
        rawBasal = 0;
    else
       if (rawBasal >= ctrlState.insulinMax)
          rawBasal = ctrlState.insulinMax;
       end
    end
    
    basalCmd = rawBasal ;
    newState = ctrlState;
    newState.oldG = G;
    
end