from semantic_kernel.functions import kernel_function


class IncidentCreation:
    @kernel_function(
        name="incident_creation", description="Create an IT support incident with the specified impact, category, and issue"
    )
    def incident_creation(self, staff_id,impact,category, issue: str) -> str:
        return f"IT support ticket created for issue: {issue}."
