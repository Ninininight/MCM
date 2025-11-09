![[Pasted image 20251109170913.png]]


---

### 1. 数学模型

这是一个有两个变量 ($x_1, x_2$) 的**非线性规划 (NLP)** 问题：

$$\min f(\mathbf{x}) = x_1^2 + x_2^2 - 4x_1 + 4$$

**约束条件 (s.t. - subject to):**

$$g_1(\mathbf{x}) = -x_1 + x_2 - 2 \le 0$$

$$g_2(\mathbf{x}) = x_1^2 - x_2 + 1 \le 0$$

$$x_1 \ge 0, x_2 \ge 0$$

### 2. 凸性分析（理论基础）

为了确定这是一个**凸规划问题 (Convex Programming)**，需要检查目标函数 $f(\mathbf{x})$ 和约束函数 $g_i(\mathbf{x})$ 的凸性：

#### 目标函数 $f(\mathbf{x})$ 的 Hessian 矩阵 $\mathbf{H}_f$：

- 一阶偏导：
    
    $$\frac{\partial f}{\partial x_1} = 2x_1 - 4 \quad \frac{\partial f}{\partial x_2} = 2x_2$$
    
- 二阶偏导（Hessian 矩阵 $\mathbf{H}_f$）：
    
    $$\mathbf{H}_f = \begin{vmatrix} \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} \\ \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} \end{vmatrix} = \begin{vmatrix} 2 & 0 \\ 0 & 2 \end{vmatrix}$$
    
- **结论：** 由于 $\mathbf{H}_f$ 的所有主子式行列式 ($\mathbf{H}_1=2 > 0, \mathbf{H}_2=4 > 0$) 均大于零，$\mathbf{H}_f$ 是正定矩阵。因此，$f(\mathbf{x})$ 是**严格凸函数**。
    

#### 约束函数 $g_2(\mathbf{x}) = x_1^2 - x_2 + 1$ 的 Hessian 矩阵 $\mathbf{H}_{g_2}$：

- 一阶偏导：
    
    $$\frac{\partial g_2}{\partial x_1} = 2x_1 \quad \frac{\partial g_2}{\partial x_2} = -1$$
    
- 二阶偏导（Hessian 矩阵 $\mathbf{H}_{g_2}$）：
    
    $$\mathbf{H}_{g_2} = \begin{vmatrix} 2 & 0 \\ 0 & 0 \end{vmatrix}$$
    
- **结论：** $\mathbf{H}_{g_2}$ 的特征值是 $2$ 和 $0$ (或主子式行列式 $\mathbf{H}_1=2 > 0, \mathbf{H}_2=0$)，是**半正定矩阵**，因此 $g_2(\mathbf{x})$ 是**凸函数**。
    

#### 约束函数 $g_1(\mathbf{x}) = -x_1 + x_2 - 2$ 和 $x_i \ge 0$：

- 这两个是**线性函数**，线性函数同时是凸函数和凹函数。
    
- **最终结论：** 这是一个**凸规划问题**（目标函数是凸函数，约束集合由凸函数定义）。凸规划的局部最优解就是全局最优解。
    

---

### 3. MATLAB 代码实现分析（问题求解法）

代码使用 MATLAB 优化工具箱的**问题求解 (Problem-Based)** 方法来求解这个非线性规划问题。

|**代码行**|**语法及功能**|**对应数学模型**|
|---|---|---|
|`clc, clear, prob = optimproblem;`|初始化环境并创建优化问题结构 `prob`。|-|
|`x = optimvar('x', 2, 'LowerBound', 0);`|定义优化变量 $\mathbf{x}$ 为 $2 \times 1$ 向量（即 $x_1, x_2$），设置**下界约束** $x_1 \ge 0, x_2 \ge 0$。|$x_1 \ge 0, x_2 \ge 0$|
|`prob.Objective = sum(x.^2) - 4 * x(1) + 4;`|定义**目标函数**。`sum(x.^2)` 即 $x_1^2 + x_2^2$。|$\min x_1^2 + x_2^2 - 4x_1 + 4$|
|`con = [-x(1) + x(2) - 2 <= 0; x(1)^2 - x(2) + 1 <= 0];`|定义**非线性不等式约束** $g_1(\mathbf{x}) \le 0$ 和 $g_2(\mathbf{x}) \le 0$。|$g_1(\mathbf{x}) \le 0, g_2(\mathbf{x}) \le 0$|
|`prob.Constraints.con = con;`|将约束添加到问题结构中。|-|
|`x0.x = rand(2,1);`|**定义初始点** $\mathbf{x}^{(0)}$。对于非线性规划，需要提供初始猜测值。`rand(2,1)` 生成 $2 \times 1$ 的随机向量。|-|
|`[sol, fval, flag, out] = solve(prob, x0);`|**求解问题**。使用初始点 `x0` 求解 `prob`，调用的是 `fmincon` 求解器（针对 NLP）。|-|

### 4. 结果（与图片吻合）

- **最优解 (Optimal Solution):** $\mathbf{x}^* = [0.5536, 1.3064]^T$
    
- **目标函数最优值 (Optimal Value):** $f(\mathbf{x}^*) = 3.7989$





### 5.代码
```matlab
%% 非线性规划问题求解：min f(x1, x2) = x1^2 + x2^2 - 4x1 + 4

% 1. 初始化环境
clc, clear; 

% 2. 创建优化问题结构
prob = optimproblem;

% 3. 定义优化变量 x
% optimvar('名称', 维度, 'LowerBound', 下界)
% x 是一个 2x1 向量，代表 [x1; x2]，下界为 0 对应约束 x1>=0, x2>=0
x = optimvar('x', 2, 'LowerBound', 0); 

% 4. 定义目标函数 (Objective Function)
% sum(x.^2) = x1^2 + x2^2
% x(1) 代表 x1
prob.Objective = sum(x.^2) - 4 * x(1) + 4;

% 5. 定义约束条件 (Constraints)
% con 是一个约束数组，包含两个非线性不等式约束
% con(1): -x1 + x2 - 2 <= 0
% con(2): x1^2 - x2 + 1 <= 0
con = [-x(1) + x(2) - 2 <= 0; 
       x(1)^2 - x(2) + 1 <= 0]; 

% 6. 将约束添加到问题结构中
prob.Constraints.con = con;

% 7. 定义初始点 x0
% 对于非线性规划，必须提供初始猜测值。这里使用随机数。
x0.x = rand(2, 1); 

% 8. 求解问题
% [sol, fval, flag, out] = solve(prob, x0)
% sol: 包含最优变量值的结构体
% fval: 目标函数的最小值 (最优值)
[sol, fval, flag, out] = solve(prob, x0);

% 9. 显示结果 (打印 sol.x 和 fval 的值)
disp('最优解 x* =');
disp(sol.x);
disp(['目标函数最优值 f(x*) = ', num2str(fval)]);
```
