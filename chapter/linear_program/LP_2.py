import pulp

# 1. 创建最小化问题实例（对应文档“带绝对值LP的最小化目标”）
prob = pulp.LpProblem("例1.7_带绝对值的LP", pulp.LpMinimize)

# 2. 定义拆分变量（u_i、v_i ≥0，替代原x_i，文档1-108转化逻辑）
u = [pulp.LpVariable(f"u{i+1}", lowBound=0) for i in range(4)]  # u1~u4
v = [pulp.LpVariable(f"v{i+1}", lowBound=0) for i in range(4)]  # v1~v4

# 3. 目标函数（|x1|+2|x2|+3|x3|+4|x4| = u1+v1 + 2(u2+v2) + 3(u3+v3) + 4(u4+v4)）
prob += (u[0] + v[0]) + 2*(u[1] + v[1]) + 3*(u[2] + v[2]) + 4*(u[3] + v[3]), "目标函数z"

# 4. 添加约束条件（x_i=u_i-v_i代入原约束，文档1-113转化逻辑）
prob += (u[0]-v[0]) - (u[1]-v[1]) - (u[2]-v[2]) + (u[3]-v[3]) <= -2, "约束1"
prob += (u[0]-v[0]) - (u[1]-v[1]) + (u[2]-v[2]) - 3*(u[3]-v[3]) <= -1, "约束2"
prob += (u[0]-v[0]) - (u[1]-v[1]) - 2*(u[2]-v[2]) + 3*(u[3]-v[3]) <= -0.5, "约束3"

# 5. 求解
prob.solve()

# 6. 输出结果（还原原变量x_i=u_i-v_i，验证与文档1-114一致）
print("求解状态：", pulp.LpStatus[prob.status])  # 应输出"Optimal"
print("="*50)
print("最优拆分变量(u_i, v_i):")
for i in range(4):
    print(f"u{i+1}={round(u[i].varValue, 4)}, v{i+1}={round(v[i].varValue, 4)}")
print("="*50)
print("还原原变量x_i=u_i-v_i:")
x = [round(u[i].varValue - v[i].varValue, 4) for i in range(4)]
for i in range(4):
    print(f"x{i+1}={x[i]}")  # x1=-2.0, x2=x3=x4=0.0
print("="*50)
print("最小目标函数值z:", round(pulp.value(prob.objective), 4))  # z=2.0