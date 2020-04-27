from itertools import chain

from get_post import get_post


def generate_tag_string(post_id, tags=[], new=False):
    """
    Given a post_id, retrieve the tags and combine them
    with the argument `tags`, if any, to create a string
    that joins tags into a command separated string along
    with the author.  If the boolean argument `new` is
    `True`, then add the 'new' tag.
    """
    if new:
        tags.append('new')

    post = get_post(post_id)

    tags2 = map(lambda x: x.decode("utf8", "ignore"), chain(post.get('tags'), tags))

    return '{}: {}'.format(post.get('author'), ', '.join(tags2))


