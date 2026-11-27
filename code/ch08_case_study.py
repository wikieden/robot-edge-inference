"""第 8 章 · 综合案例：把一个 π0 级 VLA 装上机器人。

讲义：ai-infra-edge/notes/lessons/08-case-study.md
运行：uv run python ch08_case_study.py
π0 的 3.3B、300M 动作专家、10 步 flow、H = 50、50 Hz 来自论文；带宽、算力来自官方页面。
利用率 40%、前缀 816 个 token、Thor FP8 稠密按 FP4 稀疏的 1/4 算、系统预留 3 GB 都是编的假设。
"""

DEVICES = {  # 名字: (内存 GB, 带宽 GB/s, 稠密算力 万亿次/秒（INT8 或 FP8）)
    "Orin NX 16GB（Super）": (16, 102.4, 78),
    "AGX Orin 64GB": (64, 204.8, 138),
    "Jetson T5000（Thor）": (128, 273, 2070 / 4),
}


def prefix_ms(dense_tops: float, params: float = 3e9, tokens: int = 816, util: float = 0.4) -> float:
    """前缀算力下限：2 × 参数 × token ÷ (稠密算力 × 利用率)。"""
    return 2 * params * tokens / (dense_tops * 1e12 * util) * 1000


def action_ms(bw_gbps: float, expert_gb: float = 0.6, steps: int = 10) -> float:
    """动作专家带宽下限：每个 flow 步都把 300M 参数（bf16 0.6 GB）读一遍。"""
    return steps * expert_gb / bw_gbps * 1000


def plan(name: str, model_gb: float = 6.6, reserve_gb: float = 3.0, budget_ms: float = 500) -> dict:
    """把一台设备的容量、下限、预算一起算出来。"""
    mem, bw, tops = DEVICES[name]
    p, a = prefix_ms(tops), action_ms(bw)
    return {"fits": model_gb <= mem - reserve_gb, "prefix": p, "action": a, "total": p + a,
            "margin": budget_ms / (p + a)}


def main() -> None:
    print("\n第一步：容量（π0 3.3B × 2 字节 = 6.6 GB，系统预留 3 GB 是编的）")
    for name in DEVICES:
        print(f"  {name:<20} {'放得下' if plan(name)['fits'] else '放不下'}")

    print("\n第二步：两段下限（前缀算力受限 + 动作专家带宽受限）")
    for name in DEVICES:
        r = plan(name)
        print(f"  {name:<20} 前缀 {r['prefix']:6.1f} ms + 动作 {r['action']:5.1f} ms = {r['total']:6.1f} ms")

    print("\n第三步：和 500 ms 预算比（50 Hz、每执行 25 步推理一次）")
    for name in DEVICES:
        r = plan(name)
        print(f"  {name:<20} 预算 ÷ 下限 = {r['margin']:.1f} 倍余量")
    print("  下限只是物理极限。GR00T 2 在 Thor 上，没优化的 PyTorch 比优化后慢 5.8 倍：")
    print("  余量不到 5 倍的设备，先做量化、TensorRT（第 4、5 章）再谈上车")


if __name__ == "__main__":
    main()
