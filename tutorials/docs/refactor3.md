Let's do it. We're now going to extract all the logic related to loading, saving, and encrypting your application's settings.

---

### Stage 1.5: Separating Configuration Management

Your application needs to know its settings: the GitLab URL, API tokens, etc. Currently, the classes that handle this (`ConfigManager` and `EncryptionManager`) are in the main script. We'll move them to their own dedicated configuration module.

#### The "Why"

This is a powerful demonstration of two computer science principles: **Encapsulation** and the **Single Responsibility Principle (SRP)**.

- **Encapsulation:** We are bundling the configuration data and the logic that operates on that data (`save`, `load`, `encrypt`) into a single, self-contained unit. The rest of the application doesn't need to know _how_ the configuration is stored (is it a JSON file? Is it encrypted?); it just asks the `ConfigManager` for what it needs.
- **Single Responsibility Principle:** This new `config.py` file will have only one reason to change: if we alter how we manage configuration. The API endpoints don't need to change, and the Git logic doesn't need to change. This isolation makes the system far more robust and easier to maintain.

A key part of this step is that we will also move the `AppConfig` Pydantic model from `schemas.py` into our new `config.py` file. This is an example of **High Cohesion**—we are grouping code that is thematically and functionally related. `AppConfig` is part of the internal configuration _system_, not part of the data being sent over the API, so it belongs with the `ConfigManager` that uses it.

#### Your Action Items

1. Create a new file at `backend/app/core/config.py`.
2. Add the following code to it. This code is moved from your original `mastercam_main.py` and `schemas.py`.
3. **Important:** After creating the new file, go back to `backend/app/models/schemas.py` and **delete** the `AppConfig` class from it, as it now lives in its new home.

---

#### Code for `backend/app/core/config.py`

```python
import json
import logging
import base64
import os
import sys
from pathlib import Path

from cryptography.fernet import Fernet
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AppConfig(BaseModel):
  """Defines the structure of the application's configuration."""
  version: str = "2.0.0"
  gitlab: dict = Field(default_factory=dict)
  local: dict = Field(default_factory=dict)
  ui: dict = Field(default_factory=dict)
  security: dict = Field(default_factory=lambda: {"allow_insecure_ssl": False})
  polling: dict = Field(default_factory=lambda: {
    "enabled": True, "interval_seconds": 15, "check_on_activity": True
  })


class EncryptionManager:
  """Handles encryption and decryption of sensitive configuration data."""

  def __init__(self, config_dir: Path):
    self.key_file = config_dir / '.encryption_key'
    self._fernet: Fernet | None = None
    self._initialize_encryption()

  def _initialize_encryption(self):
    try:
      if self.key_file.exists():
        key = self.key_file.read_bytes()
      else:
        key = Fernet.generate_key()
        self.key_file.write_bytes(key)
        # Set file permissions to be readable only by the owner on non-Windows systems
        if os.name != 'nt':
          os.chmod(self.key_file, 0o600)
      self._fernet = Fernet(key)
    except Exception as e:
      logger.error(f"Failed to initialize encryption: {e}")

  def encrypt(self, data: str) -> str:
    """Encrypts a string."""
    if self._fernet:
      return base64.b64encode(self._fernet.encrypt(data.encode())).decode()
    # Fallback if encryption fails to initialize (not ideal, but prevents crash)
    return data

  def decrypt(self, encrypted_data: str) -> str:
    """Decrypts a string."""
    if self._fernet:
      try:
        return self._fernet.decrypt(base64.b64decode(encrypted_data.encode())).decode()
      except Exception:
        # If decryption fails (e.g., key changed, data corrupted), return the raw data
        logger.warning("Failed to decrypt data, returning raw value.")
        return encrypted_data
    return encrypted_data


class ConfigManager:
  """Manages loading, saving, and accessing the application configuration."""

  def __init__(self, base_dir: Path | None = None):
    if base_dir is None:
      # Determine the base directory based on whether running as a script or bundled executable
      if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent
      else:
        base_dir = Path(__file__).resolve().parents[2] # Moves up from /app/core to /backend

    self.config_dir = base_dir / 'app_data'
    self.config_file = self.config_dir / 'config.json'
    self.config_dir.mkdir(parents=True, exist_ok=True) # Ensure the directory exists

    self.encryption = EncryptionManager(self.config_dir)
    self.config = self._load_config()

  def _load_config(self) -> AppConfig:
    """Loads configuration from the JSON file."""
    if not self.config_file.exists() or not self.config_file.read_text():
      return AppConfig()

    try:
      data = json.loads(self.config_file.read_text())
      # Decrypt the token if it exists
      if token := data.get('gitlab', {}).get('token'):
        data['gitlab']['token'] = self.encryption.decrypt(token)
      return AppConfig(**data)
    except (json.JSONDecodeError, TypeError) as e:
      logger.error(f"Failed to load or parse config file, creating a default config: {e}")
      return AppConfig()

  def save_config(self):
    """Saves the current configuration to the JSON file, encrypting sensitive data."""
    try:
      # model_dump() is the Pydantic v2 replacement for .dict()
      data = self.config.model_dump()
      # Encrypt the token before saving
      if token := data.get('gitlab', {}).get('token'):
        data['gitlab']['token'] = self.encryption.encrypt(token)

      self.config_file.write_text(json.dumps(data, indent=2))
    except Exception as e:
      logger.error(f"CRITICAL: Failed to save config file at {self.config_file}: {e}")
      raise

```

---

We've now successfully encapsulated our entire configuration system. The rest of our application will no longer need to know _anything_ about JSON files or encryption; it will just interact with the `ConfigManager`.

Once you've created `config.py` and removed `AppConfig` from `schemas.py`, let me know you're ready and we'll tackle the security and authentication logic next.
