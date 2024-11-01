from hardware.low.port import Port


class Robot:
    def __init__(self, port: Port):
        self.port = port
        self.handlers = {}
        self.modules = []

    async def loop(
            self,
            fsm: object
    ):
        async with self.port:
            while True:
                data: bytes | str = await self.port.read()
                # print("Get data:", data)

                try:
                    data = data.decode("utf-8")
                except UnicodeDecodeError:
                    print("Can`t read data")
                    continue

                data = data.replace("\n", "").replace("\r", "")

                header = data.split(" ")[0]
                body = data[len(header) + 1:]
                handled = False
                for module in self.modules:
                    if module.check_header(header):
                        await module.handle(data, body, self.port)
                        handled = True

                if not handled:
                    print("Error, unknown header:", header)

    def add_modules(self, *modules):
        self.modules.extend(modules)

    def remove_module(self, module):
        self.modules.remove(module)

    # TODO: Make all functions below

    def check_current_position(self):
        pass

    def move(self, point):
        pass


class RobotModule:
    def check_header(self, header: str) -> bool:
        return False

    async def handle(self, header: str, body: str, port: Port):
        pass
