import pytest

from performance import recommend_locust

@pytest.fixture(scope='session')
def tasks():
    user = recommend_locust.WebsiteUser()
    _tasks = recommend_locust.WebsiteTasks(user)
    _tasks.on_start()
    return _tasks

def test_post_recommend_news(tasks):
    res = tasks.post_recommend_news()
    assert res.status_code == 200
