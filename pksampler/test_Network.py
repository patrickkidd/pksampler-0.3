
import sys
if sys.argv[1] == 'HCS':
    from Grouping.Network import test_HostCacheServer
    test_HostCacheServer()
elif sys.argv[1] == 'PAS':
    from Grouping.Network import test_PKAudioServer
    test_PKAudioServer()
elif sys.argv[1] == 'Dispatch':
    from Grouping.Network import test_Dispatch
    test_Dispatch()
