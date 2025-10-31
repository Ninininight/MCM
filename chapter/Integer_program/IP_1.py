# 1. 导入Pulp库（若未安装，先执行pip install pulp）
from pulp import LpProblem, LpVariable, LpMaximize, LpBinary, value

# 2. 创建整数规划问题：问题名称为"KnapsackProblem"，目标为最大化（LpMaximize）
# 对应文档中“总使用价值最大”的目标（1-23、1-24）
prob = LpProblem(name="KnapsackProblem", sense=LpMaximize)

# 3. 定义决策变量：0-1变量（要么带=1，要么不带=0）
# 文档中明确“x_i=1表示携带第i种物品，x_i=0表示不携带”（1-21）
# 这里定义3个变量，分别对应3件物品，变量名x0、x1、x2，类型为LpBinary（0-1）
x = [LpVariable(name=f"x{i}", cat=LpBinary) for i in range(3)]  # i=0对应第1件，i=1对应第2件，i=2对应第3件

# 4. 构建目标函数：总使用价值=各物品价值×是否携带，即max z=5x0 + 3x1 + 4x2
# 文档中目标函数公式为max z=∑c_i x_i（1-24、1-29）
prob += 5 * x[0] + 3 * x[1] + 4 * x[2], "TotalValue"  # 后面的"TotalValue"是目标函数的名称（自定义）

# 5. 构建约束条件：总质量≤背包最大承重（5千克）
# 文档中约束条件为∑a_i x_i ≤ b（1-26、1-29），这里a=[3,2,3]，b=5
prob += 3 * x[0] + 2 * x[1] + 3 * x[2] <= 5, "WeightConstraint"  # "WeightConstraint"是约束名称（自定义）

# 6. 求解问题：调用Pulp默认的CBC求解器（适用于整数规划）
# 求解器会自动处理0-1约束，找到满足条件的最优解
prob.solve()

# 7. 输出求解结果（分步骤解释，便于理解）
print("="*50)
print("例题1：背包问题求解结果")
print("="*50)
# 输出求解状态（Optimal表示找到最优解，文档中要求“总价值最大”的最优方案）
print(f"求解状态：{prob.status}（1=最优解，2=无可行解，3=无界解）")
# 输出最优解：各物品是否携带（1=带，0=不带）
print("各物品携带方案（1=携带，0=不携带）：")
for i in range(3):
    print(f"第{i+1}件物品：{value(x[i])}")  # value()函数获取变量的最优值
# 输出最大总使用价值（目标函数的最优值）
print(f"最大总使用价值：{value(prob.objective)}")
print("="*50)