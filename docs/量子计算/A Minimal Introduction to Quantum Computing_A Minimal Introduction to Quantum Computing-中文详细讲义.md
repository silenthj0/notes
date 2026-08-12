# 量子计算入门与算法实现：两篇文献中文详细讲义

---

## 0. 原文摘要翻译

本文面向程序员、机器学习工程师和数据科学家介绍量子计算。作者暂时抽去较难掌握的量子物理背景，把量子计算当作一种类似图灵机的计算模型，从纯逻辑角度说明其基本原则。文章先定义量子态和量子比特，介绍基态、量子门和张量积如何构成量子计算的基本组件；随后讲解 Deutsch-Jozsa 算法，这是展示量子计算机能够优于经典计算机的最简单算法之一；最后给出继续学习量子算法、实现方法和产业应用的资料。

原文的主线可压缩为：

$$
\boxed{\text{量子态}}\xrightarrow{\text{酉变换/量子门}}
\boxed{\text{新的量子态}}\xrightarrow{\text{测量}}
\boxed{\text{经典比特串}}
$$

对物理学生而言，这条主线还应补上一层含义：**量子态不是“同时装着许多经典答案的容器”，而是一个复向量；量子算法通过调节各分量的相位，使错误答案发生相消、目标答案发生相长。**

## 1. 阅读前准备

### 1.1 只需掌握的数学

读懂本文主要需要：

- 复数及复共轭，例如 $|a+ib|^2=a^2+b^2$；
- 列向量、矩阵乘法和正交归一基；
- 概率的归一化；
- 张量积（Kronecker 积）的基本运算。

### 1.2 符号速查

| 符号                                   | 含义                            |
| ------------------------------------ | ----------------------------- |
| $\lvert\psi\rangle$                  | ket，表示列向量形式的量子态               |
| $\langle\psi\rvert$                  | bra，$\lvert\psi\rangle$ 的共轭转置 |
| $\langle\phi\vert\psi\rangle$        | 内积，是一个复数                      |
| $\lvert\psi\rangle\langle\phi\rvert$ | 外积，是一个算符或矩阵                   |
| $\otimes$                            | 张量积，用于组合多个系统                  |
| $U^\dagger$                          | $U$ 的共轭转置                     |
| $\lvert a\rvert^2$                   | 复数 $a$ 的模平方                   |
| $\oplus$                             | 模 2 加法，即 XOR                  |
| $H^{\otimes n}$                      | 对 $n$ 个量子比特分别施加 Hadamard 门    |

### 1.3 三个容易混淆的“维数”

- 1 个量子比特的希尔伯特空间维数是 $2$；
- $n$ 个量子比特的希尔伯特空间维数是 $2^n$；
- 描述这 $n$ 个量子比特的态矢量有 $2^n$ 个复振幅，但系统仍然只有 $n$ 个量子比特。

例如，三量子比特态属于 $\mathbb C^8$，其计算基为

$$
|000\rangle,|001\rangle,\ldots,|111\rangle.
$$

## 2. 把量子计算看作一种计算模型

原文首先把图灵机、lambda 演算、组合子逻辑和编程语言都称为“计算模型”：一个模型需要一组符号，以及操作这些符号的规则。

量子线路模型中：

- 符号是量子态，通常由量子比特组成；
- 演化规则是量子门，即酉线性变换；
- 输出规则是测量，得到普通的经典比特串。

这种讲法有意暂时忽略物理实现，但物理学生应知道其背后的对应关系：

| 计算语言                    | 量子力学语言                |
| ----------------------- | --------------------- |
| 量子态 $\lvert\psi\rangle$ | 封闭系统的态矢量              |
| 量子门 $U$                 | 由薛定谔方程产生的酉时间演化        |
| 测量                      | 可观测量对应的投影测量或更一般的 POVM |
| 退相干与噪声                  | 系统和环境纠缠后，有效演化不再是理想酉变换 |

因此，“先不讲物理”是一条入门路线，不代表量子计算与物理无关。量子线路模型的规则正是从量子力学中抽象出来的。

## 3. 基态、量子态与量子比特

### 3.1 计算基态

二进制串写进 ket 就得到一个计算基态，例如

$$
|0\rangle,\quad |1\rangle,\quad |001\rangle,\quad |010010\rangle.
$$

单量子比特的计算基向量是

$$
|0\rangle=\begin{pmatrix}1\\0\end{pmatrix},\qquad
|1\rangle=\begin{pmatrix}0\\1\end{pmatrix}.
$$

三量子比特基态 $|001\rangle$ 对应十进制数 $1$，所以在从 $0$ 开始编号的八维标准基中

$$
|001\rangle=
\begin{pmatrix}0&1&0&0&0&0&0&0\end{pmatrix}^{\mathrm T}.
$$

一般地，$n$ 位二进制串共有 $2^n$ 种，因此 $n$ 量子比特系统有 $2^n$ 个计算基态。

### 3.2 从基态到一般量子态

单量子比特纯态的一般形式为

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle,\quad
\alpha,\beta\in\mathbb C,\quad
|\alpha|^2+|\beta|^2=1.
$$

$n$ 量子比特纯态为

$$
|\psi\rangle=\sum_{x=0}^{2^n-1}c_x|x\rangle,\quad
\sum_x|c_x|^2=1.
$$

这里 $c_x$ 叫**概率振幅**。它通常是复数，不能直接当概率；在计算基中测得 $x$ 的概率才是

$$
P(x)=|c_x|^2.
$$

原文给出的一个例子是

$$
|\psi\rangle=
\frac{i}{2}|010010\rangle+
\frac{i}{2}|110010\rangle+
\frac{1}{2}|011010\rangle+
\frac{1}{2}|010011\rangle.
$$

四个振幅的模平方均为 $1/4$，所以归一化成立。测量时四个比特串各以 $1/4$ 的概率出现。

### 3.3 “叠加”究竟意味着什么

$\alpha|0\rangle+\beta|1\rangle$ 称为 $|0\rangle$ 和 $|1\rangle$ 的叠加。叠加不是“系统暗中已经取了 0 或 1，只是我们不知道”，因为振幅还带有相位，后续操作能让不同路径发生干涉。

比较

$$
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},\qquad
|-\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2}.
$$

若立刻在计算基测量，两者都以 $1/2$ 概率给出 0 或 1；但再施加一次 Hadamard 门后，

$$
H|+\rangle=|0\rangle,\quad H|-\rangle=|1\rangle.
$$

两态的相对负号能够被实验区分，这正是干涉在量子算法中的作用。

### 3.4 全局相位与相对相位

$|\psi\rangle$ 与 $e^{i\gamma}|\psi\rangle$ 表示同一物理纯态，因为所有测量概率都不变。这叫**全局相位不可观测**。

但 $\alpha|0\rangle+\beta|1\rangle$ 中 $\alpha$ 和 $\beta$ 的**相对相位**可以影响干涉，所以不能随意删去。Deutsch-Jozsa 算法正是把函数值写入相对相位。

### 3.5 十进制简写要保留比特数语境

原文有时把 $|000001\rangle$ 写成 $|1\rangle$，把 $|100001\rangle$ 写成 $|33\rangle$。这种简写方便求和，但 $|1\rangle$ 可能表示单量子比特态，也可能表示六量子比特空间中的编号 1 基态。严谨写法可加下标或直接保留二进制串，例如 $|1\rangle_6=|000001\rangle$。

## 4. Bra-ket、内积与外积

### 4.1 从 ket 到 bra

若

$$
|\psi\rangle=\begin{pmatrix}\alpha\\\beta\end{pmatrix},
$$

则

$$
\langle\psi|=|\psi\rangle^\dagger=
\begin{pmatrix}\alpha^*&\beta^*\end{pmatrix}.
$$

必须取复共轭。例如 $i^*=-i$。这是原文内积例子中负号的来源。

### 4.2 内积：比较两个态

计算基满足正交归一关系

$$
\langle x|y\rangle=\delta_{xy}=
\begin{cases}
1,&x=y,\\
0,&x\ne y.
\end{cases}
$$

若

$$
|\phi\rangle=\sum_x a_x|x\rangle,\quad
|\psi\rangle=\sum_x b_x|x\rangle,
$$

则

$$
\langle\phi|\psi\rangle=\sum_x a_x^*b_x.
$$

因此归一化条件也可写作 $\langle\psi|\psi\rangle=1$。

### 4.3 外积：构造算符

外积 $|x\rangle\langle y|$ 是矩阵。例如

$$
|0\rangle\langle1|=
\begin{pmatrix}1\\0\end{pmatrix}
\begin{pmatrix}0&1\end{pmatrix}
=\begin{pmatrix}0&1\\0&0\end{pmatrix}.
$$

它作用在基态上时像“**选择并替换**”：

$$
(|w\rangle\langle x|)|y\rangle
=|w\rangle\langle x|y\rangle
=\delta_{xy}|w\rangle.
$$

也就是说，只有输入 $|y\rangle$ 与 $|x\rangle$ 相同时，这一项才把它映射成 $|w\rangle$。

特别地，$|x\rangle\langle x|$ 是投影到 $|x\rangle$ 方向的投影算符。

## 5. 张量积与多量子比特系统

### 5.1 组合两个系统

设

$$
|\psi\rangle=a_0|0\rangle+a_1|1\rangle,\quad
|\phi\rangle=b_0|0\rangle+b_1|1\rangle,
$$

则

$$
\begin{aligned}
|\psi\rangle\otimes|\phi\rangle
={}&a_0b_0|00\rangle+a_0b_1|01\rangle\\
&+a_1b_0|10\rangle+a_1b_1|11\rangle.
\end{aligned}
$$

列向量表示为

$$
\begin{pmatrix}a_0\\a_1\end{pmatrix}\otimes
\begin{pmatrix}b_0\\b_1\end{pmatrix}
=
\begin{pmatrix}
a_0b_0\\a_0b_1\\a_1b_0\\a_1b_1
\end{pmatrix}.
$$

这说明维数相乘：$2^m\times2^n=2^{m+n}$；而量子比特数相加：$m+n$。

### 5.2 算符的张量积

若只对两量子比特中的第一个施加 $H$，对第二个什么也不做，整体算符写成

$$
H\otimes I.
$$

若 $A$ 是 $m\times m$ 矩阵、$B$ 是 $n\times n$ 矩阵，则 $A\otimes B$ 是 $mn\times mn$ 矩阵。它把 $A$ 的每个元素 $A_{ij}$ 替换为分块矩阵 $A_{ij}B$。

具体地，若 $A=(A_{ij})$，则

$$
A\otimes B=
\begin{pmatrix}
A_{11}B&A_{12}B&\cdots&A_{1m}B\\
A_{21}B&A_{22}B&\cdots&A_{2m}B\\
\vdots&\vdots&\ddots&\vdots\\
A_{m1}B&A_{m2}B&\cdots&A_{mm}B
\end{pmatrix}.
$$

例如，取两个一般的 $2\times2$ 矩阵

$$
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad
B=\begin{pmatrix}e&f\\g&h\end{pmatrix},
$$

那么


