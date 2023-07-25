from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Post, User
from .model_helpers import get_timestamp, get_num_posts
from . import db
import json, base64

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note created!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_view(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        caption = request.form.get('caption')
        image = request.files['image']
        image_b64 = base64.b64encode(image.read()).decode('utf-8')

        if len(image_b64) < 1:
            flash('Invalid image!', category='error')
        else:
            new_post = Post(image=image_b64, caption=caption, user_id=user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
    
    num_posts = get_num_posts(user)
    
    context = {
        'current_user': current_user,
        'user_page': user,
        'num_posts': num_posts,
        'name': user.name
    }

    return render_template("user.html", **context)

@views.route('/posts/<postid>', methods=['GET', 'POST'])
@login_required
def post_view(postid):
    post = Post.query.filter_by(id=postid).first()
    if not post:
        return "Post not found", 404
    
    post_owner = User.query.filter_by(id=post.user_id).first()
    timestamp = get_timestamp(post)

    context = {
        'current_user': current_user,
        'post': post,
        'post_owner': post_owner,
        'timestamp': timestamp
    }
    
    return render_template("posts.html", **context)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
    return jsonify({})
