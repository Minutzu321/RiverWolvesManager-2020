from flask import render_template

def getGeneralTemplate(user, seccode):
    generaldivs = '' 
    if user.getTasks():

        #prezenta
        generaldivs += '''
            <div class="card text-center">
                <div class="card-body">
                <h4 class="card-title">Inregistreaza prezenta la activitate</h4>
                <p class="card-text">(Presupune activarea locatiei)</p>
                <button class="btn btn-primary btn-round btn-lg btn-block col-md-4 ml-auto mr-auto" onclick="execPrezent()">Prezent</button>
                </div>
            </div>
'''
    return generaldivs

def getTestTemplate():
    return render_template("general/prezenta.html")

def getScripts(user, seccode):
    scripts = '''
    <script type="text/javascript">
    
            </script>
    '''
    return scripts