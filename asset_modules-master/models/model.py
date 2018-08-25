from odoo import models, fields, api


class asset_asset(models.Model):
	_inherit = "asset.asset"

	parameter_ids=fields.One2many('asset.parameter', 'asset_parameter_id', string='Parameters')
	other_parameter_ids=fields.One2many('asset.parameter', 'asset_parameter_id', string='Parameters', compute="_get_component_parameters")
	asset_group_ids=fields.One2many('asset.group', 'main_asset_id', string='Assets')
	asset_image=fields.Binary(string="Construction image")
	button_one=fields.Char(compute="_get_component_parameters",default=u"")
	button_two=fields.Char(compute="_get_component_parameters",default=u"")
	button_three=fields.Char(compute="_get_component_parameters",default=u"")
	button_four=fields.Char(compute="_get_component_parameters",default=u"")
	button_five=fields.Char(compute="_get_component_parameters",default=u"")
	button_six=fields.Char(compute="_get_component_parameters",default=u"")
	
	@api.one
	def _get_component_parameters(self):
		all_params = self.env['asset.parameter']
		required_params=[]
		for i in self.asset_group_ids:
			required_params.extend(i.child_asset_id.parameter_ids.filtered(lambda parameter_ids: parameter_ids.is_required==True).ids)
		self.other_parameter_ids = all_params.search([('id','in',required_params)])
		#button functional
		mybuttons=["", "", "", "", "", ""]
		for x in range(len(self.other_parameter_ids)):
			mybuttons[x]=self.other_parameter_ids[x].value+u" "+self.other_parameter_ids[x].mkey.name
			if x>=5:
				break
		self.button_one=mybuttons[0]
		self.button_two=mybuttons[1]
		self.button_three=mybuttons[2]
		self.button_four=mybuttons[3]
		self.button_five=mybuttons[4]
		self.button_six=mybuttons[5]

	@api.one
	def button_asset_to_product(self):
		product = self.env['product.template']
		child_assets=["NONE"]
		child_assets[0]=self.name
		for i in self.asset_group_ids:
			child_assets.append(i.child_asset_id.name)
		child_assets=list(child_assets)
		new_product = False
		if len(child_assets)>1:
			bom=self.env['mrp.bom']
			bom_line=self.env['mrp.bom.line']
			product_product=self.env['product.product']
			new_bom_line=False
			created_products=[]
			created_bom_line=[]
			product_id=False
			new_bom=False
			for i in child_assets:
				new_product=product.create({'name': i,'type':'product'})
				created_products.append(new_product)
				
			print 'bom line'
			new_bom=bom.create({'product_tmpl_id': created_products[0].id})
			for j in created_products[1:]:
				print j
				product_id=product_product.search([('id','=',j.id)])
				print product_id
				new_bom_line=bom_line.create({'product_id': product_id.id, 'bom_id': new_bom.id})


		else:
			new_product=product.create({'name': self.name})
		print "PRODUCT CREATED"
		
class asset_group(models.Model):
	_name = 'asset.group'

	main_asset_id = fields.Many2one('asset.asset',required=True, auto_join=True, index=True)    
	child_asset_id = fields.Many2one('asset.asset', required=True, auto_join=True, index=True)


class asset_parameter(models.Model):
	_name = 'asset.parameter'

	asset_parameter_id=fields.Many2one("asset.asset")
	parameter_name = fields.Many2one('parameter.type', "Parameter type", required=True, auto_join=True, index=True)
	value = fields.Char(string='Value', default=u".")
	mkey = fields.Many2one('asset.mkey', "Unit of measure")
	is_required = fields.Boolean("Required", default=False)
	

class parameter_type(models.Model):
	_name = 'parameter.type'
	#MKEY SYUDA
	name = fields.Char(string="Parameter type", required=True, default=u".")


class mkey_record(models.Model):
	_name = "asset.mkey"

	name = fields.Char(string='Unit of measure', required=True, default=u".")
	code = fields.Char(string='MKEI Code', required=False)