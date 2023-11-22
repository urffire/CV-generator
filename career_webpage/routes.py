from flask import render_template, url_for, flash, redirect, request, jsonify
from career_webpage import app, db, bcrypt
from career_webpage.forms import RegistrationForm, LoginForm, EditUserdataForm, \
    EditUserdataAdminForm, CreateUserForm
from career_webpage.gpt import call_gpt_generate_cv, call_gpt_generate_cl, call_gpt_generate_advice
from career_webpage.models import User, Role, UserRoles
from flask_login import login_user, current_user, logout_user, login_required
import requests


def check_role(role_name):
    roles = current_user.roles
    role_names = map(lambda r: r.name, roles)
    return role_name in role_names


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        role = Role.query.filter_by(name='User').first_or_404()
        user_role = UserRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


def do_login(user_email, user_pswd, remember) -> bool:
    user = User.query.filter_by(email=user_email).first()
    if user and bcrypt.check_password_hash(user.password, user_pswd):
        login_user(user, remember=remember)
        return True
    return False


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        login_success = do_login(form.email.data, form.password.data, form.remember.data)
        if login_success:
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/cv")
def cv():
    return render_template('cv.html', title='CV')

@app.route("/cover_letter")
def cover_letter():
    return render_template('cover_letter.html', title='Cover Letter')

@app.route("/career_advice")
def career_advice():
    return render_template('career_advice.html', title='Career Advice')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/edit_user")
def edit_user():
    if check_role('Admin'):
        return redirect(url_for('manage_users'))
    else:
        return redirect(url_for('edit_userdata'))

@app.route("/edit_userdata", methods=['GET', 'POST'])
@login_required
def edit_userdata():
    userdata = User.query.get_or_404(current_user.id)
    form = EditUserdataForm()
    if request.method == 'GET':
        form.username.data = userdata.username
        form.email.data = userdata.email
    if form.validate_on_submit():
        userdata.username = form.username.data
        userdata.email = form.email.data

        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            userdata.password = hashed_password

        db.session.add(userdata)
        db.session.commit()
        flash('Profile updated successfully!', 'success')

    return render_template('edit_user.html', title='Edit Userdata', form=form)

@app.route("/edit_userdata_admin/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_userdata_admin(user_id):

    if not check_role("Admin"):
        flash("You have to be admin to access this feature", "danger")
        return redirect(url_for('home'))

    userdata = User.query.get_or_404(user_id)
    form = EditUserdataAdminForm()

    if request.method == 'GET':
        form.username.data = userdata.username
        form.email.data = userdata.email

        role_names = map(lambda r: r.name, userdata.roles)
        form.admin.data = ('Admin' in role_names)

    if form.validate_on_submit():
        userdata.username = form.username.data
        userdata.email = form.email.data

        admin_role_id = Role.query.filter_by(name='Admin').first_or_404().id

        current_admin_role = UserRoles.query.filter_by(user_id=user_id, role_id=admin_role_id).first()
        if current_admin_role is not None:
            db.session.delete(current_admin_role)

        if form.admin.data:
            new_admin_role = UserRoles(user_id=userdata.id, role_id=admin_role_id)
            db.session.add(new_admin_role)

        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            userdata.password = hashed_password

        db.session.add(userdata)
        db.session.commit()
        flash('Profile updated successfully!', 'success')

    return render_template('edit_user_admin.html', title='Edit Userdata', form=form)

@app.route("/create_user", methods=['GET', 'POST'])
@login_required
def create_user():
    if not check_role('Admin'):
        flash('You have to be admin to access this feature', 'danger')
        return redirect(url_for('home'))
    form = CreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)

        role = Role.query.filter_by(name='User').first_or_404()
        user_role = UserRoles(user_id=user.id, role_id=role.id)
        db.session.add(user_role)
        db.session.commit()

        flash('The account has been created!', 'success')

    return render_template('create_user.html', title='Create User', form=form)

@app.route("/manage_users")
@login_required
def manage_users():
    if not check_role('Admin'):
        flash('You have to be admin to access this feature', 'danger')
        return redirect(url_for('home'))

    users = User.query.all()
    return render_template('manage_users.html', users=users, title='Manage users')

@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    if not check_role("Admin"):
        flash("You have to be admin to access this feature", "danger")
        return redirect(url_for('home'))

    if current_user.id == user_id:
        flash("You cannot delete your own account", "danger")
        return redirect(url_for('home'))

    UserRoles.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    flash("User account deleted.", 'success')
    return redirect(url_for('manage_users'))

PROXYCURL_API_KEY = 'yMNOf5XqLO4mtJpjeXGzlg'

@app.route('/fetch_profile', methods=['POST'])
@login_required
def fetch_profile():
    linkedin_url = request.json.get('linkedin_url')
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    headers = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
    params = {'url': linkedin_url}

    try:
        response = requests.get(api_endpoint, params=params, headers=headers)
        response.raise_for_status()
        profile_data = response.json()
        return jsonify(profile_data)
    except requests.RequestException as e:
        return jsonify(error=str(e)), 500


@app.route('/save_profile', methods=['POST'])
@login_required
def save_profile():
    try:
        # Save the profile data to the database
        if request.content_type != 'application/json':
            return jsonify({'message': 'Invalid content type. Expected JSON.'}), 400

        profile_data = request.json
        current_user.set_profile_data(profile_data)
        db.session.commit()
        return jsonify({'message': 'Profile saved successfully!'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to save profile data.'}), 500

@app.route('/load_profile')
@login_required
def load_profile():
    try:
        profile_data = current_user.get_profile_data()
        return jsonify(profile_data)
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to load profile data.'}), 500

@app.route('/generate_cv', methods=['POST'])
@login_required
def generate_cv():
    try:
        profile_data = current_user.get_profile_data()
        md = call_gpt_generate_cv(profile_data)
        print(md)
        return jsonify({'content': md})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to load profile data.'}), 500


@app.route('/generate_cl', methods=['POST'])
@login_required
def generate_cl():
    try:
        job_description = request.json
        profile_data = current_user.get_profile_data()
        md = call_gpt_generate_cl(profile_data, job_description)
        print(md)
        return jsonify({'content': md})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to load profile data.'}), 500


@app.route('/generate_advice', methods=['POST'])
@login_required
def generate_advice():
    try:
        profile_data = current_user.get_profile_data()
        md = call_gpt_generate_advice(profile_data)
        print(md)
        return jsonify({'content': md})
    except Exception as e:
        print(str(e))
        return jsonify({'message': 'Failed to load profile data.'}), 500