$$
\begin{aligned}
A\otimes B
&=\begin{pmatrix}
aB&bB\\
cB&dB
\end{pmatrix}\\
&=\begin{pmatrix}
ae&af&be&bf\\
ag&ah&bg&bh\\
ce&cf&de&df\\
cg&ch&dg&dh
\end{pmatrix}.
\end{aligned}
$$

可以看到，$A$ 的第一行元素 $a,b$ 生成上半部分的两个分块 $aB,bB$，第二行元素 $c,d$ 则生成下半部分的两个分块 $cB,dB$。

还要注意次序：一般 $|a\rangle\otimes|b\rangle\ne|b\rangle\otimes|a\rangle$，量子线路中导线的排列决定矩阵中的基态排序。

**算符的张量积作用在直积态上时，可以分别作用于各自的子系统：**

$$
(A\otimes B)(|\psi\rangle\otimes|\phi\rangle)
=(A|\psi\rangle)\otimes(B|\phi\rangle).
$$

**证明：** 设 $\{|j\rangle\}$ 和 $\{|\nu\rangle\}$ 分别是两个子系统的一组基，并将两个态展开为

$$
|\psi\rangle=\sum_j\psi_j|j\rangle,
\qquad
|\phi\rangle=\sum_\nu\phi_\nu|\nu\rangle.
$$

由 Kronecker 积的矩阵元定义，

$$
(A\otimes B)_{(i,\mu),(j,\nu)}
=A_{ij}B_{\mu\nu}.
$$

这里的 $(i,\mu)$ 和 $(j,\nu)$ 称为复合指标：

- $i,j$ 分别是矩阵 $A$ 的行指标和列指标；
- $\mu,\nu$ 分别是矩阵 $B$ 的行指标和列指标；
- $(i,\mu)$ 共同指定 $A\otimes B$ 的一行，对应张量积基 $|i\rangle\otimes|\mu\rangle$；
- $(j,\nu)$ 共同指定 $A\otimes B$ 的一列，对应张量积基 $|j\rangle\otimes|\nu\rangle$。

若 $A$ 是 $m\times m$ 矩阵、$B$ 是 $n\times n$ 矩阵，采用从 1 开始的编号，则复合指标对应的普通行列编号为

$$
r=(i-1)n+\mu,
\qquad
c=(j-1)n+\nu.
$$

所以也可以把原公式写成

$$
(A\otimes B)_{(i-1)n+\mu,\,(j-1)n+\nu}
=A_{ij}B_{\mu\nu}.
$$

因此左边可以逐分量展开为

$$
\begin{aligned}
&(A\otimes B)(|\psi\rangle\otimes|\phi\rangle)\\
&=(A\otimes B)
\sum_{j,\nu}\psi_j\phi_\nu
\bigl(|j\rangle\otimes|\nu\rangle\bigr)\\
&=\sum_{i,\mu,j,\nu}
A_{ij}B_{\mu\nu}\psi_j\phi_\nu
\bigl(|i\rangle\otimes|\mu\rangle\bigr)\\
&=\left(\sum_{i,j}A_{ij}\psi_j|i\rangle\right)
\otimes
\left(\sum_{\mu,\nu}B_{\mu\nu}\phi_\nu|\mu\rangle\right)\\
&=(A|\psi\rangle)\otimes(B|\phi\rangle).
\end{aligned}
$$

最后一步只是普通矩阵乘法的分量形式。于是该恒等式对任意 $|\psi\rangle$ 和 $|\phi\rangle$ 都成立。$\square$

#### 例 1：比较 $H\otimes I$ 与 $I\otimes H$

按 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$ 的顺序排列计算基，有

$$
\begin{aligned}
H\otimes I
&=\frac1{\sqrt2}
\begin{pmatrix}
1&1\\
1&-1
\end{pmatrix}
\otimes
\begin{pmatrix}
1&0\\
0&1
\end{pmatrix}\\
&=\frac1{\sqrt2}
\begin{pmatrix}
1&0&1&0\\
0&1&0&1\\
1&0&-1&0\\
0&1&0&-1
\end{pmatrix}.
\end{aligned}
$$

它作用在 $|01\rangle=|0\rangle\otimes|1\rangle$ 上时，只改变第一个量子比特：

$$
(H\otimes I)|01\rangle
=H|0\rangle\otimes|1\rangle
=\frac{|01\rangle+|11\rangle}{\sqrt2}.
$$

若把次序换成 $I\otimes H$，则改变的是第二个量子比特：

$$
(I\otimes H)|01\rangle
=|0\rangle\otimes H|1\rangle
=\frac{|00\rangle-|01\rangle}{\sqrt2}.
$$

两者结果不同，说明 $H\otimes I\ne I\otimes H$；张量积中算符的位置对应量子线路中的具体导线。

#### 例 2：把 $X\otimes Z$ 展开为分块矩阵

取


$$
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
$$

把 $X$ 的每个矩阵元替换为相应的 $2\times2$ 分块 $X_{ij}Z$，得到


$$
\begin{aligned}
X\otimes Z
&=\begin{pmatrix}
0Z&1Z\\
1Z&0Z
\end{pmatrix}\\
&=\begin{pmatrix}
0&0&1&0\\
0&0&0&-1\\
1&0&0&0\\
0&-1&0&0
\end{pmatrix}.
\end{aligned}
$$

它同时对第一位做比特翻转、对第二位施加相位：

$$
\begin{aligned}
|00\rangle&\longmapsto |10\rangle,\\
|01\rangle&\longmapsto- |11\rangle,\\
|10\rangle&\longmapsto |00\rangle,\\
|11\rangle&\longmapsto- |01\rangle.
\end{aligned}
$$

其中负号来自 $Z|1\rangle=-|1\rangle$，而第一位的 $0\leftrightarrow1$ 来自 $X$ 门。

### 5.3 纠缠：不能拆成各部分的独立状态

两量子比特 Bell 态

$$
|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}
$$

不能写成两个单量子比特态的张量积。假设可以写成

$$
(a|0\rangle+b|1\rangle)\otimes(c|0\rangle+d|1\rangle),
$$

展开后各振幅必须满足

$$
ac=\frac1{\sqrt2},\quad ad=0,\quad bc=0,\quad bd=\frac1{\sqrt2}.
$$

由 $ac\ne0$ 得 $a,c\ne0$；由 $ad=0$ 得 $d=0$，这又与 $bd\ne0$ 矛盾。因此不能分解，态是纠缠态。

物理直觉是：整体态完全确定，但每个子系统单独并没有纯态描述。若测量第一个量子比特得到 0，第二个必为 0；若第一个得到 1，第二个必为 1。**相关性不等于超光速通信，因为单看任一方的结果仍是随机的。**

## 6. 量子门：保持归一化的可逆演化

### 6.1 一般形式与酉性

$n$ 量子比特门是在 $2^n$ 维空间上的线性算符：

$$
U=\sum_{i,j=0}^{2^n-1}U_{ij}|i\rangle\langle j|.
$$

理想量子门必须满足

$$
U^\dagger U=UU^\dagger=I.
$$

于是

$$
\|U|\psi\rangle\|^2
=\langle\psi|U^\dagger U|\psi\rangle
=\langle\psi|\psi\rangle=1.
$$

因此，**合法量子门作用后不需要额外手动归一化**。酉性还保证 $U^{-1}=U^\dagger$，所以**封闭系统的门演化可逆**。不可逆的经典门（如把两个输入都擦成 0）不能直接作为孤立量子门实现；若要实现，必须把信息保存在辅助系统或环境中。

### 6.2 常用门

用外积的“选择并替换”作用：

$$
(|w\rangle\langle x|)|y\rangle
=\delta_{xy}|w\rangle.
$$

也就是说，$\langle x|$ 先检查输入是不是 $|x\rangle$：若是，就由左边的 $|w\rangle$ 给出输出；若不是，该项给出 0。一个门写成若干外积之和后，每一项分别处理它所选中的输入分量。

#### 恒等门

$$
I=|0\rangle\langle0|+|1\rangle\langle1|
=\begin{pmatrix}1&0\\0&1\end{pmatrix}.
$$

其中，$|0\rangle\langle0|$ 选中 $|0\rangle$ 并仍把它替换为 $|0\rangle$；$|1\rangle\langle1|$ 选中 $|1\rangle$ 并仍把它替换为 $|1\rangle$。因此

$$
\begin{aligned}
I|0\rangle
&=|0\rangle\langle0|0\rangle
 +|1\rangle\langle1|0\rangle
 =|0\rangle,\\
I|1\rangle
&=|0\rangle\langle0|1\rangle
 +|1\rangle\langle1|1\rangle
 =|1\rangle.
\end{aligned}
$$

所以恒等门对任意量子态都不作改变。

#### Pauli-$X$ 门（量子 NOT）

$$
X=|0\rangle\langle1|+|1\rangle\langle0|
=\begin{pmatrix}0&1\\1&0\end{pmatrix},
$$

这里，$|1\rangle\langle0|$ 选中输入 $|0\rangle$，并把它替换成 $|1\rangle$；$|0\rangle\langle1|$ 选中输入 $|1\rangle$，并把它替换成 $|0\rangle$。逐项计算为

$$
\begin{aligned}
X|0\rangle
&=|0\rangle\langle1|0\rangle
 +|1\rangle\langle0|0\rangle
 =|1\rangle,\\
X|1\rangle
&=|0\rangle\langle1|1\rangle
 +|1\rangle\langle0|1\rangle
 =|0\rangle.
\end{aligned}
$$

因此 $X$ 门交换 $|0\rangle$ 和 $|1\rangle$，相当于量子版本的 NOT 门。

#### Hadamard 门

$$
H=\frac1{\sqrt2}\left[
(|0\rangle+|1\rangle)\langle0|
+(|0\rangle-|1\rangle)\langle1|
\right]=\frac1{\sqrt2}
\begin{pmatrix}1&1\\1&-1\end{pmatrix}
.
$$

第一项用 $\langle0|$ 选中 $|0\rangle$，并把它替换成 $(|0\rangle+|1\rangle)/\sqrt2$；第二项用 $\langle1|$ 选中 $|1\rangle$，并把它替换成 $(|0\rangle-|1\rangle)/\sqrt2$。因此

$$
\begin{aligned}
H|0\rangle
&=\frac{|0\rangle+|1\rangle}{\sqrt2}=|+\rangle,\\
H|1\rangle
&=\frac{|0\rangle-|1\rangle}{\sqrt2}=|-\rangle.
\end{aligned}
$$

与 $I$、$X$ 不同，$H$ 门不是简单地把一个基态换成另一个基态，而是把一个基态替换成两个基态的相干叠加。式中的正负号表示相对相位；不同外积项产生的振幅之后可以相长或相消。又因 $H^2=I$，Hadamard 门既能制造计算基中的均匀叠加，也能把相位差重新变成可测量的 0/1 差异。

#### 受控非门 CNOT

**以第一位为控制位、第二位为目标位**：

$$
\operatorname{CNOT}|x,y\rangle=|x,y\oplus x\rangle.
$$

用外积表示为

$$
\operatorname{CNOT}
=|00\rangle\langle00|
+|01\rangle\langle01|
+|11\rangle\langle10|
+|10\rangle\langle11|.
$$

