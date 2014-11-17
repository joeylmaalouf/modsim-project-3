function res = iteration1(a1, a2, l1, l2)
    n = 200;
    P = zeros(n, 2);
    P(1, 1) = a1;
    % P(1, 2) = a2;
    for t = 2:n
        P(t, 1) = mod(a1*sin(sqrt(9.81/l1))*t, 360);
        % P(i, 2) = ??
    end
    comet(l1*sin(P(:, 1)), -l1*cos(P(:, 1)));
end
