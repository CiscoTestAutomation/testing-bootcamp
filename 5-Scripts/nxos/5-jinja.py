import jinja2
from genie.testbed import load
tb = load('../../testbed.yaml')

device = tb.devices['xr-1']
device.connect(via='cli')

kwargs = {}
kwargs['process_id'] = "SR"


interface = 'GigabitEthernet0/0/0/1'

# Load the Jinja template
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))
template = env.get_template('config_isis.j2')

# Render the template and populate the field
configuration = template.render(process_id='SR',
                      net_address='49.0001.1111.1111.1111.00',
                      address_family='ipv4 unicast',
                      metric_style='wide',
                      loopback_interface='Loopback0',
                      interface_name=interface,
                      metric='10')
device.configure(configuration)

#output = device.parse('show isis neighbors')
is_neighbor_up = device.api.verify_isis_neighbor_in_state(interfaces=[interface])
if not is_neighbor_up:
    raise Exception("'{intf}' is not up as expected".format(intf=interface))


