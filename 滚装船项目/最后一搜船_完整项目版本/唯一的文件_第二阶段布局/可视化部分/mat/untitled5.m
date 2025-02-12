% 定义Excel文件的路径
filePath = "D:\Github\RORO_Project\OROR-PROJECT\唯一的文件_第二阶段布局\阶段二布局.csv"; % 替换为实际的文件路径

% 从Excel文件中读取数据到表格中
data = readtable(filePath);

% 显示数据的前几行，检查读取的内容
disp(head(data));

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