四个外积项分别表示：

- $|00\rangle\langle00|$ 选中 $|00\rangle$，仍替换为 $|00\rangle$；
- $|01\rangle\langle01|$ 选中 $|01\rangle$，仍替换为 $|01\rangle$；
- $|11\rangle\langle10|$ 选中 $|10\rangle$，替换为 $|11\rangle$；
- $|10\rangle\langle11|$ 选中 $|11\rangle$，替换为 $|10\rangle$。

例如，对 $|10\rangle$ 逐项作用，只有第三项被选中：

$$
\begin{aligned}
\operatorname{CNOT}|10\rangle
={}&|00\rangle\langle00|10\rangle
+|01\rangle\langle01|10\rangle\\
&+|11\rangle\langle10|10\rangle
+|10\rangle\langle11|10\rangle
=|11\rangle.
\end{aligned}
$$

因此，当控制位是 0 时目标位不变；当控制位是 1 时目标位翻转。

其作用为

$$
|00\rangle\mapsto|00\rangle,\quad
|01\rangle\mapsto|01\rangle,\quad
|10\rangle\mapsto|11\rangle,\quad
|11\rangle\mapsto|10\rangle.
$$

*下面从外积形式一步步得到矩阵。*
先固定有序计算基

$$
\mathcal B=(|00\rangle,|01\rangle,|10\rangle,|11\rangle).
$$

在这个基下，四个基态的列向量是

$$
\begin{aligned}
|00\rangle&=\begin{pmatrix}1\\0\\0\\0\end{pmatrix},&
|01\rangle&=\begin{pmatrix}0\\1\\0\\0\end{pmatrix},\\[4pt]
|10\rangle&=\begin{pmatrix}0\\0\\1\\0\end{pmatrix},&
|11\rangle&=\begin{pmatrix}0\\0\\0\\1\end{pmatrix}.
\end{aligned}
$$

外积 $|u\rangle\langle v|$ 是“列向量乘行向量”。它的矩阵中，**行**对应输出基态 $|u\rangle$，**列**对应被选中的输入基态 $|v\rangle$。例如

$$
|11\rangle\langle10|
=\begin{pmatrix}0\\0\\0\\1\end{pmatrix}
 \begin{pmatrix}0&0&1&0\end{pmatrix}
=\begin{pmatrix}
0&0&0&0\\
0&0&0&0\\
0&0&0&0\\
0&0&1&0
\end{pmatrix}.
$$

它在第 4 行、第 3 列出现 1，正好表示“把第 3 个基态 $|10\rangle$ 替换成第 4 个基态 $|11\rangle$”。同理，四个外积分别为

$$
\begin{aligned}
|00\rangle\langle00|
&=\begin{pmatrix}
1&0&0&0\\
0&0&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix},\\[6pt]
|01\rangle\langle01|
&=\begin{pmatrix}
0&0&0&0\\
0&1&0&0\\
0&0&0&0\\
0&0&0&0
\end{pmatrix},\\[6pt]
|11\rangle\langle10|
&=\begin{pmatrix}
0&0&0&0\\
0&0&0&0\\
0&0&0&0\\
0&0&1&0
\end{pmatrix},\\[6pt]
|10\rangle\langle11|
&=\begin{pmatrix}
0&0&0&0\\
0&0&0&0\\
0&0&0&1\\
0&0&0&0
\end{pmatrix}.
\end{aligned}
$$

把这四个矩阵逐项相加，得到

$$
\begin{aligned}
\operatorname{CNOT}
&=|00\rangle\langle00|
+|01\rangle\langle01|
+|11\rangle\langle10|
+|10\rangle\langle11|\\
&=\begin{pmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&0&1\\
0&0&1&0
\end{pmatrix}.
\end{aligned}
$$

也可以按列检查：矩阵第 $j$ 列就是门作用在第 $j$ 个输入基态后得到的输出向量。因此四列依次是 $|00\rangle$、$|01\rangle$、$|11\rangle$、$|10\rangle$，与上面的基态映射完全一致。

它能和单量子比特门共同产生纠缠：

$$
|00\rangle\xrightarrow{H\otimes I}
\frac{|00\rangle+|10\rangle}{\sqrt2}
\xrightarrow{\operatorname{CNOT}}
\frac{|00\rangle+|11\rangle}{\sqrt2}.
$$

### 6.3 线路中的复合顺序

若先施加 $U$、后施加 $V$，最终态为

$$
V(U|\psi\rangle)=(VU)|\psi\rangle.
$$

矩阵从右向左作用，这与普通线性代数一致；画线路时通常从左向右读。两种阅读方向不要混淆。

## 7. 测量：从量子振幅得到经典数据

若

$$
|\psi\rangle=\sum_x c_x|x\rangle,
$$

在计算基测量得到 $x$ 的概率为

$$
P(x)=|c_x|^2.
$$

测得 $x$ 后，在理想投影测量模型中，状态塌缩为 $|x\rangle$。单次测量只给出一个经典比特串，不能把全部 $2^n$ 个振幅一次性读出来。

例如

$$
|\psi\rangle=i\sqrt{\frac13}|01\rangle+
\sqrt{\frac23}|11\rangle
$$

会以 $1/3$ 概率输出 `01`，以 $2/3$ 概率输出 `11`。系数中的 $i$ **不影响这一次计算基测量的概率，但能影响测量前的干涉。**

实际运行量子程序时通常重复很多次，每次称为一个 shot。若运行 1000 次，结果频率大致接近理论概率，但有统计涨落。

## 8. Deutsch-Jozsa 算法

### 8.1 问题与承诺条件

给定黑箱函数

$$
f:\{0,1\}^n\to\{0,1\},
$$
具体来说，$\{0,1\}^n$ 表示所有长度为 $n$ 的二进制串，共有 $2^n$ 个。例如 $n=2$ 时，输入集合是

$$
\{0,1\}^2=\{00,01,10,11\}.
$$
并承诺它只可能属于两类：

- **常函数**：所有输入的函数值都相同，全为 0 或全为 1；
- **平衡函数**：恰有一半输入映射到 0，另一半映射到 1。

任务是判断 $f$ 属于哪一类。

函数对每个输入只输出一个比特。所谓“黑箱”，是指我们不知道 $f$ 的公式或内部实现，只能选取一个输入 $x$，向黑箱查询并得到 $f(x)$。算法复杂度主要用**调用黑箱的次数**来衡量。

以 $n=2$ 为例，下面列出了几种可能的函数：

| 输入 $x$ | 常函数 $f_0$ | 常函数 $f_1$ | 平衡函数 $f_2$ | 平衡函数 $f_3$ | 非承诺函数 $g$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| $00$ | 0 | 1 | 0 | 0 | 0 |
| $01$ | 0 | 1 | 0 | 1 | 0 |
| $10$ | 0 | 1 | 1 | 1 | 0 |
| $11$ | 0 | 1 | 1 | 0 | 1 |

- $f_0$ 的四个输出全为 0，$f_1$ 的四个输出全为 1，所以它们都是常函数；
- $f_2$ 和 $f_3$ 都有两个输出为 0、两个输出为 1，所以它们都是平衡函数。平衡只限制 0 和 1 的数量相等，**并不限制哪些输入对应 0；**
- $g$ 有三个输出为 0、一个输出为 1，既不是常函数，也不是平衡函数，因此不满足题目的承诺，在 Deutsch-Jozsa 问题中不会把这样的函数交给算法。

“承诺”可以理解为出题者预先保证：黑箱一定来自允许的两类之一。算法只负责在这两类之间判断，**并不负责检验承诺本身是否真实**。例如，对上表的未知函数查询 $00$ 和 $01$，若两次都得到 0，此时它既可能是常函数 $f_0$，也可能是平衡函数 $f_2$，还不能分类。若黑箱实际上是 $g$ 这类非承诺函数，那么后续量子算法的测量结果也不能被简单解释为“常函数”或“平衡函数”。

一般地，平衡函数要求 $2^n$ 个输入中恰好有

$$
2^{n-1}
$$

个输入的函数值为 0，其余 $2^{n-1}$ 个输入的函数值为 1。Deutsch-Jozsa 算法利用的正是“全都相同”和“正好各占一半”这两种*极端结构之间的差别*。

### 8.2 经典算法需要多少次查询

确定性经典算法在最坏情况下要查询

$$
2^{n-1}+1
$$

次。因为前 $2^{n-1}$ 次即使结果完全相同，仍可能刚好查到了平衡函数中取同一值的那一半；再查一次才能排除。

随机抽样能更快给出高置信度判断。如果连续 $k$ 次都得到同一函数值，而真实函数是平衡函数，漏判概率至多约为 $2^{1-k}$（具体数值取决于是否允许重复抽样及采样方案）。但想要零错误，最坏情况仍需指数级查询。

这个概率可以如下得到。假设每次从全部输入中独立、均匀地随机选取一个输入，允许重复选到同一个输入，也就是**有放回抽样**。真实函数平衡时，一次查询得到 0 或 1 的概率各为

$$
P(f(x)=0)=P(f(x)=1)=\frac12.
$$

只要 $k$ 次查询中既出现 0 又出现 1，就能立即确定函数不是常函数，因此不会漏判。漏判只会发生在以下两个互斥事件之一：

1. $k$ 次结果全为 0；
2. $k$ 次结果全为 1。

由于各次抽样相互独立，二者的概率分别为

$$
P(\text{全为 0})=\left(\frac12\right)^k,
\qquad
P(\text{全为 1})=\left(\frac12\right)^k.
$$

所以总漏判概率为

$$
\begin{aligned}
P(\text{漏判})
&=P(\text{全为 0})+P(\text{全为 1})\\
&=2\left(\frac12\right)^k
=2^{1-k}.
\end{aligned}
$$

也可以换一种理解：第一次查询得到 0 还是 1 都无所谓；为了始终不暴露平衡性，后面的 $k-1$ 次必须每次都与第一次相同，每次发生的概率都是 $1/2$，所以

$$
P(\text{漏判})=\left(\frac12\right)^{k-1}=2^{1-k}.
$$

例如，若随机查询 $k=5$ 次，则有放回抽样时的漏判概率为

$$
2^{1-5}=\frac1{16}=6.25\%.
$$

若每次都选取一个尚未查询过的新输入，即**无放回抽样**，漏判概率还会更小。令输入总数为 $N=2^n$，当 $k\le N/2$ 时，精确概率为

$$
\begin{aligned}
P(\text{漏判})
&=2\frac{\binom{N/2}{k}}{\binom{N}{k}}\\
&=\prod_{j=1}^{k-1}\frac{N/2-j}{N-j}
\le \left(\frac12\right)^{k-1}
=2^{1-k}.
\end{aligned}
$$

乘积中的每一项都小于或等于 $1/2$：查询过一个相同输出的输入后，尚未查询的同类输入所占比例会逐渐下降。如果 $k>N/2$，平衡函数不可能让所有查询结果仍然相同，漏判概率直接变为 0。因此，$2^{1-k}$ 是有放回独立抽样时的精确结果，也是无放回抽样时一个方便的上界。

### 8.3 量子线路

使用 $n$ 个输入量子比特和 1 个辅助量子比特。量子 oracle 定义为

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle.
$$

这个式子描述了量子黑箱 $U_f$ 对一组计算基态的作用。其中：

- $|x\rangle$ 是由 $n$ 个量子比特组成的**输入寄存器**，$x\in\{0,1\}^n$；
- $|y\rangle$ 是一个**辅助量子比特**，$y\in\{0,1\}$；
- $f(x)$ 是经典布尔函数对输入 $x$ 给出的一个比特；
- $\oplus$ 表示模 2 加法，即 XOR（异或）。

这里把张量积符号省略了，即 $|x\rangle|y\rangle$ 是 $|x\rangle\otimes|y\rangle$ 的简写，表示输入寄存器与辅助位组成的联合量子态。

式子的含义是：输入寄存器 $|x\rangle$ 保持不变，而辅助位根据 $f(x)$ 的值决定是否翻转。具体分成两种情况：

$$
U_f|x\rangle|y\rangle=
\begin{cases}
|x\rangle|y\rangle,&f(x)=0,\\
|x\rangle|y\oplus1\rangle,&f(x)=1.
\end{cases}
$$

因此，若 $f(x)=0$，辅助位不变；若 $f(x)=1$，辅助位经历一次 Pauli-$X$ 翻转。四种可能可以写成

| $f(x)$ | 原辅助位 $y$ | 新辅助位 $y\oplus f(x)$ | 作用                                  |
| -----: | -------: | ------------------: | :---------------------------------- |
|      0 |        0 |                   0 | 不变                                  |
|      0 |        1 |                   1 | 不变                                  |
|      1 |        0 |                   1 | $\lvert 0\rangle\to\lvert 1\rangle$ |
|      1 |        1 |                   0 | $\lvert 1\rangle\to\lvert 0\rangle$ |

特别地，如果把辅助位初始化为 $|0\rangle$，那么

$$
U_f|x\rangle|0\rangle
=|x\rangle|0\oplus f(x)\rangle
=|x\rangle|f(x)\rangle,
$$

函数值就被写入了辅助位。例如，若 $f(10)=1$、$f(01)=0$，则

$$
\begin{aligned}
U_f|10\rangle|0\rangle
&=|10\rangle|0\oplus f(10)\rangle
=|10\rangle|0\oplus1\rangle
=|10\rangle|1\rangle,\\[4pt]
U_f|01\rangle|0\rangle
&=|01\rangle|0\oplus f(01)\rangle
=|01\rangle|0\oplus0\rangle
=|01\rangle|0\rangle.
\end{aligned}
$$
或
$$
\begin{aligned}
U_f|10\rangle|0\rangle
&=|10\rangle|0\oplus f(10)\rangle
=|10\rangle|f(10)\rangle
=|10\rangle|1\rangle,\\[4pt]
U_f|01\rangle|0\rangle
&=|01\rangle|0\oplus f(01)\rangle
=|01\rangle|f(01)\rangle
=|01\rangle|0\rangle.
\end{aligned}
$$
#### 为什么要写成异或形式

**量子门必须是酉变换，因此必须可逆**。若简单地规定

$$
|x\rangle\longmapsto|f(x)\rangle,
$$

许多不同的 $x$ 可能得到同一个 $f(x)$，原来的输入信息会丢失，这种映射一般不可逆，也就不能直接作为量子门。$U_f$ 保留 $x$，并把 $f(x)$ 通过 XOR 写入辅助位，从而避免信息丢失。

事实上，对同一状态连续作用两次 $U_f$，有

$$
\begin{aligned}
U_f^2|x\rangle|y\rangle
&=U_f|x\rangle|y\oplus f(x)\rangle\\
&=|x\rangle|y\oplus f(x)\oplus f(x)\rangle\\
&=|x\rangle|y\rangle,
\end{aligned}
$$

因为一个比特与自身异或两次会抵消，即 $f(x)\oplus f(x)=0$。所以

$$
U_f^2=I,
\qquad
U_f^{-1}=U_f.
$$

$U_f$ 只是重新排列计算基态，因而保持内积，是合法的酉变换。

#### 对叠加态的作用

上面的定义虽然只写了基态 $|x\rangle|y\rangle$，但由量子力学的线性性，它也唯一确定了 $U_f$ 对任意叠加态的作用：

$$
U_f\left(\sum_x\alpha_x|x\rangle|y\rangle\right)
=\sum_x\alpha_x|x\rangle|y\oplus f(x)\rangle.
$$

也就是说，一次调用 $U_f$ 会在叠加态的每个 $|x\rangle$ 分量上写入对应的 $f(x)$。这常被简称为“同时计算所有输入”，但它不表示测量一次就能读出所有函数值：测量仍只会给出一个经典结果。Deutsch-Jozsa 算法真正利用的是不同分量之间的相位干涉；辅助位为何被制备成 $|-\rangle$，将在 8.5 节的相位回踢中说明。

算法流程：
![](https://ik.imagekit.io/obzl69adx/obsidian/picture_xtB1hy1qy)

等价地：

1. 准备 $|0\rangle^{\otimes n}|1\rangle$；
2. 对全部 $n+1$ 个量子比特施加 Hadamard 门；
3. 查询一次 $U_f$；
4. 对前 $n$ 个量子比特施加 $H^{\otimes n}$；
5. 测量前 $n$ 个量子比特。若结果为 $0^n$，则 $f$ 为常函数；否则为平衡函数。

### 8.4 第一步：制造均匀叠加

两个基本公式是

$$
H|0\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},\qquad
H|1\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2}.
$$

