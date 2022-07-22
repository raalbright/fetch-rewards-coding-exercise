from datetime import datetime

def test_sends_the_point_balance(client):
    response = client.get('/transactions')

    expected = [
        {"payer": "DANNON", "points": 1100},
        {"payer": "MILLER COORS", "points": 10000},
        {"payer": "UNILEVER", "points": 200}
    ]

    assert response.json == expected

def test_adds_points(client):
    client.post('/transactions', json={"payer": "DANNON",
                "points": 100, "timestamp": datetime.now().isoformat()})

    response = client.get('/transactions')

    expected = [
        {"payer": "DANNON", "points": 1200},
        {"payer": "MILLER COORS", "points": 10000},
        {"payer": "UNILEVER", "points": 200}
    ]

    assert response.json == expected

def test_spend_points(client):
    response1 = client.post('/transactions/spend', json={"points": 5000})

    expected1 = [
        {"payer": "DANNON", "points": -100},
        {"payer": "UNILEVER", "points": -200},
        {"payer": "MILLER COORS", "points": -4_700}
    ]

    assert response1.json == expected1

    expected2 = [
        {"payer": "DANNON", "points": 1000},
        {"payer": "MILLER COORS", "points": 5300},
        {"payer": "UNILEVER", "points": 0}
    ]

    response2 = client.get('/transactions')

    assert response2.json == expected2
