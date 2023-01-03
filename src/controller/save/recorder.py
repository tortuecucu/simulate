from pathlib import Path
from typing import  Set, Any, List
import aiofiles
from aiocsv.writers import AsyncWriter
import csv
import asyncio
import blinker

class Recorder():
    _instances:List['Recorder']=[]
    def __init__(self, signal_name:str, path:Path, fields:Set[str]) -> None:
        self.signal_name=signal_name
        self.path=path
        self.fields=fields
        self._instances.append(self)
        self._file=None
        self._writer=None
        signal:blinker.NamedSignal=blinker.signal(self.signal_name)
        signal.connect(self._listener)


    async def __aenter__(self):
        file_exists=self.path.exists()
        self._file= await aiofiles.open(self.path, 'a', encoding='utf-8', newline="").__aenter__()
        self._writer=AsyncWriter(self._file, quoting=csv.QUOTE_NONNUMERIC)
        if not file_exists:
            await self.record(self.fields)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if self._file:
            self._file.close()
        if self._writer:
            self._writer=None

    async def record(self, row:Set[Any])->None:
        await self._writer.writerow(row)

    async def _listener(self, *args, **kwargs):
        if 'row' in kwargs:
            await self.record(kwargs['row'])


""" async def main():
    sig:blinker.NamedSignal=blinker.signal('truc')
    async with Recorder('truc', Path('truc.txt'), set(['col1', 'col2'])) as recorder:
        sig.send_async(sender=Any ,row=[1,2])
        while len(asyncio.all_tasks())>1:
            await asyncio.sleep(0.5)

asyncio.run(main()) """