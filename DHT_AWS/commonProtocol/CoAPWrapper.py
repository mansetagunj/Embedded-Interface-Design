#reference - https://aiocoap.readthedocs.io/en/latest/examples.html#client
import asyncio
import logging
import aiocoap.resource as resource
import aiocoap


class EchoResource(resource.Resource):
    
    def __init__(self):
        super().__init__()
        self.set_content("")

    def set_content(self, content):
        self.content = content

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        #print("COAP PUT payload:",str(request.payload))
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
    
    
class CoAPWrapper():
    def __init__(self):
        logging.getLogger("coap-server").setLevel(logging.CRITICAL)
        # Resource tree creation
        self.root = resource.Site()

        #root.add_resource(('.well-known', 'core'),
        #        resource.WKCResource(root.get_resources_as_linkheader))
        self.root.add_resource(('echo',), EchoResource())
        #root.add_resource(('test', 'new'), Resource())

        print ("__Init CoAP server__")

        
    def start(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        print ("__Starting CoAP server__")
        asyncio.Task(aiocoap.Context.create_server_context(self.root))
        asyncio.get_event_loop().run_forever()
        
    def stop(self):
        print ("__Closing CoAP server__")
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()


if __name__ == "__main__":
    #main()
    coap = CoAPWrapper()
    coap.start()