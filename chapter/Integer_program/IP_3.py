# 1. 导入所需库：Pulp（变量定义）、numpy（随机抽样）
from pulp import LpVariable, LpInteger
import numpy as np

# 2. 步骤1：用Pulp定义例2.9的变量（匹配文档约束1-163）
# 定义5个整数变量x1~x5，范围0~99（lowBound=0，upperBound=99，类型LpInteger）
x1 = LpVariable(name="x1", lowBound=0, upperBound=99, cat=LpInteger)
x2 = LpVariable(name="x2", lowBound=0, upperBound=99, cat=LpInteger)
x3 = LpVariable(name="x3", lowBound=0, upperBound=99, cat=LpInteger)
x4 = LpVariable(name="x4", lowBound=0, upperBound=99, cat=LpInteger)
x5 = LpVariable(name="x5", lowBound=0, upperBound=99, cat=LpInteger)

# 提取变量取值范围（从Pulp变量中获取，确保与文档约束一致）
var_bounds = {
    "x1": (x1.lowBound(), x1.upperBound()),
    "x2": (x2.lowBound(), x2.upperBound()),
    "x3": (x3.lowBound(), x3.upperBound()),
    "x4": (x4.lowBound(), x4.upperBound()),
    "x5": (x5.lowBound(), x5.upperBound())
}
print("变量取值范围（文档约束：0≤x_i≤99）：")
for var, bounds in var_bounds.items():
    print(f"{var}: {bounds[0]}~{bounds[1]}")

# 3. 步骤2：定义目标函数与约束条件（文档1-163）
def calculate_objective(x1, x2, x3, x4, x5):
    """计算目标函数值（最大化，文档公式）"""
    return (x1**2 + x2**2 + 3*x3**2 + 4*x4**2 + 2*x5**2 
            - 8*x1 - 2*x2 - 3*x3 - x4 - 2*x5)

def is_feasible(x1, x2, x3, x4, x5):
    """判断解是否满足所有约束条件（文档约束1~5）"""
    # 约束1：0≤x_i≤99（已通过抽样范围保证，此处可二次验证）
    if not (0<=x1<=99 and 0<=x2<=99 and 0<=x3<=99 and 0<=x4<=99 and 0<=x5<=99):
        return False
    # 约束2：x1+x2+x3+x4+x5 ≤400
    if x1 + x2 + x3 + x4 + x5 > 400:
        return False
    # 约束3：x1+2x2+2x3+x4+6x5 ≤800
    if x1 + 2*x2 + 2*x3 + x4 + 6*x5 > 800:
        return False
    # 约束4：2x1+x2+6x3 ≤200
    if 2*x1 + x2 + 6*x3 > 200:
        return False
    # 约束5：x3+x4+5x5 ≤200
    if x3 + x4 + 5*x5 > 200:
        return False
    return True  # 满足所有约束，为可行解

# 4. 步骤3：蒙特卡洛抽样（文档1-164、1-168）
np.random.seed(0)  # 固定随机种子，保证结果可复现
n_samples = 10**6  # 抽样次数（文档建议10^6次，平衡精度与速度）
best_value = -np.inf  # 初始最优目标函数值（最小化设inf，最大化设-inf）
best_solution = None  # 初始最优解（存储x1~x5）

print(f"\n开始蒙特卡洛抽样（共{int(n_samples/1000)}千次）...")
for sample in range(n_samples):
    # 生成符合Pulp变量范围的随机整数（0~99）
    x1_rand = np.random.randint(var_bounds["x1"][0], var_bounds["x1"][1]+1)
    x2_rand = np.random.randint(var_bounds["x2"][0], var_bounds["x2"][1]+1)
    x3_rand = np.random.randint(var_bounds["x3"][0], var_bounds["x3"][1]+1)
    x4_rand = np.random.randint(var_bounds["x4"][0], var_bounds["x4"][1]+1)
    x5_rand = np.random.randint(var_bounds["x5"][0], var_bounds["x5"][1]+1)
    
    # 筛选可行解
    if is_feasible(x1_rand, x2_rand, x3_rand, x4_rand, x5_rand):
        # 计算目标函数值
        current_value = calculate_objective(x1_rand, x2_rand, x3_rand, x4_rand, x5_rand)
        # 更新最优解（目标函数最大化，值更大则替换）
        if current_value > best_value:
            best_value = current_value
            best_solution = (x1_rand, x2_rand, x3_rand, x4_rand, x5_rand)

# 5. 步骤4：输出结果（对比文档精确解与蒙特卡洛满意解）
print("\n" + "="*60)
print("例题2.9（非线性整数规划）Pulp+蒙特卡洛法求解结果")
print("="*60)
print(f"抽样次数：{n_samples}次（文档建议次数1-164）")
print(f"最优解（x1, x2, x3, x4, x5）：{best_solution}")
print(f"最优目标函数值：{best_value}")
print(f"文档精确解（Lingo求得1-173）：x1=50, x2=99, x3=0, x4=99, x5=20，目标值=51568")
print(f"与精确解的误差：{abs(best_value - 51568)}（抽样次数越多，误差越小）")
print("="*60)