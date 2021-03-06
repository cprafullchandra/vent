import curses
import npyscreen

from vent.menu import VentApp
from vent.menus.add import AddForm
from vent.menus.help import HelpForm
from vent.menus.main import MainForm
from vent.menus.services import ServicesForm
from vent.menus.choose_tools import ChooseToolsForm
from vent.menus.add_options import AddOptionsForm
from vent.menus.tutorials.tutorials import TutorialForm
from vent.menus.tutorials.tutorial_forms import TutorialAddingFilesForm
from vent.menus.tutorials.tutorial_forms import TutorialAddingPluginsForm
from vent.menus.tutorials.tutorial_forms import TutorialBackgroundForm
from vent.menus.tutorials.tutorial_forms import TutorialBuildingCoresForm
from vent.menus.tutorials.tutorial_forms import TutorialGettingSetupForm
from vent.menus.tutorials.tutorial_forms import TutorialIntroForm
from vent.menus.tutorials.tutorial_forms import TutorialSettingUpServicesForm
from vent.menus.tutorials.tutorial_forms import TutorialStartingCoresForm
from vent.menus.tutorials.tutorial_forms import TutorialTerminologyForm

def test_menu():
    """ Test the menu """
    npyscreen.TEST_SETTINGS['TEST_INPUT'] = ['^X', '^T']
    npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = True

    A = VentApp()
    try:
        A.run(fork=False)
    except Exception as e:
        pass
