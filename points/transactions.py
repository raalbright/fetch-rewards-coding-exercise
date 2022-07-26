from select import select
from marshmallow import EXCLUDE, ValidationError
from points.schema import PointsSchema, TransactionSchema
from .db import query_db, get_db
from flask import Blueprint, jsonify, request

blueprint = Blueprint('transactions', __name__, url_prefix='/transactions')

@blueprint.route("", methods=['GET'])
def get_points_balance():
    points = query_db(
        'select t.payer, sum(t.points) as points from transactions t group by t.payer')

    return jsonify({p["payer"]: p["points"] for p in points})

@blueprint.route("", methods=['POST'])
def post_points_balance():
    try:
        transaction = TransactionSchema().load(request.json)
        print(transaction)
    except ValidationError as err:
        return jsonify({"errors": err}), 400
    else:
        db = get_db()
        cur = db.execute(
            'insert into transactions (payer, points, timestamp) values (:payer, :points, :timestamp)', transaction)
        cur.close()
        db.commit()

        return "", 200

def points_for_payer(payer):
    points = query_db('select ifnull(sum(t.points), 0) as points from transactions t where t.payer = ?', [
                      payer], one=True)['points']
    return points

@blueprint.route("/spend", methods=['POST'])
def spend_points():
    try:
        request_json = PointsSchema(unknown=EXCLUDE).load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err}), 400
    else:
        balance = query_db(
            'select ifnull(sum(t.points), 0) as balance from transactions t', one=True)['balance']
        points_to_spend = request_json["points"]

        if balance < points_to_spend:
            return jsonify({"error": "Insufficient points"}), 400

        entries = query_db('''
        select t.payer, t.points
from transactions t
where t.payer in (select tt.payer from transactions tt group by tt.payer having sum(tt.points) > 0 )
order by t.timestamp asc''')

        acc = {}
        for entry in entries:
            if entry["payer"] not in acc:
                acc[entry["payer"]] = 0

            value = min(entry["points"], points_to_spend)
            points_to_spend -= value
            acc[entry["payer"]] += -value

            if points_to_spend <= 0:
                break

        acc = [{"payer": k, "points": v} for (k, v) in acc.items()]

        print(acc)

        db = get_db()
        cur = db.executemany(
            'insert into transactions (payer, points, timestamp) values (:payer, :points, datetime())', acc)
        cur.close()
        db.commit()

        return jsonify(acc)
