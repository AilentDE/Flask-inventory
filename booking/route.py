from flask import render_template, redirect, url_for, request, current_app, get_flashed_messages, flash
from flask_login import login_user, current_user, logout_user, login_required
from booking.forms import LoginForm, RegisterRequestForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm, BookingForm, ReportForm
from booking.email import send_email
#import flask-migrate
from booking.models import User, Product, Order_info, Order_list, Report
from booking import db
from datetime import datetime

@login_required
def index():
    products = Product.query.order_by(Product.sku).all()
    return render_template('index.html', title='Index', products=products)

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None or not u.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('login'))
        login_user(u, remember=form.remember_me.data)
        print(u.username, 'Login')
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)

@login_required
def logout():
    print(current_user.username, 'Logout')
    logout_user()
    return redirect(url_for('login'))

@login_required
def register_request():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegisterRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Invitation has been sent.\n\
                Please make sure to check spam and trash if invitee can't find the email.")
            token = current_user.get_jwt(expire=1800)
            url_register = url_for(
                'register', token=token, _external=True
            )
            send_email(
                subject=current_app.config['MAIL_SUBJECT_REGISTER'],
                recipients=[form.email.data],
                text_body= render_template(
                    'email/user_register.txt',
                    url_register = url_register
                ),
                html_body= render_template(
                    'email/user_register.html',
                    url_register = url_register
                )
            )
        return redirect(url_for('register_request'))
    return render_template('register_request.html', title='Request', form=form)

def register(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    from_user = User.verify_jwt(token)
    if not from_user:
        return redirect(url_for('login'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(user=form.user.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Registeration', form=form)

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("You should soon receive an email allowing you to reset your password.\n\
                Please make sure to check your spam and trash if you can't find the email.")
            token = user.get_jwt()
            url_password_reset = url_for(
                'reset_password', token=token, _external=True
            )
            url_password_reset_request = url_for(
                'reset_password_request', _external=True
            )
            send_email(
                subject=current_app.config['MAIL_SUBJECT_RESET_PASSWORD'],
                recipients=[user.email],
                text_body= render_template(
                    'email/passwd_reset.txt',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                ),
                html_body=render_template(
                    'email/passwd_reset.html',
                    url_password_reset=url_password_reset,
                    url_password_reset_request=url_password_reset_request
                )
            )
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Request', form=form)

def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_jwt(token)
    if not user:
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password reset successful.")
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        if not form.order_number.data:
            form.order_number.data = datetime.utcnow().strftime("%y%m%d_%H%M%S")
        order_info = Order_info(
            order_by = current_user.id,
            order_number = form.order_number.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            phone = form.phone.data,
            address = form.address.data,
            city = form.city.data,
            state_code = form.state_code.data,
            postcode = form.postcode.data,
            country = form.country.data,
            shipping_method = form.shipping_method.data,
            remark = form.remark.data
        )
        report_data = Report(order_number = form.order_number.data)
        db.session.add(order_info)
        db.session.add(report_data)
        db.session.commit()
        flash(
            "Order # {} has been send.".format(order_info.order_number)
        )

        for x,y in zip(request.form.getlist('sku'), request.form.getlist('quantity')):
            temp = Order_list(
                order_number = form.order_number.data,
                sku = x,
                quantity = y
            )
            db.session.add(temp)
        db.session.commit()
        print(request.form.getlist('sku'))
        print(request.form.getlist('quantity'))
        return redirect(url_for('booking'))
    return render_template('booking.html', title='Booking', form=form)

# @login_required
def progress():
    orders = db.session.query(Order_info, Report).join(Report, Report.order_number==Order_info.order_number).order_by(Order_info.order_date.desc()).all()
    form = ReportForm()
    if request.method == 'POST': #No-validate-needed prepare jQuery input tag only for needed
        order_number = request.form.getlist('order_number')
        tracking_number = request.form.getlist('tracking_number')
        shipping_date = request.form.getlist('shipping_date')
        delivery_fee = request.form.getlist('delivery_fee')
        materials_fee = request.form.getlist('materials_fee')
        package_weight = request.form.getlist('package_weight')
        for i, target in enumerate(order_number):
            target = Report.query.filter_by(order_number=target).first()
            print(target.order_number)
            if tracking_number[i] == '':
                pass
            else:
                target.tracking_number = tracking_number[i]
            if shipping_date[i] == '':
                pass
            else:
                target.shipping_date = shipping_date[i]
            if delivery_fee[i] == '':
                pass
            else:
                target.delivery_fee = delivery_fee[i]
            if materials_fee[i] == '':
                pass
            else:
                target.materials_fee = materials_fee[i]
            if package_weight[i] == '':
                pass
            else:
                target.package_weight = package_weight[i]
            db.session.commit()

            
            state_change = Order_info.query.filter_by(order_number=target.order_number).first()
            state_change.state = 'Send Out'
            db.session.commit()
        flash(
            "report Updated ."
        )
        return redirect(url_for('progress'))
    return render_template('progress.html', title='Progress', orders=orders, form=form)