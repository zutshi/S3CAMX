function idx = searchSorted(arr,val)
% Function: searchSorted
% find max_i array(i) <= val
% arr is sorted ascending

l = 1;
if (size(arr,1) == 1 && size(arr,2) > 1)
    arr=arr';
end

u = size(arr,1)+1;

if (arr(1) > val)
    idx = -1;
    return
end

if (arr(u-1) < val)
   idx = u-1;
   return
end

if (size(arr,1)==1)
   idx = 1;
   return
end

while (l < u-1 )
  
    m = floor((l+u)/2);

    if (arr(m) <= val)
       l = m; 
    else %% arr(m) >= val
       u = m ;
    end
end

idx = l;



end