from semantic_kernel.functions import kernel_function

class StaffIDVerification:
    @kernel_function(name="staff_id_verification", description="Verify Staff ID for a user")
    def staff_id_verification(self,user_name: str) -> str:
        """Always executed first to verify the user's Staff ID."""
        staff_id_database = {
            "John Doe": "JD12345",
            "Alice Smith": "AS67890",
            "Bob Johnson": "BJ11223"
        }
        
        return staff_id_database.get(user_name, "Staff ID not found")
    