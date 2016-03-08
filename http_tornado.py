# encoding:utf-8
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.gen
import tornado.concurrent
from tornado.options import define, options
import time

define("port", default=80, help="run on the given port", type=int)


def log(ip):
    print str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " + ip + "访问")


class PostHandlder(tornado.web.RequestHandler):
    executor = tornado.concurrent.futures.ThreadPoolExecutor(max_workers=1000)

    @tornado.gen.coroutine
    def get(self):
        yield self.executor.submit(log, self.request.remote_ip)
        for i, v in self.request.headers.iteritems():
            self.write(i + ":" + v + "\r\n")
        self.write("\r\n")
        self.write(self.request.body + "\r\n")
        self.write("your ip is " + self.request.remote_ip + "\r\n")

def make_app():
    return tornado.web.Application([
        (r"/", PostHandlder),
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
