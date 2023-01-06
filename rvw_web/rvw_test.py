from rvw_web import app, render_template, request
from rvw_structuri import Membru
import rvw_template
import uuid
import rvw_event

@app.route('/test/design', methods=['GET'])
def dezain_test():
    cookie = request.cookies.get("devs")
    if cookie:
        user = Membru.getByLoguid(cookie) 
        if user and len(cookie) > 6:
            if user.status == "acceptat":
                uid = str(uuid.uuid4())
                seccs = user.seccodes
                seccs.append(uid)
                while len(seccs) > 1:
                    seccs.pop(0)
                user.seccodes = seccs
                user.save()
                return render_template("test.html", seccode = uid)
    return "Cookie-ul nu a fost gasit :0"


@app.route('/test/get_t_t/<seccode>/', methods=['GET'])
def template_test(seccode):
    return render_template("general/prezenta.html", seccode = seccode)