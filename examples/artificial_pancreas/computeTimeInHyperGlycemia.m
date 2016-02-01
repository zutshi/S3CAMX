function hyperTime = computeTimeInHyperGlycemia(T,G)
    n = size(T,1);
    assert(size(G,1) == n);
    inHyper=0;
    tHyper = 0;
    hyperLimit=180;
    hyperTime = zeros(n,1);
    for i = 1:n
        hyperTime(i,1) = 0;
        if (G(i,1) >= hyperLimit)
           if (inHyper == 0)
              inHyper=1;
              tHyper = T(i);
           else
              inHyper=1;
              assert(tHyper > 0);
              hyperTime(i,1) = T(i) - tHyper;
           end
        else
           inHyper = 0;
           tHyper=0;
        end
    end

end