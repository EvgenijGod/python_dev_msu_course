import asyncio
import cowsay

clients = {}

class User:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.login = None
        self.queue = asyncio.Queue()

    def __str__(self):
        return f"{self.ip}:::{self.port}"

    async def warning(self, what, cow=None):
        if cow is None:
            await self.queue.put(cowsay.cowsay(what))
        else:
            await self.queue.put(cowsay.cowsay(what, cow=cow))

    async def try_login(self, name):
        if self.login is not None:
            await self.warning(f"You have already logged in. Your login is {self.login}")
        elif name in set(client.login for client in clients.values() if client.login):
            await self.warning(f"login {name} is already used. Try another one")
        elif name not in cowsay.list_cows():
            await self.warning(f"login {self.login} is not in cowlist. Try another one\nCowlist:\n{cowsay.list_cows()}")
        else:
            self.login = name
            await self.warning(f"Welcome to cowchat, {name}")

def get_args(s : str):
    args = s.split()
    return list(x for x in args if x)

async def chat(reader, writer):
    ip, port = writer.get_extra_info('peername')
    user = User(ip, port)
    clients[str(user)] = user

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(user.queue.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                q_input = q.result().decode()
                q_cmd = get_args(q_input)
                if len(q_cmd) == 0:
                    await user.warning("Unknown command")
                if q_cmd[0] == "login":
                    if len(q_cmd) != 2:
                        await user.warning("login requieres only one argument - your name")
                    else:
                        name = q_cmd[1]
                        await user.try_login(name)
                elif user.login:
                    # need login
                    if q_cmd[0] == "who":
                        if len(q_cmd) != 1:
                            await user.warning("who doesnt requiere any arguments")
                        else:
                            used_names = set(client.login for client in clients.values() if client.login)
                            await user.warning("Logged users: " + ", ".join(used_names))
                    elif q_cmd[0] == "cows":
                        if len(q_cmd) != 1:
                            await user.warning("cows doesnt requiere any arguments")
                        else:
                            used_names = set(client.login for client in clients.values() if client.login)
                            all_names = set(cowsay.list_cows())
                            await user.warning(str(all_names - used_names))
                    elif q_cmd[0] == "say":
                        if len(q_cmd) < 3:
                            await user.warning("say requieres two arguments - name and message")
                        else:
                            name = q_cmd[1]
                            message = q_input.replace("say", "", 1).replace(name, "", 1).strip()
                            found = False
                            for client in clients.values():
                                if client.login is None or client.login != name:
                                    continue
                                found = True
                                await client.warning(f"You recieved message from {user.login}. Message: {message}", cow = user.login)

                            if not found:
                                await user.warning(f"user {name} doesnt exist")
                    elif q_cmd[0] == "yield":
                        if len(q_cmd) < 2:
                            await user.warning("yield requieres your text")
                        else:
                            message = q_input[len("yield"):].strip()
                            for client in clients.values():
                                await client.warning(f"You recieved message from {user.login}. Message: {message}", cow = user.login)
                    elif q_cmd[0] == "quit":
                        if len(q_cmd) != 1:
                            await user.warning("quit doesnt requiere any arguments")
                        else:
                            send.cancel()
                            receive.cancel()
                            del clients[str(user)]
                            writer.close()
                            await writer.wait_closed()
                            return
                    else:
                        await user.warning("Unknown command")
            elif q is receive:
                receive = asyncio.create_task(user.queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    
    send.cancel()
    receive.cancel()
    del clients[str(user)]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())