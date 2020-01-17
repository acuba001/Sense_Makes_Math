from app import create_app

app = create_app('development')
app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app)