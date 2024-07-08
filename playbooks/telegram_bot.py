import logging
import subprocess
import shlex
import os
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

async def run_deploy_playbook(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run an Ansible playbook."""
    chat_id = update.message.chat_id

    if chat_id != "<enter chat id here>":
        await update.message.reply_text("Droplet: Unauthorized access attempt.")
        return


    playbook = 'code_droplet.yml'
    args = ['--tags', 'create, deploy, containers', '--vault-password-file', '../.pswd']

    # Use shlex.split to handle additional arguments correctly
    command = ['ansible-playbook', playbook] + args

    try:

        current_dir = os.getcwd()
        # Run the ansible-playbook command
        await update.message.reply_text("Droplet: Started")
        result = subprocess.run(command, capture_output=True, text=True, cwd=current_dir)
        output = result.stdout if result.returncode == 0 else result.stderr
        await update.message.reply_text(f"Droplet: Success")
    except Exception as e:
        await update.message.reply_text(f"Droplet: Failed")

async def run_destroy_playbook(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run an Ansible playbook."""
    chat_id = update.message.chat_id

    if chat_id != "<enter chat id here>":
        await update.message.reply_text("Droplet: Unauthorized access attempt.")
        return


    playbook = 'code_droplet.yml'
    args = ['--tags', 'destroy', '--vault-password-file', '../.pswd']

    # Use shlex.split to handle additional arguments correctly
    command = ['ansible-playbook', playbook] + args

    try:

        current_dir = os.getcwd()
        # Run the ansible-playbook command
        result = subprocess.run(command, capture_output=True, text=True, cwd=current_dir)
        output = result.stdout if result.returncode == 0 else result.stderr
        await update.message.reply_text(f"Droplet: Destroyed")
    except Exception as e:
        await update.message.reply_text(f"Droplet: Failed")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("enter token here").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("deploy", run_deploy_playbook))
    application.add_handler(CommandHandler("destroy", run_destroy_playbook))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()