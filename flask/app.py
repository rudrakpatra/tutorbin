from flask import Flask, redirect, url_for, request
app = Flask(__name__)
 
@app.route('/')
def home():
    return '''
<html>
  <body>
    <form action="http://localhost:5000/login" method="post">
      <p>Enter Name:</p>
      <p><input type="text" name="nm" /></p>
      <p><input type="submit" value="submit" /></p>
    </form>
  </body>
</html>
'''
 
@app.route('/read/<filename>')
def read(filename):
    return 'reading %s' % filename
 
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))
 
 
if __name__ == '__main__':
    app.run(debug=True)