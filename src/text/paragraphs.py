discord_rules = """

==============================================================

:sparkles: **Discord Community Rules** :sparkles:

1. **Respect Others** :handshake: - Treat all members with respect. No harassment, bullying, or demeaning behavior towards any member.
2. **No Trolling** :no_entry_sign: - Trolling, baiting, or inciting drama is not allowed. This includes making provocative statements to get a reaction out of others.
3. **Avoid Sexual Content** :underage: - Do not share or discuss sexually explicit content. This includes texts, images, videos, or links to such content.
4. **No Griefing** :angry: - Deliberately irritating or harassing other players in games, destroying game structures built by others, or causing any sort of in-game trouble is not allowed.
5. **No Spamming** :no_entry_sign: - Do not flood the chat with messages, images, or emojis. Refrain from excessive use of caps, large texts, or unnecessary tags.
6. **Respect Privacy** :lock: - Do not share personal information of others without consent. This includes real names, addresses, and confidential information.
7. **Follow Channel Guidelines** :pushpin: - Respect the purpose of each channel. Keep discussions relevant to the channel topic.
8. **No Illegal Activities** :police_car: - Discussion or sharing of illegal activities, substances, or pirated content is strictly forbidden.
9. **Use Common Sense** :bulb: - If you're unsure if something is appropriate, it's probably best not to post it. When in doubt, ask a moderator.
10. **Listen to Staff** :ear: - Follow the guidance of the server staff (moderators, admins). Their word is final in matters of rule enforcement and interpretation.
11. **Report Rule Breaking** :warning: - If you see members breaking rules, report it to the staff. Do not take matters into your own hands.

==============================================================

:reminder_ribbon: Remember, the goal of these rules is to create a friendly, safe, and engaging environment for all members.

==============================================================


"""

acceptance_message = "Please type  :sparkles: **I accept** :sparkles: to agree to the rules and gain full access to the server."

aviable_commands = [ 'commands', 'help', 'roll [number]', "!xp" ]

commands_list = '\n'.join([f"{i+1}. {command}" for i, command in enumerate(aviable_commands)])


help_message = (f"""

==============================================================

If u need help, contact Staff.
All the aviable commands are: \n{commands_list}

==============================================================

""")

commands_message = (f"""

==============================================================

All the aviable commands are: \n{commands_list}

==============================================================

""")

prohibited_words = ['niga', 'nigger', 'n1gga', 'niggaa', 'niggers', 'n!gga', 'n1gg@', 'nigga', 'nigers']

warning_message = "Sending links is not allowed in this channel."

rankings = """

For your activity, you will be rewarded with XP points, each rank has unique perks like +entries for giveaways,
VIP statuss in Twitch, Free subs in Twitch etc.

1. Bot 🤖: 0 to 250 XP - The starting phase where new members begin their journey.
2. Alcoholic 🍺: 251 to 700 XP - Progressing to a more engaged and social level.
3. MethHead 💊: 701 to 1200 XP - A stage representing increased activity and involvement.
4. Rockstar 🎸: 1201 to 2000 XP - Achieving a status of prominence and recognition.
5. Heisenberg 👨‍🔬: 2001 to 4000 XP - Symbolizing mastery and significant influence within the community.
6. KURWAMACH 💥: 4001 XP and above - The elite rank, marking a legendary and commanding presence.

"""