class PricingModel:
    def __init__(self):
        self.pricing_data = {
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
            "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
            "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
            "gpt-4": {"input": 30.0, "output": 60.0},
            "gpt-4-turbo-preview": {"input": 10.0, "output": 30.0}
        }

    def get_token_cost(self, model, input_tokens, output_tokens):
        pricing = self.pricing_data.get(model.lower(), None)
        if pricing is None:
            return None

        input_cost = pricing["input"] * input_tokens / 1_000_000
        output_cost = pricing["output"] * output_tokens / 1_000_000
        total_cost = input_cost + output_cost

        return total_cost
