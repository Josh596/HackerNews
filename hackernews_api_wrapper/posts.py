from .baseapi import BaseAPI

class Post(BaseAPI):
    pass
    @staticmethod
    def get_post(post_id):
        url = Post._url(f'/item/{post_id}.json')
        print(url)
        return Post._handle_request(url)

    @staticmethod
    def get_all_posts_from_id(from_id):
        url = Post._url("/maxitem.json")
        post_id = Post._handle_request(url)

        no_of_posts = post_id - from_id
        print('Total posts is', no_of_posts)
        posts = Post.get_last_n_post(no_of_posts, post_id)
        print('Total posts is', len(posts))
        return posts

    @staticmethod
    def get_last_n_post(n, from_id:int=None):
        """
        Parameters
        ----------
        n: int
            The number of posts to get
        from_id: int, optional
            The starting id of the post to backtrack from, if the id is 1000, we get last posts from 1000.
            If none given, then start from the max id.

        Returns
        -------
        list
            A list of dictionaries, where each item in the list is a dictionary about the post.
        """
        posts = []
        if not from_id:
            url = Post._url("/maxitem.json")
            post_id = Post._handle_request(url)
        else:
            post_id = from_id

        assert type(post_id) == int

        # Traverse the tree upwards
        while len(posts) != n:
            post_id -= 1
            post = Post.get_post(post_id)
            if not post.get('dead') and not post.get('deleted'):
                posts.append(post)

        return posts

    @staticmethod
    def get_all_children(post_id):
        kids = []
        data = Post.get_post(post_id)
        if data.get('kids'):
            for post_id in data['kids']:
                kids.append(Post.get_post(post_id))

        return kids

    @staticmethod
    def get_parent(post_id):
        data = Post.get_post(post_id)
        if data.get('parent'):
            return Post.get_post(data['parent'])

    