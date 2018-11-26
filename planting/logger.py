#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging

import os
import colorama


def _color_wrap(*colors):
    def wrapped(inp):
        return "".join(list(colors) + [inp, colorama.Style.RESET_ALL])

    return wrapped


def should_color(consumer, environ, std=(sys.stdout, sys.stderr)):
    real_consumer = (consumer if not isinstance(consumer, colorama.AnsiToWin32)
                     else consumer.wrapped)

    # If consumer isn't stdout or stderr we shouldn't colorize it
    if real_consumer not in std:
        return False

    # If consumer is a tty we should color it
    if hasattr(real_consumer, "isatty") and real_consumer.isatty():
        return True

    # If we have an ASNI term we should color it
    if environ.get("TERM") == "ANSI":
        return True

    # If anything else we should not color it
    return False


class Logger(object):
    VERBOSE_DEBUG = logging.DEBUG - 1
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    NOTIFY = (logging.INFO + logging.WARN) / 2
    WARN = WARNING = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL

    LEVELS = [VERBOSE_DEBUG, DEBUG, INFO, NOTIFY, WARN, ERROR, FATAL]

    COLORS = {
        WARN: _color_wrap(colorama.Fore.YELLOW),
        ERROR: _color_wrap(colorama.Fore.RED),
        FATAL: _color_wrap(colorama.Fore.RED),
        NOTIFY: _color_wrap(colorama.Fore.GREEN)
    }

    def __init__(self):
        self.consumers = []
        self.indent = 0
        self.explicit_levels = False
        self.in_progress = None
        self.in_progress_hanging = False

    def add_consumers(self, *consumers):
        if sys.platform.startswith("win"):
            for level, consumer in consumers:
                if hasattr(consumer, "write"):
                    self.consumers.append(
                        (level, colorama.AnsiToWin32(consumer)),
                    )
                else:
                    self.consumers.append((level, consumer))
        else:
            self.consumers.extend(consumers)

    def debug(self, msg, *args, **kw):
        self.log(self.DEBUG, msg, *args, **kw)

    def info(self, msg, *args, **kw):
        self.log(self.INFO, msg, *args, **kw)

    def notify(self, msg, *args, **kw):
        self.log(self.NOTIFY, msg, *args, **kw)

    def warn(self, msg, *args, **kw):
        self.log(self.WARN, msg, *args, **kw)

    def error(self, msg, *args, **kw):
        self.log(self.ERROR, msg, *args, **kw)

    def fatal(self, msg, *args, **kw):
        self.log(self.FATAL, msg, *args, **kw)

    # FIXME: should a name not only level
    def log(self, level, msg, *args, **kw):
        if args and kw:
            raise TypeError(
                "You may give positional or keyword arguments, not both")
        args = args or kw

        if args:
            rendered = msg % args
        else:
            rendered = msg

        rendered = ' ' * self.indent + rendered
        if self.explicit_levels:
            # FIXME: should this be a name, not a level number?
            rendered = '%02i %s' % (level, rendered)

        # add the prefix wrapper
        rendered = self.prefix_msg_wrapper(rendered)

        for consumer_level, consumer in self.consumers:
            if self.level_matches(level, consumer_level):
                if (self.in_progress_hanging
                        and consumer in (sys.stdout, sys.stderr)):
                    self.in_progress_hanging = False
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                if hasattr(consumer, 'write'):
                    write_content = rendered + '\n'
                    if should_color(consumer, os.environ):
                        # We are printing to stdout or stderr and it supports
                        #   colors so render our text colored
                        colorizer = self.COLORS.get(level, lambda x: x)
                        write_content = colorizer(write_content)

                    consumer.write(write_content)
                    if hasattr(consumer, 'flush'):
                        consumer.flush()
                else:
                    consumer(rendered)

    def _show_progress(self):
        """Should we display download progress?"""
        return (self.stdout_level_matches(self.NOTIFY) and sys.stdout.isatty())

    def start_progress(self, msg):
        assert not self.in_progress, (
            "Tried to start_progress(%r) while in_progress %r"
            % (msg, self.in_progress))
        if self._show_progress():
            sys.stdout.write(' ' * self.indent + msg)
            sys.stdout.flush()
            self.in_progress_hanging = True
        else:
            self.in_progress_hanging = False
        self.in_progress = msg
        self.last_message = None

    def end_progress(self, msg='done.'):
        assert self.in_progress, (
            "Tried to end_progress without start_progress")
        if self._show_progress():
            if not self.in_progress_hanging:
                sys.stdout.write('...' + self.in_progress + msg + '\n')
                sys.stdout.flush()
            else:
                logger.show_progress('')
                logger.show_progress('')
                sys.stdout.write(msg + '\n')
                sys.stdout.flush()
        self.in_progress = None
        self.in_progress_hanging = False

    def show_progress(self, message=None):
        """If we are in a progress scope, and no log messages have been
        shown, write out another '.'"""
        if self.in_progress_hanging:
            if message is None:
                sys.stdout.write('.')
                sys.stdout.flush()
            else:
                if self.last_message:
                    padding = ' ' * \
                        max(0, len(self.last_message) - len(message))
                else:
                    padding = ''
                sys.stdout.write('\r%s%s%s%s' %
                                 (' ' * self.indent,
                                  self.in_progress,
                                  message, padding))
                sys.stdout.flush()
                self.last_message = message

    def stdout_level_matches(self, level):
        """Returns true if a message at this level will go to stdout"""
        return self.level_matches(level, self._stdout_level())

    def _stdout_level(self):
        """Returns the level that stdout runs at"""
        for level, consumer in self.consumers:
            if consumer is sys.stdout:
                return level
        return self.FATAL

    def level_matches(self, level, consumer_level):
        """
        >>> l = Logger()
        >>> l.level_matches(3, 4)
        False
        >>> l.level_matches(3, 2)
        True
        >>> l.level_matches(slice(None, 3), 3)
        False
        >>> l.level_matches(slice(None, 3), 2)
        True
        >>> l.level_matches(slice(1, 3), 1)
        True
        >>> l.level_matches(slice(2, 3), 1)
        False
        """
        if isinstance(level, slice):
            start, stop = level.start, level.stop
            if start is not None and start > consumer_level:
                return False
            if stop is not None or stop <= consumer_level:
                return False
            return True
        else:
            return level >= consumer_level

    @classmethod
    def level_for_integer(cls, level):
        levels = cls.LEVELS
        if level < 0:
            return levels[0]
        if level >= len(levels):
            return levels[-1]
        return levels[level]

    def move_stdout_to_stderr(self):
        to_remove = []
        to_add = []
        for consumer_level, consumer in self.consumers:
            if consumer == sys.stdout:
                to_remove.append((consumer_level, consumer))
                to_add.append((consumer_level, sys.stderr))
        for item in to_remove:
            self.consumers.remove(item)
        self.consumers.extend(to_add)

    def prefix_msg_wrapper(self, msg):
        return "[planting] %s" % msg


logger = Logger()
