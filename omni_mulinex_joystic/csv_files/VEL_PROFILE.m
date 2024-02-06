close all
clc

T = 60;
time_grid = 0:1:T;
v = 0.3;
% points = v/3*ones(20);
waypoints = [0, v/3*ones(1,36), 0, 0, 0, 0, 0, 0, -v/3*ones(1,17), 0];
grid = 0:1e-1:T;
velocity = makima(time_grid, waypoints,grid);

figure()
plot(grid, velocity, 'LineWidth', 2)
grid on
% ylim([0, 1])

file_name = '/home/pietro/ros2_ws/src/omni_mulinex_joystic/csv_files/velocity_ref.csv';
writematrix(velocity, file_name)

integ = cumsum(velocity.*1e-1);

figure()
plot(grid, integ, 'LineWidth', 2)
grid on