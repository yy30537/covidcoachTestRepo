from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, PasswordRestRequestForm, ResetPasswordForm, PostTweetForm
from app.email import send_reset_password_mail
from app.models import User, Post

from app.initDB import initDB

from app.helperFunctions import get_news_list
from app.helperFunctions import get_stats_list
import sqlite3


@app.route('/')
def index():
    title = 'COVID Coach'
    listOf2 = get_stats_list()
    world_dict = listOf2[0]
    usa_dict = listOf2[1]
    return render_template('index.html', world=world_dict, usa=usa_dict, title=title)

@app.route('/initDB')
def initDB_page():
    a = initDB()
    a.run()
    title = 'COVID Coach'
    listOf2 = get_stats_list()
    world_dict = listOf2[0]
    usa_dict = listOf2[1]
    return render_template('index.html', world=world_dict, usa=usa_dict, title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'COVID Coach Account Registration'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Success', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title=title)


@app.route('/news')
def news_page():
    title = 'COVID Coach Get News'
    news_list = get_news_list()
    return render_template('news.html', context=news_list, title=title)


@app.route('/news_detail/<key>')
def news_detail_page(key):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news_table where news_id = ?',(key,))
    fetched_item = c.fetchone()

    pass_context = (fetched_item[0],fetched_item[1],fetched_item[2],fetched_item[3],fetched_item[4],fetched_item[5],fetched_item[6],fetched_item[7])
    c.execute('SELECT count (liked) FROM user_behavior_table WHERE user_id = ? AND news_id = ?',(current_user.id, key))
    ifLiked = c.fetchone()
    return render_template('news_detail.html', context = pass_context, ifLiked = ifLiked)

@app.route('/like/<news_id>')
def like_page(news_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT count(*) FROM user_behavior_table WHERE user_id = ? AND news_id = ?',(current_user.id, news_id))
    fetched_item = c.fetchone()
    #print(fetched_item[0])
    if(fetched_item[0] == 0):
        c.execute('INSERT INTO user_behavior_table(user_id, news_id, liked, viewed) VALUES(?,?,?,?)', (current_user.id, news_id, 1, 0))
        conn.commit()
    c.execute('SELECT * FROM news_table where news_id = ?',(news_id,))
    fetched_item = c.fetchone()
    pass_context = (fetched_item[0],fetched_item[1],fetched_item[2],fetched_item[3],fetched_item[4],fetched_item[5],fetched_item[6],fetched_item[7])
    c.execute('SELECT count (liked) FROM user_behavior_table WHERE user_id = ? AND news_id = ?',(current_user.id, news_id))
    ifLiked = c.fetchone()[0]
    #print(ifLiked)
    return render_template('news_detail.html', context = pass_context, ifLiked = ifLiked)

@app.route('/unlike/<news_id>')
def unlike_page(news_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT count(*) FROM user_behavior_table WHERE user_id = ? AND news_id = ?',(current_user.id, news_id))
    fetched_item = c.fetchone()
    #print(fetched_item)
    if(fetched_item[0] > 0):
        c.execute('DELETE FROM user_behavior_table WHERE user_id = ? AND news_id = ?', (current_user.id, news_id))
        conn.commit()
    c.execute('SELECT * FROM news_table where news_id = ?',(news_id,))
    fetched_item = c.fetchone()
    pass_context = (fetched_item[0],fetched_item[1],fetched_item[2],fetched_item[3],fetched_item[4],fetched_item[5],fetched_item[6],fetched_item[7])
    c.execute('SELECT count (liked) FROM user_behavior_table WHERE user_id = ? AND news_id = ?',(current_user.id, news_id))
    ifLiked = c.fetchone()[0]
    return render_template('news_detail.html', context = pass_context, ifLiked = ifLiked)

@app.route('/help')
def instruction_page():
    title = 'COVID Coach Get Help'
    return render_template('help.html', title=title)

@app.route('/find')
def find_page():
    title = 'COVID Coach Get Help'
    return render_template('find.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'COVID Coach Account Log In'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # Check if password is matched
        user = User.query.filter_by(username=username).first()
        # The reason we are combining these two conditions together is due to security, we don't want hackers to know if account exist or just password is wrong
        if user and bcrypt.check_password_hash(user.password, password):
            # User exists and password matched
            login_user(user, remember=remember)
            flash('Login success', category='info')
            # Next three lines: we don't want redirect index page everytime when user login,we'll get which page user would like to access and redirect to that page
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('User not exists or password not matched', category='danger')
    return render_template('login.html', form=form, title=title)


@app.route('/account')
@login_required
def user_account_page():
    title = 'COVID Coach My Account'
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT user_behavior_table.news_id, title, description, url, url_to_image FROM news_table INNER JOIN user_behavior_table ON news_table.news_id = user_behavior_table.news_id AND user_behavior_table.user_id = ?',(current_user.id,))
    fetched_item = c.fetchall()
    #print(fetched_item)
    n_followers = len(current_user.followers)
    n_followed = len(current_user.followed)
    return render_template('myaccount.html', title=title, likedHistory=fetched_item, n_followers=n_followers, n_followed=n_followed)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    title = 'COVID Coach Reset Password'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordRestRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('Password reset email is sent successfully, please check your mailbox', category='info')
    return render_template('send_password_reset_request.html', form=form, title=title)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_passwor_token(token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password reset successfully!', category='info')
            return redirect(url_for('login'))
        else:
            flash('The user is not exist', category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/board', methods=['GET', 'POST'])
def board_page():
    title = 'COVID Coach Message Board'
    form = PostTweetForm()
    if form.validate_on_submit():
        body = form.text.data
        post = Post(body=body)
        current_user.posts.append(post)
        db.session.commit()
        flash('You have post a new message', category='success')
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 5, False)
    return render_template('board.html', title=title, form=form, posts=posts)


@app.route('/user_post_page/<username>')
@login_required
def user_post_page(username):
    user = User.query.filter_by(username=username).first()
    if user:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 5, False)
        return render_template('user_post_page.html', user=user, posts=posts)
    else:
        return '404'


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.follow(user)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 5, False)
        return render_template('user_post_page.html', user=user, posts=posts)
    else:
        return '404'


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user:
        current_user.unfollow(user)
        db.session.commit()
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).paginate(page, 5, False)
        return render_template('user_post_page.html', user=user, posts=posts)
    else:
        return '404'

