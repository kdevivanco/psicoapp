
from flask import Flask, render_template, request, redirect, Blueprint,session,flash
from app.models.users import User
from app.models.therapists import Therapist
from app.models.messages import Message
from app.decorators import login_required
import json
import pdb

messages = Blueprint('messages', __name__, template_folder='templates')




@messages.route('/send-msg/<reciever_id>', methods=['POST'])
#@login_required
def send_message(reciever_id):
    if 'user' not in session or session['user'] == None: 
        flash('No puedes mandar mensajes si no te has registrado', 'error')
        return redirect ('/register')
    reciever_id = int(reciever_id)
    sender_id = session['user']['id']
    Message.send_msg(sender_id,reciever_id,request.form)

    return redirect ('/dashboard')

@messages.route('/messages')
@login_required
def show_message(): #hay que pasarle el id
    recieved_messages = Message.get_recieved(session['user']['id'])
    sent_messages = Message.get_sent(session['user']['id'])
    user = User.get_one(session['user']['id'])
    logged = True
    for message in recieved_messages:
        if message.status == 'deleted':
            recieved_messages.remove(message)

    return render_template('message.html',recieved_messages = recieved_messages, sent_messages = sent_messages, user = user, logged = logged)


@messages.route('/message-update/<message_id>')
@login_required
def contact_message(message_id):
    user = User.get_one(session['user']['id'])
    message = Message.get_one(int(message_id))
    if message == False:
        return redirect('/messages')
    if user.id != message.reciever_id:
        flash('Not your message!','error')
        return redirect('/dashboard')
    status = 'contacto'
    Message.update_message(message_id,status)
    return redirect('/messages')

@messages.route('/message-seen/<message_id>')
@login_required
def read_message(message_id):
    user = User.get_one(session['user']['id'])
    message = Message.get_one(message_id)
    if message == False:
        return redirect('/messages')
    if user.id != message.reciever_id:
        flash('Not your message!','error')
        return redirect('/dashboard')
    status = 'read'
    Message.update_message(message_id,status)
    return redirect('/messages')

@messages.route('/message-delete/<message_id>')
@login_required
def delete_message(message_id):
    user = User.get_one(session['user']['id'])
    message = Message.get_one(message_id)
    if message == False:
        return redirect('/messages')
    if user.id != message.reciever_id:
        flash('Not your message!','error')
        return redirect('/dashboard')
    status = 'deleted'
    Message.update_message(message_id,status)
    return redirect('/messages')