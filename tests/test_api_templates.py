from vent.api.templates import Template

def test_options():
    """ Test the options function """
    instance = Template()
    instance.options('foo')

def test_option():
    """ Test the option function """
    instance = Template()
    instance.option('foo', 'bar')

def test_add_option():
    """ Test the add_option function """
    instance = Template()
    instance.add_option('foo', 'bar')

def test_del_section():
    """ Test the del_section function """
    instance = Template()
    instance.del_section('foo')

def test_del_option():
    """ Test the del_option function """
    instance = Template()
    instance.del_option('foo', 'bar')
