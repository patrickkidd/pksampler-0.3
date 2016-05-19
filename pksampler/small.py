""" small.py: Run the small project. """

import sys

if len(sys.argv) == 1 or sys.argv[1] == 'main':
    from Small import Small
    Small.main()
elif sys.argv[1] == 'group':
    from Small import SampleGroup
    SampleGroup.main()
    
elif sys.argv[1] == 'animation':
    from Small import Animation
    Animation.main()

