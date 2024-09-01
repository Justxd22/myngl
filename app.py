"""Main app."""
import time
from flask import Flask, request, redirect, abort, render_template, make_response
from ua import nglxD



app = Flask("NGL_XD")
ngl = nglxD()

@app.route('/')
def home():
    aa = request.headers.get('Sec-Ch-Ua-Platform-Version')
    ua = request.user_agent.string
    x = bool('windows' in ua.lower())
    if not aa and x:
        r = render_template('request_accept_platform.html')
        res = make_response(r)
        res.headers['Critical-CH'] = 'Accept-CH'
        res.headers['accept-ch'] = "Sec-Ch-Ua-Platform,Sec-Ch-Ua-Platform-Version"
        return res

    user = ngl.break_ua(ua, winver=aa if x else None)
    print(user, '\n\n\n', ngl.get_me(user))
    res = make_response(f"Hello world!,\n\n\n\n{ngl.get_me(user)}")
    res.set_cookie('session_id', user, path='/', samesite='None', secure=True, domain="", expires=time.time() + 99999999)
    return res




app.run(debug=True)
