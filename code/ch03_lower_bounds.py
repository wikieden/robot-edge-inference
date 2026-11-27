"""第 3 章 · 先算下限：读权重要多久、算一遍要多久、放不放得下。

讲义：ai-infra-edge/notes/lessons/03-lower-bounds.md
运行：uv run python ch03_lower_bounds.py
OpenVLA 15 GB / 7.0 GB、6 Hz，π0 的 46 ms 来自论文；带宽来自官方页面和 AII 的硬件表。
π0 前缀里"48 个文字 token"、利用率 40% 是编的。
"""

BW = {"RTX 4090": 1008, "AGX Orin 64GB": 204.8, "Jetson T5000（Thor）": 273, "Orin NX 16GB": 102.4}  # GB/s


def read_ms(gb: float, bw_gbps: float) -> float:
    """读一遍 gb 字节要多久：t = 字节 ÷ 带宽。"""
    return gb / bw_gbps * 1000


def compute_ms(flops: float, tflops: float) -> float:
    """算一遍要多久：t = 运算量 ÷ 算力（tflops 是每秒万亿次）。"""
    return flops / (tflops * 1e12) * 1000


def openvla_step_ms(model_gb: float, bw_gbps: float, n_tokens: int = 7) -> float:
    """OpenVLA 一步要逐个吐 7 个动作 token，每吐一个都要把权重读一遍。"""
    return n_tokens * read_ms(model_gb, bw_gbps)


def prefill_flops(params: float, tokens: int) -> float:
    """前缀（图像 + 文字）一次算完：运算量 ≈ 2 × 参数量 × token 数。"""
    return 2 * params * tokens


def fits(model_gb: float, mem_gb: float, reserve_gb: float = 3.0) -> bool:
    """放不放得下：模型 ≤ 总内存 − 系统预留。"""
    return model_gb <= mem_gb - reserve_gb


def main() -> None:
    print("\n第二步：OpenVLA（7B，bf16 占 15 GB）一步的带宽下限")
    t = openvla_step_ms(15, BW["RTX 4090"])
    print(f"  RTX 4090：7 × 15 GB ÷ 1008 GB/s = {t:.1f} ms → 最多 {1000 / t:.1f} Hz（论文实测约 6 Hz）")
    for dev in ("AGX Orin 64GB", "Jetson T5000（Thor）"):
        for label, gb in (("bf16 15 GB", 15), ("int4 7.0 GB", 7.0)):
            t = openvla_step_ms(gb, BW[dev])
            print(f"  {dev:<20} {label:<12} {t:6.1f} ms → 最多 {1000 / t:.2f} Hz")

    print("\n第三步：π0 的前缀是算力受限（3 张图 × 256 token + 48 个文字 token，48 是编的）")
    tokens = 3 * 256 + 48
    flops = prefill_flops(3e9, tokens)
    print(f"  token 数 {tokens}，运算量 ≈ 2 × 3e9 × {tokens} = {flops / 1e12:.2f} 万亿次")
    print(f"  4090 实测前缀 14 + 32 = 46 ms → 反推有效算力 {flops / 0.046 / 1e12:.0f} 万亿次 / 秒")
    print(f"  同一份权重读一遍只要 {read_ms(6.0, BW['RTX 4090']):.1f} ms（3B × 2 字节 = 6 GB）→ 前缀被算力卡住")
    eff = 138 * 0.4
    print(f"  AGX Orin：稠密 138 INT8 TOPS × 40%（编的）= {eff:.0f} → 前缀约 {compute_ms(flops, eff):.0f} ms")

    print("\n第四步：放不放得下（系统预留 3 GB 是编的）")
    for dev, mem in (("Orin Nano 8GB", 8), ("Orin NX 16GB", 16), ("AGX Orin 64GB", 64)):
        print(f"  {dev:<14} bf16 15 GB：{'放得下' if fits(15, mem) else '放不下'}；"
              f"int4 7.0 GB：{'放得下' if fits(7.0, mem) else '放不下'}")


if __name__ == "__main__":
    main()