所以

$$
H^{\otimes(n+1)}|0\rangle^{\otimes n}|1\rangle
=\frac1{\sqrt{2^n}}
\sum_{x\in\{0,1\}^n}|x\rangle
\otimes\frac{|0\rangle-|1\rangle}{\sqrt2}.
$$

输入寄存器现在均匀覆盖全部 $2^n$ 个 $x$，辅助位处于 $|-\rangle$。

### 8.5 第二步：相位回踢

对辅助位 $|-\rangle$ 使用 oracle：

$$
\begin{aligned}
U_f\left(|x\rangle\frac{|0\rangle-|1\rangle}{\sqrt2}\right)
&=|x\rangle\frac{|f(x)\rangle-|1\oplus f(x)\rangle}{\sqrt2}\\
&=(-1)^{f(x)}|x\rangle\frac{|0\rangle-|1\rangle}{\sqrt2}.
\end{aligned}
$$

函数值没有以普通比特形式留在辅助位上，而是变成输入分量的正负相位：

$$
\frac1{\sqrt{2^n}}
\sum_x(-1)^{f(x)}|x\rangle\otimes|-\rangle.
$$

这叫**相位回踢**。辅助位此后与判断结果无关，可以暂时略去。

### 8.6 第三步：Hadamard 干涉

对任意 $n$ 位串 $x$，有

$$
H^{\otimes n}|x\rangle
=\frac1{\sqrt{2^n}}
\sum_{z\in\{0,1\}^n}(-1)^{x\cdot z}|z\rangle,
$$

其中

$$
x\cdot z=x_0z_0\oplus x_1z_1\oplus\cdots\oplus x_{n-1}z_{n-1}.
$$

因此第二次 Hadamard 后，输入寄存器为

$$
\frac1{2^n}\sum_z
\left[\sum_x(-1)^{f(x)}(-1)^{x\cdot z}\right]|z\rangle.
$$

输出 $z$ 的振幅是

$$
A_z=\frac1{2^n}\sum_x(-1)^{f(x)+x\cdot z}.
$$

这其实是布尔函数 $(-1)^{f(x)}$ 的 Walsh-Hadamard 变换。

### 8.7 为什么只看 $0^n$ 就够了

令 $z=0^n$，则 $x\cdot z=0$，故

$$
A_{0^n}=\frac1{2^n}\sum_x(-1)^{f(x)}.
$$

- 若 $f(x)\equiv0$，每一项都是 $+1$，所以 $A_{0^n}=1$；
- 若 $f(x)\equiv1$，每一项都是 $-1$，所以 $A_{0^n}=-1$，测量概率仍为 1；
- 若 $f$ 平衡，正负项各一半，完全相消，所以 $A_{0^n}=0$。

因此

$$
P(0^n)=|A_{0^n}|^2=
\begin{cases}
1,&f\text{ 为常函数},\\
0,&f\text{ 为平衡函数}.
\end{cases}
$$

只调用一次 $U_f$ 就能无误判定。这是确定性查询复杂度中的指数分离。

### 8.8 一个 $n=2$ 的手算例子

若 $f(x_1x_0)=x_1$，则

| $x$ | $f(x)$ | $(-1)^{f(x)}$ |
|---|---:|---:|
| 00 | 0 | $+1$ |
| 01 | 0 | $+1$ |
| 10 | 1 | $-1$ |
| 11 | 1 | $-1$ |

oracle 后输入寄存器为

$$
\frac12(|00\rangle+|01\rangle-|10\rangle-|11\rangle)
=|-\rangle\otimes|+\rangle.
$$

再施加 $H\otimes H$：

$$
(H|-\rangle)\otimes(H|+\rangle)=|1\rangle\otimes|0\rangle=|10\rangle.
$$

结果必定不是 $|00\rangle$，所以函数被判定为平衡。若 $f\equiv0$ 或 $f\equiv1$，最终输入寄存器都必为 $|00\rangle$；两种常函数只差一个不可观测的全局负号。

### 8.9 “指数加速”需要加的限定语

Deutsch-Jozsa 算法展示的是**黑箱查询复杂度**：量子算法查询 oracle 1 次，经典确定性算法最坏查询 $2^{n-1}+1$ 次。不能简单理解为任何实际程序都在固定时间内完成，因为：

- $H^{\otimes n}$ 含 $n$ 个单量子比特门，虽然可并行，门数仍随 $n$ 增长；
- oracle $U_f$ 的具体线路可能很复杂，其构造成本在黑箱模型中被隐藏；
- 随机经典算法用少量查询也能以很高置信度判断，只是不能做到一次查询且零误差；
- 噪声、编译和纠错成本也不在抽象查询模型中。

这个算法的真正教学价值，是清楚展示“叠加 + 相位回踢 + 干涉 + 测量”的标准量子算法套路。

## 9. 原文中需要订正或谨慎理解的地方

