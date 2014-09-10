def plugin(bot):

    @bot.respond(r'(hello|hi)')
    def say_hello(response):
        response.emote("tips his fedora.")

    @bot.httpd.route("/foo")
    def foo():
        bot.messageRoom('Shell', 'Hello')
        return "Hello"
