#  pulp 和 scipy 的线性规划求解步骤对比




## 一、基于pulp求解线性规划的步骤



pulp无需手动转换线性规划标准型，语法直接对应文档中“决策变量-目标函数-约束条件”三要素，步骤如下：



### 步骤1：明确问题与模型要素



从实际问题中提取三大要素：



- **决策变量**：确定需优化的未知量（如产量 $x_1$ 、运量 $x_{ij}$ ），需满足非负约束；

- **目标函数**：明确最大化（如利润）或最小化（如成本），表达式为决策变量的线性函数；

- **约束条件**：梳理线性不等式（≤/≥）或等式（=）约束，包括资源限制、需求匹配等。



### 步骤2：安装并导入pulp库



```Python
# 安装（首次使用时）
# !pip install pulp
import pulp
```



### 步骤3：创建优化问题实例



根据目标函数方向（最大化/最小化），创建问题对象，名称建议与文档案例对应（如“机床生产利润最大化”）：



```Python
# 最大化问题（如文档例1.1的利润最大化）
prob = pulp.LpProblem("问题名称", pulp.LpMaximize)
# 最小化问题（如文档例1.4的仓库租赁成本最小）
# prob = pulp.LpProblem("问题名称", pulp.LpMinimize)
```



### 步骤4：定义决策变量



使用`pulp.LpVariable`定义变量，需指定：



- 变量名称（便于识别，如“x1_甲机床产量”）；

- 下界（`lowBound`，文档中均为0，即非负约束）；

- 变量类型（`cat`，文档中为连续型，设为`pulp.LpContinuous`）：



```Python
# 单变量定义（如文档例1.1的x1、x2）
x1 = pulp.LpVariable("x1_甲机床日产量", lowBound=0, cat=pulp.LpContinuous)
x2 = pulp.LpVariable("x2_乙机床日产量", lowBound=0, cat=pulp.LpContinuous)

# 多变量批量定义（如文档例1.4的仓库租赁x_ij）
# x = pulp.LpVariable.dicts("x_ij", (range(1,5), range(1,5)), lowBound=0)  # 4×4变量矩阵
```



### 步骤5：设置目标函数



通过`prob +=`添加目标函数，表达式需与文档中线性目标函数完全一致（如文档1-13的 $max\ z=4x_1+3x_2$ ）：



```Python
# 最大化目标（文档例1.1）
prob += 4 * x1 + 3 * x2, "总利润_千元"  # 逗号后为目标函数名称（可选）
# 最小化目标（文档例1.4）
# prob += 2800*(x[1][1]+x[2][1]+x[3][1]+x[4][1]) + 4500*(x[1][2]+x[2][2]+x[3][2]) + 6000*(x[1][3]+x[2][3]) + 7300*x[1][4], "总租金_元"
```



### 步骤6：添加约束条件



同样通过`prob +=`添加约束，每个约束需标注名称（便于追溯），表达式严格对应文档中的线性约束（如文档1-14的机器工时约束）：



```Python
# 不等式约束（≤，文档例1.1的A机器工时）
prob += 2 * x1 + x2 <= 10, "A机器工时约束_10h"
# 不等式约束（≥，文档例1.4的1月仓库面积需求）
# prob += x[1][1] + x[1][2] + x[1][3] + x[1][4] >= 15, "1月仓库面积约束_15×100m²"
# 等式约束（=，文档例1.9的总投资约束）
# prob += x0 + 1.01*x1 + 1.02*x2 + 1.045*x3 + 1.065*x4 == 10000, "总投资约束_10000元"
```



### 步骤7：求解优化问题



调用`prob.solve()`求解，默认使用CBC求解器，与文档中Matlab求解器逻辑一致（文档1-50）：



```Python
prob.solve()
```



### 步骤8：查看求解结果



验证求解状态（是否为最优解），并输出决策变量值与目标函数值，结果需与文档一致（如文档1-64的机床生产最优解）：



