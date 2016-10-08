"""
    Python library for SolusVM's XMLRPC API

        https://documentation.solusvm.com/display/DOCS/API

    @thanks : https://github.com/bensnyde/py-solusvm-api
    @author : zhangnq
    @website : http://www.sijitao.net/
"""
import requests

class SolusVMAdmin:
    def __init__(self, base_url, api_id, api_key):
        """SolusVM JSON API Library constructor.

        Parameters
            base_url: SolusVM base_url
            api_id: SolusVM API authentiction ID hash
            api_key: SolusVM API authentication key hash
        Returns
            None
        """
        self.base_url = base_url
        self.id = api_id
        self.key = api_key

    def _sQuery(self, kwargs):
        """Queries specified SolusVM API with specified query string.

        Parameters
            kwargs: dictionary GET vars
        Returns
            json
        """
        kwargs.update({
                'rdtype':'json',
                'id':self.id,
                'key':self.key
        })

        response = requests.get(self.base_url+'api/admin/command.php', params=kwargs, timeout=2)
        return response.json()

    def listVirtualServers(self, nodeid):
        """Lists virtual servers allocated on specified node.

            https://documentation.solusvm.com/display/DOCS/List+Virtual+Servers

        Parameters
            nodeid: id of node
        Returns
            json
        """
        return self._sQuery({
            'action': 'node-virtualservers',
            'nodeid': nodeid
        })

    def diablePXE(self, vserverid):
        """Disables PXE on specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Disable+PXE

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-network-disable',
            'vserverid': vserverid
        })

    def enablePXE(self, vserverid):
        """Enables PXE on specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Enable+PXE

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-network-enable',
            'vserverid': vserverid
        })

    def enableTUN(self, vserverid):
        """Enables TUN/TAP on specified virtual server.

            https://documentation.solusvm.com/pages/viewpage.action?pageId=558498

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-tun-enable',
            'vserverid': vserverid
        })

    def disableTUN(self, vserverid):
        """Disables TUN/TAP on specified virtual server.

            https://documentation.solusvm.com/pages/viewpage.action?pageId=558494

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-tun-disable',
            'vserverid': vserverid
        })

    def togglePAE(self, vserverid, pae):
        """Toggles PAE for specified virtual server.

            https://documentation.solusvm.com/pages/viewpage.action?pageId=558505

        Parameters
            vserverid: id of virtual server
            pae: on|off
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-pae',
            'vserverid': vserverid,
            'pae':pae
        })

    def shutdownVirtualServer(self, vserverid):
        """Shuts down specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Shutdown+Virtual+Server

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-shutdown',
            'vserverid': vserverid
        })

    def terminateVirtualServer(self, vserverid, deleteclient=False):
        """Deletes specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Terminate+Virtual+Server

        Parameters
            vserverid: id of virtual server
            deleteclient: whether or not to delete client too
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-terminate',
            'vserverid': vserverid,
            'deleteclient': deleteclient
        })

    def changeVNCPassword(self, vserverid, vncpassword):
        """Updates VNC password for specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Change+VNC+Password

        Parameters
            vserverid: id of virtual server
            vncpassword: new password
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-vncpass',
            'vserverid': vserverid,
            'vncpassword': vncpassword
        })

    def vncInfo(self, vserverid):
        """Retrieves VNC information for specified virtual server.

            https://documentation.solusvm.com/display/DOCS/VNC+Info

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-vnc',
            'vserverid': vserverid
        })

    def suspendVirtualServer(self, vserverid):
        """Suspends specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Suspend+Virtual+Server

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-suspend',
            'vserverid':vserverid
        })

    def unsuspendVirtualServer(self, vserverid):
        """Unsuspends specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Unsuspend+Virtual+Server

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-unsuspend',
            'vserverid': vserverid
        })

    def virtualServerStatus(self, vserverid):
        """Retrieves status of specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Virtual+Server+Status

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-status',
            'vserverid': vserverid
        })

    def changeRootPassword(self, vserverid, rootpassword):
        """Retrieves status of specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Change+Root+Password

        Parameters
            vserverid: id of virtual server
            rootpassword: new root password
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-rootpassword',
            'vserverid': vserverid,
            'rootpassword': rootpassword
        })

    def rebuildVirtualServer(self, vserverid, template):
        """Rebuilds specified virtual server with specified template.

            https://documentation.solusvm.com/display/DOCS/Rebuild+Virtual+Server

        Parameters
            vserverid: id of virtual server
            template: template filename without extension
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-rebuild',
            'vserverid': vserverid,
            'template': template
        })

    def changeHostname(self, vserverid, hostname):
        """Updates specified virtual server's hostname.

            https://documentation.solusvm.com/display/DOCS/Change+Hostname

        Parameters
            vserverid: id of virtual server
            hostname: new hostname
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-hostname',
            'vserverid': vserverid,
            'hostname': hostname
        })

    def rebootVirtualServer(self, vserverid):
        """Reboots specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Reboot+Virtual+Server

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-reboot',
            'vserverid': vserverid
        })

    def unmountISO(self, vserverid):
        """Unmounts ISO from specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Unmount+ISO

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-unmountiso',
            'vserverid': vserverid
        })

    def mountISO(self, vserverid, iso):
        """Mounts specified ISO to specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Mount+ISO

        Parameters
            vserverid: id of virtual server
            iso: filename of iso
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-mountiso',
            'vserverid': vserverid,
            'iso': iso
        })

    def checkVirtualServerExists(self, vserverid):
        """Checks if specified virtual server exists.

            https://documentation.solusvm.com/display/DOCS/Check+Exists

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-checkexists',
            'vserverid': vserverid
        })

    def virtualServerState(self, vserverid, nostatus=False, nographs=False):
        """Retrieves information about specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Virtual+Server+State

        Parameters
            vserverid: id of virtual server
            nostatus: whether or not to retrieve status
            nographs: whether or not to generate graphs
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-infoall',
            'vserverid': vserverid,
            'nostatus': nostatus,
            'nographs': nographs
        })

    def virtualServerInfo(self, vserverid):
        """Retrieves information about specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Virtual+Server+Information

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-info',
            'vserverid': vserverid
        })

    def deleteIPAddress(self, vserverid, ipaddr):
        """Removes specified IP Address from specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Delete+IP+Address

        Parameters
            vserverid: id of virtual server
            ipaddr: ip address
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-delip',
            'vserverid': vserverid,
            'ipaddr': ipaddr
        })

    def toggleSerialConsole(self, vserverid, access=None, time=None):
        """Retrieves, enables or disables serial console for specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Serial+Console

        Parameters
            vserverid: id of virtual server
            access: enable|disable
            time: 1|2|3|4|5|6|7|8
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-console',
            'vserverid': vserverid,
            'time': time,
            'access': access
        })

    def changePlan(self, vserverid, plan):
        """Changes specified virtual server's plan.

            https://documentation.solusvm.com/display/DOCS/Change+Plan

        Parameters
            vserverid: id of virtual server
            plan: new plan name
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-change',
            'vserverid': vserverid,
            'plan':plan
        })

    def changeOwner(self, vserverid, clientid):
        """Changes specified virtual server's owner.

            https://documentation.solusvm.com/display/DOCS/Change+Owner

        Parameters
            vserverid: id of virtual server
            clientid: new clients id
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-changeowner',
            'vserverid': vserverid,
            'clientid': clientid
        })

    def changeBootOrder(self, vserverid, bootorder):
        """Changes specified virtual server's boot order.

            https://documentation.solusvm.com/display/DOCS/Change+Boot+Order

        Parameters
            vserverid: id of virtual server
            bootorder: cd|dc|c|d (c=CDROM, d=HDD)
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-bootorder',
            'vserverid': vserverid,
            'bootorder': bootorder
        })


    def changeBandwidthLimits(self, vserverid, limit, overlimit):
        """Changes specified virtual server's bandwidth limits.

            https://documentation.solusvm.com/display/DOCS/Change+Bandwidth+Limits

        Parameters
            vserverid: id of virtual server
            limit: bandwidth limit in Gb
            overlimit: bandwidth overlimit in Gb
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-bandwidth',
            'vserverid': vserverid,
            'limit': limit,
            'overlimit': overlimit
        })

    def changeMemory(self, vserverid, memory):
        """Changes specified virtual server's allocated memory.

            https://documentation.solusvm.com/display/DOCS/Change+Memory

        Parameters
            vserverid: id of virtual server
            memory: amount in Mb
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-change-memory',
            'vserverid': vserverid,
            'memory': memory
        })

    def changeCPU(self, vserverid, cpu):
        """Changes specified virtual server's number of CPU cores.

            https://documentation.solusvm.com/display/DOCS/Change+CPU

        Parameters
            vserverid: id of virtual server
            cpu: number of cpu cores [1-128]
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-change-cpu',
            'vserverid': vserverid,
            'cpu': cpu,
        })

    def changeHDD(self, vserverid, hdd):
        """Changes specified virtual server's hard disk size.

            https://documentation.solusvm.com/display/DOCS/Change+Hard+Disk+Size

        Parameters
            vserverid: id of virtual server
            hdd: hard disk size in Gb
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-change-hdd',
            'vserverid': vserverid,
            'hdd': hdd,
        })


    def addIPAddress(self, vserverid):
        """Adds an IP address to specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Add+IP+Address

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-addip',
            'vserverid': vserverid
        })

    def bootVirtualServer(self, vserverid):
        """Boots specified virtual server.

            https://documentation.solusvm.com/display/DOCS/Boot+Virtual+Server

        Parameters
            vserverid: id of virtual server
        Returns
            json
        """
        return self._sQuery({
            'action': 'vserver-boot',
            'vserverid': vserverid
        })

    def createVirtualServer(self, kwargs):
        """Creates virtual server.

            https://documentation.solusvm.com/display/DOCS/Create+Virtual+Server

        Parameters
            data: dictionary parameter pairs
        Returns
            json
        """
        kwargs['action'] = 'vserver-create'
        return self._sQuery(kwargs)

    def listNodesById(self, vtype='kvm'):
        """Lists Nodes by their ID.

            https://documentation.solusvm.com/display/DOCS/List+Nodes+by+ID

        Parameters
            vtype: openvz|xen|xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'node-idlist',
            'type': vtype
        })

    def listNodesByName(self, vtype='kvm'):
        """List nodes by name.

            https://documentation.solusvm.com/display/DOCS/List+Nodes+by+Name

        Parameters
            vtype: openvz|xen|xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'listnodes',
            'type': vtype
        })

    def listISO(self, vtype='kvm'):
        """Lists available ISO images.

            https://documentation.solusvm.com/display/DOCS/List+ISO+Images

        Parameters
            vtype: xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'listiso',
            'type': vtype
        })

    def listNodeGroups(self, vtype='kvm'):
        """List node groups.

            https://documentation.solusvm.com/display/DOCS/List+Node+Groups

        Parameters
            vtype: xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'listnodegroups',
            'type': vtype
        })

    def listNodesIPAddresses(self, nodeid):
        """List all IP addresses for a node.

            https://documentation.solusvm.com/display/DOCS/List+All+IP+Addresses+for+a+Node

        Parameters
            nodeid: id of node
        Returns
            json
        """
        return self._sQuery({
            'action': 'node-iplist',
            'nodeid': nodeid
        })

    def listPlans(self, vtype='kvm'):
        """List plans.

            https://documentation.solusvm.com/display/DOCS/List+Plans

        Parameters
            vtype: openvz|xen|xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'listplans',
            'type': vtype
        })

    def listTemplates(self, vtype='kvm'):
        """List templates.

            https://documentation.solusvm.com/display/DOCS/List+Templates

        Parameters
            vtype: openvz|xen|xen hvm|kvm
        Returns
            json
        """
        return self._sQuery({
            'action': 'listtemplates',
            'type': vtype
        })

    def xenNodeResources(self, nodeid):
        """Retrieve resource count from specified xen node.

            https://documentation.solusvm.com/display/DOCS/Xen+Node+Resources

        Parameters
            nodeid: id of node
        Returns
            json
        """
        return self._sQuery({
            'action': 'node-xenresources',
            'nodeid': nodeid
        })

    def nodeStatistics(self, nodeid):
        """Retrieve statistics for specified node.

            https://documentation.solusvm.com/display/DOCS/Node+Statistics

        Parameters
            nodeid: id of node
        Returns
            json
        """
        return self._sQuery({
            'action': 'node-statistics',
            'nodeid': nodeid
        })

    def clientAuthenticate(self, username, password):
        """Authenticates specified username and password.

            https://documentation.solusvm.com/display/DOCS/Client+Authenticate

        Parameters
            username:
            password:
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-authenticate',
            'username': username,
            'password': password
        })

    def clientExists(self, username):
        """Checks to see if the specified client exists.

            https://documentation.solusvm.com/display/DOCS/Check+if+Client+Exists


        Parameters
            username:
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-checkexists',
            'username': username
        })

    def createClient(self, username, password, email, firstname, lastname, company):
        """Creates a client.

            https://documentation.solusvm.com/pages/viewpage.action?pageId=558430

        Parameters
            username:
            password:
            email:
            firstname:
            lastname:
            company:
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-create',
            'username': username,
            'password': password,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'company': company
        })

    def changeClientPassword(self, username, password):
        """Updates the specified client's password.

            https://documentation.solusvm.com/display/DOCS/Change+Client+Password

        Parameters
            username:
            password:
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-updatepassword',
            'username': username,
            'password': password
        })

    def changeClientUsername(self, username, newusername):
        """Updates the specified client's password.

            https://documentation.solusvm.com/display/DOCS/Change+Client+Username

        Parameters
            username: old username
            newusername: new username
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-change-username',
            'username': username,
            'newusername': newusername
        })

    def listClients(self):
        """Lists all clients.

            https://documentation.solusvm.com/display/DOCS/List+Clients

        Parameters
            None
        Returns
            json
        """
        return self._sQuery({
            'action':'client-list'
        })

    def deleteClient(self, username):
        """Deletes specified client.

            https://documentation.solusvm.com/display/DOCS/Delete+Client

        Parameters
            username:
        Returns
            json
        """
        return self._sQuery({
            'action': 'client-delete',
            'username': username
        })

    def editClient(self, username, kwargs):
        """Edits specified client.

            https://documentation.solusvm.com/display/DOCS/Edit+Client

        Parameters
            username:
            *firsntame
            *lastname
            *company
            *email
        Returns
            json
        """
        kwargs['action'] = 'client-edit'
        kwargs['username'] = username
        return self._sQuery(kwargs)

    def deleteReseller(self, username):
        """Deletes specified reseller.

            https://documentation.solusvm.com/display/DOCS/Delete+Reseller

        Parameters
            username:
        Returns
            json
        """
        return self._sQuery({
            'action': 'reseller-delete',
            'username': username
        })

    def resellerInfo(self, username):
        """Retrieves details of specified reseller.

            https://documentation.solusvm.com/display/DOCS/Reseller+Information

        Parameters
            username:
        Returns
            json
        """
        return self._sQuery({
            'action': 'reseller-info',
            'username': username
        })

    def listResellers(self):
        """Lists all resellers.

            https://documentation.solusvm.com/display/DOCS/List+Resellers

        Parameters
            None
        Returns
            json
        """
        return self._sQuery({
            'action':'reseller-list'
        })

    def createReseller(self, kwargs):
        """Creates reseller.

            https://documentation.solusvm.com/display/DOCS/Create+Reseller

        Parameters
            data: dictionary key/value pairs
        Returns
            json
        """
        kwargs['action'] = 'reseller-create'
        return self._sQuery(kwargs)

    def modifyResellerResources(self, username, kwargs):
        """Modifies reseller's available resources.

            https://documentation.solusvm.com/display/DOCS/Modify+Reseller+Resources

        Parameters
            username:
            data: dictionary key/value pairs
        Returns
            json
        """
        kwargs['action'] = 'reseller-modifyresources'
        kwargs['username'] = username
        return self._sQuery(kwargs)

class SolusVMClient:
    def __init__(self, base_url, api_key, api_hash):
        self.base_url = base_url
        self.key = api_key
        self.hash = api_hash
    
    def _sQuery(self, kwargs):
        kwargs.update({
                'rdtype':'json',
                'hash':self.hash,
                'key':self.key
        })

        response = requests.get(self.base_url+'api/client/command.php', params=kwargs, timeout=2)
        return response

    def serverStatus(self):
        return self._sQuery({
            'action': 'status'
        })
