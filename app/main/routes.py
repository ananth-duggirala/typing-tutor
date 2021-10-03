from flask import render_template, flash, redirect, request, url_for, current_app
from app import db
from app.main.forms import EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Leaderboard
from werkzeug.urls import url_parse
from datetime import datetime
from app.main import bp
import json

@bp.route('/')
@bp.route('/index')
def index():
  user = {'username': 'testUser'}
  text = "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before final copy is available. It is also used to temporarily replace text in a process called greeking, which allows designers to consider the form of a webpage or publication, without the meaning of the text influencing the design. "
  return render_template('index.html', title='Home', text=text)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

@bp.route('/user_highscores/<username>')
@login_required
def user_highscores(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    scores = user.scores.order_by(Leaderboard.speed.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user_highscores', username=user.username, page=scores.next_num) \
        if scores.has_next else None
    prev_url = url_for('main.user_highscores', username=user.username, page=scores.prev_num) \
        if scores.has_prev else None
    form = EmptyForm()
    return render_template('user_highscores.html', user=user, scores=scores.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(original_username=current_user)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
                           
@bp.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(body=form.post.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('main.forum'))
    
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)

  next_url = url_for('main.forum', page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('main.forum', page=posts.prev_num) \
    if posts.has_prev else None
  return render_template('forum.html', title='Forum', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/leaderboard', methods=['GET', 'POST'])
@login_required
def leaderboard():
  page = request.args.get('page', 1, type=int)
  scores = Leaderboard.query.order_by(Leaderboard.speed.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)

  next_url = url_for('main.leaderboard', page=scores.next_num) \
    if scores.has_next else None
  prev_url = url_for('main.leaderboard', page=scores.prev_num) \
    if scores.has_prev else None
  return render_template('leaderboard.html', title='Leaderboard',
                           scores=scores.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/post_score', methods = ['POST'])
def post_score():
  if request.method == 'POST':
    try:
      speed = request.form["speed"]
      user_id = current_user
      username = current_user.username
      score = Leaderboard(speed=speed, author=current_user, username=current_user.username)
      db.session.add(score)
      db.session.commit()
      return redirect(url_for('main.index'))
    except Exception as e:
      return str(e), 400