| 原文表述 | 问题 | 本讲义采用的正确表述 |
|---|---|---|
| 某态是“over $2^1$ / $2^2$ / $2^8$ qubits” | 把量子比特数和空间维数混淆 | 1、2、8 个量子比特分别对应 $2$、$4$、$256$ 维空间 |
| $\lvert1000\rangle\langle0001\rvert$ 是 $4\times4$ 矩阵 | 四量子比特空间维数为 $16$ | 它是 $16\times16$ 矩阵，只有第 $(8,1)$ 元为 1（从 0 编号） |
| 一般算符作用后再除以归一化因子就得到量子门输出 | 非线性的“事后归一化”不能把任意矩阵变成合法量子门 | 理想量子门本身必须酉；酉性自动保持范数，不需手动归一化 |
| $\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt2}$ 是“四量子比特态” | ket 中只有两位 | 这是两量子比特 Bell 态 |
| 纠缠证明中两个单比特因子都写成 $a\lvert0\rangle+b\lvert0\rangle$ | 应同时包含 $\lvert0\rangle$ 与 $\lvert1\rangle$，且展开式漏了加号 | 使用 $(a\lvert0\rangle+b\lvert1\rangle)\otimes(c\lvert0\rangle+d\lvert1\rangle)$，见 5.3 节 |
| 算法“constant time (a single step)”或只需“三次门操作” | 混淆 oracle 查询次数、线路深度和总门数 | 严格优势是 1 次量子查询对比指数次经典确定性查询；其余资源仍需单独计算 |
| 测得 $\lvert0\rangle$ 就判定为常函数 | 前寄存器有 $n$ 位，写法不完整 | 应为测得 $\lvert0\rangle^{\otimes n}=\lvert0^n\rangle$ |
| 纠缠在 Deutsch-Jozsa 的抽象推导中不出现，但实际实现必需 | 该说法依赖 oracle 和实现方式，不能一概而论 | 算法的核心干涉推导不依赖把纠缠作为显式资源；具体线路是否产生纠缠取决于 $f$ 与实现 |

这些问题不影响原文作为“最小化导论”的整体路线，但做计算时应采用本讲义中的订正版公式。

## 10. 原文结论与后续学习路线

原文的结论是：量子线路模型可以在暂时不深入量子物理的情况下，用基础线性代数和复数知识建立；Deutsch-Jozsa 算法则给出了量子算法优于经典确定性算法的一个清晰示例。

建议按以下顺序继续学习：

1. 单量子比特的 Bloch 球、Pauli 矩阵和旋转门；
2. 密度矩阵、部分迹、混合态与量子测量；
3. Bell 态、纠缠判据和 Bell 不等式；
4. 可逆计算、通用量子门集和线路分解；
5. Bernstein-Vazirani、Simon 和 Grover 算法；
6. 量子傅里叶变换、相位估计与 Shor 算法；
7. 噪声模型、量子纠错和容错量子计算；
8. 使用 Qiskit 等框架把抽象线路映射到真实或模拟后端。

原文推荐的主要书目包括：

- Nielsen 与 Chuang，*Quantum Computation and Quantum Information*，体系严谨，适合进阶；
- Rieffel 与 Polak，*Quantum Computing: A Gentle Introduction*，入门较平缓；
- Wong，*Introduction to Classical and Quantum Computing*，前置要求较少；
- Yanofsky 与 Mannucci，*Quantum Computing for Computer Scientists*，偏计算机科学视角；
- Schuld 与 Petruccione，*Machine Learning with Quantum Computers*，偏量子机器学习。

## 11. 自测题

1. 写出 $|101\rangle$ 的八维列向量，并说明它是几个量子比特、处于几维空间。
2. 判断 $\frac12|00\rangle+\frac{i}{2}|01\rangle+\frac1{\sqrt2}|11\rangle$ 是否归一化，并求各测量结果概率。
3. 直接用外积验证 $X=|0\rangle\langle1|+|1\rangle\langle0|$ 的矩阵形式。
4. 证明 $H^2=I$，并解释为什么 $H$ 既能“产生叠加”又能“消除叠加”。
5. 判断 $\frac{|00\rangle+|01\rangle+|10\rangle+|11\rangle}{2}$ 是否纠缠，并给出分解。
6. 从 $|00\rangle$ 出发，用 $H$ 和 CNOT 构造 Bell 态。
7. 对 $n=2$、$f(x_1x_0)=x_0$ 完整手算 Deutsch-Jozsa 算法的最终态。
8. 解释为什么“对所有 $x$ 同时计算了 $f(x)$”并不意味着可以一次测量读出全部 $f(x)$。

### 自测题简答

1. $|101\rangle=(0,0,0,0,0,1,0,0)^{\mathrm T}$；3 个量子比特，八维空间。
2. 概率和为 $1/4+1/4+1/2=1$；结果 `00`、`01`、`11` 的概率依次为 $1/4,1/4,1/2$。
3. 两个外积分别为 $\begin{pmatrix}0&1\\0&0\end{pmatrix}$ 与 $\begin{pmatrix}0&0\\1&0\end{pmatrix}$，相加得到 $X$。
4. 矩阵相乘可得 $H^2=I$；是否呈现为叠加取决于所选测量基，相位经第二次 $H$ 转成确定的计算基结果。
5. 不纠缠，它等于 $|+\rangle\otimes|+\rangle$。
6. 依次施加 $H\otimes I$ 与 CNOT。
7. 最终输入寄存器为 $|01\rangle$，因此判定平衡。
8. 测量只抽取一个基态结果；量子优势来自振幅干涉所提取的整体性质，而不是读取指数多条经典数据。

---

## 第一部分一页复习

$$
|\psi\rangle=\sum_x c_x|x\rangle,\qquad \sum_x|c_x|^2=1
$$

$$
P(x)=|c_x|^2,\quad U^\dagger U=I
$$

$$
H|0\rangle=|+\rangle,\qquad H|1\rangle=|-\rangle
$$

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle
$$

$$
U_f(|x\rangle|-\rangle)=(-1)^{f(x)}|x\rangle|-\rangle
$$

$$
A_{0^n}=\frac1{2^n}\sum_x(-1)^{f(x)}
=\begin{cases}
\pm1,&f\text{ 常值},\\
0,&f\text{ 平衡}.
\end{cases}
$$

**核心认识：量子算法不是把所有答案直接读出，而是先把所需的整体信息编码进相位，再利用干涉把它集中到少数可测量结果中。**

---

# 第二部分：《Quantum Algorithm Implementations for Beginners》补充

## 12. 文献定位与摘要翻译

第二篇文献的目标是训练具有经典编程经验的量子程序员。作者用尽量直接的代数介绍量子编程，并把算法落实到真实量子硬件。论文共调查 20 个算法或量子计算任务，给出 IBM 量子计算机上的小规模实现，并比较理想模拟器和实际硬件结果。

原文摘要的核心意思是：

> 随着量子计算机逐渐开放给普通用户，需要培养能够编写量子程序的人才。当时可用设备的量子比特数还不到 100，但硬件规模、质量和连通性预计会继续提高。本文介绍量子编程原理以及算法在真实硬件上的实现，力求让底层量子力学不是阅读的硬性前提。作者调查 20 种量子算法，展示其在 IBM 量子计算机上的实现，并讨论模拟器结果与硬件结果的差异，为计算机科学家、物理学家和工程师提供实现蓝图。

与第一篇文献相比，本篇新增了三条主线：

1. 从“量子态和量子门是什么”前进到“怎样构造完整算法”；
2. 从理想线路前进到编译、连通性、噪声和线路深度；
3. 从单一的 Deutsch-Jozsa 算法扩展到搜索、数论、线性代数、图算法、机器学习、量子模拟和误差处理。

> **版本提醒**：论文的算法原理仍有学习价值，但其中的 IBM 设备名称、校准数据、Qiskit 模块划分和代码接口属于 2018-2022 年生态。阅读时应把它们视为历史实验记录，而不是 2026 年可直接运行的 API 文档。

## 13. 可观测量、期望值与测量基

### 13.1 从概率到期望值

第一部分只讨论了“测到某个比特串的概率”。实际物理实验更常关心可观测量的平均值。

设单量子比特态为

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle.
$$

若测得 $|0\rangle$ 记作 $+1$，测得 $|1\rangle$ 记作 $-1$，平均值为

$$
|\alpha|^2-|\beta|^2.
$$

这个实验对应 Pauli-$Z$ 算符

$$
Z=|0\rangle\langle0|-|1\rangle\langle1|
=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
$$

期望值可紧凑写成

$$
\langle Z\rangle_\psi=\langle\psi|Z|\psi\rangle
=|\alpha|^2-|\beta|^2.
$$

一般可观测量 $O$ 必须是 Hermitian 算符：

$$
O^\dagger=O.
$$

它可以谱分解为

$$
O=\sum_i o_i|\phi_i\rangle\langle\phi_i|,
$$

其中 $o_i$ 为实特征值，$|\phi_i\rangle$ 为正交归一特征态。测量得到 $o_i$ 的概率是

$$
P(o_i)=|\langle\phi_i|\psi\rangle|^2,
$$

因此

$$
\langle O\rangle_\psi
=\sum_i o_iP(o_i)
=\langle\psi|O|\psi\rangle.
$$

### 13.2 怎样测量 $X$、$Y$ 和一般基

硬件通常原生执行计算基（$Z$ 基）测量。若想测量另一组正交基，可以先做基变换，再测量 $Z$。

| 目标可观测量 | 测量前操作 | 随后执行 |
|---|---|---|
| $Z$ | 无 | 计算基测量 |
| $X$ | $H$ | 计算基测量 |
| $Y$ | 先 $S^\dagger$，后 $H$ | 计算基测量 |

例如 $X$ 的本征态是 $|+\rangle$ 和 $|-\rangle$，而

$$
H|+\rangle=|0\rangle,\qquad H|-\rangle=|1\rangle.
$$

所以“先做 $H$ 再测 $Z$”等价于直接测 $X$。

### 13.3 多量子比特 Pauli 串

量子模拟和变分算法常把 Hamiltonian 写成 Pauli 串之和：

$$
\mathcal H=\sum_\mu c_\mu P_\mu,\qquad
P_\mu\in\{I,X,Y,Z\}^{\otimes n}.
$$

于是能量为

$$
E=\langle\mathcal H\rangle
=\sum_\mu c_\mu\langle P_\mu\rangle.
$$

每个 $\langle P_\mu\rangle$ 都可通过选择合适的单比特测量基并重复采样估计。这里出现了真实算法的重要成本：Hamiltonian 的项数、每项所需 shots，以及不同 Pauli 项能否分组共同测量。

## 14. 新增量子门与通用门集

### 14.1 Pauli 门和相位门

除 $X$ 外，常用单比特门还有

$$
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\qquad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
$$

$$
S=\begin{pmatrix}1&0\\0&i\end{pmatrix},\qquad
T=\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}.
$$

$S$ 和 $T$ 改变 $|1\rangle$ 分量相对于 $|0\rangle$ 的相位，并满足

$$
S=T^2,\qquad Z=S^2=T^4.
$$

一般相位门为

$$
P(\phi)=\begin{pmatrix}1&0\\0&e^{i\phi}\end{pmatrix}.
$$

绕 Bloch 球轴旋转的标准写法是

$$
R_\nu(\theta)=e^{-i\theta\sigma_\nu/2},
\qquad \nu=x,y,z.
$$

### 14.2 受控-$U$ 与 Toffoli 门

任意受控门可写成

$$
CU=|0\rangle\langle0|\otimes I
+|1\rangle\langle1|\otimes U.
$$

控制位为 0 时不操作目标系统，控制位为 1 时施加 $U$。

Toffoli 门又称 CCNOT，有两个控制位和一个目标位：

$$
|a,b,c\rangle\longmapsto|a,b,c\oplus ab\rangle.
$$

它能把经典 AND 嵌入可逆线路，并常用于构造 oracle。

