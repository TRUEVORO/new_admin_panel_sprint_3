from query_templates import get_movies_query, get_genres_query, get_persons_query


QUERY_MAPPER = {
    'movies': get_movies_query,
    'genres': get_genres_query,
    'persons': get_persons_query,
}


def get_query_by_index(index: str, load_from: str | None) -> str:
    """Формирует нужный sql запрос в зависимости от индекса"""
    if not load_from:
        raise ValueError('For getting sql query datetime string required')
    query = QUERY_MAPPER.get(index)
    if query is not None:
        return query(load_from)
    raise ValueError(f'No query for index {index}')
