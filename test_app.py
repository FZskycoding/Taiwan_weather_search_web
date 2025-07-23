import pytest
from app import app, check_location_in_message

@pytest.fixture
def client():
    """建立並設定一個用於測試的 Flask client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_check_location_in_message():
    """測試地點名稱檢查函式"""
    assert check_location_in_message("台北市") == "臺北市"
    assert check_location_in_message("台中") == "臺中市"
    assert check_location_in_message("臺南") == "臺南市"
    assert check_location_in_message("高雄") == "高雄市"
    assert check_location_in_message("一個不存在的地點") == "臺北市" # 測試無效輸入
    assert check_location_in_message("臺東縣") == "臺東縣"

def test_index_get(client):
    """測試首頁 (GET) 是否能正常載入"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<h1>\xe5\x8f\xb0\xe7\x81\xa3\xe5\xa4\xa9\xe6\xb0\xa3\xe6\x9f\xa5\xe8\xa9\xa2</h1>" in response.data # 檢查標題是否存在


