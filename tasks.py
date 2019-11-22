from invoke import task

@task
def build(c, docs=False):
    c.run("pyinstaller --clean --noconfirm  app.spec")
    

@task
def test(c, docs=False):
    c.run("pytest -n 4 ./tests")