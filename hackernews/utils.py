from .models import PostBase, Comment, Poll, PollOption, Story, Job

available_models = {
        'all': PostBase,
        'job': Job,
        'story': Story,
        'poll': Poll,
        'pollopt': PollOption,
        'comment': Comment
    }

def get_model_from_type(item_type:str):
    """
    Parameter
    ---------
    item_type: str
        A string like comment, job, poll, story
    
    Returns
    -------
    A django model object
    """


    
    model = available_models.get(item_type.lower())

    if model:
        return model
    
    raise Exception('Item Type Does Not Exist')
    pass