from invoke import task

@task
def build(c, docs=False):
    c.run("pyinstaller --clean --noconfirm  app.spec")
    

@task
def test(c, docs=False):
    c.run("pytest -n 4 ./tests")

@task
def env(c, docs=False):
    c.run(r".\cfsplayer\Scripts\activate this.py")

@task
def doc(c, docs=False):
    c.run(r"pdoc --html --force slothplayer")
