"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, redirect, flash, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    """ List all cupcakes """
    cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<cupcake_id>') 
def get_cupcake(cupcake_id):
    """ Render cupcake """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(
      flavor=request.json['flavor'],
      size = request.json['size'],
      rating = request.json['rating'],
      image = request.json['image']  
    )
    db.session.add(new_cupcake)
    db.session.commit()
    response_json=jsonify(cupcake=new_cupcake.serialize_cupcake())
    return (response_json, 201)

@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize_cupcake())

@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)   
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
    