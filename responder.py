#!/usr/bin/env python3
from argparse import ArgumentParser
from configparser import ConfigParser
import logging
import logging.handlers
from praw import Reddit

def setup_logging(debug=False):
    logger = logging.getLogger('Responder')
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%m-%d %H:%M:%S')
    fh = logging.handlers.RotatingFileHandler(
        'responder.log',
        maxBytes=256000,
        backupCount=7)
    fh.setLevel(logging.INFO if not debug else logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO if not debug else logging.DEBUG)
    logger.debug('Logger initialized')

def respond(config, debug=False):
    setup_logging(debug)
    logger = logging.getLogger('Responder')
    logger.info('Initialized')
    reddit = Reddit(config['Bot'])
    with open(config['Track file']) as f:
        last_response = float(f.read())
    logger.debug('Last comment read in')
    comments = list(
        filter(
            lambda c: c.subreddit.display_name.lower() in config['Subreddits'].lower(),
            reddit.redditor(config['Target']).comments.new(limit=50)
        )
    )
    logger.debug('Fetched latest comments. Count: %i', len(comments))
    for comment in comments:
        if last_response < comment.created_utc:
            logger.debug('Target comment found')
            response = comment.reply(config['Message'])
            if response:
                logger.info('Responded to comment. Response URL: https://reddit.com%s', response.permalink)
                with open(config['Track file'], 'w') as f:
                    f.write(str(comment.created_utc))
                break
            else:
                logger.warning('Unable to respond to comment: %s', comment.link_url)
    logger.debug('Exiting')

if __name__ == '__main__':
    argparse = ArgumentParser(
        description="Respond to someone's latest comment with a fixed message"
    )
    argparse.add_argument('config', help='Name of configuration file')
    argparse.add_argument(
        '-g',
        '--generate',
        action='store_true',
        help='Generate a default configuration file for first-time setup'
    )
    argparse.add_argument('-d', '--debug', action='store_true')
    argparse.add_argument(
        '-s',
        '--config-section',
        default='DEFAULT',
        type=str,
        help='Section name to use in configuration'
    )
    args = argparse.parse_args()
    config = ConfigParser()
    if args.generate:
        config[args.config_section] = {
            'Target': 'target_user',
            'Subreddits': 'worldoftanksconsole',
            'Bot': 'bot_name',
            # Storage to determine last comment responded to; prevents spam
            'Track file': 'latest_responded_to.txt',
            'Message': "This was a triumph.\n\n[I'm making a note here - huge success!](https://www.youtube.com/watch?v=Y6ljFaKRTrI)"
        }
        with open(args.config, 'w') as f:
            config.write(f)
            with open(config[args.config_section]['Track file'], 'w') as f:
                f.write('0')
    else:
        config.read(args.config)
        respond(config[args.config_section], args.debug)
