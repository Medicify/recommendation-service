from service import recommendationRoute


def routes(server):
    server.include_router(recommendationRoute)
    