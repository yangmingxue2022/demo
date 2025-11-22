import sys
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

import json
from app import create_app


def test_create_and_list_story(tmp_path):
    # use a temp sqlite file to isolate DB
    db_file = tmp_path / "test.db"
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    app.config['TESTING'] = True
    with app.app_context():
        from db import db
        db.create_all()
    client = app.test_client()

    # create
    r = client.post('/api/stories', json={"title":"测试需求","description":"描述"})
    assert r.status_code == 201
    body = r.get_json()
    assert body['title'] == '测试需求'

    # list
    r = client.get('/api/stories')
    assert r.status_code == 200
    arr = r.get_json()
    assert isinstance(arr, list)
    assert any(s['title'] == '测试需求' for s in arr)
