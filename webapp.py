#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import re
import urllib
from flask import Flask, request, url_for, redirect, render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='nopw'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

socket = urllib.urlopen("http://rest.kegg.jp/list/pathway/hsa")
htmlSource = socket.read()
socket.close()
pathways = re.findall('path:((?:.)*?)	', htmlSource)
# numberofpathways = len(pathways)
pathwayname = re.findall('(?:	).*', htmlSource)
for line, i in enumerate(pathwayname):
    pathwayname[line] = pathwayname[line].strip("\t")


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html', pathways=pathways, pathwayname=pathwayname)
    else:
        path = request.form['path']
        return redirect(url_for('preview', path=path))

@app.route("/<string:path>", methods=['GET', 'POST'])
def preview(path):
    if request.method == 'GET':
        return render_template('view.html', pathways=pathways, path=path, pathname=pathwayname[pathways.index(path)])
    else:
        path = request.form['path']
        return redirect(url_for('preview', path=path))

@app.errorhandler(404)
def not_found(error):
    flash('404 - Page not found!')
    return redirect(url_for('home'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)