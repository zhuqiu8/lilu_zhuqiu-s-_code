% 定义Excel文件的路径
filePath = "D:\Github\RORO_Project\OROR-PROJECT\唯一的文件_第二阶段布局\阶段二布局.csv"; % 替换为实际的文件路径
% 从Excel文件中读取数据到表格中
data = readtable(filePath);


% 将BinID列转换为字符串类型
if iscell(data.BinID)
    data.BinID = string(data.BinID); % 如果BinID是单元格，则转换为字符串
else
    data.BinID = string(data.BinID); % 如果已经是其他类型，直接转换为字符串
end

% 获取所有唯一的Bin ID字符串
binIDs = unique(data.BinID);

% 创建一个结构体来存储每个Bin ID字符串的数据
groupedData = struct();

% 遍历所有的Bin ID字符串，将对应的数据放到结构体中
for i = 1:length(binIDs)
    % 去除空格或其他非法字符，将其替换为下划线
    validBinID = strrep(binIDs(i), ' ', '_');
    
    % 获取当前Bin ID的数据
    currentData = data(data.BinID == binIDs(i), :);
    
    % 将当前数据存储到结构体中
    groupedData.(sprintf('Bin_%s', validBinID)) = currentData;
end


% 创建一个图形
figure('Position', [500, 500, 800, 600]);  % 创建一个更大的图形窗口

d=groupedData.Bin_Bin_12;
% 循环遍历每一行数据来绘制矩形
hold on;
for i = 1:size(d, 1)
    % 提取矩形的位置和大小
    x = d{i, 6};
    y = d{i, 7};
    width = d{i, 4};
    height = d{i, 5};
    brand = d{i, 3}; % 假设第3列是Brand
    
    % 绘制矩形
    rectangle('Position', [x, y, width, height], 'EdgeColor', 'b', 'LineWidth', 1.5);
    
    
end

% 调整图形属性
axis equal;
% 假设x和y坐标的范围是0到100和0到200
x_margin = 20; % 在x轴上增加的边距
y_margin = 30; % 在y轴上增加的边距

% 调整坐标轴范围，加入缓冲区
xlim([min(d{:, 6}) - x_margin, max(d{:, 6}) + x_margin]);
ylim([min(d{:, 7}) - y_margin, max(d{:, 7}) + y_margin]);

xlabel('X Position');
ylabel('Y Position');
title('Visualization of Rectangles in Bin 7');

grid on;

hold off;