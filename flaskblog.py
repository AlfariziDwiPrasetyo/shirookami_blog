from flask import Flask, render_template, flash, redirect,url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__, static_folder='./img')
app.config['SECRET_KEY'] = 'fd51538b5168f164a1b57b018e859e54fa9fdde7'

posts = [
    {
    'author':'Al Farizi Dwi Prasetyo',
    'date_posted':'11 April 2023',
    },
    {
    'author':'Al Farizi Dwi Prasetyo',
    'date_posted':'12 April 2023',
    },

]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Posts')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Your account has been created')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'admin':
            flash(f'Welcome Back {form.password.data}')
            return redirect(url_for('home'))
        else:
            flash('Wrong username or password', 'gray-900')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)