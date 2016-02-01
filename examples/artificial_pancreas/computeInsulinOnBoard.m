function iob = computeInsulinOnBoard(bolus, T, iValues, curTime)
iobTimes=[0; 10; 20; 30; 40; 50; 60; 70; 80; 90; 100; 110; 120; 130; 140; 180; 240; 300; 360; 420; 720];
iobValues = 1/350 *   [ 0; 10; 40; 80;  110;  130;  140; 150; 140; 125;110; 90;75; 60;  50; 30; 25;10; 5; 0; 0];
pp = pchip(iobTimes,iobValues);
iob = 0;
nB = size(bolus.times,1);
for i = 1:nB
   ti = bolus.times(i);
   if (ti <= curTime)
      iob = iob + bolus.values(i)*60/5* ppval(pp, (curTime - ti)); %% Convert bolus in U/hr by assuming it was delivered in 5 minutes
   end
end

n  = size(T,1);
if ( n > 2) 
    for i = (n-1):-1:(n-40)
       ti = T(i);
       tip = min(T(i+1), curTime);
       m = 0.5 * (ti + tip);
       if (tip < curTime)
          v = ppval(pp, (curTime - m));
          iob = iob + v *  iValues(i) ;
           
       end
       
    end

end

end