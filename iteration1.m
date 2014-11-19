function res = iteration1(a1, l1)
    n = 200;
    g = -9.81;
    V = 0;
    [T, O] = ode45(@calc, 0:0.01:100, [a1, V]);
    hold on;
    plot(l1*sin(O(:, 1)), l1*cos(O(:, 1)), 'r');
    res = [O(end, 1), O(end, 2)];
    
    function res = calc(t, W)
        theta = W(1);  % angle of pendulum
        omega = W(2);  % rotational velocity
        dTHETAdt = omega;
        dOMEGAdt = -g*sin(theta)/l1;
        res = [dTHETAdt; dOMEGAdt];
    end
end
