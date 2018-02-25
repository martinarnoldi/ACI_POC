TenantName = "ARNO-TENANT01"
AppName = TenantName + "-APP01"
VRFName = TenantName + "-VRF01"
BDName = TenantName + "-BD01"
Subnet01Name = TenantName + "-Subnet01"
print AppName
# import libraries
from credentials import *
from acitoolkit.acitoolkit import *

# create session with apic
session = Session(URL, LOGIN, PASSWORD)
session.login()

#create tenant and vrf
tenant = Tenant(TenantName)
vrf = Context(VRFName, tenant)

# create bridge domain with vrf relationship
bridge_domain = BridgeDomain(BDName, tenant)
bridge_domain.add_context(vrf)

# create public subnet and assign gateway
subnet = Subnet("ARNO_Subnet", bridge_domain)
subnet.set_scope("public")
subnet.set_addr("10.10.10.1/24")

# create http filter and filter entry
filter_http = Filter("http", tenant)
filter_entry_tcp80 = FilterEntry("tcp-80", filter_http, etherT="ip", prot="tcp", dFromPort="http", dToPort="http")

# create sql filter and filter entry
filter_sql = Filter("sql", tenant)
filter_entry_tcp1433 = FilterEntry("tcp-1433", filter_sql, etherT="ip", prot="tcp", dFromPort="1433", dToPort="1433")

# create app filter and filter entry
filter_app = Filter("app", tenant)
filter_entry_tcp1433 = FilterEntry("tcp-5723", filter_sql, etherT="ip", prot="tcp", dFromPort="5723", dToPort="5723")

# create web contract and associate to http filter
contract_web = Contract("web", tenant)
contract_subject_http = ContractSubject("http", contract_web)
contract_subject_http.add_filter(filter_http)

# create database contract and associate to sql filter
contract_database = Contract("database", tenant)
contract_subject_sql = ContractSubject("sql", contract_database)
contract_subject_sql.add_filter(filter_sql)

# create application contract and associate to app filter
contract_application = Contract("application", tenant)
contract_subject_sql = ContractSubject("app", contract_database)
contract_subject_sql.add_filter(filter_app)


# create application profile
app_profile = AppProfile(AppName, tenant)

# create web epg and associate bridge domain and contracts
epg_web = EPG("Web", app_profile)
epg_web.add_bd(bridge_domain)
epg_web.provide(contract_web)
epg_web.consume(contract_application)

# create app epg and associate bridge domain and contracts
epg_web = EPG("App", app_profile)
epg_web.add_bd(bridge_domain)
epg_web.provide(contract_application)
epg_web.consume(contract_database)

# create db epg and associate bridge domain and contract
epg_database = EPG("Database", app_profile)
epg_database.add_bd(bridge_domain)
epg_database.provide(contract_database)

# collect list of tenants
tenant_list = Tenant.get(session)

# print list of tenants
tenant_list
for tn in tenant_list:
    print(tn.name)

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

# re-check tenant list
new_tenant_list = Tenant.get(session)
for tn in new_tenant_list:
    print(tn.name)

#check app list in new tenant
app_list = AppProfile.get(session, tenant)
for app in app_list:
    print(app.name)

# check epg list in new app
epg_list = EPG.get(session, app_profile, tenant)
for epg in epg_list:
    print(epg.name)

# exit
exit()
