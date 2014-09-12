def plugin(bot):

    @bot.respond(r'(hello|hi)')
    def say_hello(response):
        response.emote("tips his fedora.")

    @bot.respond(r'topic')
    def set_topic(response):
        response.topic()

    @bot.httpd.route("/foo")
    def foo():
        bot.messageRoom('#irc3', 'Hello')
        return "Hello"
