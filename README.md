# PyPass 🔐
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1F6AA5)
![Argon2](https://img.shields.io/badge/Password%20Hashing-Argon2-5C2D91)
![Cryptography](https://img.shields.io/badge/Encryption-AES--256-success)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

A simple password management app built using Python
> [!NOTE]
> This program was built with the assistance of LLMs such as OpenAI's ChatGPT and Anthropic's Claude. However I fully understand the underlying logic and modules. The specifics on where AI was utilized can be found below. Feel free to disagree with my use of AI and to offer recommendations for the program.

# AI Usage 🤖
> *The program does not contain any directly copy-and-pasted code. I primarily used AI for module recommendations and architectural guidance.*

- Recommendation for what modules to use for cryptography such as Argon2 for password hashing, Fernet for data encryption/decryption, and Argon2id for key derivation alongside its parameters.
- Architectural recommendations such as giving the PassInfo dataclass its own file and the idea of creating custom errors.
- Bug and security checking.
- How to avoid circular imports using the typing module.
- Most frequently, I used it for explaining why it chose X modules and how their classes worked with the program.

# Description ℹ️
**What is PyPass?** 

PyPass is a locally hosted password management application that uses modern cryptographic primitives including Argon2, Argon2id, and Fernet.

**What modules does PyPass use?**

PyPass was built primarily using:
  - customtkinter for its GUI
  - Argon2 for password hashing and verification
  - Fernet for data encryption and decryption
  - Argon2id for key derivation

**Why was PyPass developed?**

Before PyPass's development, I had an interest in how cybersecurity programs worked; I figured a password manager would be a good place to start. However I do not see myself developing any more cybersecurity-oriented programs in the near future.

**How does it work? (conceptually assuming correct password and no errors)**

    password attempt -> argon2 hash verification -> argon2id key derivation -> fernet decryption -> access decrypted data

# Security Limitations ❗
> [!NOTE]
> Due to the following limitations, I would not recommend using PyPass as a regular password manager. PyPass is more of an educational project than a legitimate piece of cybersecurity software.

- PyPass does not contain a way to prevent config.json tampering (the file that stores failed attempts and lock times) so an attacker with access to your machine could edit it and bypass the locks.
- Sensitive data such as the plaintext password, encryption key, and the decrypted vault are stored in memory throughout the entire lifespan of the program.

# Theoretical Improvements ➕
> [!NOTE]
> I do not intend to personally continue working on this project. The ideas below are just improvements I researched during development, but was too lazy to implement.
- Add a hmac signature to the config.json file to detect file tampering.
- Limit the flow of plaintext sensitive data throughout the program (with Python, I believe it is impossible to 100% limit this).
- A button that allows the user to wipe vault with verification.
- Allow the user to sort entries alphabetically or by date.

# Installation 🚀
Assuming you're using Windows and have the Python standard library installed (I never tested PyPass on Linux)
```bash
git clone https://github.com/qclarity/PyPass.git
cd PyPass
pip install -r requirements.txt
python main.py

```
On launch, if you see a sign-in page, you likely installed everything correctly and are free to roam around PyPass's simple interface and feel the joy of securely saving password data on your own machine.

# Features 👾
- Master password authentication using Argon2.
- Vault encryption using Fernet.
- Argon2id key derivation.
- PyPass can detect inactivity and automatically sign the user out. With a default inactivity timer of 5 minutes.
- PyPass contains keybinds that allow the user to quickly open the program, get/add whatever information they wish, then immediately close it.
- PyPass allows the user to copy passwords and automatically clears the users clipboard after 30 seconds. Even when the user closes the program.
- Local encrypted vault storage.

# Default Keybinds ⚡
> *The following keybinds are configurable via the constants.py file.*

    Esc --This will close the currently opened window
    Shift+A --This will open the 'Add data' window
    Shift+D --This will delete the currently opened entry

# Fun Facts 💯
- Throughout ~90% of PyPass's development, it was originally called "Oblique." But I changed it after staring at a brick wall in school and thought "PyPass" looks much cleaner. I also realized naming a piece of software "Oblique" may not be the best idea because one of its definitons is: [not straightforward or obscure](https://www.merriam-webster.com/dictionary/oblique).
- PyPass was developed with 3 different text editors: VSCode, NeoVim, and PyCharm (in that order).

# Goodbye 👋
I hope whoever is reading this has a wonderful day--and installs my software.

-- QClarity 
