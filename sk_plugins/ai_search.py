from semantic_kernel.functions import kernel_function


class AiSearch:
    @kernel_function(
        name="ai_search", description=""
    )
    def ai_search(self, staff_id: str) -> str:
        return f""