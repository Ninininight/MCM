# 1. 导入Pulp库
from pulp import LpProblem, LpVariable, LpMinimize, LpInteger, value

# 2. 创建问题：目标为最小化总人数（文档中“降低经营成本，人数越少越好”1-95）
prob = LpProblem(name="WorkerScheduling", sense=LpMinimize)

# 3. 定义决策变量：x[i]为第i+1班报到的人数（非负整数）
# 文档中定义“x_i表示第i个班次报到的工人数量，i=1~6”（1-100），这里i=0~5对应6个班次
# 变量类型为LpInteger（纯整数），下界为0（人数不能为负）
x = [LpVariable(name=f"x{i+1}", lowBound=0, cat=LpInteger) for i in range(6)]

# 4. 构建目标函数：总人数=6个班次报到人数之和，即min z=x1+x2+x3+x4+x5+x6
# 文档中目标函数公式为min z=∑x_i（1-105）
total_workers = sum(x)  # 累加6个班次的人数
prob += total_workers, "TotalWorkers"  # 目标：最小化总人数

# 5. 构建约束条件：每班实际人数≥最低需求（文档中1-105的约束）
# 班次1（0:00-4:00）：由第6班报到的人（x6）和第1班报到的人（x1）覆盖，需≥35
prob += x[5] + x[0] >= 35, "Shift1Demand"  # x5是x6，x0是x1

# 班次2（4:00-8:00）：由第1班（x1）和第2班（x2）覆盖，需≥40
prob += x[0] + x[1] >= 40, "Shift2Demand"

# 班次3（8:00-12:00）：由第2班（x2）和第3班（x3）覆盖，需≥50
prob += x[1] + x[2] >= 50, "Shift3Demand"

# 班次4（12:00-16:00）：由第3班（x3）和第4班（x4）覆盖，需≥45
prob += x[2] + x[3] >= 45, "Shift4Demand"

# 班次5（16:00-20:00）：由第4班（x4）和第5班（x5）覆盖，需≥55
prob += x[3] + x[4] >= 55, "Shift5Demand"

# 班次6（20:00-24:00）：由第5班（x5）和第6班（x6）覆盖，需≥30
prob += x[4] + x[5] >= 30, "Shift6Demand"

# 6. 求解问题（CBC求解器适合纯整数规划，效率高）
prob.solve()

# 7. 输出结果（对应文档中“最少需要140人”的结论1-106）
print("例题2：生产线人员排班问题求解结果")
print("="*50)
print(f"求解状态：{prob.status}（1=最优解）")
print("各班次报到人数（x1~x6对应6个班次）：")
for i in range(6):
    print(f"第{i+1}班报到人数：{int(value(x[i]))}")
print(f"最少雇佣总人数：{int(value(prob.objective))}")  # 转换为整数（文档结果为140）
print("="*50)