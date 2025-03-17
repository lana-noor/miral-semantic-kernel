import os
import json
import uuid
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from sk_plugins.bitlocker_recovery import BitLockerRecovery
from sk_plugins.aviva_password_reset import AvivaPasswordReset
from sk_plugins.generic_password_reset import GenericPasswordReset
from sk_plugins.etech_log_pin_reset import EtchLogPinReset
from sk_plugins.incident_creation import IncidentCreation
from sk_plugins.ai_search import AiSearch
from sk_plugins.staff_id_verification import StaffIDVerification

from azure.cosmos import CosmosClient

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")


async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion
    chat_completion = AzureChatCompletion(
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
        api_key=AZURE_OPENAI_API_KEY,
        base_url=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )
    kernel.add_service(chat_completion)

    # Add a plugin
    kernel.add_plugin(
        BitLockerRecovery(),
        plugin_name="bitlocker_recovery",
    )
    kernel.add_plugin(
        AvivaPasswordReset(),
        plugin_name="aviva_password_reset",
    )
    kernel.add_plugin(
        GenericPasswordReset(),
        plugin_name="generic_password_reset",
    )
    kernel.add_plugin(
        IncidentCreation(),
        plugin_name="incident_creation",
    )
    kernel.add_plugin(
        EtchLogPinReset(),
        plugin_name="etech_log_pin_reset",
    )
    kernel.add_plugin(
        AiSearch(),
        plugin_name="ai_search",
    )
    kernel.add_plugin(
        StaffIDVerification(),
        plugin_name="staff_id_verification",
    )
    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    prompt = """
You are an AI Assistant for the Emirates internal team, designed to provide insights and automate specific tasks and workflows. Your responsibilities include IT support, configuring Outlook, managing shared mailboxes, and facilitating password resets.
You have access to Emirates Knowledge Base articles via Azure AI Search to retrieve relevant information on configuring Outlook, accessing shared mailboxes, and troubleshooting email-related issues. When a user requests assistance with these topics, invoke the SearchAISearch function to provide them with detailed and relevant information.
If a user requests a specific action, invoke the appropriate function to perform the task.
Before invoking a function, you need to retrieve the staff id, call {{staff_id_verification $input}}. 
Guidelines for Function Invocation
 • Azure AI Search: Call {{ai_search $input}} if the user asks about Outlook configuration, shared mailboxes, or troubleshooting email-related issues, use this function to search the Emirates Knowledge Base for relevant guidance.
 • BitlockerRecoverKey: Call {{bitlocker_recovery $input}} if the user requests a BitLocker recovery key, ask for their PC number if not provided. Ensure it starts with PC, NB, or TB, then invoke this function to retrieve the key.
 • AvivaPasswordReset: Call {{bitlocker_recovery $input}} if the user requests an Aviva password reset or mentions their password is not working, invoke this function to initiate the reset.
 • ETechLogPinReset: Call {{etech_log_pin_reset $input}} if the user requests a PIN reset for the ETechLog application, use this function to generate a new PIN.
 • GenericPasswordReset: Call {{generic_password_reset $input}} if the user requests a password reset but does not specify the type, ask for clarification. 
  ○ If they need an application password reset, retrieve relevant instructions from the Emirates Knowledge Base.
  ○ If they need a network password reset, provide the predefined Microsoft password reset link.
 • IncidentCreation: Call {{incident_creation $input}} if the user’s issue remains unresolved, or they express frustration, ask if they want to create an incident request. If they agree, invoke this function to log their issue for further support.

When responding to the user, always format the response in a clear, structured manner with proper headings, bold text for important details, and step-by-step instructions when necessary. Follow these rules when generating a response: 
 • Start with a short introduction summarizing the task or solution.
 • Clearly state any prerequisites before proceeding.
 • Structure the response logically with numbered steps.
 • Use bold text to highlight critical details, inputs, or user actions.
 • If applicable, provide links to external resources.


Here is an example of a response from AI Search articles: 

"To configure a Generic or Shared Mailbox in Outlook 2013, follow these steps:

Prerequisites:
1. Request Access: If you have never accessed the Generic or Shared mailbox, you need to request access via the REQUEST IT module in ServiceNow. Select the catalogue item Access to Generic Mailbox.
2. Once the request is processed and completed, proceed with the following steps.

Configuration Steps:
 
3. Close Outlook: Before starting, ensure Outlook is closed.
4. Open Control Panel:
• Click on the Start Menu.
• Type Control Panel and open it.
5. Locate Mail Settings:
• In the Control Panel, click on Mail (32-bit).
6. Open Email Account Settings:
• Select E-mail Accounts from the Mail Setup window.
7. Add New Account:
• Click on New to add a new mailbox .
8. Enter Mailbox Information:
• Type the email address of the Generic Mailbox in the Your Name and E-mail Address fields.
• Click on Next 1 2 .
9. Auto-Configuration or Manual Input:
• The mailbox will auto-configure in most cases.
• If prompted, enter your corporate email address, and click Next .
10. Finalize Setup:
• Once the configuration completes, click Close .
11. Open Outlook:
• Open Outlook, and the Generic Mailbox should appear under your profile.
• Allow time for emails to download and sync.

Following these steps will successfully configure your shared or generic mailbox in Outlook."
"""

    history.add_system_message(prompt)

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)
        # print(history.model_dump_json())
        save_history(history.serialize())


def save_history(history_json):
    COSMOSDB_URL = os.getenv(
        "COSMOSDB_URL", "https://cosmos-ek-itsm-ddemo-22v.documents.azure.com:443/"
    )
    COSMOSDB_KEY = os.getenv(
        "COSMOSDB_KEY",
        "kQyd4iODo0Qrb4PliJ3dpUI0O7FYU9q54lCOkpkiBHjBCYETRS7VpoL7qE7WIg6V4BUIAsvVvOJrACDbeQ26Kg==",
    )
    client = CosmosClient(COSMOSDB_URL, credential=COSMOSDB_KEY)
    DATABASE_NAME = os.getenv("AZURE_COSMOSDB_DATABASE_ID", "GenAIBot")
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = os.getenv("AZURE_COSMOSDB_CONTAINER_ID", "Conversations")
    container = database.get_container_client(CONTAINER_NAME)
    # Convert string to dict and add an "id"
    conversation_data = {
        "id": str(uuid.uuid4()),
        "conversation": json.loads(history_json),
    }
    container.upsert_item(conversation_data)


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())