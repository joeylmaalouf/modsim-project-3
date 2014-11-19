function res = iteration2(a1, l1, a2, l2)
    n = 200;
    g = -9.81;
    v1 = 0;
    v2 = 0;
    [T, O] = ode45(@calc, 0:0.01:100, [a1, a2, v1, v2]);
    hold on;
    plot(l1*sin(O(:, 1)), l1*cos(O(:, 1)), 'r');
    plot(l1*sin(O(:, 1))+l2*sin(O(:, 2)), l1*cos(O(:, 1))+l2*cos(O(:, 2)), 'g');
    res = [O(end, 1), O(end, 2)];
    
    function res = calc(t, W)
        theta1 = W(1);  % angle of pendulum 1
        theta2 = W(2);  % angle of pendulum 2
        omega1 = W(3);  % rotational velocity 1
        omega2 = W(4);  % rotational velocity 1
        dTHETA1dt = omega1;
        dTHETA2dt = omega2;
        dOMEGA1dt = -g*sin(theta1)/l1;
        dOMEGA2dt = -g*sin(theta2)/l2;
        res = [dTHETA1dt; dTHETA2dt; dOMEGA1dt; dOMEGA2dt];
    end
end
