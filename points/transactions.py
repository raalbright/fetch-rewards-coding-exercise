from .transaction import Transaction
from .db import query_db, get_db
from flask import Blueprint, jsonify, request
from sqlalchemy import func, text

blueprint = Blueprint('transactions', __name__, url_prefix='/transactions')


@blueprint.route("", methods=['GET', 'POST'])
def get_points_balance():
    if request.method == 'POST':
        db = get_db()
        cur = db.execute(
            'insert into transactions (payer, points, timestamp) values (:payer, :points, :timestamp)', request.json)
        cur.close()
        db.commit()
        return "", 200

    points = query_db(
        'select t.payer, sum(t.points) as points from transactions t group by t.payer')

    return jsonify(points)


@blueprint.route("/spend", methods=['POST'])
def spend_points():
    balance = query_db(
        'select sum(t.points) as balance from transactions t', one=True)['balance']
    points_to_spend = request.json["points"]

    if balance < points_to_spend:
        return "Insufficient points", 400

    entries = query_db(
        'select t.payer, t.points, t.timestamp from transactions t order by timestamp asc')

    acc = {}
    for entry in entries:
        if points_to_spend <= 0:
            break

        if entry["payer"] not in acc:
            acc[entry["payer"]] = 0

        if entry["points"] >= points_to_spend:
            acc[entry["payer"]] = -points_to_spend
            points_to_spend = 0
        elif entry["points"] < points_to_spend:
            acc[entry["payer"]] = -(abs(acc[entry["payer"]]) + entry["points"])
            points_to_spend -= entry["points"]

    acc = [{"payer": k, "points": v} for (k, v) in acc.items()]

    db = get_db()
    cur = db.executemany(
        'insert into transactions (payer, points, timestamp) values (:payer, :points, datetime())', acc)
    cur.close()
    db.commit()

    return jsonify(acc)
