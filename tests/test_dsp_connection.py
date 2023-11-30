from pyfmodex.enums import DSPCONNECTION_TYPE
import time

import pytest


@pytest.mark.xfail
def test_input(conn, echo):
    time.sleep(0.1)
    assert conn.input == echo

def test_mix(conn):
    assert conn.mix == 1.0
    conn.mix = 0.5
    assert conn.mix == 0.5

def test_mix_matrix(conn):
    assert conn.get_mix_matrix() == []
    matrix = [0.5, 0.5]
    conn.set_mix_matrix(matrix, 1, 2)
    assert conn.get_mix_matrix() == matrix

@pytest.mark.xfail
def test_output(conn, echo):
    time.sleep(0.1)
    assert conn.output == echo

def test_type(conn):
    assert conn.type is DSPCONNECTION_TYPE.STANDARD
