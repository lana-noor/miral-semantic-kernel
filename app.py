import os
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

################
from semantic_kernel.connectors.memory.azure_ai_search import AzureAISearchStore
from azure.search.documents.indexes import SearchIndexClient
################


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

    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()
    
    
    vector_store = AzureAISearchStore()


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


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
