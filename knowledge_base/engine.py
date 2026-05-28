class Rule:
    def __init__(self, name, condition, action, explanation, priority=1, cf=1.0):
        self.name = name
        self.condition = condition  # Lambda evaluating to True/False
        self.action = action  # Lambda updating the facts dictionary
        self.explanation = explanation  # For the 10% Explanation Capability grade
        self.priority = priority  # Higher numbers evaluate first for conflict resolution
        self.cf = cf
        self.fired = False  # Prevents infinite loops


class PCBuilderExpertSystem:
    def __init__(self):
        self.facts = {}
        self.rules = []
        self.explanations = []

    def add_fact(self, key, value):
        self.facts[key] = value

    def add_rule(self, rule):
        self.rules.append(rule)

    def run_inference(self):
        """
        Forward chaining engine. Loops through rules until no new facts are deduced.
        """
        new_fact_added = True

        while new_fact_added:
            new_fact_added = False
            # Sort by priority: Evaluates conflict overrides before standard mapping
            self.rules.sort(key=lambda r: r.priority, reverse=True)

            for rule in self.rules:
                if not rule.fired and rule.condition(self.facts):
                    rule.action(self.facts)
                    rule.fired = True
                    new_fact_added = True
                    self.explanations.append(f"[{rule.name}] (CF: {rule.cf}) {rule.explanation}")

                    # If a high-priority conflict rule fires, reset to re-evaluate new constraints
                    break

    def get_results(self):
        """Filters out raw inputs and returns hardware and explanations for the web UI."""
        hidden_keys = ["Budget", "Target_Resolution", "Preference", "Tier", "Conflict", "Adjust_Resolution",
                       "Adjust_CPU", "Total_System_TDP"]
        hardware = {k: v for k, v in self.facts.items() if k not in hidden_keys}
        return hardware, self.explanations