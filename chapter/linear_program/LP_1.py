import pulp

# 1. 创建最大化问题实例（对应文档“机床生产利润最大化”需求）
prob = pulp.LpProblem("例1.2_机床生产优化", pulp.LpMaximize)#LpMinimize

# 2. 定义决策变量（x1=甲机床日产量，x2=乙机床日产量，非负）
x1 = pulp.LpVariable("x1_甲机床日产量", lowBound=0, cat=pulp.LpContinuous)
x2 = pulp.LpVariable("x2_乙机床日产量", lowBound=0, cat=pulp.LpContinuous)

# 3. 设置目标函数（与文档1-13一致：max z=4x1+3x2）
prob += 4 * x1 + 3 * x2, "总利润_千元"

# 4. 添加约束条件（对应文档1-14的机器工时约束）
prob += 2 * x1 + x2 <= 10, "A机器工时约束_10h"
prob += x1 + x2 <= 8, "B机器工时约束_8h"
prob += x2 <= 7, "C机器工时约束_7h"

# 5. 求解（调用CBC求解器，与Matlab求解逻辑一致）
prob.solve()

# 6. 输出结果（验证与文档1-64一致）
print("求解状态：", pulp.LpStatus[prob.status])  # 应输出"Optimal"（最优解）
print("="*50)
print("最优决策变量：")
for var in prob.variables():
    print(f"{var.name} = {round(var.varValue, 2)} 台")  # x1=2.00，x2=6.00
print("="*50)
print("最大总利润：", round(pulp.value(prob.objective), 2), "千元")  # 26.00千元