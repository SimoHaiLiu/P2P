from flask import render_template, redirect, request, url_for, flash
from init import *
# from . import init
from filter import receivable_auctions_filter
from forms import *
from flask_login import login_user, logout_user, LoginManager, current_user, login_required


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({'username': username})
    if not user:
        print('用户为空')
        return None

    print('返回用户对象')
    return User(user['email'], user['username'], user['password_hash'])


@app.route('/')
@login_required
def index():
    filter_result = receivable_auctions_filter('past_auctions')

    if filter_result == 'params is none':
        flash('Please add params first, otherwise you will not be able to filter the invoice', 'alert-warning')
        return redirect(url_for('params'))
    elif filter_result == 'single invoice not less than 1%':
        return render_template('index.html')
    else:
        passing_all_criteria, passing_the_critical_criteria, auctions = filter_result

    return render_template('index.html', passing_all_criteria=passing_all_criteria, passing_the_critical_criteria=passing_the_critical_criteria, auctions=auctions)


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         # 根据表单数据创建用户对象
#         user = User(email=form.email.data, username=form.username.data, password=form.password.data)
#         # 将用户添加到数据库
#         user.new_user()
#         flash('注册成功')
#         return redirect(url_for('index'))
#
#     return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('用户名：{}\n密码：{}'.format(form.username.data, form.password.data))
    # request.method == 'POST' and
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'username': form.username.data})
        print('查找到的用户为：{}'.format(user))
        if user and User.validate_login(user['password_hash'], form.password.data):
            user_obj = User(user['email'], user['username'], user['password_hash'])
            login_user(user_obj)
            flash('登录成功', category='success')
            print('登录成功')
            return redirect(request.args.get('next') or url_for('index'))

        flash('用户名或密码错误', category='error')
        print('用户名或密码失败')
    return render_template('login.html', form=form)


@app.route('/logout/')
# @login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('login'))


@app.route('/detail/<auction_no>')
@login_required
def detail(auction_no):
    # print(auction_no)
    auction = mongo.db.past_auctions.find_one({'auction_no': auction_no})
    print(auction)

    return render_template('detail.html', auction=auction)


@app.route('/params', methods=['GET', 'POST'])
@login_required
def params():
    db_params = mongo.db.params.find_one()

    params = Params()
    if params.validate_on_submit():
        advanced_amount = params.advanced_amount.data
        account_receivable = params.account_receivable.data

        if account_receivable < 1000000 or account_receivable > 100000000:
            flash('Account Receivable must be 1000000 to 100000000')
            return redirect(url_for('params'))

        flash('Params is changed!', 'alert-success')
        if db_params:
            mongo.db.params.update_one({'_id': db_params['_id']}, {'$set': {'advanced_amount': advanced_amount, 'account_receivable': account_receivable}})
        else:
            mongo.db.params.insert_one({'advanced_amount': advanced_amount, 'account_receivable': account_receivable})
        return redirect(url_for('params'))
        # return render_template('params.html', form=params, advanced_amount=advanced_amount, account_receivable=account_receivable)

    if db_params:
        return render_template('params.html', form=params, advanced_amount=db_params['advanced_amount'], account_receivable=db_params['account_receivable'])
    else:
        return render_template('params.html', form=params)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
