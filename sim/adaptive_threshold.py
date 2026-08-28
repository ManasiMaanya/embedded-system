"""PC simulation of T(v) and the SAFE/MOD/HIGH state machine.

L3/L4 math: docs/mathematics.md. Constants must match firmware/src/math_params.h.
"""

from __future__ import annotations

import csv
from pathlib import Path

# Keep in lockstep with firmware/src/math_params.h
T_MOD_0 = 180.0
K_MOD = 0.8
T_HIGH_0 = 420.0
K_HIGH = 1.2
HYST = 40
V_MAX = 120.0

STATE_SAFE = 1
STATE_MOD = 2
STATE_HIGH = 3
STATE_NAME = {STATE_SAFE: "SAFE", STATE_MOD: "MOD", STATE_HIGH: "HIGH"}

OUT_DIR = Path(__file__).resolve().parent / "out"


def t_mod(speed_kmh: float) -> float:
    return T_MOD_0 + K_MOD * speed_kmh


def t_high(speed_kmh: float) -> float:
    return T_HIGH_0 + K_HIGH * speed_kmh


def v_enter_mod(delta: float) -> float:
    """d = T_mod(v), ignore hysteresis. docs/mathematics.md §5."""
    return (delta - T_MOD_0) / K_MOD


def v_leave_mod(delta: float) -> float:
    """d = T_mod(v) - H (implemented leave-SAFE test)."""
    return (delta + HYST - T_MOD_0) / K_MOD


def d_enter_mod(speed_kmh: float) -> float:
    return t_mod(speed_kmh)


def d_enter_high(speed_kmh: float) -> float:
    return t_high(speed_kmh)


def next_state(state: int, delta: float, speed_kmh: float) -> int:
    enter_mod = t_mod(speed_kmh)
    enter_high = t_high(speed_kmh)
    if delta >= enter_high:
        return STATE_HIGH
    if delta >= enter_mod:
        return STATE_MOD
    if delta < enter_mod - HYST:
        return STATE_SAFE
    return state


def run_sweep(speeds: list[float], deltas: list[float]) -> list[dict]:
    state = STATE_SAFE
    rows: list[dict] = []
    t_ms = 0
    for speed, delta in zip(speeds, deltas):
        state = next_state(state, delta, speed)
        rows.append(
            {
                "t_ms": t_ms,
                "raw": "",
                "baseline": "",
                "delta": round(delta, 1),
                "speed": round(speed, 1),
                "Tmod": round(t_mod(speed), 1),
                "Thigh": round(t_high(speed), 1),
                "state": state,
                "state_name": STATE_NAME[state],
            }
        )
        t_ms += 500
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["t_ms", "raw", "baseline", "delta", "speed", "Tmod", "Thigh", "state"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def print_table(title: str, rows: list[dict], every: int = 1) -> None:
    print(title)
    print(f"{'v':>8} {'d':>8} {'Tmod':>8} {'Thigh':>8} {'state':>8}")
    for i, r in enumerate(rows):
        if i % every != 0:
            continue
        print(
            f"{r['speed']:8.1f} {r['delta']:8.1f} {r['Tmod']:8.1f} "
            f"{r['Thigh']:8.1f} {r['state_name']:>8}"
        )
    print()


def print_closed_form(delta: float) -> None:
    print("Closed form (docs/mathematics.md §5), d =", delta)
    print(f"  T_mod(v) = {T_MOD_0:g} + {K_MOD:g} * v")
    print(f"  T_high(v) = {T_HIGH_0:g} + {K_HIGH:g} * v")
    print(f"  v_enter_mod = (d - T_MOD_0)/K_MOD = {v_enter_mod(delta):.2f} km/h")
    print(f"  v_leave_mod = (d + H - T_MOD_0)/K_MOD = {v_leave_mod(delta):.2f} km/h")
    print(f"  hysteresis width in speed = H/K_MOD = {HYST / K_MOD:.2f} km/h")
    for v in (0.0, 80.0, V_MAX):
        print(
            f"  v={v:g}: d_enter_mod={d_enter_mod(v):.1f}  "
            f"d_enter_high={d_enter_high(v):.1f}  "
            f"(fixed T_MOD_0 would trip MOD at d>={T_MOD_0:g})"
        )
    print()


def write_math_summary(path: Path, delta: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"d = {delta}",
        f"T_mod(v) = {T_MOD_0:g} + {K_MOD:g} * v",
        f"T_high(v) = {T_HIGH_0:g} + {K_HIGH:g} * v",
        f"H = {HYST:g}",
        f"v_enter_mod = {v_enter_mod(delta):.2f}",
        f"v_leave_mod = {v_leave_mod(delta):.2f}",
        f"H/K_MOD = {HYST / K_MOD:.2f}",
        f"d_enter_mod(0) = {d_enter_mod(0):.1f}",
        f"d_enter_mod(80) = {d_enter_mod(80):.1f}",
        f"d_enter_high(0) = {d_enter_high(0):.1f}",
        f"d_enter_high(80) = {d_enter_high(80):.1f}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    speeds = [float(v) for v in range(0, 121, 5)]
    fixed_d = 200.0
    print_closed_form(fixed_d)
    write_math_summary(OUT_DIR / "math_summary.txt", fixed_d)
    rows_a = run_sweep(speeds, [fixed_d] * len(speeds))
    write_csv(OUT_DIR / "sim_speed_sweep_d200.csv", rows_a)
    print_table(f"A: delta held at {fixed_d}, speed 0–120 km/h", rows_a, every=2)

    deltas = [float(d) for d in range(0, 801, 20)]
    for v_hold in (0.0, 80.0):
        rows_b = run_sweep([v_hold] * len(deltas), deltas)
        write_csv(OUT_DIR / f"sim_delta_sweep_v{int(v_hold)}.csv", rows_b)
        print_table(f"B: speed held at {v_hold:.0f} km/h, delta 0–800", rows_b, every=4)

    print(f"CSV written under {OUT_DIR}")
    print("Same columns as firmware serial (raw/baseline empty in sim).")


if __name__ == "__main__":
    main()
