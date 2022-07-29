from datetime import datetime
from points.db import get_db

def test_sends_the_point_balance(client):
    response = client.get('/transactions')

    expected = {
        "DANNON": 1100,
        "MILLER COORS": 10000,
        "UNILEVER": 200
    }
    

    assert response.json == expected

def test_adds_points(client):
    client.post('/transactions', json={"payer": "DANNON",
                "points": 100, "timestamp": datetime.now().isoformat()})

    response = client.get('/transactions')

    expected = {
        "DANNON": 1200,
        "MILLER COORS": 10000,
        "UNILEVER": 200
    }

    assert response.json == expected

def test_spend_points(client):
    response1 = client.post('/transactions/spend', json={"points": 5000})

    expected1 = [
        {"payer": "DANNON", "points": -100},
        {"payer": "UNILEVER", "points": -200},
        {"payer": "MILLER COORS", "points": -4_700}
    ]

    assert response1.json == expected1

    expected2 = {
        "DANNON": 1000,
        "MILLER COORS": 5300,
        "UNILEVER": 0
    }

    response2 = client.get('/transactions')

    assert response2.json == expected2


def test_payer_points_dont_go_negative(client, app):
    with app.app_context():
        db = get_db()
        db.execute('delete from transactions');
        db.execute('''
        insert into transactions (payer, points, timestamp)
    values 
    ("DANNON", 200, datetime("2020-10-31T10:00:00Z")),
    ("UNILEVER", 100, datetime("2020-10-31T11:00:00Z")),
    ("DANNON", -200, datetime("2020-10-31T12:00:00Z"))
        ''')
        db.commit()
        db.close()

    response1 = client.post('/transactions/spend', json={"points": 100})

    expected1 = [
        {"payer": "UNILEVER", "points": -100}
    ]

    assert response1.json == expected1

    expected2 = {
        "DANNON": 0,
        "UNILEVER": 0
    }

    response2 = client.get('/transactions')

    assert response2.json == expected2