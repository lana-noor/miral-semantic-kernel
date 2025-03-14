from semantic_kernel.functions import kernel_function


class IncidentCreation:
    @kernel_function(
        name="incident_creation", description="Create an IT support incident"
    )
    def incident_creation(self, staff_id, issue: str) -> str:
        return f"IT support ticket created for issue: {issue}."
