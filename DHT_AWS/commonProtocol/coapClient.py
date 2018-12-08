import logging
import asyncio
import time
from aiocoap import *

#logging.basicConfig(level=logging.INFO)

async def main():

    context = await Context.create_client_context()

    payload = b"Hello Frans, chai peelo\n"
    request = Message(code=PUT, payload=payload, uri="coap://localhost/echo")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    print ("Time:",time.time())
    #asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.get_event_loop().run_until_complete(main())
    print ("Time:",time.time())
    #main()