# tqdmx

This small module provides a way to view your [tqdm](https://github.com/tqdm/tqdm) progress bar
in your [matrix](https://matrix.org) client,
similar to what is already possible out of the box
for [telegram](https://tqdm.github.io/docs/contrib.telegram/).

## Setup

   NOTE: So far `tqdmx` does not support encryption. The `room_id` is assumed to point to an unencrypted room.

1. Create a new matrix account for your bot (recommended) or use an existing one.
2. Login to the account to get an `access_token` (in element this is in *All Settings* > *Help & About* at the very bottom). Also you need to join the room you want to post updates in manually.
3. Install this module, e.g. via `pip install git+https://github.com/frcl/tqdmx.git`.
4. Provide the `homeserver` where the bot lives, the `access_token` from step 2 and the `room_id` where you want the bot to post updates, either directly as kwargs
   ```python
   from tqdmx import trange

   homeserver = 'matrix.org'
   token='syt_some_long_secret_token'
   room_id = '#some_room:matrix.org'

   for _ in trange(10, homeserver=homeserver, access_token=token, room_id=room_id):
        do_stuff()
   ```
   or via the environment variables `TQDM_MATRIX_HOMESERVER`, `TQDM_MATRIX_ACCESS_TOKEN` and `TQDM_MATRIX_ROOM_ID`.
