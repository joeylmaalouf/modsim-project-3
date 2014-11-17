function res = iteration1(a1, a2, l1, l2)
    P1 = [l1*sin(a1), -l1*cos(a1)];
    % P2 = [l2*sin(a2), -l2*cos(a2)];
    n = 100;
    P = zeros(n, 2);
    P(1, 1) = P1(1);
    P(1, 2) = P1(2);
    for i = 1:n
        % do stuff
    end
end
