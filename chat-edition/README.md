# Chat edition of site-setup

`site-setup-chat/` is the **regular Claude chat (claude.ai)** version of the `site-setup` skill. The Claude Code version lives in `.claude/skills/site-setup/`.

## Install (regular chat)
1. Zip the `site-setup-chat` folder so the folder itself is the top level of the ZIP (`site-setup-chat.zip` > `site-setup-chat/SKILL.md`).
2. In claude.ai open **Customize > Skills**, click **+**, **Create skill**, **Upload a skill**, and choose the ZIP.
3. Make sure **code execution** is on (Settings > Capabilities). On Team and Enterprise plans an owner must enable skills first.
4. Start a new chat and type: `Use site-setup-chat to set up my website project. I'm brand new.`

## How it differs from the Claude Code version
| | Claude Code `site-setup` | Chat `site-setup-chat` |
|---|---|---|
| Sees the owner's computer | Yes | **No** |
| Creates the project folder | In place | As a **starter ZIP** the owner downloads |
| Project files | Written into the project | Delivered as a second ZIP that unpacks to `_incoming/` |
| Checks | Real folder | A **copy in the sandbox** (not the owner's computer) |
| Builds the site | No (writes a build prompt) | No (writes a build prompt, with a Step 0 that moves `_incoming/`) |

## Notes
- The description is under Anthropic's 200-character limit and the name differs from the Claude Code skill, so both can exist side by side.
- Tested: the starter builder for Astro and Next.js, rejected unsafe paths and names, the `_incoming` pack layout, and the verification script on an assembled copy (no secret printed). The skill's instructions have not been run end to end in claude.ai.