> **订正**：原文说“Toffoli 门本身是通用的”，若指任意量子计算并不准确。Toffoli 对经典可逆计算是通用的，但它不能独自从计算基态制造叠加。常见近似通用量子门集是 $\{H,T,\mathrm{CNOT}\}$；“任意单比特门 + CNOT”则可精确生成任意多比特酉变换。

## 15. 从理想线路到真实硬件

### 15.1 用户门、基门与编译

程序员写出的 $H$、$X$、受控相位门等通常不是硬件直接执行的脉冲。编译器要完成：

$$
\text{抽象线路}
\rightarrow\text{基门分解}
\rightarrow\text{量子比特映射}
\rightarrow\text{路由与 SWAP}
\rightarrow\text{调度和脉冲}.
$$

因此，“算法只含 10 个高层门”并不等于“硬件只执行 10 个物理操作”。

### 15.2 连通性与线路深度

两量子比特门通常只能在芯片耦合图的相邻量子比特之间执行。若逻辑量子比特不相邻，编译器必须插入 SWAP 或等价路由。

需要区分：

- **门数**：线路中门的总量；
- **线路深度**：考虑可并行门之后的最长依赖链；
- **两比特门数**：通常比单比特门更能预测噪声；
- **关键路径时间**：从初始化到测量的实际持续时间。

原文的 Grover 实验显示，同一逻辑算法若不顺应芯片连通性，正确率会从约 $65\%$ 降到 $48\%$。这说明量子程序性能不仅由算法决定，也由映射和编译决定。

### 15.3 主要误差来源

- **读出误差**：真实态与记录的经典比特不一致；
- **单比特和双比特门误差**：实际酉变换偏离目标门；
- **能量弛豫 $T_1$**：激发态向基态衰减；
- **退相干 $T_2$**：相对相位信息丢失；
- **串扰和漂移**：一个操作影响邻近量子比特，设备参数随时间改变；
- **有限 shots**：概率估计有统计误差。

模拟器与硬件的差异不是附属问题，而是 NISQ 算法设计的一部分。

## 16. 论文中的算法全景

| 类别 | 论文主题 | 核心范式 | 主要输出或目标 |
|---|---|---|---|
| 搜索 | Grover 搜索 | 振幅放大 | 找到被 oracle 标记的元素 |
| 隐藏字符串 | Bernstein-Vazirani | 相位回踢、Hadamard 干涉 | 一次查询恢复隐藏串 |
| 线性代数 | HHL 线性方程组 | 相位估计、受控旋转 | 制备与 $A^{-1}b$ 成比例的量子态 |
| 数论 | Shor 分解 | 周期寻找、QFT | 分解整数 |
| 群表示 | 矩阵元计算 | Hadamard test、群 Fourier 变换 | 估计 $\langle\psi\vert U\vert\psi\rangle$ |
| 线性代数验证 | 矩阵乘积验证 | 嵌套振幅放大 | 判断 $AB=C$ |
| 抽象代数 | Abel 群同构 | 隐子群问题、QFT | 分解有限 Abel 群 |
| 图算法 | 量子随机游走 | coin + shift | 在图上相干传播或搜索 |
| 图算法 | 最小生成树 | Grover 最小值搜索 | 找到低权生成树 |
| 图算法 | 最大流 | Grover 加速分层图构造 | 求网络最大流 |
| 组合优化 | QAOA | 变分量子-经典循环 | 采样高质量近似解 |
| 机器学习 | qPCA | 密度矩阵、相位估计 | 提取主成分信息 |
| 机器学习 | 量子 SVM | 量子内积、HHL | 二分类 |
| 量子模拟 | 薛定谔方程 | QFT、分裂算符 | 模拟波函数演化 |
| 多体物理 | 横场 Ising 基态 | VQE | 估计基态能量与可观测量 |
| 统计物理 | 配分函数 | Gauss 和、QFT | 计算特定模型的 $Z$ |
| 工具 | 量子态制备 | Bloch 球、Schmidt 分解 | 从全零态制备目标态 |
| 工具 | 量子层析 | 多基测量、统计估计 | 重建密度矩阵 |
| 可靠性 | 量子纠错测试 | 三比特重复码 | 检测简单比特翻转保护效果 |

这些应用表面差别很大，但大多是少数范式的组合。学习时应优先掌握 Grover/振幅放大、QFT/相位估计、Hamiltonian 模拟和变分循环。

## 17. Grover 搜索与振幅放大

### 17.1 问题

在 $N=2^n$ 个候选中有 $M$ 个目标。相位 oracle 的作用为

$$
O_f|x\rangle=(-1)^{f(x)}|x\rangle,
$$

其中目标态满足 $f(x)=1$。

从均匀叠加

$$
|s\rangle=\frac1{\sqrt N}\sum_{x=0}^{N-1}|x\rangle
$$

出发，Grover 迭代为

$$
G=(2|s\rangle\langle s|-I)O_f.
$$

第一部分是扩散算符，第二部分是 oracle。

### 17.2 “关于平均振幅翻转”

若当前态为 $\sum_x a_x|x\rangle$，平均振幅为

$$
\bar a=\frac1N\sum_xa_x,
$$

则扩散算符把每个振幅变为

$$
a_x\longmapsto2\bar a-a_x.
$$

oracle 先把目标振幅变号，使它落到平均值下方；扩散算符再关于平均值反射，于是目标振幅被抬高。

### 17.3 二维旋转图像

令 $|w\rangle$ 是所有目标态的均匀叠加，$|r\rangle$ 是所有非目标态的均匀叠加，并定义

$$
\sin\theta=\sqrt{\frac MN}.
$$

则

$$
|s\rangle=\sin\theta|w\rangle+\cos\theta|r\rangle.
$$

每次 Grover 迭代在 $\{|w\rangle,|r\rangle\}$ 平面内旋转 $2\theta$。约经过

$$
k\approx\frac\pi4\sqrt{\frac NM}
$$

次迭代，态接近目标子空间。迭代过多会“转过头”，成功率反而下降。

### 17.4 从 Grover 到一般振幅放大

若某个量子子程序 $U$ 一次成功的概率为 $p$，经典重复通常需要 $O(1/p)$ 次。量子振幅放大使用

$$
Q=U(2|0\rangle\langle0|-I)U^\dagger O
$$

把次数降为 $O(1/\sqrt p)$。Grover 搜索就是 $U=H^{\otimes n}$ 的特例。

> Grover 提供平方加速而不是指数加速；oracle 的构造成本仍必须计入完整资源。

## 18. Bernstein-Vazirani 算法

### 18.1 问题

给定隐藏串 $s\in\{0,1\}^n$，函数满足

$$
f_s(x)=s\cdot x
=s_0x_0\oplus\cdots\oplus s_{n-1}x_{n-1}.
$$

经典确定性查询每次只得到 1 bit，最坏需要 $n$ 次；量子算法只查询 oracle 一次。

### 18.2 推导

准备

$$
|0\rangle^{\otimes n}|1\rangle
\xrightarrow{H^{\otimes(n+1)}}
\frac1{\sqrt{2^n}}\sum_x|x\rangle|-\rangle.
$$

相位回踢给出

$$
\frac1{\sqrt{2^n}}\sum_x(-1)^{s\cdot x}|x\rangle|-\rangle.
$$

利用

$$
H^{\otimes n}|s\rangle
=\frac1{\sqrt{2^n}}\sum_x(-1)^{s\cdot x}|x\rangle,
$$

可知再施加 $H^{\otimes n}$ 后

$$
|s\rangle|-\rangle
$$

以概率 1 得到。Deutsch-Jozsa 判断函数属于哪一类；Bernstein-Vazirani 则恢复定义函数的完整隐藏串。

> **实现提示**：查询复杂度把 oracle 当黑箱。原文讨论了把任意酉矩阵分解时可能出现的指数门数，但标准 BV oracle 利用 $f_s$ 的线性结构，只需对每个 $s_i=1$ 的位置添加一条指向辅助位的 CNOT，最多 $n$ 条。不能把“任意酉分解成本”误当成 BV oracle 的必要成本。

## 19. 量子 Fourier 变换与相位估计

### 19.1 QFT

对 $N=2^n$，

$$
\operatorname{QFT}_N|x\rangle
=\frac1{\sqrt N}\sum_{y=0}^{N-1}
e^{2\pi ixy/N}|y\rangle.
$$

经典 DFT 变换一个显式长度 $N$ 的数组；QFT 变换的是 $n=\log_2N$ 个量子比特的振幅。标准精确 QFT 线路包含 $O(n^2)$ 个 Hadamard 和受控相位门。

QFT 的指数优势不能理解为“用 $O(n^2)$ 门输出全部 $N$ 个 Fourier 系数”。测量仍只得到一个样本。只有当后续任务需要周期、相位等可通过干涉提取的整体性质时，QFT 才产生算法优势。

### 19.2 量子相位估计 QPE

若

$$
U|u\rangle=e^{2\pi i\varphi}|u\rangle,
$$

QPE 用 $t$ 个计数辅助位估计 $\varphi$：

1. 对计数寄存器施加 $H^{\otimes t}$；
2. 依次施加受控 $U^{2^0},U^{2^1},\ldots,U^{2^{t-1}}$；
3. 对计数寄存器施加逆 QFT；
4. 测量得到 $\varphi$ 的 $t$ 位近似。

若输入不是单个本征态，而是

$$
|\psi\rangle=\sum_jc_j|u_j\rangle,
$$

输出会把本征相位与本征态关联：

$$
\sum_jc_j|\widetilde\varphi_j\rangle|u_j\rangle.
$$

测量相位寄存器得到 $\widetilde\varphi_j$ 的概率约为 $|c_j|^2$。

> QPE 的主要成本常常不是逆 QFT，而是实现高次受控 $U^{2^k}$。精度提高一位通常意味着更长的相干演化或更多受控操作。

## 20. HHL：量子线性方程组算法

### 20.1 它解决的不是“打印完整解向量”

给定 Hermitian 矩阵 $A$ 和向量 $b$，希望制备

$$
|x\rangle=
\frac{A^{-1}|b\rangle}{\|A^{-1}|b\rangle\|}.
$$

若

$$
A|u_j\rangle=\lambda_j|u_j\rangle,\qquad
|b\rangle=\sum_j\beta_j|u_j\rangle,
$$

则目标态满足

$$
|x\rangle\propto\sum_j\frac{\beta_j}{\lambda_j}|u_j\rangle.
$$

### 20.2 三个关键步骤

1. 用 $e^{iAt}$ 做 QPE，把 $\lambda_j$ 写入特征值寄存器；
2. 根据 $\lambda_j$ 对辅助位做受控旋转，使 $|1\rangle$ 振幅正比于 $C/\lambda_j$；
3. 反做 QPE，消去特征值寄存器；后选择辅助位为 $|1\rangle$ 时，主寄存器即与 $A^{-1}|b\rangle$ 成比例。

### 20.3 必须写在“量子加速”旁边的条件

