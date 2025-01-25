#!/usr/bin/env python3

from app import app
from models import db, Bakery, BakedGood

with app.app_context():
    print("Clearing old data...")
    BakedGood.query.delete()
    Bakery.query.delete()
    
    print("Seeding bakeries...")
    bakeries = [
        Bakery(name='Delightful Donuts'),
        Bakery(name='Incredible Crullers')
    ]
    db.session.add_all(bakeries)
    db.session.commit()

    print("Seeding baked goods...")
    baked_goods = [
        BakedGood(name='Chocolate Dipped Donut', price=2.75, bakery=bakeries[0]),
        BakedGood(name='Apple-Spice Filled Donut', price=3.50, bakery=bakeries[0]),
        BakedGood(name='Glazed Honey Cruller', price=3.25, bakery=bakeries[1]),
        BakedGood(name='Chocolate Cruller', price=3.40, bakery=bakeries[1]),
    ]
    db.session.add_all(baked_goods)
    db.session.commit()

    print("Seeding complete!")
