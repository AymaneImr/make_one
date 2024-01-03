from flask import Blueprint, render_template, request, redirect, url_for, session

fourth = Blueprint('fourth', __name__)

@fourth.route('/my_channel')
def my_channel():
    username = session['username']
    return f'my channel {username}'

'''create a quote or a post / pictures
'''

@fourth.route('/create_chaneel', methods=['POST', 'GET'])
def create_channel():
    if request.method == 'POST':
        channel_name = request.form.get('channel_name')
        pass
