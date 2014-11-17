function res = iteration1(a1, a2, l1, l2)
    n = 200;
    g = -9.81;
    % use ode45
end

function res = td(tdd, g, L)
    res = cos(asin(-L/g*tdd))*2*g/L;
end
