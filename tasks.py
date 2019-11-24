from invoke import task

@task
def build(c, docs=False):
    #c.run(r"rmdir /q /s build")
    #c.run(r"rmdir /q /s dist")
    c.run("pyinstaller --clean --noconfirm  play.spec")
    

@task
def test(c, docs=False):
    c.run("pytest -n 4 ./tests")

@task
def env(c, docs=False):
    c.run(r".\cfsplayer\Scripts\activate this.py")

@task
def doc(c, docs=False):
    #c.run(r"rmdir /q /s docs")
    c.run(r"pdoc --html -o docs --force slothplayer")
    c.run(r"pdoc --html -o docs --force tests")


    
