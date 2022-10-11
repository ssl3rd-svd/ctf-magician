from cmag.project import CMagProject

project = CMagProject('workspace/kkk')
# project.add_challenge('test challenge!')
print(project.list_challenges())
challenge = project.get_challenge_by_name('test challenge!')
# challenge.create_file('jaja')
print(challenge.list_files())