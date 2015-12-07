import os
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from subprocess import Popen,PIPE
sys.path.append('/data')
from keys import access_key_id, secret_access_key

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

# List all queues
@app.route('/queues', methods=['GET'])
def queues_index():

     conn = boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
     rs = conn.get_all_queues()
     for q in rs:
	print q.id
     return q.id

# Inspect specific container
@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    return Response(response=docker('inspect', id), mimetype="application/json")

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
    return stdout





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
    app.run(host="0.0.0.0",port=5000)
