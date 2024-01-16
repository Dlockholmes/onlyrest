from app import app

# Test Running
app.run(host="0.0.0.0", port=80, debug=True)

# Service Setting
# app.run(host="0.0.0.0",  port=80, ssl_context='adhoc')