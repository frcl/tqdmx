import json
import traceback
from os import getenv
from urllib.parse import quote
from uuid import uuid4

from requests import Session

from tqdm.auto import tqdm as tqdm_auto
from tqdm.contrib.utils_worker import MonoWorker


__version__ = '0.1.0'


class MatrxIO(MonoWorker):

    def __init__(self, homeserver, access_token, room_id):
        super().__init__()

        self.token = access_token
        self.homeserver = homeserver
        self.room_id = room_id

        self.session = Session()

        self.text = self.__class__.__name__
        self._event_id = None

    def api_endpoint(self, tx_id):
        return (f'https://{self.homeserver}/_matrix/client/r0/rooms/'
                f'{quote(self.room_id)}/send/m.room.message/{tx_id}')

    @property
    def event_id(self):

        if self._event_id:
            return self._event_id

        try:
            response = self.session.put(
                self.api_endpoint(uuid4()),
                params={'access_token': self.token},
                json={"msgtype": "m.text", "body": self.text},

            )
            response.raise_for_status()
        except Exception as exc:
            tqdm_auto.write(str(exc))
        else:
            self._event_id = response.json()['event_id']
            return self._event_id

    def write(self, s):
        """Replaces internal `message_id`'s text with `s`."""

        if not s:
            s = "..."

        s = s.replace('\r', '').strip()

        if s == self.text:
            return  # avoid duplicate message Bot error

        event_id = self.event_id
        if event_id is None:
            return

        self.text = s
        try:
            future = self.submit(
                self.session.put,
                self.api_endpoint(uuid4()),
                params={'access_token': self.token},
                json={
                    "msgtype": "m.text",
                    "body": "foo",
                    "m.relates_to": {
                        "rel_type": "m.replace",
                        "event_id": event_id,
                    },
                    "m.new_content": {
                        "msgtype": "m.text",
                        "body": self.text,
                    },
                },
            )
        except Exception as exc:
            tqdm_auto.write(str(exc))
        else:
            return future


class tqdm_matrix(tqdm_auto):
    """
    Standard `tqdm.auto.tqdm` but also sends updates to a Matrix Bot.
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.get('disable'):
            kwargs = kwargs.copy()
            self.mxio = MatrxIO(
                kwargs.pop('homeserver', getenv('TQDM_MATRIX_HOMESERVER')),
                kwargs.pop('access_token', getenv('TQDM_MATRIX_ACCESS_TOKEN')),
                kwargs.pop('room_id', getenv('TQDM_MATRIX_ROOM_ID')),
            )
        super(tqdm_matrix, self).__init__(*args, **kwargs)

    def display(self, **kwargs):
        super(tqdm_matrix, self).display(**kwargs)
        fmt = self.format_dict
        if fmt.get('bar_format'):
            fmt['bar_format'] = fmt['bar_format'].replace(
                '<bar/>', '{bar:20u}').replace('{bar}', '{bar:20u}')
        else:
            fmt['bar_format'] = '{l_bar}{bar:20u}{r_bar}'
        self.mxio.write(self.format_meter(**fmt))

    def clear(self, *args, **kwargs):
        super(tqdm_matrix, self).clear(*args, **kwargs)
        if not self.disable:
            self.mxio.write("")


def tmxrange(*args, **kwargs):
    return tqdm_matrix(range(*args), **kwargs)


# Aliases
tqdm = tqdm_matrix
trange = tmxrange
