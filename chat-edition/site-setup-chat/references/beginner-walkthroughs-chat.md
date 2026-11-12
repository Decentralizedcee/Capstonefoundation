# Beginner walkthroughs (chat edition)

In this chat you **cannot see or change the owner's computer**. You make files here, and the owner downloads them and does the clicking. So every step below is something **they** do. Give **one step at a time** and wait for "done". Ask once **"Mac, Windows or Linux?"** and give only their steps.

Say what a thing is **before** you use its name. Never rush. Never make the owner feel behind.

---

## 1. Get your project folder

**What it is (say this):** "Everything for your website lives in one folder on your computer. I will make that folder for you as a ZIP file. You download it and unzip it."

1. **Download** the ZIP from this chat (the file link or button I show you). It usually lands in your **Downloads** folder.
2. **Unzip it.**
   - **Mac:** double-click the ZIP. A folder with your project's name appears next to it.
   - **Windows:** right-click the ZIP → **Extract All** → **Extract**.
3. **Move the new folder to Documents** (drag it there). Avoid keeping it in Downloads or Desktop, and avoid folders synced by OneDrive, iCloud or Dropbox (they can slow or break installs).
4. **Open it** and look inside. You should see folders like `docs`, `references` and `public`. If a folder seems empty, that is normal: a tiny hidden placeholder file keeps it alive.

---

## 2. What each starter folder is for (explain one line each)

| Folder or file | In plain words |
|---|---|
| `docs/` | Notes about your project: your answers, the plan, the checklist. |
| `references/` | Short files that teach Claude how your business sounds and what is true about it. |
| `<images folder>/` | Where **you** put your own photos. They are never uploaded by mistake. |
| `public/` | Files the website shows as they are: your logo, the icon in the browser tab. |
| `scripts/` | Small helper programs, for example one that shrinks photos. |
| `.gitignore` | A list of things that must never be uploaded (like your keys). |
| `.env` | A private notes file for keys and passwords. Never shared. |
| `.env.example` | The same list with the values blank, as a reminder. |
| `README.md` | A short "how this project works" note, filled in later. |

---

## 3. Hidden files (why you may not see `.env`)

Names that start with a dot (`.env`, `.gitignore`) are **hidden** by default. To see them:
- **Mac (Finder):** press **Command + Shift + .** (period). Press again to hide.
- **Windows 11:** File Explorer → **View** → **Show** → **Hidden items**.
- **Windows 10:** File Explorer → **View** tab → tick **Hidden items**.
- **Linux (most file managers):** press **Ctrl + H**.

---

## 4. The `.env` file, step by step

**What it is (say this):** "A small private notes file where your keys and passwords live. Your website never publishes it, and the project is set up to ignore it, so it cannot be uploaded by mistake."

Only walk through this if the owner **wants to now** and has a key. Otherwise it can wait.

1. **Where it is:** in your project folder, at the top level (next to `README.md`). It is named exactly `.env`.
2. **Get the key (Unsplash example):** go to unsplash.com/developers → **Your apps** → **New Application** → accept the terms → copy the **Access Key**. **Never** the Secret Key. New apps start in demo mode (about 50 requests an hour), which is plenty for one post at a time.
3. **Open the file:**
   - **Mac:** right-click `.env` → **Open With** → **TextEdit**. If the text looks formatted, choose **Format → Make Plain Text**.
   - **Windows:** right-click `.env` → **Open with** → **Notepad**.
4. **Paste the key** straight after the `=` on the right line. **No spaces and no quotes.** It looks like this (with your own key):
   `UNSPLASH_ACCESS_KEY=abc123yourkeyhere`
5. **Save** (Command + S or Ctrl + S) and close.
6. **Self-check** (you cannot check it for them): the key is right after `=`, nothing else is on that line, and the file is still named exactly `.env`. Later, when they use Claude Code, `site-setup audit` can confirm each key is set without ever showing it.

**Rules for you (Claude):**
- **Never** ask the owner to paste a key into this chat. **Never** ask them to paste the contents of `.env`. If they do, tell them calmly to make a **new key** in that service and replace it, and treat the old one as lost.
- You cannot see their `.env`. Never claim you checked it.

**If something goes wrong**
- *Windows saved it as `.env.txt`:* in File Explorer turn on **View → Show → File name extensions**, then rename it to exactly `.env`.
- *The file is not visible:* show hidden files (section 3).
- *Nothing seems to work later:* the key may be on the wrong line, have quotes or spaces, or be in a different `.env` in another folder.

---

## 5. The second ZIP (the project files) and the `_incoming` folder

Near the end you give the owner a second ZIP that unzips to **one folder called `_incoming`**. It holds the project's rulebook and notes. It is built this way so **nothing can be overwritten by accident**.

1. **Download and unzip** it (same as section 1). You get a folder called `_incoming`.
2. **Drag the whole `_incoming` folder into the project folder** (the one from the first ZIP). It has a new name, so there is **no "Replace" question**.
3. **Do not drag the files out one by one.** The build prompt's first step tells Claude Code to move each file into its right place and ask before replacing anything.
4. If the owner is **not using Claude Code**, the file `_incoming/MOVE-ME.md` explains where each file goes, in a short table.

---

## 6. Words in one line

- **Folder:** a box that holds files.
- **File:** one document. Its name ends with a short type, like `.md` or `.csv`.
- **ZIP:** several files packed into one download. Unzip to open it.
- **Hidden file:** a file whose name starts with a dot; the computer hides it on purpose.
- **Key (API key):** a long password that lets one program talk to another service.
- **Build:** turning your project files into the finished website files.
- **Deploy:** putting the finished website on the internet.
