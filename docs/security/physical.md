# Physical security

> Practical habits for protecting your seeds, backups, and device in the real world.

SeedSigner's air-gapped design protects you from remote attacks, but physical security is entirely in your hands.

## Using SeedSigner safely

**Work in private.** Always use SeedSigner in a location where you are not being observed. Stay away from security cameras, windows, and other people. If someone can see your screen, they can see your seed words.

**Shield the screen.** When SeedSigner displays seed words, QR codes containing seed data, or other sensitive information, angle the screen so that only you can see it.

**Discard seeds from memory when finished.** After you complete a signing session, use SeedSigner's option to discard the loaded seed. Do not leave seeds loaded longer than necessary.

**Remove the SD card after boot.** Once SeedSigner has started up, you can remove the microSD card. This eliminates any theoretical possibility of the device writing data to persistent storage during your session.

## Storing seed backups

Your seed phrases are the keys to your funds. Physical storage deserves serious thought.

**Use secure storage locations:**
- Fireproof safes at home
- Safety deposit boxes at a bank
- Other secure, access-controlled locations

**Distribute across locations.** For multi-sig setups, store each seed backup in a separate physical location. This protects you against localized disasters and theft.

**Keep backups legible.** Seed words written on paper can degrade over time. Consider stamping words into metal backup plates for long-term durability. Periodically check that your backups are still readable.

## Tamper evidence

If you are concerned about someone accessing your seed backups without your knowledge, consider tamper-evident packaging:

- Store seed backups in **evidence bags** or tamper-evident envelopes.
- Write your initials across the seal so any opening is visible.
- When you check on a backup, inspect the seal before opening.

This does not prevent theft, but it tells you if someone has accessed your backup so you can move your funds to new keys.

## Periodic key checks

Set a recurring reminder — quarterly or twice a year — to verify your backups:

- Confirm each seed backup is still in its expected location.
- Check that the words are legible.
- Verify tamper-evident seals are intact.
- For multi-sig, confirm your wallet descriptor backup is also present and accessible.

> **Tip:** A key check does not require powering on SeedSigner. You are simply confirming that your physical backups are safe, present, and readable.

## Protecting your privacy

**Use fresh receiving addresses.** Every time you receive Bitcoin, use a new address. Sparrow Wallet handles this automatically, but always verify you are not reusing an old address.

**Never scan seed QR codes with phones or computers.** SeedQR backups and any QR code containing seed data should only ever be scanned by your SeedSigner. Phones and computers are networked devices — scanning a seed QR with them defeats the entire purpose of an air-gapped setup.

> **Warning:** A seed phrase photographed by a phone or scanned by a networked device should be considered compromised. Move your funds to a new key immediately if this happens.
