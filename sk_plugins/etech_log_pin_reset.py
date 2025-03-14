from semantic_kernel.functions import kernel_function

class EtchLogPinReset:
    @kernel_function(name="etech_log_pin_reset", description="Reset Etech Log PIN for a user")
    def etech_log_pin_reset(self,staff_id: str) -> str:
        return f"Etech Log PIN reset for {staff_id} was successful."