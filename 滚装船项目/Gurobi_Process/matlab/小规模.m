% 参数
B = 3;  % 品牌数量
J = [5, 7, 6];  % 每个品牌的车辆数量
K = 4;  % 堆场数量
l = {[4, 5, 3, 6, 4], [3, 4, 3, 5, 4, 6, 2], [2, 4, 6, 5, 3, 4]};  % 每辆车的长度
w = {[2, 3, 1, 4, 2], [2, 3, 2, 4, 3, 3, 1], [3, 4, 3, 4, 2, 1]};  % 每辆车的宽度
A = [100*34, 270*14.5, 270*34, 225*34];  % 堆场面积
alpha = 0.5;  % 品牌集中度权重
beta = 0.5;  % 堆场未使用面积权重

% 计算每辆车的面积 a_j^i
a = cell(B, 1);  % 存储每辆车的面积
for i = 1:B
    a{i} = l{i} .* w{i};  % 每辆车的面积为长度 * 宽度
end

% 决策变量
nVars = sum(J)*K + B*K;  % x_{ijk} 和 y_{ik}
lb = zeros(nVars, 1);
ub = ones(nVars, 1);
ctype = repmat('B', nVars, 1);  % 二进制变量

% 变量索引
x_idx = @(i, j, k) (sum(J(1:i-1)) + j - 1) * K + k;  % x 的索引
y_idx = @(i, k) sum(J)*K + (i-1)*K + k;             % y 的索引

% 目标函数：品牌集中度 + 堆场未使用面积
f = zeros(nVars, 1);
% 品牌集中度
for i = 1:B
    for k = 1:K
        f(y_idx(i, k)) = alpha;  % 目标函数中只需要 y
    end
end

% 约束 1: 每辆车必须分配到一个堆场
Aeq = [];
beq = [];
for i = 1:B
    for j = 1:J(i)
        eq_row = zeros(1, nVars);
        for k = 1:K
            eq_row(x_idx(i, j, k)) = 1;
        end
        Aeq = [Aeq; eq_row];
        beq = [beq; 1];  % 每辆车只能分配到一个堆场
    end
end

% 约束 2: 辅助变量 y_k^i 的关系
Aineq = [];
bineq = [];
for i = 1:B
    for k = 1:K
        for j = 1:J(i)
            ineq_row = zeros(1, nVars);
            ineq_row(x_idx(i, j, k)) = -1;  % -x_{ijk}
            ineq_row(y_idx(i, k)) = 1;     % +y_{ik}
            Aineq = [Aineq; ineq_row];
            bineq = [bineq; 0];  % y_k^i >= x_{ijk}
        end
    end
end

% 约束 3: 堆场容量限制
for k = 1:K
    ineq_row = zeros(1, nVars);
    for i = 1:B
        for j = 1:J(i)
            ineq_row(x_idx(i, j, k)) = a{i}(j);  % a_j^i * x_{jk}^i
        end
    end
    Aineq = [Aineq; ineq_row];
    bineq = [bineq; A(k)];  % 堆场容量限制
end

% 使用 MATLAB 优化工具求解
opts = optimoptions('intlinprog', 'Display', 'iter');
[x_sol, fval, exitflag] = intlinprog(f, 1:nVars, Aineq, bineq, Aeq, beq, lb, ub, opts);

% 解析结果
if exitflag == 1
    disp('Optimal solution found:');
    for i = 1:B
        for j = 1:J(i)
            for k = 1:K
                if x_sol(x_idx(i, j, k)) > 0.5
                    fprintf('Car %d of Brand %d assigned to Yard %d\n', j, i, k);
                end
            end
        end
    end
else
    disp('No optimal solution found.');
end
