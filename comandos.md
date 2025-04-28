enable

config

interface gpon 0/1 

display ont info 1 all

                                         (host='10.55.160.2', 
                                          username='smartolt', 
                                          password='rJXf2JA1p4NjTui', 
                                          chassi_placa=b'0/9', 
                                          porta='1'))
=============================================================================================
enable

config

interface gpon  #subrack#/#slot#

ont add #pon#  sn-auth #onu_mac# omci ont-lineprofile-id 900 ont-srvprofile-id 900 desc #nome#

ont port native-vlan #pon# #onu_numero# eth 1 vlan 900 priority 0

quit

service-port vlan #vlan# gpon #pon_id# ont #onu_numero# gemport 900 multi-service user-vlan 900 tag-transform translate