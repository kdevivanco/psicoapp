
from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.users import User
from app.models.therapists import Therapist
from app.models.messages import Message
from app.decorators import login_required
import json
import pdb

messages = Blueprint('messages', __name__, template_folder='templates')




@messages.route('/send-msg/<reciever_id>', methods=['POST'])
@login_required
def send_message(reciever_id):
    reciever_id = int(reciever_id)
    sender_id = session['user']['id']
    Message.send_msg(sender_id,reciever_id,request.form)

    return redirect ('/dashboard')