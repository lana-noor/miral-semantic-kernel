from semantic_kernel.functions import kernel_function


class GenericPasswordReset:
    @kernel_function(
        name="generic_password_reset", description="Reset a generic password for a user"
    )
    def generic_password_reset(self, staff_id: str) -> str:
        return f"Generic password reset for {staff_id} was successful."
