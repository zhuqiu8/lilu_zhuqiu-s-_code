% 假设有 5 个客户，3 辆车
N = 5;  % 客户数量
K = 3;  % 车辆数量
d = rand(N+1, N+1);  % 客户之间的距离矩阵（包括配送中心）

% 创建 Gurobi 模型
model = struct();

% 决策变量 x_ijk, 车辆 k 是否从客户 i 到客户 j
model.vars = [];
for k = 1:K
    for i = 1:N
        for j = 1:N
            model.vars = [model.vars; sprintf('x_%d_%d_%d', i, j, k)];
        end
    end
end

% 目标函数：最小化总行驶距离
model.obj = [];
for k = 1:K
    for i = 1:N
        for j = 1:N
            model.obj = [model.obj; d(i,j)];
        end
    end
end

% 约束条件
model.A = [];
model.rhs = [];
model.sense = [];

% 每个客户必须被访问一次
for i = 1:N
    row = zeros(1, length(model.vars));
    for k = 1:K
        for j = 1:N
            varIndex = find(strcmp(model.vars, sprintf('x_%d_%d_%d', i, j, k)));
            row(varIndex) = 1;
        end
    end
    model.A = [model.A; row];
    model.rhs = [model.rhs; 1];
    model.sense = [model.sense; '='];
end

% 每个车辆只访问一次每个客户
for k = 1:K
    for j = 1:N
        row = zeros(1, length(model.vars));
        for i = 1:N
            varIndex = find(strcmp(model.vars, sprintf('x_%d_%d_%d', i, j, k)));
            row(varIndex) = 1;
        end
        model.A = [model.A; row];
        model.rhs = [model.rhs; 1];
        model.sense = [model.sense; '='];
    end
end

% 每辆车只能在客户之间行驶
for k = 1:K
    for i = 1:N
        for j = 1:N
            row = zeros(1, length(model.vars));
            varIndex = find(strcmp(model.vars, sprintf('x_%d_%d_%d', i, j, k)));
            row(varIndex) = 1;
            model.A = [model.A; row];
            model.rhs = [model.rhs; 1];
            model.sense = [model.sense; '<='];
        end
    end
end

% 设置 Gurobi 参数
params.outputflag = 1;  % 输出求解过程

% 求解模型
result = gurobi(model, params);

% 输出结果
if strcmp(result.status, 'OPTIMAL')
    fprintf('Optimal solution found:\n');
    for k = 1:K
        fprintf('Vehicle %d route:\n', k);
        for i = 1:N
            for j = 1:N
                if result.x(strcmp(model.vars, sprintf('x_%d_%d_%d', i, j, k))) > 0.5
                    fprintf('  %d -> %d\n', i, j);
                end
            end
        end
    end
else
    fprintf('No optimal solution found\n');
end
