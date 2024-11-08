from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.ref('base.USD').id
    )
    
    exchange_rate_usd_eur = fields.Float(
        string="USD/EUR Exchange",
        help="Exchange rate from USD to EUR",
        default=0.93
    )

    number_of_containers = fields.Integer(
    string="Number of Containers",
    default=1
    )

    
    vessel_route = fields.Selection(
        [
            ('mersin_algeciras_40hc', 'Mersin - Algeciras (40\'HC)'),
            ('mersin_barcelona_40hc', 'Mersin - Barcelona (40\'HC)'),
            ('mersin_casablanca_40hc', 'Mersin - Casablanca (40\'HC)'),
            ('mersin_leixoes_40hc', 'Mersin - Leixoes (40\'HC)'),
            ('mersin_valencia_40hc', 'Mersin - Valencia (40\'HC)'),
            ('qingdao_algeciras_20dc', 'Qingdao - Algeciras (20\'DC)'),
            ('shanghai_algeciras_20dc', 'Shanghai - Algeciras (20\'DC)'),
            ('xingang_algeciras_40hc', 'Xingang - Algeciras (40\'HC)'),
            ('qingdao_barcelona_20dc', 'Qingdao - Barcelona (20\'DC)'),
            ('qingdao_valencia_20dc', 'Qingdao - Valencia (20\'DC)'),
            ('shanghai_barcelona_20dc', 'Shanghai - Barcelona (20\'DC)'),
            ('shanghai_leixoes_20dc', 'Shanghai - Leixoes (20\'DC)'),
            ('shanghai_valencia_20dc', 'Shanghai - Valencia (20\'DC)'),
            ('xingang_barcelona_40hc', 'Xingang - Barcelona (40\'HC)'),
            ('xingang_valencia_40hc', 'Xingang - Valencia (40\'HC)')
        ],
        string="Vessel Route",
        help="Select the route of the vessel."
    )

    freight_cost = fields.Float(
        string="Freight Cost",
        compute="_compute_freight_cost",
        store=True
    )

    warning_message = fields.Char(
        string="Freight Warning",
        compute="_compute_freight_cost",
        store=True
    )

    @api.depends('vessel_route', 'exchange_rate_usd_eur', 'number_of_containers')
    def _compute_freight_cost(self):
        for record in self:
            freight_cost = 1.0
            route = record.vessel_route
            exchange_rate = record.exchange_rate_usd_eur or 1.0
            num_contenedores = record.number_of_containers or 1.0
            warning_message = ""
            
            if route == 'mersin_algeciras_40hc':
                freight_cost = 990.0 * exchange_rate
            elif route == 'mersin_barcelona_40hc':
                freight_cost = 900.0 * exchange_rate
            elif route == 'mersin_casablanca_40hc':
                freight_cost = 950.0
            elif route == 'mersin_leixoes_40hc':
                freight_cost = 995.0 * exchange_rate
            elif route == 'mersin_valencia_40hc':
                freight_cost = 900.0 * exchange_rate
            elif route in ['qingdao_algeciras_20dc', 'shanghai_algeciras_20dc', 'xingang_algeciras_40hc']:
                freight_cost = 1111111111111111.11
                warning_message = "*FREIGHT ERROR!*"
            elif route == 'qingdao_barcelona_20dc':
                freight_cost = 2490.0
            elif route == 'qingdao_valencia_20dc':
                freight_cost = 2490.0
            elif route == 'shanghai_barcelona_20dc':
                freight_cost = 3100.0
            elif route == 'shanghai_leixoes_20dc':
                freight_cost = 3100.0
            elif route == 'shanghai_valencia_20dc':
                freight_cost = 3100.0
            elif route == 'xingang_barcelona_40hc':
                freight_cost = 4500.0
            elif route == 'xingang_valencia_40hc':
                freight_cost = 4500.0
    
            # Calcular el costo total del flete basado en el número de contenedores
            total_freight_cost = freight_cost * num_contenedores
    
            # Asegurarse de que el valor no sea cero antes de asignarlo
            if total_freight_cost == 0:
                total_freight_cost = 1.0  # Valor de seguridad o manejo alternativo
            
            record.freight_cost = total_freight_cost
            record.warning_message = warning_message if warning_message else ""
 

    
    number_of_shipments = fields.Integer(
            string="Number of Shipments",
            default=1
    )

    bl_cost = fields.Monetary(
        string="BL Cost",
        compute="_compute_bl_cost",
        store=True,
        currency_field="currency_id"
    )
    @api.depends('exchange_rate_usd_eur', 'number_of_shipments')
    def _compute_bl_cost(self):
        for record in self:
            # Usamos un tipo de cambio predeterminado de 1 si `exchange_rate_usd_eur` está vacío
            exchange_rate = record.exchange_rate_usd_eur or 1.0  
            # Aseguramos que `number_of_shipments` tiene un valor mínimo de 1
            num_shipments = record.number_of_shipments or 1  
            # Calculamos `bl_cost` en USD
            record.bl_cost = 75.0 * exchange_rate * num_shipments


    custom_clearance = fields.Monetary(
        string="Custom Clearance",
        compute="_compute_custom_clearance",
        store=True,
        currency_field="currency_id"
    )

    @api.depends('number_of_shipments', 'exchange_rate_usd_eur')
    def _compute_custom_clearance(self):
        for record in self:
            exchange_rate = record.exchange_rate_usd_eur or 1.0  # Si no hay tipo de cambio, usa 1.0
            num_shipments = record.number_of_shipments or 1  # Si no hay envíos, usa 1
            record.custom_clearance = 90.0 * exchange_rate * num_shipments  # Calcula el clearance en USD

    
    commission = fields.Monetary(
        string="Commission",
        currency_field="currency_id"
    )

    bank_charge = fields.Monetary(
        string="Bank Charge",
        currency_field="currency_id",
        default=100.0
    )

    @api.depends('number_of_shipments')
    def _compute_bank_charge(self):
        for record in self:
            # Aseguramos que `number_of_shipments` tiene un valor mínimo de 1
            num_shipments = record.number_of_shipments or 1  
            # Calculamos `bank_charge` multiplicando el costo fijo por el número de envíos
            record.bank_charge = 100.0 * num_shipments
            
    palletization_cost = fields.Monetary(
        string="Palletization Cost",
        currency_field="currency_id",
        default=0.0
    )

    fob_cost = fields.Monetary(
        string="Total FOB Cost",
        compute="_compute_fob_cost",
        store=True,
        currency_field="currency_id"
    )
    
    @api.depends('order_line.x_studio_cost_fob', 'order_line.product_uom_qty', 'exchange_rate_usd_eur')
    def _compute_fob_cost(self):
        for record in self:
            total_fob_cost = 0.0
            for line in record.order_line:
                # Multiplicamos el costo FOB por la cantidad en la línea y luego convertimos a USD si es necesario
                total_fob_cost += line.x_studio_cost_fob * line.product_uom_qty
            
            # Asigna el valor total al campo 'fob_cost' en el modelo de la orden
            record.fob_cost = total_fob_cost
            
    costo_total = fields.Monetary(
        string="Total Cost",
        currency_field="currency_id",
        compute="_compute_total_cost",
        store=True,
        readonly=True
    )

    @api.depends('fob_cost', 'freight_cost', 'bl_cost', 'custom_clearance', 
                 'bank_charge', 'commission', 'palletization_cost')
    def _compute_total_cost(self):
        for record in self:
            total_cost = (record.fob_cost or 0.0) + (record.freight_cost or 0.0) + \
                         (record.bl_cost or 0.0) + (record.custom_clearance or 0.0) + \
                         (record.bank_charge or 0.0) + (record.commission or 0.0) + \
                         (record.palletization_cost or 0.0)
            record.costo_total = total_cost
            
    x_margen = fields.Float(
        string="Invoice Margin %",
        compute="_compute_margin",
        store=True,
        readonly=True
    )

    @api.depends('amount_total', 'costo_total')
    def _compute_margin(self):
        for record in self:
            if record.amount_total:
                record.x_margen = ((record.amount_total - record.costo_total) / record.amount_total) * 100
            else:
                record.x_margen = 0.0