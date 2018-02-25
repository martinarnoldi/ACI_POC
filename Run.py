TenantName = "ARNO-TENANT01"
AppName = TenantName + "-APP01"
VRFName = TenantName + "-VRF01"
BDName = TenantName + "-BD01"
Subnet01Name = TenantName + "-Subnet01"

try:
    from credentials import *
    import GetACIObject
    from acitoolkit.acitoolkit import *


    tenant_list = GetACIObject.aciobjectexcists(Tenant)
    print(tenant_list)
    if not tenant_list:
        print("NOASD")

    # create session with apic
    session = Session(URL, LOGIN, PASSWORD)
    session.login()

    tenant = AttEntityP("ARNO-AEP")

    # push configuration to apic
    resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json()) 
    #if len(tenant_list) == 0:
    #    print("AASD")


#    for tn in tenant_list:
#        print(tn.name)
#        if tn == TenantName:
#            print("TRUE")

except: 
    print("-------------------------")
    raise