- $A$ 要能被高效表示或 block-encode，并适合 Hamiltonian 模拟；
- $|b\rangle$ 要能高效制备；
- 复杂度强烈依赖条件数 $\kappa=|\lambda_{\max}/\lambda_{\min}|$；
- 输出是量子态 $|x\rangle$，逐项读出全部 $N$ 个分量一般要付出至少线性成本；
- HHL 最适合估计 $\langle x|M|x\rangle$ 等整体量，而不是替代所有经典线性求解器；
- 数据装载、精度 $\epsilon$、稀疏性和读出成本都必须计入。

原文的五量子比特实验在模拟器上符合理论，但真实硬件没有给出正确答案，说明深 QPE、受控旋转和后选择对噪声非常敏感。

## 21. Shor 算法：从整数分解到周期寻找

### 21.1 经典外壳

要分解奇合数 $N$：

1. 随机选 $a<N$；
2. 若 $\gcd(a,N)>1$，已得到因子；
3. 否则寻找最小正整数 $r$，使 $a^r\equiv1\pmod N$；
4. 若 $r$ 为偶数且 $a^{r/2}\not\equiv-1\pmod N$，计算

$$
\gcd(a^{r/2}-1,N),\qquad
\gcd(a^{r/2}+1,N).
$$

它们以较高概率给出非平凡因子；失败时重新选择 $a$。

### 21.2 量子核心

量子部分高效寻找周期 $r$：

$$
|x\rangle|0\rangle
\longmapsto
|x\rangle|a^x\bmod N\rangle,
$$

随后对第一寄存器做逆 QFT。测量值接近某个 $k/r$ 的二进制近似，再用经典连分数恢复 $r$。

例：$N=15,a=7$ 时

$$
7^x\bmod15:1,7,4,13,1,\ldots
$$

周期 $r=4$。于是

$$
\gcd(7^2-1,15)=3,\qquad
\gcd(7^2+1,15)=5.
$$

原文在五量子比特设备上使用了专门为 $N=15$ 编译的 11 门线路；这只是展示周期寻找机制，并不是可扩展整数分解的完整资源规模。

## 22. Hadamard test：估计酉算符矩阵元

目标是估计

$$
\langle\psi|U|\psi\rangle.
$$

使用一个辅助位：

1. 从 $|0\rangle|\psi\rangle$ 开始；
2. 对辅助位做 $H$；
3. 以辅助位控制施加 $U$；
4. 再对辅助位做 $H$ 并测量。

测得 0 的概率为

$$
P(0)=\frac{1+\operatorname{Re}\langle\psi|U|\psi\rangle}{2},
$$

所以

$$
\operatorname{Re}\langle\psi|U|\psi\rangle=2P(0)-1.
$$

在辅助位加入适当相位门可同样得到虚部。Hadamard test 把“估计复杂矩阵元”化成“实现受控-$U$ 并统计一个辅助位”，但受控-$U$ 的实现可能仍然昂贵。

## 23. 量子随机游走与图算法

### 23.1 离散时间量子游走

在一个 $N=2^n$ 个顶点的环上，用 $n$ 个位置量子比特和 1 个 coin 量子比特。一步游走为

$$
W=SC,
$$

其中 $C=I\otimes H$ 混合 coin 状态，$S$ 根据 coin 状态向左或向右移动。$T$ 步后状态为

$$
|\psi_T\rangle=(SC)^T|\psi_0\rangle.
$$

经典随机游走演化概率；量子游走演化复振幅，因此不同路径能够干涉。额外 coin 自由度用于保持演化可逆和酉。

### 23.2 最小生成树

论文的量子方案把 Borůvka 算法与 Grover 最小值搜索结合。经典 Borůvka 每轮为每个连通分量寻找最轻出边并合并分量；量子最小值搜索把长度 $N$ 列表的比较次数从 $O(N)$ 降为 $O(\sqrt N)$ 量级。

论文给出的查询复杂度为

$$
O(\sqrt{nm}),
$$

其中 $n$ 是顶点数、$m$ 是边数。这个结果依赖能够以 oracle 方式访问边和权重，不能直接等同于端到端运行时间。

### 23.3 最大流与矩阵乘积验证

- 最大流算法用 Grover 搜索加速 Edmonds-Karp 中的分层图构造，是“经典算法外壳 + 量子子程序”的例子；
- 矩阵乘积验证先随机压缩问题，再用嵌套振幅放大搜索错误块和错误行；
- 论文所述矩阵验证量子复杂度优于其引用的经典界，但线路和数据 oracle 太大，无法在当时 IBM 设备上实现。

这类算法提醒我们区分三种结论：查询复杂度加速、门复杂度加速、端到端实际加速。

### 23.4 有限 Abel 群与隐子群问题

论文还讨论了群同构和群表示矩阵元。有限 Abel 群可分解为循环群的直积，量子算法把分解任务约化为隐子群问题（HSP）。给定函数 $g:A\to X$，若它在子群 $K$ 的每个陪集上取常值、不同陪集取不同值，则 $K$ 是隐藏子群。

量子过程先制备群元素均匀叠加，查询一次 $g$，再做群 Fourier 变换并采样与 $K$ 正交的特征标。多次样本经经典后处理恢复 $K$ 的生成元。周期寻找、阶寻找和离散对数都可以看作 HSP 的具体形式。

非 Abel 群的高效 Fourier 变换与采样通常更困难，所以“Shor 思路推广到任意群”并不自动成立。

## 24. QAOA：组合优化的量子-经典混合算法

### 24.1 把目标函数写成 Hamiltonian

以 MaxCut 为例，对边 $(u,v)$ 定义

$$
C_{uv}=\frac12(I-Z_uZ_v).
$$

若两个端点的计算基比特不同，该项本征值为 1；相同则为 0。总成本 Hamiltonian 为

$$
C=\sum_{(u,v)\in E}C_{uv}.
$$

混合 Hamiltonian 常取

$$
B=\sum_{j=1}^nX_j.
$$

### 24.2 $p$ 层 QAOA 状态

从 $|+\rangle^{\otimes n}$ 出发：

$$
|\boldsymbol\beta,\boldsymbol\gamma\rangle
=\prod_{k=1}^{p}
e^{-i\beta_kB}e^{-i\gamma_kC}
|+\rangle^{\otimes n}.
$$

量子设备重复制备和测量该态，估计

$$
F(\boldsymbol\beta,\boldsymbol\gamma)
=\langle C\rangle.
$$

经典优化器据此更新参数，再把新参数送回量子设备。

### 24.3 物理直觉和限制

$e^{-i\gamma C}$ 按解的目标函数值写入相位，$e^{-i\beta B}$ 在候选解之间混合振幅。多轮交替试图把高成本解的概率抬高。

理想无噪声条件下，增大 $p$ 扩大可表示线路族；但实际中：

- 线路变深导致双比特门误差和退相干增加；
- 参数空间维数为 $2p$，经典优化可能陷入局部极值；
- 每次函数评估需要许多 shots；
- 更高的理想层数不保证真实硬件效果更好；
- QAOA 一般是启发式算法，不意味着多项式时间求解 NP-hard 问题。

原文的 Triangle+Edge 小图实验中，$p=2$ 的理想模拟优于 $p=1$，但硬件增益大幅缩小，正是“表达能力增加”和“噪声增加”的竞争。

## 25. 量子机器学习：qPCA 与量子 SVM

### 25.1 密度矩阵与纯化

若系统以概率 $p_i$ 处于 $|\psi_i\rangle$，则

$$
\rho=\sum_ip_i|\psi_i\rangle\langle\psi_i|.
$$

密度矩阵满足

$$
\rho^\dagger=\rho,\qquad \rho\succeq0,\qquad\operatorname{Tr}\rho=1.
$$

纯态满足 $\rho^2=\rho$ 和 $\operatorname{Tr}\rho^2=1$；混合态则有 $\operatorname{Tr}\rho^2<1$。

任何混合态都可看成更大系统纯态的一部分，这叫纯化。若

$$
|\Psi\rangle_{AB}=\sum_i\sqrt{p_i}|\psi_i\rangle_A|i\rangle_B,
$$

则对 $B$ 做部分迹得到

$$
\rho_A=\operatorname{Tr}_B|\Psi\rangle\langle\Psi|.
$$

### 25.2 qPCA

经典 PCA 对协方差矩阵 $\Sigma$ 对角化，保留大特征值对应的主成分。原始 qPCA 思路是：

1. 把归一化后的 $\Sigma$ 编码为密度矩阵 $\rho$；
2. 准备多份 $\rho$；
3. 通过 density matrix exponentiation 实现与 $e^{-i\rho t}$ 有关的演化；
4. 用 QPE 估计特征值和主成分。

原文受五量子比特限制，只实现了两维数据的 purity 测量。模拟器给出合理特征值，硬件却得到带虚部的“协方差特征值”，显然不物理。

### 25.3 量子 SVM 与数据访问假设

论文的量子 SVM 以最小二乘 SVM 为基础：

1. 用量子内积构造 kernel；
2. 用 HHL 类算法求训练线性方程；
3. 以量子态形式保存分类器并对查询态分类。

这类指数加速结论通常依赖 qRAM、振幅编码、高效状态制备、良好条件数和只输出少量统计量。若输入是普通经典数组，数据装载本身可能抵消优势；若要读出全部模型参数，也会失去对数维度优势。

## 26. Hamiltonian 模拟与 VQE

### 26.1 分裂算符法模拟薛定谔方程

对

$$
H=T(\hat p)+V(\hat x),
$$

短时间演化可作一阶 Trotter 近似：

$$
e^{-iH\Delta t}
\approx e^{-iV(\hat x)\Delta t}
e^{-iT(\hat p)\Delta t}
+O(\Delta t^2).
$$

位置表象中 $V(\hat x)$ 对角，动量表象中 $T(\hat p)$ 对角。QFT 在二者之间转换：

$$
|\psi(t+\Delta t)\rangle
\approx e^{-iV\Delta t}
\operatorname{QFT}^{\dagger}
e^{-iT\Delta t}
\operatorname{QFT}
|\psi(t)\rangle.
$$

重复若干时间步即可模拟演化。误差来自空间离散化、有限时间步、Trotter 截断、门分解和硬件噪声。

> 原文写“$|\psi(x,t)|^2$ 是在位置 $x$ 找到粒子的概率”，连续变量下更准确的说法是概率密度；有限区间概率为 $\int_a^b|\psi(x,t)|^2dx$。

### 26.2 VQE 与变分原理

对任意归一化试探态，

$$
E(\theta)=\langle\psi(\theta)|H|\psi(\theta)\rangle\ge E_0.
$$

VQE 流程：

1. 量子线路制备参数化态 $|\psi(\theta)\rangle$；
2. 将 $H$ 分解成 Pauli 串并测量各项期望值；
3. 经典优化器更新 $\theta$；
4. 重复直到能量收敛。

论文以横场 Ising 模型为例：

$$
H=-\sum_iZ_iZ_{i+1}-h\sum_iX_i.
$$

不含纠缠的乘积态 ansatz 在铁磁有序区表现尚可，但在量子临界区域偏差明显；加入能表达 GHZ 型相关的纠缠 ansatz 后结果改善。这说明 ansatz 既要足够有表达力，又不能深到被噪声淹没。

VQE 的常见限制包括 ansatz 偏差、barren plateau、采样成本、优化器不稳定、噪声偏差，以及量子-经典通信开销。

