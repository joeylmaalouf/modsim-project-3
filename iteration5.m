function res = iteration5(a1, l1, a2, l2, mratio)
    a1 = a1*pi/180;
    a2 = a2*pi/180;
    m1 = mratio; m2 = 1;
    n = 200; g = -9.81;
    v1 = 0; v2 = 0;
    [T, O] = ode45(@calc, 0:0.01:100, [a1, a2, v1, v2]);
    res = [O(end, 1), O(end, 2)];
    % calculate x and y coords from length and angle
    coords = zeros(length(O), 4);
    coords(:, 1) = l1*sin(O(:, 1));
    coords(:, 2) = l1*cos(O(:, 1));
    coords(:, 3) = l1*sin(O(:, 1))+l2*sin(O(:, 2));
    coords(:, 4) = l1*cos(O(:, 1))+l2*cos(O(:, 2));
    animate(T, coords);
    
    function res = calc(t, W)
        theta1 = W(1);  % angle of pendulum 1
        theta2 = W(2);  % angle of pendulum 2
        omega1 = W(3);  % rotational velocity 1
        omega2 = W(4);  % rotational velocity 1
        dTHETA1dt = sqrt((2*(cos(theta1)-cos(a1)))/(m1*l1));
        dTHETA2dt = omega2;  % FIX
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
    
    function animate(T, C)
        X1 = C(:,1); Y1 = C(:,2);
        X2 = C(:,3); Y2 = C(:,4);
        minmax = [min([X1;X2]), max([X1;X2]), min([Y1;Y2]), max([Y1;Y2])];
        for i=1:length(T)
            clf;
            axis(minmax);
            hold on;
            plot(X1(i), Y1(i), 'ro', 'MarkerSize', 10);
            plot(X2(i), Y2(i), 'go', 'MarkerSize', 10);
            plot(X1(1:i), Y1(1:i), 'r.', 'MarkerSize', 4);
            plot(X2(1:i), Y2(1:i), 'g.', 'MarkerSize', 4);
            line([X1(i), X2(i)], [Y1(i), Y2(i)]);
            drawnow;
        end
    end
end
