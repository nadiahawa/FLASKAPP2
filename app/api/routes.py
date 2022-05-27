from xml.sax import xmlreader
from flask import Blueprint, jsonify, request
from .services import token_required

api = Blueprint('api', __name__, url_prefix='/api')

from app.models import Animal, db

@api.route('/test', methods=['GET'])
def test():
    fox = Animal.query.all()[0]
    return jsonify(fox.to_dict()), 200


@api.route('/animals', methods=['GET'])
def getAnimals():
    animals = Animal.query.all()
    print(animals)
    # a in single animal object in animal objecxts dict
    # animals = [a.to_dict() for a in animals]
    animals = {a.id:a.to_dict() for a in animals}
    return jsonify(animals), 200


@api.route('/animal<string:name>', methods = ['GET'])
def getAnimalName(name):
    print(name)
    animal = Animal.query.filer_by(species=name.title()).first()
    if animal:
        return jsonify(animal.to_dict()), 200
    return jsonify({'{error': f'no such animal with the name: {name.title()}'})


@api.route('/create', methods=['POST'])
@token_required
def createAnimal():
    #this is going to create anuimal in db with data provided in rerquest body 
    #expected in JSON dict
    try:
        newdict=request.get_json()
        print(newdict)
        a = Animal(newdict)
        print(a)
    except:
        return jsonify({'error': 'improper request or body data'}), 400
    try:
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error': 'species already exists in the database'}), 400
    return jsonify({'created': a.to_dict()}), 200

@api.route('/update/<string:id>')
@token_required
def updateAnimal(id):
    try:
        newvals = request.get_json()
        animal = Animal.query.get(id)
        animal.from_dict(newvals)
        db.session.commit()
        return jsonify({'Updated animal': animal.to_dict()}), 200
    except:
        return jsonify({'Request failed': 'Invalid request or animal ID does not exist.'}), 400

@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def removeAnimal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'Remove failed': f'No animal with ID {id} in the database.'}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'Removed animal': animal.to_dict()}), 200


# @api.route('/shirts', methods=['GET'])
# def shirts():
#     return jsonify('estting some data'), 200  