"""第 4 章 · 量化：省内存、省带宽，但不一定变快。

讲义：ai-infra-edge/notes/lessons/04-quantization.md
运行：uv run python ch04_quantization.py
OpenVLA 的量化表来自论文 Table 2；q4_0 的字节数来自 AII §8.4；那 5 个权重是编的。
"""

BYTES_PER_VALUE = {"bf16": 2.0, "fp8": 1.0, "int8": 1.0, "int4": 0.5, "q4_0": 18 / 32}

OPENVLA = {"bf16": (71.3, 16.8), "int8": (58.1, 10.2), "int4": (71.9, 7.0)}  # (成功率 %, 显存 GB)


def weights_gb(params_billion: float, fmt: str) -> float:
    """权重占多少 GB：参数量 × 每个值的字节数。"""
    return params_billion * BYTES_PER_VALUE[fmt]


def q4_0_block_bytes(n_values: int = 32) -> int:
    """q4_0 一组 32 个值：每个值 4 位（共 16 字节）+ 一个 2 字节的缩放系数。"""
    return n_values * 4 // 8 + 2


def quantize(xs: list[float], bits: int) -> tuple[float, list[int]]:
    """对称量化：scale = 最大绝对值 ÷ 最大整数，每个值除以 scale 再四舍五入。"""
    qmax = 2 ** (bits - 1) - 1
    scale = max(abs(x) for x in xs) / qmax
    return scale, [round(x / scale) for x in xs]


def dequantize(scale: float, qs: list[int]) -> list[float]:
    """反量化：整数乘回 scale。"""
    return [q * scale for q in qs]


def main() -> None:
    print("\n第一步：7B 模型在不同格式下的权重大小")
    for fmt in BYTES_PER_VALUE:
        print(f"  {fmt:<5} {BYTES_PER_VALUE[fmt]:.4g} 字节 / 值 → {weights_gb(7, fmt):5.2f} GB")
    print(f"  q4_0 一组 32 个值 = {q4_0_block_bytes()} 字节（bf16 要 64 字节），平均 {q4_0_block_bytes() * 8 / 32} 位")

    print("\n第二步：亲手量化 5 个权重（编的）")
    xs = [0.12, -0.5, 0.33, 0.9, -0.07]
    for bits in (8, 4):
        scale, qs = quantize(xs, bits)
        back = dequantize(scale, qs)
        err = max(abs(a - b) for a, b in zip(xs, back))
        print(f"  int{bits}：scale = 0.9 ÷ {2 ** (bits - 1) - 1} = {scale:.5f}，整数 {qs}")
        print(f"         还原 {[round(b, 3) for b in back]}，最大误差 {err:.4f}")

    print("\n第三步：OpenVLA 的真实结果（论文 Table 2）")
    for fmt, (succ, mem) in OPENVLA.items():
        print(f"  {fmt:<5} 成功率 {succ}%  显存 {mem} GB")
    print("  int8 更省内存却更差：多出的量化算子让推理变慢，A5000 上只有 1.2 Hz")


if __name__ == "__main__":
    main()
