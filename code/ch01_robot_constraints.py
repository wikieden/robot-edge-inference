"""第 1 章 · 机器人上的推理和云上有什么不同。

讲义：ai-infra-edge/notes/lessons/01-robot-constraints.md
运行：uv run python ch01_robot_constraints.py
π0 的耗时分解来自论文 Table I（RTX 4090），GR00T N1 的频率来自论文 §2，都不是编的。
"""

PI0_PARTS_MS = {"图像编码": 14, "观测前向": 32, "10 步 flow 动作": 27}  # π0 Table I，RTX 4090
PI0_NETWORK_MS = 13  # 走 Wi-Fi 放到板外时多出的网络时间


def period_ms(hz: float) -> float:
    """频率换成周期：每秒 hz 次，每次隔 1000 / hz 毫秒。"""
    return 1000.0 / hz


def infer_interval_ms(steps_between: int, control_hz: float) -> float:
    """每执行 steps_between 步动作推理一次，两次推理之间隔多久。"""
    return steps_between * period_ms(control_hz)


def busy_fraction(infer_ms: float, interval_ms: float) -> float:
    """推理时间占两次推理间隔的几成。"""
    return infer_ms / interval_ms


def main() -> None:
    print("\n第一步：π0 在 RTX 4090 上一次推理的耗时分解（论文 Table I）")
    total = sum(PI0_PARTS_MS.values())
    for k, v in PI0_PARTS_MS.items():
        print(f"  {k:<10} {v:>3} ms")
    print(f"  板上合计 {total} ms；放到板外走 Wi-Fi 再加 {PI0_NETWORK_MS} ms → {total + PI0_NETWORK_MS} ms")

    print("\n第二步：控制 50 Hz、动作块 50 步、每执行 25 步推理一次")
    print(f"  控制周期 {period_ms(50):.0f} ms")
    gap = infer_interval_ms(25, 50)
    print(f"  每 {gap:.0f} ms 推理一次 → 推理频率 {1000 / gap:.0f} Hz，控制频率仍是 50 Hz")
    print(f"  推理 {total} ms 只占这段间隔的 {busy_fraction(total, gap):.1%}")

    print("\n第二步：GR00T N1 的两套频率（论文 §2）")
    print(f"  System 2（看图想事）10 Hz → 每 {period_ms(10):.0f} ms 一次")
    print(f"  System 1（出动作）120 Hz → 每 {period_ms(120):.2f} ms 一次")


if __name__ == "__main__":
    main()
