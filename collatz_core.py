"""Canonical, reproducible measurements for the standard Collatz map.

The exploratory scripts in this repository predate a shared measurement
convention.  This module provides that convention without making claims about
the unresolved Collatz conjecture.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional


def validate_positive_integer(n: int) -> None:
    """Reject values outside the positive-integer Collatz domain."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")


def is_power_of_two(n: int) -> bool:
    """Return whether *n* is a positive power of two."""
    return n > 0 and (n & (n - 1)) == 0


def v2(n: int) -> int:
    """Return the 2-adic valuation, i.e. the number of factors of two in n."""
    validate_positive_integer(n)
    return (n & -n).bit_length() - 1


def collatz_step(n: int) -> int:
    """Apply one step of the standard Collatz map."""
    validate_positive_integer(n)
    return n // 2 if n % 2 == 0 else 3 * n + 1


def l_harbor(k: int) -> int:
    """Return L_k = (2^(2k) - 1) / 3 for k >= 1."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    return (2 ** (2 * k) - 1) // 3


def l_harbor_binary(k: int) -> str:
    """Return the exact alternating binary representation of L_k."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    return "10" * (k - 1) + "1"


def is_l_harbor(n: int) -> bool:
    """Return whether n belongs to the exact L-family."""
    validate_positive_integer(n)
    return n % 2 == 1 and 3 * n + 1 > 0 and is_power_of_two(3 * n + 1)


def secondary_harbor_member(n: int, odd_base: int) -> bool:
    """Return whether n is in S(odd_base) = {2^a * odd_base : a >= 0}."""
    validate_positive_integer(n)
    validate_positive_integer(odd_base)
    if odd_base % 2 == 0:
        raise ValueError("odd_base must be odd")
    while n % 2 == 0:
        n //= 2
    return n == odd_base


def shannon_entropy(symbols: str) -> float:
    """Return Shannon entropy in bits for a finite symbol string."""
    if not symbols:
        return 0.0
    counts = {symbol: symbols.count(symbol) for symbol in set(symbols)}
    length = len(symbols)
    return -sum((count / length) * math.log2(count / length)
                for count in counts.values())


def to_base(n: int, base: int) -> str:
    """Return a base-2..36 representation of n."""
    validate_positive_integer(n)
    if not isinstance(base, int) or not 2 <= base <= 36:
        raise ValueError("base must be an integer from 2 through 36")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while n:
        n, digit = divmod(n, base)
        result.append(digits[digit])
    return "".join(reversed(result))


def binary_features(n: int) -> dict[str, int | float | str]:
    """Return consistently defined structural features for n."""
    validate_positive_integer(n)
    bits = format(n, "b")
    runs = [len(run) for run in bits.split("0") if run]
    zero_runs = [len(run) for run in bits.split("1") if run]
    alternating_violations = sum(
        bit != ("1" if index % 2 == 0 else "0")
        for index, bit in enumerate(bits)
    )
    return {
        "binary": bits,
        "bit_length": len(bits),
        "ones": bits.count("1"),
        "zeros": bits.count("0"),
        "v2": v2(n),
        "max_consecutive_ones": max(runs, default=0),
        "max_zero_run": max(zero_runs, default=0),
        "has_101": int("101" in bits),
        "has_11": int("11" in bits),
        "alternating_violations": alternating_violations,
        "binary_digit_entropy": shannon_entropy(bits),
    }


@dataclass(frozen=True)
class TrajectoryMetrics:
    """Canonical metrics for one trajectory.

    Steps count transitions, while sequence_length counts visited values.
    A bounded or cyclic run has ``total_stopping_time=None``.
    """

    start: int
    steps: int
    sequence_length: int
    total_stopping_time: Optional[int]
    first_power_of_two_step: Optional[int]
    first_power_of_two_value: Optional[int]
    first_descent_step: Optional[int]
    maximum_value: int
    odd_steps: int
    even_steps: int
    converged: bool
    termination: str
    sequence: tuple[int, ...]


def trajectory(n: int, max_steps: int = 100_000) -> TrajectoryMetrics:
    """Generate a bounded trajectory and calculate canonical metrics."""
    validate_positive_integer(n)
    if not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError("max_steps must be a non-negative integer")

    values = [n]
    seen = {n}
    current = n
    first_power_step = 0 if is_power_of_two(n) else None
    first_power_value = n if first_power_step == 0 else None
    first_descent = None

    for step in range(1, max_steps + 1):
        current = collatz_step(current)
        values.append(current)
        if first_descent is None and current < n:
            first_descent = step
        if first_power_step is None and is_power_of_two(current):
            first_power_step = step
            first_power_value = current
        if current == 1:
            termination = "reached_one"
            break
        if current in seen:
            termination = "cycle_detected"
            break
        seen.add(current)
    else:
        termination = "max_steps"

    converged = termination == "reached_one"
    return TrajectoryMetrics(
        start=n,
        steps=len(values) - 1,
        sequence_length=len(values),
        total_stopping_time=len(values) - 1 if converged else None,
        first_power_of_two_step=first_power_step,
        first_power_of_two_value=first_power_value,
        first_descent_step=first_descent,
        maximum_value=max(values),
        odd_steps=sum(value % 2 for value in values[:-1]),
        even_steps=sum(value % 2 == 0 for value in values[:-1]),
        converged=converged,
        termination=termination,
        sequence=tuple(values),
    )


def feature_row(n: int, base: int = 4, max_steps: int = 100_000) -> dict:
    """Combine trajectory and representation features for tabular analysis."""
    result = asdict(trajectory(n, max_steps=max_steps))
    result.pop("sequence")
    result.update(binary_features(n))
    representation = to_base(n, base)
    result.update({
        "base": base,
        "base_representation": representation,
        "base_digit_entropy": shannon_entropy(representation),
    })
    return result


def bit_length_cohort(bit_length: int) -> range:
    """Return all positive integers with exactly ``bit_length`` bits."""
    if not isinstance(bit_length, int) or bit_length < 1:
        raise ValueError("bit_length must be a positive integer")
    return range(1 << (bit_length - 1), 1 << bit_length)


def compare_mersenne_cohort(
    bit_length: int,
    max_steps: int = 100_000,
) -> list[dict]:
    """Measure every value in a bit-length cohort, including its Mersenne value."""
    return [
        feature_row(n, max_steps=max_steps)
        for n in bit_length_cohort(bit_length)
    ]


def write_rows(rows: Iterable[dict], output: str | Path) -> None:
    """Write tabular rows as CSV or JSON, selected by the output suffix."""
    rows = list(rows)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        return
    if path.suffix.lower() != ".csv":
        raise ValueError("output must end in .csv or .json")
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def l_harbor_rows(max_k: int) -> Iterator[dict]:
    """Yield exact-family records suitable for a reproducible data file."""
    if not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be a positive integer")
    for k in range(1, max_k + 1):
        n = l_harbor(k)
        metrics = trajectory(n)
        yield {
            "k": k,
            "number": n,
            "binary": l_harbor_binary(k),
            "first_power_of_two": metrics.first_power_of_two_value,
            "total_stopping_time": metrics.total_stopping_time,
            "sequence_length": metrics.sequence_length,
            "expected_stopping_time": 2 * k + 1,
            "expected_sequence_length": 2 * k + 2,
        }