### 26.3 配分函数

统计物理中

$$
Z=\sum_\sigma e^{-\beta H(\sigma)}
$$

归一化 Gibbs 分布并决定自由能。论文介绍的量子算法只对能够映射到特定不可约循环余圈码的 Potts/Ising 图类高效，并使用 Shor/QFT 相关子程序计算 Gauss 和。它不是任意模型配分函数的通用高效算法；论文硬件实验也只实现了完整流程中的二量子比特 QFT 片段。

## 27. 量子态制备与 Schmidt 分解

### 27.1 单量子比特

忽略全局相位后，任意纯态可写成

$$
|\psi\rangle=
\cos\frac\theta2|0\rangle
+e^{i\phi}\sin\frac\theta2|1\rangle.
$$

可用 $R_y(\theta)$ 和 $R_z(\phi)$ 从 $|0\rangle$ 制备。原文使用的角度约定把半角吸收进 $\theta$，与现代 Bloch 球常见写法不同；计算时要先确认约定。

### 27.2 Schmidt 分解

任意二分纯态可写成

$$
|\Psi\rangle_{AB}
=\sum_{k=1}^r\lambda_k|u_k\rangle_A|v_k\rangle_B,
\qquad \lambda_k\ge0,\qquad\sum_k\lambda_k^2=1.
$$

$\lambda_k$ 是系数矩阵的奇异值，$r$ 是 Schmidt rank：

- $r=1$ 时态可分离；
- $r>1$ 时两部分纠缠。

Schmidt 分解既是纠缠判据，也是状态制备方案：先制备 Schmidt 系数，再用 CNOT 关联两个寄存器，最后分别旋转到 $\{|u_k\rangle\}$ 和 $\{|v_k\rangle\}$ 基。

### 27.3 一般状态制备并不便宜

任意 $n$ 量子比特纯态含约 $2^{n+1}-2$ 个独立实参数，通用制备线路通常需要指数级门数。振幅编码常把 $N$ 维经典向量压进 $\log_2N$ 个量子比特，但“压进去”本身一般不是免费的。

论文给出：

- 任意两量子比特态可用 1 个 CNOT 加若干单比特门制备；
- 任意两量子比特酉门最多需要 3 个 CNOT 加单比特门；
- 其四量子比特通用态制备方案使用 9 个 CNOT 和 17 个单比特门。

## 28. 量子层析

### 28.1 单量子比特层析

单量子比特密度矩阵可写成

$$
\rho=\frac12(I+r_xX+r_yY+r_zZ),
$$

其中

$$
r_x=\langle X\rangle,\quad
r_y=\langle Y\rangle,\quad
r_z=\langle Z\rangle.
$$

分别在 $X,Y,Z$ 基重复测量即可重建 Bloch 向量 $\mathbf r$。

### 28.2 多量子比特与指数测量成本

$n$ 量子比特密度矩阵可在 Pauli 基展开：

$$
\rho=\frac1{2^n}
\sum_{P\in\{I,X,Y,Z\}^{\otimes n}}
\langle P\rangle P.
$$

完整层析涉及多达 $4^n-1$ 个非平凡 Pauli 系数，因此不可扩展到大系统。若已知态具有低秩、低纠缠或其他结构，可用压缩感知、经典阴影等方法减少测量量，但要明确附加假设。

### 28.3 估计方法

- **线性反演**：快，但有限采样下可能得到有负特征值的非物理矩阵；
- **约束最小二乘**：加入 $\rho\succeq0$、$\operatorname{Tr}\rho=1$；
- **最大似然估计**：寻找最可能产生观测频数的物理密度矩阵；
- **Bayesian 方法**：引入先验并给出后验不确定性。

论文对 $|+\rangle$ 和两量子比特纠缠态做层析，观察到等待时间增加后目标纯态权重下降，体现了退相干和设备偏置。

## 29. 量子纠错：应怎样理解论文实验

### 29.1 三比特 bit-flip 重复码

编码

$$
\alpha|0\rangle+\beta|1\rangle
\longmapsto
\alpha|000\rangle+\beta|111\rangle
$$

可以纠正任意一个 $X$ 型翻转。关键不是直接测量三个数据比特并做多数表决，因为那会破坏 $\alpha,\beta$ 的相干性；标准做法是测量稳定子或 syndrome，例如

$$
Z_1Z_2,\qquad Z_2Z_3,
$$

在不获知逻辑态振幅的前提下定位错误。

该码不能纠正相位翻转 $Z$，更不能单独构成通用容错方案。保护任意单比特 Pauli 误差至少需要更完整的编码，如五量子比特码、Steane 码或表面码框架。

### 29.2 对原文结论的批判性说明

论文在旧五量子比特设备上比较：

- 未编码单量子比特线路错误率约 $1.3\%$；
- 三比特编码并做多数表决后，逻辑误判约 $4.7\%$。

这个结果说明**该设备上的这个小实验中，额外门误差超过了简单重复码的收益**。它不能推出“量子纠错无法处理门误差”，原因包括：

- 实验不是完整容错 syndrome 提取与恢复流程；
- 三比特重复码只处理 bit flip；
- 编码、纠错门本身没有以容错方式实现；
- 物理错误率、串扰和线路规模可能高于该码的伪阈值；
- 容错阈值定理本来就要求物理错误低于阈值，并配合可扩展码和容错门构造。

因此这部分最合理的现代结论是：**量子纠错有资源开销，低于 break-even 之前会让结果更差；真正关键的实验指标是逻辑错误率是否随码距增加而下降。**

## 30. 历史硬件实验给出的共同教训

| 实验 | 理想模拟器 | 论文中的真实硬件现象 | 教训 |
|---|---|---|---|
| Bell 态 | 只出现 00/11 | 出现不应有的 01/10 | 制备、CNOT 和读出均有误差 |
| 两比特 Grover | 目标态概率 1 | 目标态约 $65\%$ | 深 Toffoli 分解降低保真度 |
| BV | 隐藏串概率 1 | 两比特已明显有噪声 | oracle 编译和连通性关键 |
| HHL | 期望值符合理论 | 未得到正确答案 | 深 QPE、后选择对噪声敏感 |
| 四步量子游走 | 概率集中到目标态 | 目标态仅约 $21.7\%$ | 重复步数导致深度快速增长 |
| QAOA 小图 | 增加层数改善结果 | 多层收益被噪声侵蚀 | NISQ 中存在最佳有限深度 |
| qPCA 小例 | 给出实非负特征值 | 得到带虚部的非物理解 | 层析/纯度线路过深会失真 |
| 三比特重复码 | 理想可纠正单翻转 | 编码后误判反而增加 | 纠错必须达到 break-even |

这些数字是论文当时设备上的个例，不适合横向比较今天的硬件；可迁移的结论是：减少两比特门、适配连通性、控制深度、记录校准数据、报告 shots 与不确定度，并用物理约束检查结果。

## 31. 综合算法设计框架

面对一个新问题，可以依次追问：

1. **输入如何进入量子态？** 状态制备和 qRAM 成本是多少？
2. **需要什么 oracle 或 block-encoding？** 它能否由局部门高效实现？
3. **利用哪种干涉骨架？** QFT、振幅放大、量子游走、Hamiltonian 模拟还是变分线路？
4. **输出是什么？** 一个比特、一个样本、期望值，还是完整经典向量？
5. **加速衡量什么？** 查询次数、门数、深度、总运行时间还是样本复杂度？
6. **依赖哪些条件？** 稀疏性、条件数、低秩、数据访问模型、误差容忍度？
7. **如何验证？** 小规模经典模拟、守恒量、归一化、Hermiticity、正定性和已知极限是否满足？
8. **硬件能否承受？** 两比特门数、连通性、相干时间和读出误差如何？

## 32. 第二部分自测题

1. 证明测量前施加 $H$ 后再测 $Z$，等价于直接测量 $X$。
2. 说明为什么 Hermitian 算符的期望值一定是实数。
3. 对 $N=16,M=1$，估算 Grover 迭代次数。
4. 取隐藏串 $s=101$，写出标准 BV oracle 所需的 CNOT。
5. 说明 QFT 有 $O(n^2)$ 门数为什么不等于能在 $O(n^2)$ 时间输出 $2^n$ 个 Fourier 系数。
6. 列出 HHL 获得实际优势所需的至少四个条件。
7. 用 $N=15,a=2$ 写出模幂序列，找周期并计算因子。
8. 推导 Hadamard test 中 $P(0)$ 的表达式。
9. 写出单边 MaxCut 的成本 Hamiltonian，并给出四个计算基态的本征值。
10. 为什么 VQE 得到的能量理论上不低于基态能量？噪声下这一性质是否一定保留？
11. 给定 $\rho=\frac12(I+0.6X+0.8Z)$，判断它是否为纯态。
12. 为什么三比特 bit-flip 码不能保护相位翻转？

### 第二部分简答

1. $H^\dagger ZH=X$，故测量概率和期望值完全相同。
2. $\langle\psi|O|\psi\rangle^*=\langle\psi|O^\dagger|\psi\rangle=\langle\psi|O|\psi\rangle$。
3. $\frac\pi4\sqrt{16}\approx3.14$，取约 3 次。
4. 对 $s_2=s_0=1$ 的两个输入位分别向辅助位施加 CNOT；$s_1=0$ 不连接。
5. 测量不能读取完整振幅数组；QFT 只在提取周期或相位等全局性质时有效。
6. 例如高效状态制备、高效 block-encoding/Hamiltonian 模拟、适中条件数、只需少量可观测量输出。
7. $2^x\bmod15=1,2,4,8,1,\ldots$，$r=4$；$\gcd(2^2-1,15)=3$，$\gcd(2^2+1,15)=5$。
8. 最终辅助位 0 分量为 $(|\psi\rangle+U|\psi\rangle)/2$，取范数平方得到 $(1+\operatorname{Re}\langle\psi|U|\psi\rangle)/2$。
9. $C=\frac12(I-Z_1Z_2)$；00、11 本征值 0，01、10 本征值 1。
10. 来自 Rayleigh-Ritz 变分原理；噪声和误差缓解可能使估计值不再严格满足上界。
11. Bloch 向量长度 $\sqrt{0.6^2+0.8^2}=1$，所以是纯态。
12. $Z$ 错误不改变计算基比特，多数表决无法发现其相位变化。

---

## 两篇文献合并后的核心认识

第一篇回答“量子计算的符号和规则是什么”，第二篇回答“这些规则怎样组成算法并落到硬件上”。把二者合并，可以得到一条完整主线：

$$
\boxed{\text{经典问题与数据}}
\xrightarrow{\text{编码}}
\boxed{\text{量子态}}
\xrightarrow{\text{oracle/酉演化}}
\boxed{\text{相位与振幅干涉}}
\xrightarrow{\text{测量}}
\boxed{\text{少量经典统计量}}
\xrightarrow{\text{后处理}}
\boxed{\text{问题答案}}.
$$

判断量子算法是否真正有优势，不能只看希尔伯特空间有 $2^n$ 维，也不能只数 oracle 调用次数；必须把输入、线路、精度、采样、输出和纠错成本放在同一资源账本里。
