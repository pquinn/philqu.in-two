from app import app

# app.run(host='0.0.0.0', port=8080, debug=True)
if __name__ == '__main__':
    print "running from run.py"
    app.run(host='0.0.0.0')