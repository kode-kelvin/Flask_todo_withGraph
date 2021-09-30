from flask import Flask, request, render_template, redirect, flash, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# get the plotly and vis modules
import pandas as pd
import json
import plotly
import plotly.express as px



# configurations and database -----------------------------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""
for secrets key--
terminal: type 
python
import secrets
secrets.token_hex(24)
results below
'cd1be90df3d568e1deffd1cd13a7ec1471dd37090f8e34e9'
"""
app.config['SECRET_KEY'] = 'cd1be90df3d568e1deffd1cd13a7ec1471dd37090f8e34e9'
db = SQLAlchemy(app)


# models -----------------------------------------
CHOICE_STATUS = [('Done', 'Done'), ('Active', 'Active')]
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Todo' + str(self.id) 


# route -----------------------------------------

# creating----------------

@app.route('/', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        todo_status = request.form['status']
        todo_content = request.form['content']
        if not todo_content:
            flash('You must enter a todo', category='error')
        else:
            new_todo = Todo(content=todo_content, status=todo_status)
            db.session.add(new_todo)
            db.session.commit()
            flash('Todo added', 'info')
        return redirect('/')
    else:
        all_todo = Todo.query.order_by(Todo.status).all()
        completed_todo = Todo.query.filter_by(status='Completed').all()
        completed_todo = len(completed_todo)

        # for uncomplete task
      
        uncomplete_todo = Todo.query.filter_by(status='Uncomplete').all()
        uncomplete_todo = len(uncomplete_todo)

        # for uncomplete task
        complete_todo = Todo.query.filter_by(status='Completed').all()
        complete_todo = len(complete_todo)
    
        df = pd.DataFrame({
            "Todo": ["Complete", "Pending"],
            "Numbers": [complete_todo,  uncomplete_todo],
            "Legend": ["Complete", "Pending"]
        })

        graph = px.bar(df, x="Todo", y="Numbers", color="Legend", barmode="group")

        graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
        header = "Todo Data"
        description = "Using plotly and flask to view data from db"
        
        return render_template('todo.html', todos=all_todo, data=completed_todo, data2=uncomplete_todo,  graphJSON=graphJSON, header=header, description=description)

# updating----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.content = request.form['content']
        todo.status = request.form['status']
        db.session.commit()
        flash('Todo Updated', 'info')
        return redirect('/')
    else:
        return render_template('update.html', todo=todo)
   
# delete----------------
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')






# to run the app
if __name__ == '__main__':
    app.run(debug=True)


# q = session.query(Genotypes).filter(Genotypes.rsid.in_(inall))
# query_as_string = str(q.statement.compile(compile_kwargs={"literal_binds": True}))
# session.execute(query_as_string).first()




# creating a connection to database
 # con = sqlite3.connect('/Users/mac/Desktop/basic_flask_crud/todo.db')
    # cur = con.cursor()
    # cur.execute('SELECT COUNT(*) FROM TODO WHERE status ="Completed";')
    # rows = cur.fetchall()
    # for row in rows:
    #     print(row)