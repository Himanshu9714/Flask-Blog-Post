# Flask-Blog-Post

#### Clone the Project

<pre>git clone https://github.com/Himanshu9714/Flask-Blog-Post.git</pre>

#### Change the directory

<pre>cd Flask-Blog-Post</pre>

#### Create virtual environment

<pre>python -m venv venv</pre>

#### Activate virtual environment

<pre>Windows: venv\Scripts\activate</pre>

#### Install requirements

<pre>pip install -r requirements.txt</pre>

#### Run Flask App

<pre>python app.py</pre>

### NOTE:

- Please make sure that you don't use <b>create_database()</b> functionality in live, as it is hard coded and can be useful only in the development.
- If you add a new `model` in the models.py file, then you've to delete the old database.db. After that, run the server again so it creates a fresh database again.
