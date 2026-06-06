# Identity Block

Identity is the root user block.

It owns user accounts and device identity. Product data belongs to the User Account, not to a single device.

## Responsibilities

- registration;
- login;
- accounts;
- users;
- `user_id`;
- devices;
- `device_id`;
- device management;
- session management;
- access recovery;
- account deletion.

## Beta Transition

Beta 1:

- access code;
- `device_id`;
- limited product access tied to beta entry.

Beta 2:

- full account;
- user-owned data;
- managed devices;
- session lifecycle;
- account recovery and deletion.

## Non-Responsibilities

- API protection policy;
- Trust Score decisions;
- billing limits;
- security event analysis.

Identity is not Security. Security consumes identity signals but owns protection decisions.
