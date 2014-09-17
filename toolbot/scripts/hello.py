import sys


def plugin(bot):

    @bot.respond(r'ping$')
    def ping(response):
        response.reply("PONG")

    @bot.respond(r'echo (.*)$')
    def decho(response):
        response.send(response.match.group(1))

    @bot.respond(r'die$')
    def die(response):
        response.send("Goodbye cruel world")
        bot.stop()
