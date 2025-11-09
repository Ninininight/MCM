## 1. 目标函数的凸性判断

对于最小化问题 $\min f(\mathbf{x})$：

- **如果 $f(\mathbf{x})$ 是凸函数，则条件满足。**
    
- **如果 $f(\mathbf{x})$ 是凹函数，则条件不满足。** (除非是最大化凹函数，等价于最小化负的凹函数，即凸函数)
### 判断方法：Hessian 矩阵

最常用的方法是计算目标函数 $f(\mathbf{x})$ 的 **Hessian 矩阵** $\mathbf{H}(\mathbf{x})$（二阶偏导矩阵）：

1. 计算 Hessian 矩阵 $\mathbf{H}(\mathbf{x})$：
    
    $$\mathbf{H}(\mathbf{x})_{ij} = \frac{\partial^2 f(\mathbf{x})}{\partial x_i \partial x_j}$$
    
2. **判断 $\mathbf{H}(\mathbf{x})$ 的定性**：
    
    - **凸函数：** 如果 $\mathbf{H}(\mathbf{x})$ 在**整个可行域内**都是**半正定矩阵**（所有主子式 $\ge 0$），则 $f(\mathbf{x})$ 是凸函数。
        
    - **严格凸函数：** 如果 $\mathbf{H}(\mathbf{x})$ 在**整个可行域内**都是**正定矩阵**（所有主子式 $> 0$），则 $f(\mathbf{x})$ 是严格凸函数。
        
    - **凹函数：** 如果 $-\mathbf{H}(\mathbf{x})$ 是半正定矩阵，则 $f(\mathbf{x})$ 是凹函数。


## 2. 可行域的凸性判断

可行域是由所有约束条件共同定义的区域：

$$G = \{\mathbf{x} \mid g_i(\mathbf{x}) \le 0, \quad h_j(\mathbf{x}) = 0, \quad \mathbf{x} \in \mathbb{R}^n\}$$

**一个集合 $G$ 是凸集，当且仅当它由以下类型的函数定义：**

### a) 不等式约束 $g_i(\mathbf{x}) \le 0$

- **要求：** 所有不等式约束 $g_i(\mathbf{x})$ 必须是**凸函数**。
    
- **原因：** 凸函数的水平集（$\{\mathbf{x} \mid g(\mathbf{x}) \le \alpha\}$）是凸集。多个凸集的交集仍然是凸集。
### b) 等式约束 $h_j(\mathbf{x}) = 0$

- **要求：** 所有等式约束 $h_j(\mathbf{x})$ 必须是**线性函数**（即 $h_j(\mathbf{x}) = \mathbf{a}_j^T \mathbf{x} - b_j = 0$）。
    
- **原因：** 只有线性等式约束才能保证其解集（一个超平面）是凸集。非线性等式约束的解集通常是非凸的。