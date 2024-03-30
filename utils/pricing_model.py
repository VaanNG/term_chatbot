class PricingModel:
    def __init__(self):
        self.pricing_data = {
            "haiku": {"input": 0.25, "output": 1.25},
            "sonnet": {"input": 3.0, "output": 15.0},
            "opus": {"input": 15.0, "output": 75.0}
        }

    def get_token_cost(self, model, input_tokens, output_tokens):
        pricing = self.pricing_data.get(model.lower(), None)
        if pricing is None:
            return None

        input_cost = pricing["input"] * input_tokens / 1_000_000
        output_cost = pricing["output"] * output_tokens / 1_000_000
        total_cost = input_cost + output_cost

        return total_cost
