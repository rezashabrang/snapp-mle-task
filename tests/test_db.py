"""database checks"""

from snapp_mle_task.lib.db import init_database, PostgresSingletonConn
import pytest


def test_initialization():
    # No error should happen
    init_database()
    assert True

def test_singleton():
    # DB instance should be created without any error
    conn = PostgresSingletonConn()
    cursor = conn.cursor()
    cursor.close()
    assert True
