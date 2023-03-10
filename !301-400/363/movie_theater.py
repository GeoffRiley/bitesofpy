"""
Refactor the code below. Try go get the functions' bodies
as close to the left side as possible (only one indentation deep).
"""
available_movies = {
    "Tomorrow Never Dies": {
        "id": "tomorrow_never_dies",
        "quality": "IMAX",
        "genre": "Action",
    },
    "Robin Hood": {"id": "robin_hood", "quality": "regular", "genre": "Adventure"},
    "Pulp Fiction": {"id": "pulp_fiction", "quality": "regular", "genre": "Crime"},
}


# def invoice_to_be_refactored(movie, tickets):
#     amount = 0
#     movie_in_available_movies = False
#     for title in available_movies:
#         if title == movie:
#             movie_in_available_movies = True
#             if tickets != 0:
#                 if available_movies[movie]["quality"] == "IMAX":
#                     price = 12
#                     if tickets >= 5:
#                         discount = 10
#                     else:
#                         discount = 0
#                 else:
#                     price = 10
#                     if tickets >= 5:
#                         discount = 10
#                     else:
#                         discount = 0
#             else:
#                 raise ValueError("Cannot calculate price for 0 tickets")
#     if movie_in_available_movies is False:
#         raise LookupError("Movie not available")
#     else:
#         total_amount = amount + (tickets * price) - discount
#         return total_amount


def invoice_refactored(movie, tickets):
    """"Refactor the above code getting rid of the arrow shape"""
    if tickets == 0:
        raise ValueError("Cannot calculate price for 0 tickets")

    movie_in_available_movies = movie in available_movies
    if not movie_in_available_movies:
        raise LookupError("Movie not available")

    amount = 0

    title = available_movies[movie]

    if tickets >= 5:
        discount = 10
    else:
        discount = 0

    price = 12 if title['quality'] == 'IMAX' else 10

    total_amount = amount + (tickets * price) - discount
    return total_amount
