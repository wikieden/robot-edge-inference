"""第 6 章 · 实时调度：动作块、异步推理、快慢两套系统。

讲义：ai-infra-edge/notes/lessons/06-realtime-scheduling.md
运行：uv run python ch06_realtime_scheduling.py
π0 的 73 ms、25 步、50 Hz 和 SmolVLA 的 g = 0.7 来自论文；300 ms 和时延预算表里的各项是编的。
"""


def sync_idle_fraction(infer_ms: float, exec_steps: int, dt_ms: float) -> float:
    """同步执行：做完 exec_steps 步动作后停下等推理，停着的时间占几成。"""
    return infer_ms / (infer_ms + exec_steps * dt_ms)


def async_budget_ms(chunk: int, g: float, dt_ms: float) -> float:
    """异步执行：队列还剩 g × chunk 步时就发起下一次推理，推理必须在这些步用完前回来。"""
    return g * chunk * dt_ms


def budget_total(parts: dict[str, float]) -> float:
    """时延预算：从拍照到动作发出，各段加起来。"""
    return sum(parts.values())


def main() -> None:
    print("\n第一步：同步执行时机器人停着等的时间（π0：做 25 步、每步 20 ms）")
    for infer in (73, 300):
        f = sync_idle_fraction(infer, 25, 20)
        print(f"  推理 {infer:>3} ms → 每轮 {infer + 500} ms 里停 {infer} ms，占 {f:.1%}")
    print("  （300 ms 是编的，代表放到小板子上变慢后的情况）")

    print("\n第二步：异步执行的时间预算（动作块 50 步、每步 20 ms）")
    for g in (0.0, 0.5, 0.7):
        print(f"  g = {g}：队列剩 {g * 50:.0f} 步时触发 → 推理必须在 {async_budget_ms(50, g, 20):.0f} ms 内回来")

    print("\n第四步：一条时延预算（各项是编的，自己的机器要实测 p99）")
    parts = {"等下一帧相机（30 fps 最坏）": 1000 / 30, "预处理": 5, "模型推理": 73, "后处理": 2, "发给控制器": 1}
    for k, v in parts.items():
        print(f"  {k:<18} {v:6.1f} ms")
    print(f"  合计 {budget_total(parts):.1f} ms")


if __name__ == "__main__":
    main()
