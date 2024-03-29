"""Blogly application."""

from flask import Flask, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "177013"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

############################## HOMEPAGE ROUTES ##############################


@app.route('/')
def home():
    """Homepage redirects to users"""
    return redirect('/users')

############################## USER ROUTES ##############################


@app.route('/users')
def users():
    """Shows list of all users in db"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html',
                           users=users)


@app.route('/users/create-new', methods=['GET'])
def create_user():
    """Show a form to create a new user"""

    return render_template('create_user.html')


@app.route("/users/create-new", methods=['POST'])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>', methods=['GET'])
def users_detail(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html',
                           user=user)


@app.route('/users/<int:user_id>/edit', methods=['GET'])
def users_edit(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html',
                           user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

############################## POST ROUTES ##############################


@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def post_form(user_id):
    """Show form to add a post for that user"""

    user = User.query.get_or_404(user_id)
    tag = Tag.query.all()

    return render_template('post_new.html', user=user, tag=tag)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def post_new(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id,
                    tag=tag)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route('/posts/<int:post_id>', methods=['GET'])
def post_show(post_id):
    """Show details of a single post"""

    post = Post.query.get_or_404(post_id)

    return render_template('post_show.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def post_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tag = Tag.query.all()

    return render_template('post_edit.html', post=post, tag=tag)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

############################## TAG ROUTES ##############################


@app.route('/tags', methods=['GET'])
def tags_index():
    """Lists all tags, with links to the tag detail page."""

    tag = Tag.query.all()

    return render_template('tag_index.html', tag=tag)


@app.route('/tags/<int:tag_id>', methods=['GET'])
def tags_show(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_show.html', tag=tag)

@app.route('/tags/new', methods=['GET'])
def tags_new_form():
    """Shows a form to add a new tag."""

    posts = Post.query.all()

    return render_template('tag_new.html', posts=posts)


@app.route("/tags/new", methods=['POST'])
def tags_new():
    """Process add form, adds tag, and redirect to tag list."""

    post_ids = [int(num) for num in request.form.getlist("post")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def tags_edit_form(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.get_or_404(tag_id)
    post = Post.query.all()

    return render_template('tag_edit.html', tag=tag, post=post)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tags_edit(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("post")]
    tag.post = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tags_destroy(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
