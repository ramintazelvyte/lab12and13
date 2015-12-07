import os
from flask import Flask, request, Response,redirect, url_for
from werkzeug import secure_filename
from subprocess import Popen,PIPE
UPLOAD_FOLDER = '/data/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
   return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="/upload" method=post enctype=multipart/form-data>
      <p><input type="file" name="file">
         <input type="submit" value="Upload">
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

# List all containers
@app.route('/containers', methods=['GET'])
def containers_index():
    return Response(response=docker('ps', '-a'), mimetype="text/html")

# Inspect specific container
@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    return Response(response=docker('inspect', id,), mimetype="application/json")

# Inspect specific container
@app.route('/restart/<id>', methods=['GET'])
def containers_restart(id):
    return Response(response=docker('restart', id), mimetype="application/json")

# List all images
@app.route('/images', methods=['GET'])
def images_index():
    return Response(response=docker('images'), mimetype="text/html")

def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()
#    return stdout
    return """
    <!doctype html>
    <title>Docker Images</title>
    <h1>Docker Images header</h1>
    <pre>%s</pre>
    """ % stdout

#@app.route("/listimages")
#def listimages():
#    p = Popen(['docker','images'],stdout=PIPE)
#    return 'Images = %s' % p.stdout.read()
#    list=['Images']
#    for line in p.stdout:
#        list.append(line)
#    return 'Images = %s' % list

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
