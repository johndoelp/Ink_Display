def next_train_time(train_schedule):
    next_train_unformat = train_schedule[0]
    hours = int(next_train_unformat[0:2])
    minutes = int(next_train_unformat[3:5])
    next_train = (hours * 60) + minutes
    return next_train