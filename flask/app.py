from flask import Flask, redirect, url_for, request
import os

app = Flask(__name__)

app.config['SESSION_FOLDER'] = './session/'
@app.route('/')
def home():
    models=['HKY', 'F84', 'GTR', 'JTT', 'WAG', 'PAM', 'BLOSUM', 'MTREV', 'CPREV','GENERAL', 'REV', 'CPREV45', 'MTART', 'LG']
    return '''
<!doctype html>
<h1>Run Seq-Gen</h1>
<form method="post" action="/run" enctype=multipart/form-data>
      <p>Enter Input File:</p>
      <p>
        <input type="file" name="file" required onchange="showTree(this)" />
      </p>
      <pre
        id="input"
        style="
          outline: 1px solid black;
          min-height: 1rem;
          padding: 0.5rem;
          max-height: 10rem;
          overflow-y: auto;
        "
      ></pre>
      <script>
        let showTree = (e) => {
          let input = document.getElementById("input");
          const reader = new FileReader();
          reader.onload = () => {
            const text = reader.result;
            input.innerText = text;
          };
          input.innerText = "";
          reader.readAsText(e.files[0]);
        };
      </script>
      <p>Enter Output File Name:</p>
      <p><input required type="text" name="outfile" id="outfile" /></p>
      <p>Enter SEQUENCE LENGTH:</p>
      <p><input required type="number" name="l" id="l" min="0" step="1" /></p>
      <p>Select Model:</p>
      <p>
        <select name="m" id="m">
    '''+''.join(['<option value="%s">%s</option>' % (m, m) for m in models])+'''
        </select>
    </p>
    <p>Enter NUMBER_OF_DATASETS:</p>
    <p><input required type="number" name="n" id="n" min="2" max="32" step="1" /></p>
    <p><input type="submit" value="run" /></p>
</form>
'''


@app.route('/reset')
def reset():
    for f in os.listdir(app.config["SESSION_FOLDER"]):
        os.remove(app.config["SESSION_FOLDER"]+f)
    return "all files deleted successfully <a href='/'>run again</a>"


@app.route('/view')
def view():
    return '<ul>' + ''.join(['<li><a href="/read/%s">%s</a></li>' % (f, f) for f in os.listdir(app.config["SESSION_FOLDER"])]) + '</ul>'+\
        '<a href="/reset">reset</a>'


@app.route('/read/<filename>')
def read(filename):
    return '<h1>'+filename+'</h1><pre>' + open(app.config["SESSION_FOLDER"]+filename).read() + '</pre>'
 
 
@app.route('/run', methods=['POST', 'GET'])
def run():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        file.save(os.path.join(app.config["SESSION_FOLDER"], file.filename))
        
        return 'file uploaded successfully <a href="/view">view</a>'
    return redirect(request.url)
 
if __name__ == '__main__':
    app.run(debug=True)