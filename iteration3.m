function res = iteration3(a1, l1, a2, l2, mratio)
    m1 = mratio; m2 = 1;
    n = 200; g = -9.81;
    v1 = 0; v2 = 0;
    [T, O] = ode45(@calc, 0:0.01:100, [a1*pi/180, a2*pi/180, v1, v2]);
    hold on;
    plot(l1*sin(O(:, 1)), l1*cos(O(:, 1)), 'r');  % calculate x and y coords from length and angle
    plot(l1*sin(O(:, 1))+l2*sin(O(:, 2)), l1*cos(O(:, 1))+l2*cos(O(:, 2)), 'g');
    res = [O(end, 1), O(end, 2)];
    
    function res = calc(t, W)
        theta1 = W(1);  % angle of pendulum 1
        theta2 = W(2);  % angle of pendulum 2
        omega1 = W(3);  % rotational velocity 1
        omega2 = W(4);  % rotational velocity 1
        dTHETA1dt = omega1; %sqrt((2*(cos(theta1)-cos(a1)))/(m1*l1));
        dTHETA2dt = omega2;
        dOMEGA1dt = (-m2*l1*omega1^2*sin(theta1-theta2)...
            *cos(theta1-theta2)+g*m2*sin(theta2)*cos(theta1-theta2)...
            -m2*l2*omega2^2*sin(theta1-theta2)-(m1+m2)*g*sin(theta1))...
            /(l1*(m1+m2)-m2*l1*cos(theta1-theta2)^2);
        dOMEGA2dt = (m2*l2*omega2^2*sin(theta1-theta2)...
            *cos(theta1-theta2)+g*sin(theta1)*cos(theta1-theta2)...
            *(m1+m2)+l1*omega1^2*sin(theta1-theta2)*(m1+m2)...
            -g*sin(theta2)*(m1+m2))...
            /(l2*(m1+m2)-m2*l2*cos(theta1-theta2)^2);
        res = [dTHETA1dt; dTHETA2dt; dOMEGA1dt; dOMEGA2dt];
    end
end
