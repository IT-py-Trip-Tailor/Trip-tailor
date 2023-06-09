# Доработаю по факту успеваемости (время как будет)

def get_user_feedback(services):
    feedback = []
    for index, service in services.iterrows():
        print(f"Please rate the following service from 1 to 5:")
        print(service)
        rating = input("Your rating: ")
        feedback.append(int(rating))
    return feedback
