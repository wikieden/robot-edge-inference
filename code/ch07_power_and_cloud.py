"""第 7 章 · 功耗、散热和端云分工。

讲义：ai-infra-edge/notes/lessons/07-power-and-cloud.md
运行：uv run python ch07_power_and_cloud.py
Thor 120 W 下 123.97 ms 来自 GR00T 2 白皮书，π0 板外多 13 ms 来自 π0 论文；
电池 480 Wh、电机平均 300 W、网络抖动和丢包的参数都是编的。
"""

import random


def energy_j(watt: float, seconds: float) -> float:
    """一次推理耗多少能量：能量（焦耳）= 功率（瓦）× 时间（秒）。"""
    return watt * seconds


def hours(battery_wh: float, load_w: float) -> float:
    """电池能撑多久：电池能量（瓦时）÷ 负载功率（瓦）。"""
    return battery_wh / load_w


def network_samples(n: int, seed: int = 0, base_ms: float = 13, tail_ms: float = 5, loss: float = 0.02,
                    retry_ms: float = 200) -> list[float]:
    """板外推理的网络时间：基础 13 ms + 随机拖尾；有 loss 的概率丢包重传，多等 retry_ms。"""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        t = base_ms + rng.expovariate(1 / tail_ms)
        if rng.random() < loss:
            t += retry_ms
        out.append(t)
    return out


def percentile(xs: list[float], p: float) -> float:
    """第 p 百分位：从小到大排好，取第 p% 位置上的数。"""
    s = sorted(xs)
    return s[min(len(s) - 1, int(p / 100 * len(s)))]


def main() -> None:
    print("\n第一步：一次推理耗多少能量（按 120 W 功率模式上限算，偏大）")
    print(f"  120 W × 0.12397 s = {energy_j(120, 0.12397):.1f} J")

    print("\n第一步：电池能撑多久（480 Wh、电机平均 300 W 是编的）")
    print(f"  只算计算模组 60 W：{hours(480, 60):.1f} h")
    print(f"  加上电机 300 W：{hours(480, 360):.2f} h，计算占总功率 {60 / 360:.1%}")

    print("\n第三步：板外推理的网络时间分布（参数是编的，种子 0，1000 次）")
    xs = network_samples(1000)
    print(f"  中位数 p50 = {percentile(xs, 50):.1f} ms，p99 = {percentile(xs, 99):.1f} ms")
    print(f"  π0 板上 73 ms；板外按 p50 约 {73 + percentile(xs, 50):.0f} ms，按 p99 约 {73 + percentile(xs, 99):.0f} ms")


if __name__ == "__main__":
    main()
