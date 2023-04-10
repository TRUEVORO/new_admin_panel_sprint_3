from psycopg2.sql import SQL, Composable, Placeholder


class QueryTemplates:
    """Class with pre-defined SQL query strings."""

    @property
    def GENRES_QUERY(self) -> Composable | SQL:  # noqa
        return SQL(
            '''
            SELECT g.id,
                   g.name
            FROM content.genre AS g
            WHERE g.modified > {last_modified}
            GROUP BY g.id
            ORDER BY MAX(g.modified);
            '''
        ).format(last_modified=Placeholder())

    @property
    def MOVIES_QUERY(self) -> Composable | SQL:  # noqa
        return SQL(
            '''
            SELECT fw.id,
                   fw.title,
                   fw.description,
                   fw.rating AS imdb_rating,
                   fw.type,
                   fw.created,
                   fw.modified,
                   COALESCE(
                                   jsonb_agg(
                                   DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'full_name', p.full_name
                                       )
                               ) FILTER (WHERE pfw.role = 'actor'),
                                   '[]'
                       )     as actors,
                   COALESCE(
                                   jsonb_agg(
                                   DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'full_name', p.full_name
                                       )
                               ) FILTER (WHERE pfw.role = 'director'),
                                   '[]'
                       )     as directors,
                   COALESCE(
                                   jsonb_agg(
                                   DISTINCT jsonb_build_object(
                                           'id', p.id,
                                           'full_name', p.full_name
                                       )
                               ) FILTER (WHERE pfw.role = 'writer'),
                                   '[]'
                       )     as writers,
                   COALESCE(
                                   jsonb_agg(
                                   DISTINCT jsonb_build_object(
                                           'id', g.id,
                                           'name', g.name
                                       )
                               ) FILTER (WHERE g.id is not null),
                                   '[]'
                       )     AS genres
            FROM content.film_work AS fw
                     LEFT JOIN content.person_film_work AS pfw ON pfw.film_work_id = fw.id
                     LEFT JOIN content.person AS p ON p.id = pfw.person_id
                     LEFT JOIN content.genre_film_work AS gfw ON gfw.film_work_id = fw.id
                     LEFT JOIN content.genre AS g ON g.id = gfw.genre_id
            WHERE GREATEST(fw.modified, g.modified, p.modified) > {last_modified}
            GROUP BY fw.id
            ORDER BY GREATEST(MAX(fw.modified), MAX(g.modified), MAX(p.modified));
            '''
        ).format(last_modified=Placeholder())

    @property
    def PERSONS_QUERY(self) -> Composable | SQL:  # noqa
        return SQL(
            '''
            WITH person_roles AS (SELECT pfw.person_id,
                                         pfw.film_work_id,
                                         COALESCE(
                                                 jsonb_agg(
                                                         pfw.role
                                                     ),
                                                 '[]'
                                             ) AS roles
                                  FROM content.person_film_work AS pfw
                                  GROUP BY pfw.person_id, pfw.film_work_id)
            SELECT p.id,
                   p.full_name,
                   COALESCE(
                                   jsonb_agg(
                                   jsonb_build_object(
                                           'id', person_roles.film_work_id,
                                           'roles', person_roles.roles
                                       )
                               ) FILTER (WHERE p.id IS NOT NULL),
                                   '[]'
                       ) AS films
            FROM content.person AS p
                     LEFT JOIN person_roles ON person_roles.person_id = p.id
            WHERE p.modified > {last_modified}
            GROUP BY p.id
            ORDER BY MAX(p.modified);
            '''
        ).format(last_modified=Placeholder())
