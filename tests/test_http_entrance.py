"""Router tests"""

from snapp_mle_task.routers.http_entrance import router
from fastapi.testclient import TestClient
import pytest

client = TestClient(router)


def test_iran_mall_entrance():
    request = client.get("/find-nearest-entrance?lat=35.754379&long=51.192205")
    exp_res = [35.75549627605236, 51.19158112375362]
    assert request.status_code == 200
    assert request.json() == exp_res


def test_no_entrance():
    request = client.get("/find-nearest-entrance?lat=35.754379&long=61.192205")
    exp_res = {"msg": "No nearby entrance located for this point!"}
    assert request.status_code == 200
    assert request.json() == exp_res
