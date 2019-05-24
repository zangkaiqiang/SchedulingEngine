import pytest

from SimulationSystem.Service import service

def test_service():
    num = 10
    s = service(num)
    assert len(s)==num