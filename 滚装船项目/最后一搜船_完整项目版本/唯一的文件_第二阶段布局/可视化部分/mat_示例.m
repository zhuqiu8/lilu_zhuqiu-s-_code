% Define the data
data = {
    'Bin 7', 0, 'SKYWELL', 2.3, 4.9, 0, 0, false;
    'Bin 7', 1, 'SKYWELL', 2.3, 4.9, 2.4, 0, false;
    'Bin 7', 2, 'SKYWELL', 2.3, 4.9, 4.8, 0, false;
    'Bin 7', 3, 'SKYWELL', 2.3, 4.9, 7.2, 0, false;
    'Bin 7', 4, 'SKYWELL', 2.3, 4.9, 9.6, 0, false;
    'Bin 7', 5, 'SKYWELL', 2.3, 4.9, 12, 0, false;
    'Bin 7', 6, 'SKYWELL', 2.3, 4.9, 0, 5.1, false;
    'Bin 7', 7, 'SKYWELL', 2.3, 4.9, 2.4, 5.1, false;
    'Bin 7', 8, 'SKYWELL', 2.3, 4.9, 4.8, 5.1, false;
    'Bin 7', 9, 'SKYWELL', 2.3, 4.9, 7.2, 5.1, false;
    'Bin 7', 10, 'SKYWELL', 2.3, 4.9, 9.6, 5.1, false;
    'Bin 7', 11, 'SKYWELL', 2.3, 4.9, 12, 5.1, false;
    'Bin 7', 12, 'SKYWELL', 2.3, 4.9, 0, 10.2, false;
    'Bin 7', 13, 'SKYWELL', 2.3, 4.9, 2.4, 10.2, false;
    'Bin 7', 14, 'SKYWELL', 2.3, 4.9, 4.8, 10.2, false;
    'Bin 7', 15, 'SKYWELL', 2.3, 4.9, 7.2, 10.2, false;
};

% Create a figure for the plot
figure;

% Loop through each row of data to plot the rectangles
hold on;
for i = 1:size(data, 1)
    % Extract the rectangle's position and size
    x = data{i, 6};
    y = data{i, 7};
    width = data{i, 4};
    height = data{i, 5};
    
    % Create the rectangle on the plot
    rectangle('Position', [x, y, width, height], 'EdgeColor', 'b', 'LineWidth', 1.5);
end

% Adjust plot properties
axis equal;
xlim([0 15]); % Adjust the x-axis limit based on the layout
ylim([0 15]); % Adjust the y-axis limit based on the layout
xlabel('X Position');
ylabel('Y Position');
title('Visualization of Rectangles in Bin 7');
grid on;

hold off;
