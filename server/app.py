#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if bakery:
        return make_response(bakery.to_dict(), 200)
    else:
        return make_response({"error": "Bakery not found"}, 404)

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = db.session.get(Bakery, id)
    if bakery:
        data = request.form
        if "name" in data:
            bakery.name = data["name"]
        db.session.commit()
        return make_response(bakery.to_dict(), 200)
    else:
        return make_response({"error": "Bakery not found"}, 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([bg.to_dict() for bg in baked_goods_by_price], 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return make_response(most_expensive.to_dict(), 200)
    else:
        return make_response({"error": "No baked goods found"}, 404)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data["name"],
        price=data["price"],
        bakery_id=data["bakery_id"],
    )
    db.session.add(new_baked_good)
    db.session.commit()
    return make_response(new_baked_good.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = db.session.get(BakedGood, id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({"message": "Baked good deleted successfully"}, 200)
    else:
        return make_response({"error": "Baked good not found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
