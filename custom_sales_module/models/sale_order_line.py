from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_studio_cost_fob = fields.Monetary(
        string="Cost FOB",
        currency_field="currency_id",
        compute="_compute_cost_fob",
        store=True
    )

    currency_id = fields.Many2one(
        related='order_id.currency_id',
        store=True,
        readonly=True
    )

    @api.depends('product_id', 'product_id.x_studio_cost_usd')
    def _compute_cost_fob(self):
        for record in self:
            if record.product_id:
                record.x_studio_cost_fob = record.product_id.x_studio_cost_usd

