from flask import request, render_template, abort, flash, redirect, url_for, Blueprint
from pony.orm import db_session

from src import app
from src.users.forms import UserForm
from src.users.models import User


users_page = Blueprint('users_page', __name__, url_prefix='/users')


@users_page.route('/', methods=['GET'])
@db_session
def users():
    users = User.select().order_by(User.updated_at)
    return render_template('users/users.html', users=users)


@users_page.route('/search', methods=['GET'])
@db_session
def search():
    search_name = request.args.get('keyword', '')
    users = User.select(lambda u: search_name in u.username)
    return render_template('users/users.html', users=users)


@users_page.route('/create', methods=['GET', 'POST'])
@db_session
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    age=form.age.data,
                    phone=form.phone.data,
                    location=form.location.data
                    )
        try:
            app.logger.info('User "{}" created successfully'.format(user.username))
            flash('User created successfully', 'success')
            return redirect(url_for('users_page.users'))
        except Exception as err:
            app.logger.warning('There was an error trying to create an user: {}'.format(repr(err)))
            flash('Error creating user.', 'danger')

    return render_template('users/create_user.html', form=form)


@users_page.route('/delete', methods=['POST'])
@db_session
def delete_user():
    try:
        user_id = request.form['user_id']
        user = User[user_id]
        user_id, username = user.id, user.username
        user.delete()
        app.logger.info('User "{}:{}" deleted successfully'.format(user_id, username))
        flash('User deleted successfully.', 'success')
    except Exception as err:
        app.logger.warning('There was an error trying to delete an user ID: {}'.format(repr(err)))
        flash('Error deleting  user.', 'danger')
    return redirect(url_for('users_page.users'))


@users_page.route('/update/<int:user_id>', methods=['GET', 'POST'])
@db_session
def update_user(user_id):
    user = User.get(id=user_id)
    if not user:
        abort(404)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            form.populate_obj(user)
            user = user
            app.logger.info('User "{}" updated successfully'.format(user.username))
            flash('Saved successfully', 'success')
        except Exception as err:
            app.logger.warning('There was an error trying to update the user "{}": {}'.format(user.username, repr(err)))
            flash('Error when editing user.', 'danger')
    return render_template('users/edit_user.html', form=form)


# Error handling
@users_page.errorhandler(404)
def not_found(error):
    app.logger.error('There was an 404 error: {}'.format(error))
    return render_template('users/404.html'), 404


@users_page.errorhandler(500)
def internal_error(error):
    app.logger.error('There was an 500 error: {}'.format(error))
    return render_template('users/500.html'), 500


@users_page.route('/dt/', methods=['GET'])
def dt():
    return render_template('users/easteregg.html')
