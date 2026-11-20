# Beginner walkthroughs

Use these in plain, friendly words when the owner says they are new to this, when they ask for help ("help me with .env", "where is my folder?"), or whenever they look lost. Ask once **"Do you use a Mac, Windows or Linux?"** (or check with `uname`) and give **only** the steps for their computer. Give **one step at a time** and wait for them to say it is done.

Say what a thing is **before** you use its name. Never rush. Never make the owner feel behind.

---

## 1. Your project folder

**What it is (say this):** "Everything for your website lives in one folder on your computer. Think of it as the box that holds all the files."

**A good place and name**
- Inside **Documents** is a good place. Use a short lowercase name with dashes and no spaces, for example `my-business-site`.
- **Avoid:** the home folder itself, the root of Desktop or Downloads, a folder that already holds unrelated files, and folders synced by OneDrive, iCloud or Dropbox if you can (they can slow down or break installs).

**Which folder am I in right now?** Run `pwd` (Mac, Linux) and tell the owner the path in plain words, for example "We are in `/Users/ada/Documents/my-business-site`." Then say whether it looks right: empty or nearly empty, not the home folder, not full of other things.

**If it is the wrong folder, make a new one (the owner does this; offer to explain each click):**
- **Mac:** open Finder → Documents → File menu → New Folder → type the name.
- **Windows:** open File Explorer → Documents → right-click an empty space → New → Folder → type the name.
- **Or in a terminal:** `mkdir ~/Documents/my-business-site` (Mac, Linux) or `mkdir "$env:USERPROFILE\Documents\my-business-site"` (Windows PowerShell).

**Then open Claude Code inside that folder.** In a terminal: go into the folder (`cd ~/Documents/my-business-site`) and start Claude Code (`claude`). If they use an app, choose that folder when it asks which folder to open.

**Important:** a running chat cannot move itself to another folder. **Stop here.** Tell the owner to start a **new chat in the new folder** and type `site-setup` again. You will carry on from there.

---

## 2. What the starter folders are for (explain one line each as you create them)

| Folder or file | In plain words |
|---|---|
| `docs/` | Notes about your project: your answers, the plan, the checklist. |
| `references/` | Short files that teach Claude how your business sounds and what is true about it. |
| `<images folder>/` | Where **you** put your own photos. They are never uploaded by mistake. |
| `public/` | Files the website shows as they are: your logo, the icon in the browser tab. |
| `scripts/` | Small helper programs, for example one that shrinks photos. |
| `.gitignore` | A list of things that must never be uploaded (like your keys). |
| `.env` | A private notes file for keys and passwords. Never shared. |
| `.env.example` | The same list, with the values blank, as a reminder of what is needed. |
| `README.md` | A short "how this project works" note, filled in later. |

---

## 3. See your folder on your computer (offer; ask permission first)

Offer: "Would you like me to open the folder on your computer so you can see it?" **Only run a command if they say yes.**
- **Mac:** `open .`
- **Windows:** `explorer .`
- **Linux:** `xdg-open .`

If they say no, or it fails, give the path and the steps: **Mac:** Finder → Go menu → Go to Folder → paste the path. **Windows:** open File Explorer and paste the path into the address bar.

---

## 4. Hidden files (why you cannot see `.env`)

Names that start with a dot (`.env`, `.gitignore`) are **hidden** by default so people do not change them by accident. To see them:
- **Mac (Finder):** press **Command + Shift + .** (the period). Press it again to hide.
- **Windows 11:** File Explorer → **View** → **Show** → **Hidden items**.
- **Windows 10:** File Explorer → **View** tab → tick **Hidden items**.
- **Linux (most file managers):** press **Ctrl + H**.
- In a code editor's file list they usually show automatically.

---

## 5. The `.env` file, step by step

**What it is (say this):** "A small private notes file where your keys and passwords live. Your website never publishes it, and the project is set up to ignore it, so it cannot be uploaded by mistake."

Only walk through this if the owner **wants to now** and has a key. Otherwise say it can wait and you will remind them at the uploads stage.

1. **Where it is.** In the project folder, next to `CLAUDE.md` (not inside any other folder). It is named exactly `.env`. Show them the full path. If it is not there, **you create it** (empty values) after asking.
2. **Get the key (Unsplash example).** Go to unsplash.com/developers → **Your apps** → **New Application** → accept the terms → copy the **Access Key**. **Never** the Secret Key. New apps start in demo mode (about 50 requests an hour), which is plenty for one post at a time.
3. **Open the file.**
   - **Mac:** right-click `.env` → **Open With** → **TextEdit**. If the text looks formatted, choose **Format → Make Plain Text**.
   - **Windows:** right-click `.env` → **Open with** → **Notepad**.
   - Any code editor works too.
4. **Paste the key.** Find the line `UNSPLASH_ACCESS_KEY=` and paste the key straight after the `=`. **No spaces and no quotes.** It should look like this (with your own key):
   `UNSPLASH_ACCESS_KEY=abc123yourkeyhere`
5. **Save** (Command + S on Mac, Ctrl + S on Windows) and close the file.
6. **Check it without showing it.** Say: "Please check my .env." Run `scripts/verify-setup.sh`. It reports each key as **SET** or **empty** and **never shows the value**.

**Rules for you (Claude):**
- **Never** ask the owner to paste a key into the chat. **Never** print, `cat`, quote or open the contents of `.env` in the chat. Use the script.
- If a key is ever pasted into the chat by mistake: tell them calmly to make a **new key** in that service and replace it in `.env`, and treat the old one as lost.
- Other keys follow the same steps (Render or other services give their own).

**If something goes wrong**
- *Windows saved it as `.env.txt`:* in File Explorer turn on **View → Show → File name extensions**, then rename the file to exactly `.env`.
- *The file is not visible:* show hidden files (section 4).
- *The check says empty:* the file was not saved, or the key was pasted on the wrong line, or into a different `.env` in another folder.
- *The key has quotes or spaces:* remove them.

---

## 6. Other files the owner adds later

- **Photos and logos:** drag them into the folders named in the checklist. Say which file is which.
- **Keyword export (for example from Semrush):** save the CSV, rename it `keywords.csv`, and drag it into the project folder (it replaces the header-only file; ask before replacing).
- You may offer to move a file for them if they tell you where it is. Ask permission first.

---

## 7. Words in one line (use when you need them)

- **Folder:** a box that holds files.
- **File:** one document. Its name ends with a short type, like `.md` or `.csv`.
- **Hidden file:** a file whose name starts with a dot; the computer hides it on purpose.
- **Terminal:** a window where you type commands instead of clicking.
- **Key (API key):** a long password that lets one program talk to another service.
- **Repository (git):** a project folder with a history of changes, so nothing is lost.
- **Build:** turning your project files into the finished website files.
- **Deploy:** putting the finished website on the internet.