```Python
# 查看求解状态（Optimal表示找到最优解）
print("求解状态：", pulp.LpStatus[prob.status])
# 输出决策变量值
print("最优决策变量：")
for var in prob.variables():
    print(f"{var.name} = {round(var.varValue, 2)}")
# 输出目标函数值
print("最优目标函数值：", round(pulp.value(prob.objective), 2))
```



## 二、基于scipy求解线性规划的步骤



scipy需手动将模型转换为文档1-54定义的“Matlab标准型”（即`min z = f^T x`，约束`Ax ≤ b`、`Aeq x = beq`、`lb ≤ x ≤ ub`），步骤如下：



### 步骤1：明确问题与标准型转换



根据文档1-57、1-59的转换规则，将原问题调整为scipy适配的标准型：



- 若目标函数为**最大化**（如 $max\ z = c^T x$ ），转换为`min w = -c^T x`（目标函数系数取负）；

- 若约束为**≥型**（如 $Ax ≥ b$ ），转换为`-Ax ≤ -b`（约束系数与右侧值同时取负）；

- 确保所有决策变量满足非负约束（`lb ≥ 0`）。



### 步骤2：安装并导入scipy库



```Python
# 安装（首次使用时）
# !pip install scipy
from scipy.optimize import linprog
import numpy as np  # 可选，用于矩阵处理
```



### 步骤3：定义标准型参数



将文档中的模型要素转换为scipy所需的参数格式：



- `c`：目标函数系数（转换后，最小化方向）；

- `A_ub`/`b_ub`：不等式约束（≤型）的系数矩阵与右侧值；

- `A_eq`/`b_eq`：等式约束的系数矩阵与右侧值；

- `bounds`：变量上下界（文档中均为`(0, None)`，即非负且无上限）。



以文档例1.1（机床生产）为例：



```Python
# 原目标：max z=4x1+3x2 → 转换为min w=-4x1-3x2，故c=[-4, -3]
c = [-4, -3]
# 不等式约束（Ax ≤ b，文档1-14的3个机器约束）
A_ub = [[2, 1], [1, 1], [0, 1]]  # 约束系数矩阵
b_ub = [10, 8, 7]  # 约束右侧值
# 等式约束（无，设为None）
A_eq = None
b_eq = None
# 变量边界（x1≥0, x2≥0）
bounds = [(0, None), (0, None)]
```



### 步骤4：调用linprog求解



使用`scipy.optimize.linprog`函数，指定求解方法（`method='highs'`为高效求解器，适配大规模问题，文档1-50）：



```Python
result = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method='highs'
)
```



### 步骤5：验证结果与还原原问题



检查求解是否成功，并将结果还原为原问题的优化方向（如最大化目标需取负），确保与文档一致：



```Python
# 验证求解状态（success=True表示求解成功）
if result.success:
    print("最优决策变量：")
    print(f"x1_甲机床日产量 = {round(result.x[0], 2)} 台")
    print(f"x2_乙机床日产量 = {round(result.x[1], 2)} 台")
    # 还原最大化目标（原z = -result.fun）
    print("最大总利润（千元）：", round(-result.fun, 2))  # 与文档1-64一致，输出26.0
else:
    print("求解失败，原因：", result.message)
```



## 三、两种工具求解步骤对比（基于文档模型）



|步骤环节|pulp（灵活型）|scipy（标准型）|
|---|---|---|
|标准型依赖|无需转换，直接支持max/min、≤/≥/=|需手动转换为min目标+≤约束，适配文档1-54标准型|
|变量定义|`LpVariable`/`LpVariable.dicts`，支持命名与批量定义|通过`bounds`指定，无显式名称，需按索引对应|
|约束添加|`prob += 约束式`，支持自然语言标注|需构建`A_ub`/`b_ub`矩阵，格式严格|
|结果还原|直接调用`pulp.value(prob.objective)`|最大化目标需取负（`-result.fun`）|
|适用场景|文档中复杂LP（如例1.4仓库租赁、例1.9投资组合）|文档中基础LP（如例1.1机床生产、例1.7绝对值问题）|