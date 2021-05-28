from flask import Flask, request

app = Flask(__name__)

@app.route('/code/<code>',methods=["GET"])
def getCode(code):
  
  return code

