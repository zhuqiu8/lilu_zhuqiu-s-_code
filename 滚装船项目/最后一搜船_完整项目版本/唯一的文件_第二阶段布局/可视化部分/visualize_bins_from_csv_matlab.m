function visualize_bins_from_csv_matlab(csv_filename, excel_file, sheet_name, column_name)
    % 从 Excel 文件读取堆场名称
    yard_names = read_excel_yard_names(excel_file, sheet_name, column_name);

    % 从 CSV 文件中读取数据
    data = readtable(csv_filename);

    % 提取唯一品牌并为每个品牌分配颜色
    brands = unique(data.Brand);
    num_brands = length(brands);
    colors = lines(num_brands); % 使用 MATLAB 的默认颜色调色板

    % 创建品牌颜色映射表
    brand_colors = containers.Map(brands, num2cell(colors, 2));

    % 按 Bin ID 分组数据
    bin_ids = unique(data.BinID);

    % 遍历每个 Bin 并绘制图形
    for i = 1:length(bin_ids)
        bin_id = bin_ids{i};
        bin_data = data(strcmp(data.BinID, bin_id), :);

        % 获取 Bin 索引和对应的堆场名称
        bin_index = sscanf(bin_id, 'Bin %d') - 1;
        if bin_index >= 0 && bin_index < length(yard_names)
            bin_name = yard_names{bin_index + 1};
        else
            bin_name = bin_id;
        end

        % 为 Bin 布局创建新图
        figure;
        hold on;
        title([bin_name, ' 布局']);
        xlabel('宽度');
        ylabel('高度');

        % 绘制矩形并添加图例
        legend_handles = gobjects(num_brands, 1);
        for j = 1:size(bin_data, 1) % 使用 size 函数获取行数
            rect = bin_data(j, :);
            x = rect.X;
            y = rect.Y;
            width = rect.Width;
            height = rect.Height;
            brand = rect.Brand{1};
            color = brand_colors(brand);

            % 绘制矩形
            rectangle('Position', [x, y, width, height], 'EdgeColor', 'k', ...
                      'FaceColor', color, 'LineWidth', 1);

            % 如果图例中尚未添加该品牌，则添加
            if isempty(find(legend_handles, @(h) ~isempty(h) && strcmp(h.DisplayName, brand), 1))
                legend_handles(j) = plot(NaN, NaN, 'Color', color, 'LineWidth', 4, 'DisplayName', brand);
            end
        end

        % 为图添加图例
        legend(legend_handles, 'Location', 'bestoutside', 'Title', '品牌');
        axis equal;
        hold off;
    end
end

function yard_names = read_excel_yard_names(file_path, sheet_name, column_name)
    % 从 Excel 文件中读取堆场名称
    data = readtable(file_path, 'Sheet', sheet_name);
    yard_names = data.(column_name);
end
