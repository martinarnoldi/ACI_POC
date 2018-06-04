TenantName = "ARNO-TENANT02"
AppName = TenantName + "-APP01"
print AppName
# import libraries
from credentials import *
from acitoolkit.acitoolkit import *

# create session with apic
session = Session(URL, LOGIN, PASSWORD)
session.login()

#create tenant and vrf
tenant = Tenant(TenantName)
tenant.mark_as_deleted()



# print url and configuration data
print("\n{}\n\n{}".format(tenant.get_url(), tenant.get_json()))

# neatly print configuration data
import json
print(json.dumps(tenant.get_json(), sort_keys=True, indent=2, separators=(',',':')))


# push configuration to apic
resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

# test configuration request
if resp.ok:
     print("\n{}: {}\n\n{} is ready for use".format(resp.status_code, resp.reason, tenant.name))
else:
     print("\n{}: {}\n\n{} was not created!\n\n Error: {}".format(resp.status_code, resp.reason, subnet.name, resp.content))


