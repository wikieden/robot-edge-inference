"""第 5 章 · 推理引擎：从 PyTorch 到 TensorRT，再到 CUDA Graph。

讲义：ai-infra-edge/notes/lessons/05-inference-engines.md
运行：uv run python ch05_inference_engines.py
Jetson Thor 的逐项耗时来自 GR00T 2 白皮书 Fig. 19；每次 launch 5 µs、一步 2000 个 kernel 是编的。
"""

THOR_WATERFALL = [  # (累计改动, ms)，Jetson Thor 120 W，G1 Turbo，500 次中位数
    ("基线 eager BF16 PyTorch", 720.41),
    ("+ 运行时优化", 614.53),
    ("+ TensorRT", 256.12),
    ("+ CUDA graph", 254.00),
    ("+ FP8 混合精度", 182.22),
    ("+ 去噪步数减半", 123.97),
]


def savings(waterfall: list[tuple[str, float]]) -> list[tuple[str, float, float]]:
    """每一步比上一步省了多少 ms，占基线的几成。"""
    base = waterfall[0][1]
    out = []
    for (_, prev), (name, cur) in zip(waterfall, waterfall[1:]):
        out.append((name, prev - cur, (prev - cur) / base))
    return out


def host_launch_ms(n_kernels: int, us_per_launch: float) -> float:
    """CPU 一个个提交 kernel 要多久：kernel 数 × 每次 launch 的时间。"""
    return n_kernels * us_per_launch / 1000


def main() -> None:
    print("\n第三步：GR00T 2 在 Jetson Thor 上一层层削延迟（Fig. 19）")
    base = THOR_WATERFALL[0][1]
    for name, saved, frac in savings(THOR_WATERFALL):
        print(f"  {name:<16} 省 {saved:7.2f} ms（占基线 {frac:5.1%}）")
    print(f"  合计 {base} → {THOR_WATERFALL[-1][1]} ms，快 {base / THOR_WATERFALL[-1][1]:.2f} 倍")

    print("\n第一步：kernel 一个个提交，CPU 光提交就要多久（5 µs、2000 个是编的）")
    eager = host_launch_ms(2000, 5)
    print(f"  2000 个 kernel × 5 µs = {eager:.0f} ms")
    print("  录成 CUDA Graph 后每步只提交 1 次 → 约 0.005 ms；kernel 本身还是要跑")


if __name__ == "__main__":
    main()
