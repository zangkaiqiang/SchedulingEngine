import pytest

from simulation_system.service import service
from simulation_system.worker import worker


def test_service():
    num = 10
    df = service(num)
    assert len(df)==num


def test_worker():
    num = 100
    df = worker(num)

    assert len(df) == num