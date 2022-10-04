from cmag.manager import CMagProject

def main():
    project = CMagProject.new(
        './workspace/project',
        {
            'modules': './modules'
        }
    )
    chall = project.add_challenge()
    chall.add_file("./workspace/abcd/a.zip")
    chall.scan()