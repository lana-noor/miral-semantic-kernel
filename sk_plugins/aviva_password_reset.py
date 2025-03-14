from semantic_kernel.functions import kernel_function


class AvivaPasswordReset:
    @kernel_function(
        name="aviva_password_reset", description="Reset Aviva password for a user"
    )
    def aviva_password_reset(self, staff_id:str) -> str:
        return f"Aviva password reset for {staff_id} was successful. Check your email for details."
