import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
import ECatInitCmd
from ECatMailbox import ECatMailbox as Mailbox
from ECatDC import ECatDC as DC
from operator import itemgetter, attrgetter


class ECatSlave:
	pass
	
	def __init__(self,xml_slave):
		self.InitCmds = list()
		self.Mailbox = None
		self.DC = None
		
		self.name_in_res = YoUtil.get_xml_node_as_text(xml_slave,'Info/NameInResource')
		self.device_name = YoUtil.get_xml_node_as_text(xml_slave,'Info/Name')
		self.ProductName = YoUtil.get_xml_node_as_text(xml_slave,'Info/ProductName')
		self.vendor_id = YoUtil.get_xml_node_as_int(xml_slave,'Info/VendorId')
		self.productCode = YoUtil.get_xml_node_as_int(xml_slave,'Info/ProductCode')
		self.revisionNo = YoUtil.get_xml_node_as_int(xml_slave,'Info/RevisionNo')
		
		self.ProcessData_Send_BitStart = YoUtil.get_xml_node_as_int(xml_slave,'ProcessData/Send/BitStart')
		self.ProcessData_Send_BitLength = YoUtil.get_xml_node_as_int(xml_slave,'ProcessData/Send/BitLength')
		self.ProcessData_Recv_BitStart = YoUtil.get_xml_node_as_int(xml_slave,'ProcessData/Recv/BitStart')
		self.ProcessData_Recv_BitLength = YoUtil.get_xml_node_as_int(xml_slave,'ProcessData/Recv/BitLength')
		
		self.load_initCmds(xml_slave)
		self.load_mailbox(xml_slave)
		self.load_DC(xml_slave)

	def load_initCmds(self,xml_slave):
		xml_initCmd_list = xml_slave.findall('InitCmds/InitCmd')
		if xml_initCmd_list!=None:
			for xml_initCmd in xml_initCmd_list:
				initcmd = ECatInitCmd.ECatInitCmd(xml_initCmd)
				self.InitCmds.append(initcmd)
		
	def load_mailbox(self,xml_slave):
		xml_mailbox = xml_slave.find('Mailbox')
		if xml_mailbox!=None:
			self.Mailbox = Mailbox(xml_mailbox)
					
		
	def load_DC(self,xml_slave):
		xml_dc = xml_slave.find('DC')
		if xml_dc!=None:
			self.DC = DC(xml_dc)
		
	def tostring(self, type,indent=0):
		ret = ("Slave ('%s','%s', (0x%x,0x%x,0x%x) -> '%s') " % (YoUtil.str_strip(self.name_in_res), YoUtil.str_strip(self.device_name),self.vendor_id,self.productCode,self.revisionNo,YoUtil.str_strip(self.ProductName)))+'\n'
		ret+=YoUtil.get_indent(indent+1)+'ProcessData '
		if self.ProcessData_Send_BitStart!= None:
			ret+= ('Send BitStart=%d, BitLength=%d'% (self.ProcessData_Send_BitStart,self.ProcessData_Send_BitLength))
		if self.ProcessData_Recv_BitStart!= None:
			ret+= (', Recv BitStart=%d, BitLength=%d'% (self.ProcessData_Recv_BitStart,self.ProcessData_Recv_BitLength))
		ret+='\n'
		if self.DC != None:
			ret+= self.DC.tostring(indent+1)
		if self.Mailbox!= None:
			ret+='\n'+self.Mailbox.tostring(indent+1)
		if type >=1:
			ret += ("%sInitCmds count= %d" % (YoUtil.get_indent(indent+1),len(self.InitCmds)))+'\n'
			self.InitCmds=sorted(self.InitCmds,key=attrgetter('Ado'))
			for initCmd in self.InitCmds:
				str = initCmd.tostring(indent+2)
				ret +=(str)
		return ret
		