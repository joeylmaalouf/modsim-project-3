function res = iteration7(a1, l1, a2, l2, mratio)
    % set up our initial numbers
    a1 = a1 * pi / 180;
    a2 = a2 * pi / 180;
    m1 = mratio; m2 = 1; m3 = m1 + m2;
    g = -9.81;
    v1 = 0; v2 = 0;
    % calculate the future angles and velocities over time
    [T, O] = ode113(@calc, 0:0.005:100, [a1, a2, v1, v2]);
    % return the angles and velocities of the two pendulums
    res = [O(end, 1), O(end, 2), O(end, 3), O(end, 4)];
    % calculate x and y coords from length and angle
    coords = zeros(length(O), 4);
    coords(:, 1) = l1 * sin(O(:, 1));
    coords(:, 2) = l1 * cos(O(:, 1));
    coords(:, 3) = l1 * sin(O(:, 1)) + l2 * sin(O(:, 2));
    coords(:, 4) = l1 * cos(O(:, 1)) + l2 * cos(O(:, 2));
    
    V1 = O(:,3)*l1;
    V2 = (O(:,4)*l2).^2 + (l1*O(:,3)).^2 + 2*l1*l2*O(:,3).*O(:,4).* cos(O(:,1)-O(:,2));
    
    U = m1*g*coords(:,2) +m2 * g *coords(:,4);
    K = .5*m1 *V1.^2 + .5*m2*V2;
    E = K -U;
    figure(1)
    plot(E)
    
    figure(2)
    animate(T, coords);
    
    function res = calc(~, W)
        theta1 = mod(W(1), 2 * pi);  % angle of pendulum 1
        theta2 = mod(W(2), 2 * pi);  % angle of pendulum 2
        omega1 = W(3);  % rotational velocity 1
        omega2 = W(4);  % rotational velocity 1
        dTHETA1dt = omega1;
        dTHETA2dt = omega2;
        delta = theta2 - theta1;
        num1 = m2 * l1 * omega1 * omega1 * sin(delta) * cos(delta) ...
            + m2 * g * sin(theta2) * cos(delta) + m2 * l2 * omega2 * omega2 ...
            * sin(delta) - m3 * g * sin(theta1);
        num2 = -m2 * l2 * omega2 * omega2* sin(delta) * cos(delta) ...
            + m3 * g * sin(theta1) * cos(delta) - m3 * l1 * omega1 * omega1 ...
            * sin(delta) - m3 * g * sin(theta2);
        den1 = m3 * l1 - m2 * l1 * cos(delta) * cos(delta);
        den2 = (l2 / l1) * den1;
        dOMEGA1dt = num1 / den1;
        dOMEGA2dt = num2 / den2;
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
            plot(0, 0, 'ko', 'MarkerSize', 10);
            plot(X1(i), Y1(i), 'ro', 'MarkerSize', 10);
            plot(X2(i), Y2(i), 'go', 'MarkerSize', 10);
            plot(X1(1:i), Y1(1:i), 'r.', 'MarkerSize', 4);
            plot(X2(1:i), Y2(1:i), 'g.', 'MarkerSize', 4);
            line([0, X1(i)], [0, Y1(i)]);
            line([X1(i), X2(i)], [Y1(i), Y2(i)]);
            drawnow;
        end
    end
end
