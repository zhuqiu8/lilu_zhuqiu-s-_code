% 文件路径
excel_file = 'C:\Users\zhuqiu\Desktop\第二次模型的输入数据.xlsx';
csv_file = 'D:\Github\RORO_Project\OROR-PROJECT\唯一的文件_第二阶段布局\阶段二布局.csv';
sheet_name = 'Yard_Areas';
column_name = 'yard_names';

% 调用函数
visualize_bins_from_csv_matlab(csv_file, excel_file, sheet_name, column_name);
