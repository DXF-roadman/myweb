from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

posts = []

@app.route('/')
def home():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', images=images, posts=posts)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        posts.append({'title': title, 'content': content, 'timestamp': timestamp, 'comments': []})
        return redirect(url_for('home'))
    return render_template('post.html')

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    content = request.form['content']
    if 0 <= post_id < len(posts):
        posts[post_id]['comments'].append(content)
    return redirect(url_for('home'))

@app.route('/delete_image/<filename>')
def delete_image(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except FileNotFoundError:
        pass
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)