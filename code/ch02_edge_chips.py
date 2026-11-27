"""第 2 章 · 端侧芯片：看懂 Jetson 的三个数。

讲义：ai-infra-edge/notes/lessons/02-edge-chips.md
运行：uv run python ch02_edge_chips.py
模组参数来自 NVIDIA 官方页面（2026-11-26 核对，见 materials/SOURCES.md）。
系统预留 3 GB、实际利用率 40% 是编的，用来演示算法，自己的机器要实测。
"""

# 名字: (内存 GB, 带宽 GB/s, 官方 AI 算力, 算力口径, 最高功率 W)
MODULES = {
    "Orin Nano 8GB（原版）": (8, 68, 40, "INT8 稀疏 TOPS", 15),
    "Orin Nano 8GB（Super）": (8, 102, 67, "INT8 稀疏 TOPS", 25),
    "Orin NX 16GB（Super）": (16, 102, 157, "INT8 稀疏 TOPS", 40),
    "AGX Orin 64GB": (64, 204.8, 275, "INT8 稀疏 TOPS", 60),
    "Jetson T5000（Thor）": (128, 273, 2070, "FP4 稀疏 TFLOPS", 130),
}


def dense(sparse: float) -> float:
    """官方稀疏口径 ÷ 2 = 稠密口径（大多数模型权重不是 2:4 稀疏的，按稠密算）。"""
    return sparse / 2


def usable_gb(total_gb: float, reserve_gb: float = 3.0) -> float:
    """统一内存里留给模型的部分：总内存减去系统、ROS 2、相机缓冲等预留。"""
    return total_gb - reserve_gb


def effective(dense_peak: float, util: float = 0.4) -> float:
    """实际能跑到的算力 ≈ 稠密峰值 × 利用率。"""
    return dense_peak * util


def gbps_per_watt(bw: float, watt: float) -> float:
    """每瓦换来多少带宽：端侧最在乎的效率。"""
    return bw / watt


def main() -> None:
    print("\n第一步：统一内存里真正留给模型的空间（预留 3 GB 是编的）")
    for name, (mem, *_rest) in MODULES.items():
        print(f"  {name:<22} {mem:>4} GB → 留给模型约 {usable_gb(mem):>5.0f} GB")

    print("\n第三步：算力的两层折扣（稀疏 → 稠密 → 利用率 40%，40% 是编的）")
    name = "AGX Orin 64GB"
    sparse = MODULES[name][2]
    print(f"  {name}：官方 {sparse} → 稠密 {dense(sparse):.1f} → 实际约 {effective(dense(sparse)):.0f} INT8 TOPS")

    print("\n第三步：Super Mode 是同一块板子提频")
    old, new = MODULES["Orin Nano 8GB（原版）"], MODULES["Orin Nano 8GB（Super）"]
    print(f"  带宽 {old[1]} → {new[1]} GB/s（×{new[1] / old[1]:.2f}），算力 {old[2]} → {new[2]}（×{new[2] / old[2]:.2f}）")
    print(f"  功率上限 {old[4]} → {new[4]} W")

    print("\n第四步：每瓦换来多少带宽（按最高功率算）")
    for name, (_m, bw, _t, _u, watt) in MODULES.items():
        print(f"  {name:<22} {bw:>6} GB/s ÷ {watt:>3} W = {gbps_per_watt(bw, watt):.2f} GB/s 每瓦")


if __name__ == "__main__":
    main()
