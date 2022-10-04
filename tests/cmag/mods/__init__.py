from cmag.modules import (
    CMagInitialScanner,
    CMagChallScanner,
    CMagFileScanner,
    CMagFileExtractor
)

class mod01(CMagChallScanner):
    name = 'test.mod01'

class mod02(CMagInitialScanner):
    name = 'test.mod02'

class mod03(CMagFileScanner):
    name = 'test.mod03'
    target = 'a;b;c'

class mod04(CMagFileScanner):
    name = 'test.mod04'
    target = 'a'

class mod05(CMagFileScanner):
    name = 'test.mod05'
    target = 'b'

class mod06(CMagFileExtractor):
    name = 'test.mod06'
    target = '*'

class mod07(CMagFileExtractor):
    name = 'test.mod07'
    target = 'a;b'

class mod08(CMagFileExtractor):
    name = 'test.mod08'
    target = 'c'

def init(project):
    return [
        mod01(project),
        mod02(project),
        mod03(project),
        mod04(project),
        mod05(project),
        mod06(project),
        mod07(project),
        mod08(project),
    ]