
![[Pasted image 20251109164222.png]]

```matlab
%% 最小费用最大流 (MCMF) 问题求解

% 1. 初始化环境
clc, clear; 

%% 2. 节点定义
% 构造中间节点名称：'v2', 'v3', 'v4', 'v5'
NN = cellstr(strcat('v', int2str([2:5]'))); 
% 添加起点 ('vs') 和收点 ('vt') 到节点名称列表
nodes = {'vs', NN{:}, 'vt'}; 

%% 3. 边数据定义
% 定义边的信息 L = [起点, 终点, 容量/权重 (C), 费用 (B)]
% 注意：这里 L 矩阵包含 4 列数据
L = {'vs','v2', 5, 3; 
     'vs','v3', 3, 6; 
     'v2','v4', 2, 8; 
     'v3','v2', 1, 2;
     'v3','v5', 4, 2;
     'v4','v3', 1, 1;
     'v4','v5', 3, 4;
     'v4','vt', 2, 10;
     'v5','vt', 5, 2};

%% 4. 创建图和计算最大流

% 初始化一个有向图对象 G
G = digraph; 
% 向图 G 中添加所有节点
G = addnode(G, nodes); 

% G1：用于计算最大流的图 (使用第 3 列作为容量)
% addedge：添加边；cell2mat(L(:,3)) 将容量列转换为数值向量
G1 = addedge(G, L(:,1), L(:,2), cell2mat(L(:,3)));

% [M, F] = maxflow(G1, 源点, 汇点)
[M, F] = maxflow(G1, 'vs', 'vt'); % 求最大流 M
disp(['最大流 M = ', num2str(M)]);

%% 5. 建立最小费用最大流的线性规划模型

% G2：用于导出费用矩阵的图 (使用第 4 列作为权重/费用)
G2 = addedge(G, L(:,1), L(:,2), cell2mat(L(:,4)));

% 导出容量矩阵 c (最大流图的邻接矩阵，权重为容量)
% full(adjacency(G1, 'weighted')) 将稀疏矩阵转换为完整矩阵
c = full(adjacency(G1, 'weighted')); 

% 导出费用矩阵 b (费用图的邻接矩阵，权重为费用)
b = full(adjacency(G2, 'weighted')); 

% 5.1. 定义优化变量 f (流矩阵)
% optimvar('f', 行数, 列数, 'LowerBound', 0)
% f 矩阵的维度与 c, b 相同
f = optimvar('f', 6, 6, 'LowerBound', 0); % 流 f 矩阵，元素 f(i,j) >= 0

% 5.2. 定义优化问题结构
prob = optimproblem; 

% 目标函数：最小化总费用 (sum(sum(b .* f)))
% b .* f 是元素级乘法，然后求和得到总费用
prob.Objective = sum(sum(b .* f)); 

% 5.3. 定义约束条件
% 约束 1：流守恒约束 (Flow Conservation)
% - sum(f(1,:)) == -M : 源点 ('vs', 对应矩阵第 1 行) 的净流出必须等于最大流 M。
% - sum(f([2:end-1],:),2) == sum(f(:,[2:end-1]),2) : 中间节点的流出等于流入。
% - sum(f(:,end)) == M : 汇点 ('vt', 对应矩阵最后一列) 的净流入必须等于最大流 M。
con1 = [sum(f(1,:)) == M; ...
        sum(f([2:end-1],:),2) == sum(f(:,[2:end-1]),2); ...
        sum(f(:,end)) == M]; 

% 约束 2：容量约束 (Capacity Constraint)
% f <= c : 流 f 不能超过容量 c
con2 = f <= c;

% 5.4. 添加约束到问题结构中
prob.Constraints.con1 = con1;
prob.Constraints.con2 = con2;

%% 6. 求解优化问题
% [sol, fval, flag, out] = solve(prob)
% sol: 包含优化变量结果的结构体
% fval: 目标函数的最小值 (即最小费用)
[sol, fval, flag, out] = solve(prob); 

% 从结果结构体中提取最优流矩阵
ff = sol.f; % ff 即为最小费用下的最大流矩阵

disp('--------------------------');
disp(['最小费用 fval = ', num2str(fval)]);
disp('最小费用下的最大流矩阵 ff:');
disp(ff);

```


|**函数 / 属性**|**语法格式**|**详细解释**|**适用场景**|
|---|---|---|---|
|**`strcat`**, **`int2str`**, **`cellstr`**|见前述解释|用于动态生成节点名称 `'v2'` 到 `'v5'`。|节点名称批量生成。|
|**`addnode`**|`G = addnode(G, nodes)`|**向图对象添加节点**。将 `nodes` 中指定的节点名称添加到图 `G` 中。|初始化图结构。|
|**`addedge`**|`G = addedge(G, s, t, weights)`|**向图对象添加边**。`s` 和 `t` 是起点和终点（可以是名称或索引）。`weights` 是边的权重。|基于边列表构建图。|
|**`cell2mat`**|`cell2mat(C)`|**元胞数组转矩阵**。将内容一致的元胞数组 `C` 转换为标准的数值矩阵或数组。此代码用于提取 `L` 中的容量和费用数据。|数据格式转换。|
|**`maxflow`**|`[M, F] = maxflow(G, S, T)`|**计算最大流**。计算从源点 `S` 到汇点 `T` 的最大流量。`M` 是最大流值。|网络最大流问题。|
|**`adjacency`**|`A = adjacency(G, 'weighted')`|**生成带权重的邻接矩阵**。返回图 `G` 的邻接矩阵 `A`。如果指定 `'weighted'`，矩阵元素为边权重（容量或费用），否则为 1。|将图结构转换为矩阵形式。|
|**`optimvar`**|`f = optimvar('f', R, C, 'LowerBound', LB)`|**定义优化变量**。定义名为 `'f'` 的 $R \times C$ 矩阵作为优化变量，并设置下界 `LB`。这里 `f` 代表流矩阵。|建立优化模型。|
|**`optimproblem`**|`prob = optimproblem`|**创建优化问题结构**。初始化一个空的优化问题结构体，用于定义目标函数和约束。|建立优化模型。|
|**`.Objective`**|`prob.Objective = expression`|**定义目标函数**。这里是 $\min \sum (\mathbf{b} \cdot \mathbf{f})$，即最小化总费用。|建立优化模型。|
|**`.Constraints`**|`prob.Constraints.name = constraint`|**添加约束**。将定义的约束（如 `con1`、`con2`）添加到问题结构中。|建立优化模型。|
|**`solve`**|`[sol, fval, ...] = solve(prob)`|**求解优化问题**。求解结构体 `prob` 中定义的线性规划、二次规划或其他优化问题。`sol` 包含优化变量的结果。|求解优化问题。|