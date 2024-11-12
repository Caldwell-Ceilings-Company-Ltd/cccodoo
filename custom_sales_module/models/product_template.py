from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_cost_usd = fields.Monetary(
        string="Cost USD",
        currency_field="currency_id",
        store=True,
        copy=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        default=lambda self: self.env.ref('base.USD').id,
        readonly=True
    )