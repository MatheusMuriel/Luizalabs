import json
import os


class ResourceManager:
    """
    Class to retrieval resources messages.

    Attributes:
        lang (str): The language code for the resource file ("en" for English).
        messages (dict): A dict with messages loaded from the resource file.
    """
    def __init__(self, lang: str = "en"):
        """
        Initializes class with the specified language and loads the messages.

        Args:
            lang (str): The language code for resource file. Defaults to "en".
        """
        self.lang = lang
        self.messages = self._load_messages()

    def _load_messages(self):
        """
        Load all messages from the resource file.

        Returns:
            dict: A dictionary containing the messages from the resource file.

        Raises:
            FileNotFoundError:  If the resource file for the specified language
                                does not exist.
        """
        resource_file = os.path.join(
            os.path.dirname(__file__), f"messages_{self.lang}.json"
        )
        if not os.path.exists(resource_file):
            raise FileNotFoundError(
              f"Resource file for language '{self.lang}' not found."
            )
        with open(resource_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get(self, key):
        """
        Retrieves a message by its key from the loaded messages.

        Args:
            key (str): The dot-separated key indicating the path to the
                       desired message (ex: "auth.login_success").

        Returns:
            str: The message corresponding to the given key.

        Raises:
            KeyError: If the key does not exist in the loaded messages.
        """
        keys = key.split(".")
        value = self.messages
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return f"Message for key '{key}' not found."
