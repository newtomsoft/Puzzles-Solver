# cd directory of file
# pytest file.py

import pytest

def sum_natural_numbers(n):
    return sum(range(1, n + 1))

def sum_natural_numbers_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

@pytest.mark.benchmark
def test_sum_natural_numbers(benchmark):
    result = benchmark(sum_natural_numbers, 1000000)
    assert result == 500000500000

@pytest.mark.benchmark
def test_sum_natural_numbers_loop(benchmark):
    result = benchmark(sum_natural_numbers_loop, 1000000)
    assert result == 500000500000

