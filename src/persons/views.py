from flask import request, render_template, redirect, url_for, Blueprint, jsonify
from pony.orm import db_session
from pony.orm.serialization import to_dict
from pony.orm.core import ObjectNotFound

from src import app

from src.users.models import Person


persons_page = Blueprint('persons_page', __name__, url_prefix='/persons')


@persons_page.route('/', methods=['GET'])
@db_session
def persons():
    persons = Person.select()
    return render_template('persons/persons.html', persons=persons)


@persons_page.route('/person/<int:person_id>', methods=['GET'])
@db_session
def person(person_id):
    try:
        person = Person[person_id]
        person = to_dict(person)
    except ObjectNotFound:
        msg = 'Person ID {} not found'.format(person_id)
        app.logger.info(msg)
        return jsonify(dict(detail=msg)), 404
    return jsonify(person), 200


@persons_page.route('/search-person', methods=['GET'])
@db_session
def search_person():
    search_name = request.args.get('q_person', '')
    persons = Person.select(lambda g: search_name in g.name)
    return render_template('persons/persons.html', persons=persons)


@persons_page.route('/create', methods=['POST'])
def create_person():
    data = request.get_json()
    try:
        with db_session:
            person = Person(name=data.get('name'),
                            city=data.get('city'),
                            phone=data.get('phone'))
    except Exception as err:
        app.logger.info('There was an error trying to create a person: {}'.format(repr(err)))
        return jsonify(status='ko'), 404
    person = to_dict(person)
    app.logger.info('Person created successfully: {}'.format(person))
    return jsonify(person), 201


@persons_page.route('/<int:person_id>', methods=['PUT'])
@db_session
def update_person(person_id):
    data = request.get_json()
    try:
        person = Person[person_id]
    except Exception as err:
        app.logger.info('There was an eror updating person ID {}: {}'.format(person_id, repr(err)))
        return jsonify(status='ko'), 404
    person.name = data.get('name')
    person.city = data.get('city')
    person.phone = data.get('phone')
    return jsonify(status='ok'), 200


@persons_page.route("/delete/<int:person_id>", methods=['GET'])
@db_session
def delete_person(person_id):
    try:
        person = Person[person_id]
        person_id, person_name = person.id, person.name
        person.delete()
        app.logger.info('Person "{}:{}" deleted successfully'.format(person_id, person_name))
    except Exception as err:
        app.logger.warning('There was an error trying to delete a person: {}'.format(repr(err)))
    return redirect(url_for('persons_page.persons'))

