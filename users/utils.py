import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from .. import mail

def save_picture(form_pic):
    """
    Prepare img to be saved into file system.  This method generates
    a random name for pic, then resizes the pic and saves to file system
    """
    # generate random name for pic
    rdm_hex = secrets.token_hex(8)
    # extract file format
    _, ext = os.path.splitext(form_pic.filename)
    # combine new name and file format
    pic_fn = f'{rdm_hex}{ext}'
    # build the picture path
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fn)

    # resize image to 125x125
    output_size = (125,125)
    img = Image.open(form_pic)
    img.thumbnail(output_size)

    # save picture to the path defined above
    img.save(pic_path)

    return pic_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password reset request', sender='noreply@flaskdemo.com',
                  recipients=[user.email])
    
    msg.body = f'''
                    To reset your password, visit the following link:
                    {url_for('users.reset_token', token=token, _external=True)}

                    If you did not make this request, then ignore this email and no
                    changes will be made.
                '''

    mail.send(msg)