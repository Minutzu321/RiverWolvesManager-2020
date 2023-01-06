from rvw_web import app, render_template, request

@app.route('/pln', methods=['GET', 'POST'])
def pln():
    if request.method == 'POST':
        pass
    return render_template("pln.html")