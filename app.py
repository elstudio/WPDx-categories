import csv, math, os, subprocess
from flask import Flask, redirect, render_template, request, send_file, url_for
app = Flask(__name__)

RESULTS_PER_PAGE = 25

# Water Source Types tab
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'train' in request.files and request.files['train'].filename:
            file = request.files['train']
            file.save('train-input.csv')
            train_file = 'train-input.csv'
        else:
            train_file = 'Python Classification Training Data.csv'

        if 'classify' in request.files and request.files['classify'].filename:
            file = request.files['classify']
            file.save('classify-input.csv')
        else:
            return 'No Classify file selected'
        process = subprocess.Popen(['python', 'training.py', train_file], stdout=subprocess.PIPE)
        out1 = process.stdout.read()
        if train_file == 'train-input.csv':
            os.remove('train-input.csv')
        process = subprocess.Popen(['python', 'classification.py', 'classify-input.csv', 'classify-output.csv'], stdout=subprocess.PIPE)
        out2 = process.stdout.read()
        os.remove('classify-input.csv')
        return redirect(url_for('.classify_results', message="{}\n{}".format(out1, out2)))

    results_exist = os.path.isfile('classify-output.csv')
    # Reading sample data
    with open('sample.csv', 'rU') as f:
        sample = f.readlines();
    return render_template('index.html', results_exist=results_exist, sample=sample, result_column='Water Source Type')

@app.route('/classify-results')
def classify_results():
    page = int(request.args.get('page', '1'))
    with open('classify-output.csv', 'rU') as f:
        reader = csv.reader(f)
        # Skip Header
        next(reader)
        results = list(reader)
    start = (page - 1) * RESULTS_PER_PAGE
    stop = start + RESULTS_PER_PAGE
    total_pages = 1 + int((len(results) - 1) / RESULTS_PER_PAGE)
    results = results[start:stop]
    return render_template('classify-results.html',
                           results=results,
                           page=page,
                           total_pages=total_pages,
                           results_exist=True,
                           message=request.args.get('message', ''))

@app.route('/export')
def export():
    return send_file('classify-output.csv', as_attachment=True)

# Status tab
@app.route('/status', methods=['GET', 'POST'])
def status_index():
    if request.method == 'POST':
        if 'train' in request.files and request.files['train'].filename:
            file = request.files['train']
            file.save('status/data/train-input.csv')
            train_file = 'data/train-input.csv'
        else:
            train_file = 'data/training.csv'

        if 'classify' in request.files and request.files['classify'].filename:
            file = request.files['classify']
            file.save('status/data/classify-input.csv')
        else:
            return 'No Classify file selected'
        process = subprocess.Popen(['python', 'training.py', train_file], cwd='status', stdout=subprocess.PIPE)
        out1 = process.stdout.read()
        if train_file == 'data/train-input.csv':
            os.remove('status/data/train-input.csv')
        process = subprocess.Popen(['python', 'classification.py', 'data/classify-input.csv', 'data/classify-output.csv'], cwd='status', stdout=subprocess.PIPE)
        out2 = process.stdout.read()
        os.remove('status/data/classify-input.csv')
        return redirect(url_for('.status_classify_results', message="{}\n{}".format(out1, out2)))

    results_exist = os.path.isfile('status/data/classify-output.csv')
    # Reading sample data
    with open('status/data/sample.csv', 'rU') as f:
        sample = f.readlines();
    return render_template('index.html', results_exist=results_exist, sample=sample, result_column='Status Category')

@app.route('/status/classify-results')
def status_classify_results():
    page = int(request.args.get('page', '1'))
    with open('status/data/classify-output.csv', 'rU') as f:
        reader = csv.reader(f)
        # Skip Header
        next(reader)
        results = list(reader)
    start = (page - 1) * RESULTS_PER_PAGE
    stop = start + RESULTS_PER_PAGE
    total_pages = 1 + int((len(results) - 1) / RESULTS_PER_PAGE)
    results = results[start:stop]
    return render_template('classify-results.html',
                           results=results,
                           page=page,
                           total_pages=total_pages,
                           results_exist=True,
                           message=request.args.get('message', ''))

@app.route('/status/export')
def status_export():
    return send_file('status/data/classify-output.csv', as_attachment=True)

# Common
@app.route('/bootstrap.min.css')
def bootstrap_min_css():
    return send_file('bootstrap.min.css')

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, port=port, host='0.0.0.0')
