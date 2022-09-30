import os

def makepath_factory(rootdir):

    def makepath(*args, relative=False):

        if args[0].startswith('/'):
            args[0] = args[0][1:]

        relpath = '/'.join(args)
        if relative:
            return relpath

        return os.path.join(rootdir, relpath)

    return makepath