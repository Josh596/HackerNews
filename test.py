# import json
# from hackernews_api_wrapper.posts import Post

# def load_initial_data():
#     data = Post.get_last_n_post(1)
#     result = []
#     for post in data:
#         # print(post['type'], post, sep='\n', end='\n\n')
#         if post['type'] == 'comment':
#             # Store comment referrence until top level parent is found, then from top level parent, create all comments.
#             comment_train = []
#             comment = post.copy()
#             while comment.get('parent'):
#                 comment = Post.get_parent(comment['id'])
#                 comment_train.append(comment)
#                 # print('getting parent')
#             else:
#                 # print('Done to parent')
#                 comment_train.append(comment)
#             # print(comment_train, 'comment_train')
#             # reverse the comment_train and load to db.
#             result.extend(comment_train)

#         elif post['type'] == 'pollopt':
#             parent = Post.get_parent(post['id'])

#             load_to_db(parent)
#             load_to_db(post)
            
#         else:
#             result.append(post)
    
#     with open('result1.json', 'w') as file:
#         json.dump(result, file, indent=6)


# def load_to_db(post):
#     if post['type'] == 'story':
#         # Add to Story Table
#         pass
#     if post['type'] == 'job':
#         # Add to Job Table
#         pass
#     if post['type'] == 'comment':
#         # Add to Comment Table
#         pass
#     if post['type'] == 'poll':
#         # Add to poll table
#         pass
#     if post['type'] == 'pollopt':
#         # Add to polloption table
#         pass


from hackernews.tasks import sync_db

sync_db()

    
# if __name__ == '__main__':
#     load_initial_data()