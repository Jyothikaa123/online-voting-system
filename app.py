from flask import Flask,session,redirect,render_template

from models import db, user,Candidate,Vote
import hashlib
app=Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
@app .route('/')
def home():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        usernmae=request.form.get('username').strip().lower()
        passsword=request.form.get('password')
        user=USer.query.filter_by(username=username).first()
        if user and user.password==hashlib.sha256(paswword.encode()).hexdigest():
            session['user_id']=user
            flash('login was successful','success')
            return redirect(url_for('vote'))
        else:
            flash('login was failed may be in valid credentials','danger')
            return render_template('login.html')
@app.route('/vote',methods=['GET','POST'])
def vote():
    if 'use_id'not in session:
        return redirect(url_for('login'))
    if request.method=='POST':
        candidate_id=request.form.get('candidate')
        new_vote=Vote(user_id=session['user_id'],candidate_id=candidate_id)
        db.session.add(new_vote)
        db.session.commit()
        flash('your vote has been concluded','succes')
        return redirect(url_for('results'))
    candidates=Candidate.query.all()
    return render_template('vote.html',candidate=candidates)
@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        if request.method == 'POST':
          candidate_id = request.form.get('candidate')
          new_vote = Vote(user_id=session['user_id'], candidate_id=candidate_id)
          db.session.add(new_vote)
          db.session.commit()
          flash('Your vote has been recorded!', 'success')
          return redirect(url_for('results'))

    candidates = Candidate.query.all()
    return render_template('vote.html', candidates=candidates)

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    results = db.session.query(Candidate, db.func.count(Vote.id)).outerjoin(Vote).group_by(Candidate.id).all()
    return render_template('results.html', results=results)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)