
    x_studio_cost_usd = fields.Monetary(
        string="Cost USD",
        currency_field="currency_id",
        store=True,
        copy=True
    )