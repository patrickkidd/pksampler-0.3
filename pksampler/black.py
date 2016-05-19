""" black.py: Run the Black project. """

import sys

if len(sys.argv) == 1 or sys.argv[1] == 'main':
    from Black import MainWindow
    MainWindow.main()
elif sys.argv[1] == 'MainWindow':
    from Black import MainWindow
    MainWindow.main()
elif sys.argv[1] == 'SampleView':
    from Black.Views.SampleView import test_SampleView
    test_SampleView()
elif sys.argv[1] == 'Button':
    from Black.GUI.Button import test_Button
    test_Button()
elif sys.argv[1] == 'Part':
    from Black import Common
    Common.test_Part()
elif sys.argv[1] == 'Fadeable':
    from Black.GUI.Fadeable import test_Fadeable
    test_Fadeable()
elif sys.argv[1] == 'TabWindow':
    from Black import Common
    Common.test_TabWindow()
elif sys.argv[1] == 'Control':
    from Black.Views.SampleView import test_Control
    test_Control()
elif sys.argv[1] == 'FilePart':
    from Black.GUI.FSParts import test_FilePart
    test_FilePart()
elif sys.argv[1] == 'DirPart':
    from Black.GUI.FSParts import test_DirPart
    test_DirPart()
elif sys.argv[1] == 'SelectorView':
    from Black.Views.SelectorView import test_SelectorView
    test_SelectorView()
elif sys.argv[1] == 'LibraryView':
    from Black.Views.LibraryView import test_LibraryView
    test_LibraryView()
elif sys.argv[1] == 'ComboBox':
    from Black.GUI.ComboBox import test_ComboBox
    test_ComboBox()
elif sys.argv[1] == 'NewGroupPart':
    from Black.Views.LibraryView import test_NewGroupPart
    test_NewGroupPart()
elif sys.argv[1] == 'TempoView':
    from Black.Views.TempoView import test_TempoView
    test_TempoView()
elif sys.argv[1] == 'TempoPart':
    from Black.Views.TempoView import test_TempoPart
    test_TempoPart()
