import time


class Base(object):

    def format_payload(self, type, now, value):
        localtime = time.localtime(now)
        pl = {'timestamp': int(now),
              'type': type,
              'datetime': time.strftime("%Y%m%d%H%M%S", localtime),
              'value': value}

        return pl
