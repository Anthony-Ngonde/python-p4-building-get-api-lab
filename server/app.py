#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    bakery_list = []
    for bakery in bakeries:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.isoformat()
        }
        
        bakery_list.append(bakery_dict)

    response = jsonify(bakery_list)
    response.headers['Content-Type'] = 'application/json'
    return response



@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = db.session.get(Bakery, id)
    if bakery:
        return jsonify({
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.isoformat(),
            'baked_goods': [{
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price,
                'created_at': baked_good.created_at.isoformat()
            } for baked_good in bakery.baked_goods]
        }), 200
    else:
        return jsonify({"error": "Bakery not found"}), 404


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    try:
        
        baked_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()
        
        
        baked_goods_list = []
        for baked_good in baked_goods:
            baked_good_dict = {
                'id': baked_good.id,
                'name': baked_good.name,
                'price': baked_good.price,
                'created_at': baked_good.created_at.isoformat(),
                'bakery_id': baked_good.bakery_id
            }
            baked_goods_list.append(baked_good_dict)
        
        
        return jsonify(baked_goods_list), 200
    except Exception as e:
        
        app.logger.error(f"Error in /baked_goods/by_price: {e}")
       
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(desc(BakedGood.price)).first()

    if baked_good is None:
        return jsonify({})
    
    baked_good_dict = {
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price,
        'created_at': baked_good.created_at.isoformat(),
        'bakery_id': baked_good.bakery_id
    }
    response = jsonify(baked_good_dict)
    response.headers['Content-Type'] = 'application/json'
    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
