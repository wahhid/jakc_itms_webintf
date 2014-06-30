from flask import render_template
from flask import request
from datetime import datetime

from app import app
import xmlrpclib

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)
        
@app.route('/approval/<int:ticket_id>')        
def approval(ticket_id):     
    return render_template("approval.html",
        title = 'Helpdesk Approval Process',
        ticket_id = ticket_id)    

@app.route('/process', methods=['GET', 'POST'])
def process():    
    openerp_server = 'localhost'
    user = 'admin'
    pwd = 'P@ssw0rd'
    dbname = 'itms_dev'
    if request.method == 'POST':
        ticket_id = request.form['ticket_id']
        approved_state = request.form['approved_state']
        comment = request.form['comment']
        sock = xmlrpclib.ServerProxy('http://' + openerp_server + ':8069/xmlrpc/common')
        uid = sock.login(dbname ,user ,pwd)
        sock = xmlrpclib.ServerProxy('http://' + openerp_server + ':8069/xmlrpc/object')        
        tickets = sock.execute(dbname, uid, pwd, 'helpdesk.ticket','read',[ticket_id],[])
        if tickets and tickets[0]['approved_state'] == '1' :            
            values = {}
            values['approved_state'] = approved_state
            values['approved_comment'] = comment            
            values['state'] = 'request_response'            
            print values
            results = sock.execute(dbname, uid, pwd, 'helpdesk.ticket', 'write', [ticket_id], values)           
            return render_template("result.html")
        else:
            return render_template("error.html")
    
    
    