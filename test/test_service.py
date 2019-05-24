import pytest

from simulation_system.service import service

def test_service():
    num = 10
    s = service(num)
    assert len(s)==num