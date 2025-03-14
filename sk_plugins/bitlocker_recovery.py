from semantic_kernel.functions import kernel_function

class BitLockerRecovery:
    @kernel_function(
        name="bitlocker_recovery",
        description="Retrieve a BitLocker recovery key for a device"
    )
    def bitlocker_recovery(self, device_id ,staff_id: str) -> str:
        """Retrieve a BitLocker recovery key for a device."""
        
        return f"BitLocker recovery key for device {device_id} is ABCD-1234-EFGH-5678."