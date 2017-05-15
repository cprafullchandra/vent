import npyscreen
import threading
import time

from vent.api.actions import Action
from vent.helpers.meta import Containers
from vent.helpers.meta import Core
from vent.helpers.meta import Timestamp
from vent.helpers.meta import Uptime

class MainForm(npyscreen.FormBaseNewWithMenus):
    """ Main information landing form for the Vent CLI """
    api_action = Action()

    def while_waiting(self):
        """ Update fields periodically if nothing is happening """
        self.addfield.value = Timestamp()
        self.addfield.display()
        self.addfield2.value = Uptime()
        self.addfield2.display()
        self.addfield3.value = str(len(Containers()))+" running"
        self.addfield3.display()

        # set core value string
        core = Core()
        installed = 0
        custom_installed = 0
        built = 0
        custom_built = 0
        running = 0
        custom_running = 0
        normal = str(len(core['normal']))
        for tool in core['running']:
            if tool in core['normal']:
                running += 1
            else:
                custom_running += 1
        for tool in core['built']:
            if tool in core['normal']:
                built += 1
            else:
                custom_built += 1
        for tool in core['installed']:
            if tool in core['normal']:
                installed += 1
            else:
                custom_installed += 1
        core_str = str(running+custom_running)+"/"+normal+" running"
        if custom_running > 0:
            core_str += " ("+str(custom_running)+" custom)"
        core_str += ", "+str(built+custom_built)+"/"+normal+" built"
        if custom_built > 0:
            core_str += " ("+str(custom_built)+" custom)"
        core_str += ", "+str(installed+custom_installed)+"/"+normal+" installed" 
        if custom_built > 0:
            core_str += " ("+str(custom_installed)+" custom)"
        self.addfield5.value = core_str
        if running+custom_running == 0:
            color = "DANGER"
        elif running >= int(normal):
            color = "GOOD"
        else:
            color = "CAUTION"
        self.addfield5.labelColor = color
        self.addfield5.display()

        # !! TODO update fields such as health status, jobs, etc. alsoo
        return

    def core_tools(self, action):
        """ Perform actions for core tools """
        def diff(first, second):
            """
            Get the elements that exist in the first list and not in the second
            """
            second = set(second)
            return [item for item in first if item not in second]

        def popup(original, orig_type, thr, title):
            """
            Start the thread and display a popup of info
            until the thread is finished
            """
            thr.start()
            info_str = ""
            while thr.is_alive():
                info = diff(Containers(), original)
                if info:
                    info_str = ""
                for entry in info:
                    # TODO limit length of info_str to fit box
                    info_str += entry[0]+": "+entry[1]+"\n"
                npyscreen.notify_wait(info_str, title=title)
                time.sleep(1)
            return

        if action == 'install':
            # !! TODO
            pass
        elif action == 'build':
            original_images = Images()
            # !! TODO
        elif action == 'start':
            original_containers = Containers()
            thr = threading.Thread(target=self.api_action.start, args=(),
                                   kwargs={'groups':'core'})
            popup(original_containers, "containers", thr,
                  'Please wait, starting core containers...')
            npyscreen.notify_confirm("Done starting core containers.",
                                     title='Started core containers')
        elif action == 'stop':
            original_containers = Containers()
            thr = threading.Thread(target=self.api_action.stop, args=(),
                                   kwargs={'groups':'core'})
            popup(original_containers, "containers", thr,
                  'Please wait, stopping core containers...')
            npyscreen.notify_confirm("Done stopping core containers.",
                                     title='Stopped core containers')
        elif action == 'clean':
            original_containers = Containers()
            thr = threading.Thread(target=self.api_action.clean, args=(),
                                   kwargs={'groups':'core'})
            popup(original_containers, "containers", thr,
                  'Please wait, cleaning core containers...')
            npyscreen.notify_confirm("Done cleaning core containers.",
                                     title='Cleaned core containers')
        return

    def perform_action(self, action):
        """ Perform actions in the api from the CLI """
        def diff(first, second):
            """
            Get the elements that exist in the first list and not in the second
            """
            second = set(second)
            return [item for item in first if item not in second]

        def popup(original_containers, thr, title):
            """
            Start the thread and display a popup of the running containers
            until the thread is finished
            """
            thr.start()
            container_str = ""
            while thr.is_alive():
                containers = diff(Containers(), original_containers)
                if containers:
                    container_str = ""
                for container in containers:
                    # TODO limit length of container_str to fit box
                    container_str += container[0]+": "+container[1]+"\n"
                npyscreen.notify_wait(container_str, title=title)
                time.sleep(1)
            return

        original_containers = Containers()
        if action == 'add':
            self.parentApp.change_form('ADD')
        elif action == 'start':
            # TODO pass in actual args and kwargs
            # TODO show a build popup first to improve UX
            thr = threading.Thread(target=self.api_action.start, args=(),
                                   kwargs={'branch':'experimental'})
            popup(original_containers, thr,
                  'Please wait, starting containers...')
            npyscreen.notify_confirm("Done starting containers.",
                                     title='Started Containers')
        elif action == 'stop':
            # TODO pass in actual args and kwargs
            thr = threading.Thread(target=self.api_action.stop, args=(),
                                   kwargs={'branch':'experimental'})
            popup(original_containers, thr,
                  'Please wait, stopping containers...')
            npyscreen.notify_confirm("Done stopping containers.",
                                     title='Stopped Containers')
        elif action == 'clean':
            # TODO pass in actual args and kwargs
            thr = threading.Thread(target=self.api_action.clean, args=(),
                                   kwargs={'branch':'experimental'})
            popup(original_containers, thr,
                  'Please wait, cleaning containers...')
            npyscreen.notify_confirm("Done cleaning containers.",
                                     title='Cleaned Containers')
        return

    def create(self):
        """ Override method for creating FormBaseNewWithMenu form """
        self.add_handlers({"^T": self.change_forms, "^S": self.services_form})
        self.addfield = self.add(npyscreen.TitleFixedText, name='Date:',
                                 labelColor='DEFAULT', value=Timestamp())
        self.addfield2 = self.add(npyscreen.TitleFixedText, name='Uptime:',
                                  labelColor='DEFAULT', value=Uptime())
        self.addfield3 = self.add(npyscreen.TitleFixedText, name='Containers:',
                                  labelColor='DEFAULT',
                                  value=str(len(Containers()))+" running")
        self.addfield4 = self.add(npyscreen.TitleFixedText, name='Status:',
                                  value="Healthy")
        self.addfield5 = self.add(npyscreen.TitleFixedText,
                                  name='Core Tools:', labelColor='DANGER',
                                  value="Not built")
        self.addfield6 = self.add(npyscreen.TitleFixedText, name='Clustered:',
                                  value="No", labelColor='DEFAULT')
        self.addfield7 = self.add(npyscreen.TitleFixedText, name='Jobs:',
                                  value="None", labelColor='DEFAULT')
        self.multifield1 =  self.add(npyscreen.MultiLineEdit, max_height=22,
                                     editable=False, value = """

            '.,
              'b      *
               '$    #.
                $:   #:
                *#  @):
                :@,@):   ,.**:'
      ,         :@@*: ..**'
       '#o.    .:(@'.@*"'
          'bq,..:,@@*'   ,*
          ,p$q8,:@)'  .p*'
         '    '@@Pp@@*'
               Y7'.'
              :@):.
             .:@:'.
           .::(@:.
                       _
      __   _____ _ __ | |_
      \ \ / / _ \ '_ \| __|
       \ V /  __/ | | | |_
        \_/ \___|_| |_|\__|
                           """)
        self.m2 = self.add_menu(name="Core Tools", shortcut="t")
        self.m2.addItem(text='Install all latest core tools',
                        onSelect=self.core_tools,
                        arguments=['install'], shortcut='i')
        self.m2.addItem(text='Build all core tools',
                        onSelect=self.core_tools,
                        arguments=['build'], shortcut='b')
        self.m2.addItem(text='Start all core tools',
                        onSelect=self.core_tools,
                        arguments=['start'], shortcut='s')
        self.m2.addItem(text='Stop all core tools',
                        onSelect=self.core_tools,
                        arguments=['stop'], shortcut='p')
        self.m2.addItem(text='Clean all core tools',
                        onSelect=self.core_tools,
                        arguments=['clean'], shortcut='c')
        self.m3 = self.add_menu(name="Plugins", shortcut="p")
        self.m3.addItem(text='Add new repository',
                        onSelect=self.perform_action,
                        arguments=['add'], shortcut='a')
        self.m3.addItem(text='List installed repositories',
                        onSelect=self.perform_action,
                        arguments=['list'], shortcut='l')
        self.m3.addItem(text='Update repositories',
                        onSelect=self.perform_action,
                        arguments=['update'], shortcut='u')
        self.m3.addItem(text='Remove tools',
                        onSelect=self.perform_action,
                        arguments=['Remove'], shortcut='r')
        self.m3.addItem(text='Build tools', onSelect=self.perform_action,
                        arguments=['build'], shortcut='b')
        self.m3.addItem(text='Start tools', onSelect=self.perform_action,
                        arguments=['start'], shortcut='s')
        self.m3.addItem(text='Stop tools', onSelect=self.perform_action,
                        arguments=['stop'], shortcut='p')
        self.m3.addItem(text='Clean tools', onSelect=self.perform_action,
                        arguments=['clean'], shortcut='c')
        self.m3.addItem(text='Services Running', onSelect=self.services_form,
                        arguments=[])
        self.m4 = self.add_menu(name="Logs", shortcut="l")
        self.m4.addItemsFromList([
            ("Just Beep", None),
        ])
        #self.m5 = self.add_menu(name="System Commands", shortcut="c")
        #self.m5.addItemsFromList([
        #    ("Just Beep", None),
        #])
        #self.m7 = self.add_menu(name="Cluster Management", shortcut="m")
        #self.m7.addItemsFromList([
        #    ("Just Beep", None),
        #])

    def services_form(self, *args, **keywords):
        self.parentApp.change_form("SERVICES")

    def change_forms(self, *args, **keywords):
        """
        Checks which form is currently displayed and toggles it to the other
        one
        """
        if self.name == "Help\t\t\t\t\t\t\t\tPress ^T to toggle help":
            change_to = "MAIN"
        else:
            change_to = "HELP"

        # Tell the VentApp object to change forms.
        self.parentApp.change_form(change_to)
